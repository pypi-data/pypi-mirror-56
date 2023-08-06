import scipy.ndimage as ndi
from tqdm import tqdm
import os

import yaml

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import argparse
import imageio

from skimage import io
from skimage.filters import threshold_otsu
from skimage import measure
from skimage.feature import peak_local_max
from skimage.morphology import watershed, disk

from .snapshot import Snapshot


def filter_image(image, blur_sig=2):
    blurred = ndi.gaussian_filter(image.astype(float), blur_sig)
    return blurred

def normalize_image(image, blur_sig):
    blurred = filter_image(image, blur_sig)
    return blurred

def load_sequence(path, blur_sig, n=None):
    seq = io.imread(path)
    
    if n is not None:
        seq = seq[:n]
    
    seq_norm = []
    
    for im in tqdm(seq, desc='loading'):
        seq_norm.append(normalize_image(im, blur_sig))
    
    return seq_norm

def find_ocean(image):
    win_rows, win_cols = 20, 20

    win_mean = ndi.uniform_filter(image, (win_rows, win_cols))
    win_sqr_mean = ndi.uniform_filter(image**2, (win_rows, win_cols))
    win_std = np.sqrt(np.clip(win_sqr_mean - win_mean**2, a_min=0, a_max=None))
    win_std_flat = win_std.flatten()
    win_std_flat = win_std_flat[(win_std_flat == win_std_flat) & (win_std_flat > 0) & (win_mean.flatten() > 0)]

    hist = np.histogram(np.log(win_std_flat), bins=20)
    counts, bins = hist
    ixs = np.where((counts[1:-1] < counts[:-2]) & (counts[1:-1] < counts[2:]))[0]
    ix = ixs[np.argmin(abs(ixs - 10))] + 1
    std_thr = np.exp((bins[ix] + bins[ix + 1]) / 2)
    
    mask = win_std <= std_thr
    bcg_level = np.percentile(image[mask].astype(float), 95)
    
    tot_mask = mask | (image <= bcg_level)
    
    for i in range(5):
        tot_mask = ndi.uniform_filter(tot_mask.astype(float), (20, 20)) > 0.5
    
    sublevel = ndi.morphology.binary_fill_holes(tot_mask)
    
    labeled_sublevel = measure.label(sublevel)
    flat_labels = labeled_sublevel.flatten()
    flat_labels = flat_labels[flat_labels != 0]
    most_common_label = Counter(flat_labels).most_common(1)[0][0]
    ocean = labeled_sublevel == most_common_label
    
    return ocean

def create_markers(image, mask):
    local_maxi = peak_local_max(image, indices=False, footprint=disk(5), exclude_border=False)
    markers = ndi.label(local_maxi)[0]
    return markers

def sequence_segmentation(sequence):
    labels_list = []
    mask_list = []
    
    for image in tqdm(sequence, desc='segmentation'):
        mask = ~find_ocean(image)
        markers = create_markers(image, mask)
        labels = watershed(-image, markers, watershed_line=True, mask=mask)
        
        # relabeling
        new_labels = np.zeros_like(labels)
        
        for i, l in enumerate(sorted(np.unique(labels))):
            new_labels[labels == l] = i
        
        labels_list.append(new_labels)
        mask_list.append(mask)
        
    return labels_list, mask_list

def plot_segmentation(image, labels, mask, ax):
    masked_image = np.ma.masked_where(
            ndi.morphology.binary_dilation(labels == 0, iterations=1) &\
            ndi.morphology.binary_dilation(mask, iterations=4), image)
    ax.imshow(masked_image, cmap='gray')
    
def fig2rgb_array(fig):
    fig.canvas.draw()
    buf = fig.canvas.tostring_rgb()
    ncols, nrows = fig.canvas.get_width_height()
    X = np.fromstring(buf, dtype=np.uint8).reshape(nrows, ncols, 3)
    mask1 = (X[:,:,0] != 255).sum(axis=1) > 0
    mask2 = (X[:,:,0] != 255).sum(axis=0) > 0
    return X[mask1][:,mask2]

def seg2tiff(sequence, labels_list, mask_list, filename, y_list=None, x_list=None):
    images = []
    
    if y_list is None and x_list is None:
        for image, labels, mask in tqdm(zip(sequence, labels_list, mask_list), total=len(sequence), desc='saving segmentation'):
            fig, ax = plt.subplots(figsize=(12,10))
            plot_segmentation(image, labels, mask, ax)

            X = fig2rgb_array(fig)
            images.append(X)
            plt.close()
    else:
        for image, labels, mask, x, y in tqdm(zip(sequence, labels_list, mask_list, x_list, y_list), total=len(sequence), desc='saving markers'):
            fig, ax = plt.subplots(figsize=(12,10))
            plot_segmentation(image, labels, mask, ax)
            ax.scatter(x, y, c='red', s=5, alpha=0.3)
            ax.set_ylim(0, image.shape[0])
            ax.set_xlim(0, image.shape[1])
            X = fig2rgb_array(fig)
            images.append(X)
            plt.close()
    
#     print(np.array())
#     tifffile.imsave(filename, np.array(images))
    imageio.mimwrite(filename, images)