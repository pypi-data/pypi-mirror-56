import numpy as np
from skimage import measure
import scipy.ndimage as ndi
from scipy.spatial import distance

class Snapshot:
    def __init__(self, image, labels, mask, min_area=350, max_distance=200, **kwargs):
        self.max_distance = max_distance
        
        bcg_level = image[~mask].astype(float).mean()
        leveled_image = np.clip(image.astype(float) - bcg_level, a_min=1e-6, a_max=None)
        reg_props_image = measure.regionprops(labels, leveled_image)
        
        self.centroids =  np.array([
            np.array(x.weighted_centroid) for x in reg_props_image if x.area > min_area])
        
        distance_map = ndi.distance_transform_edt(mask)
            
        gradients = [-x for x in np.gradient(distance_map)]
        
        reg_props_grad_y = measure.regionprops(labels, gradients[0])
        reg_props_grad_x = measure.regionprops(labels, gradients[1])
        
        y_grads = np.array([aaa.mean_intensity for aaa in reg_props_grad_y if aaa.area > min_area])
        x_grads = np.array([aaa.mean_intensity for aaa in reg_props_grad_x if aaa.area > min_area])
            
        self.gradients = np.array([y_grads, x_grads]).T
        self.norm_gradients = (self.gradients.T / np.linalg.norm(self.gradients, axis=1)).T
        self.distances = distance_map[
            self.centroids.astype(int).T[0], self.centroids.astype(int).T[1]]
        
        padgrads = np.pad(self.norm_gradients, ((0,0),(0,1)), 'constant')
        self.contours = np.cross(padgrads, [0,0,1])[:,:-1]
    
    def evaluate_shift(self, other):
        euclid_distances = distance.cdist(self.centroids, other.centroids)
        followers = (-euclid_distances).argmax(axis=1)
        predecessors = (-euclid_distances).argmax(axis=0)
        
        pairs = []

        for i, fol in enumerate(followers):
            if predecessors[fol] == i and self.distances[i] <= self.max_distance:
                pairs.append((i, fol))
        
        pairs = np.array(pairs)
        
        coords = self.centroids[pairs[:,0]]
        coords_next = other.centroids[pairs[:,1]]
        shifts = coords_next - coords
        
        ddists = (shifts * self.norm_gradients[pairs[:,0]]).sum(axis=1)
        dconts = (shifts * self.contours[pairs[:,0]]).sum(axis=1)
        
        return dict(
            y=coords[:,0],
            x=coords[:,1],
            y_next=coords_next[:,0],
            x_next=coords_next[:,1],
            dy=shifts[:,0],
            dx=shifts[:,1],
            ddists=ddists,
            dconts=dconts,
            grad_size=np.linalg.norm(self.gradients, axis=1)[pairs[:,0]]
        )