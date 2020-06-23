import uuid 
import numpy as np
from numpy import dot
from numpy.linalg import norm

def _distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**.5
    


class Object:
    def __init__(self, bbox):
        self.id = uuid.uuid4()
        self.bbox = bbox
        x, y, w, h = bbox
        self.centroid = x + w//2, y+h//2
    
    def funcname(self, parameter_list):
        pass

class Tracker:
    def __init__(self):
        self._is_inited = False
        self.current_frame_objects = []
        self.previous_frame_objects = []
        self.all_objects = []
        

    def fit(self, objects):
        """
        """
        self.previous_frame_objects = self.current_frame_objects
        self.current_frame_objects = objects

    
        D = np.zeros([
                len(self.previous_frame_objects),\
                len(self.current_frame_objects)
            ])
        
        # Caculating distance matrix between tracking object and current_frame objects
        # D \subset R^(m * n), m is number of tracking objects, n is number of current_frame objects

        for i, previous_frame_object in enumerate(self.previous_frame_objects):
            for j, current_frame_object in enumerate(self.current_frame_objects):
                D[i,j] = _distance(previous_frame_object.centroid, \
                    current_frame_object.centroid)
        
        
        for i, object_ in enumerate(self.current_frame_objects):
            
            try:
                idx = np.argmin(D[:,i])
            
            except Exception:
                idx = None
            
            # Reassign object ID of previous frame to current_frame
            if idx and D[idx, i] < 10:

                self.current_frame_objects[i].id = self.previous_frame_objects[idx].id
                print(idx)

            
            if not idx:
                print("Not Reassigned")
            print("---")
        
