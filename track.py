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
        self.status = "online"
        self.THRESH = 10
        self.MAX_DISAPPEAR = 10
        self.c = 0

    def deregister(self):
        self.status = "offline"
    
    def update(self,bbox):
        self.bbox = bbox
        x, y, w, h = bbox
        self.centroid = x + w//2, y + h//2

class Tracker:
    def __init__(self):
        self._is_inited = False
        self.tracking_objects = []
        self.THRESH = 10

    def fit(self, bboxes):
        """
        This method takes list of current frame's bboxes and compare to
        tracking object bboxes.
        
        ---
        Input:
        - bboxes: list of bbox, a bbox is a tuple of x, y coordinate and width
          and height (x, y, w, h)


        ---
        Return:
        - 

        """
        if not self.tracking_objects:
            # init list of tracking objects in the first frame
            self.tracking_objects = [Object(bbox) for bbox in bboxes]
        
        # Caculating distance matrix between tracking object and current_frame objects
        # D \subset R^(m * n), m is number of tracking objects, n is number of current_frame objects

        m, n = len(self.tracking_objects), len(bboxes)
        D = np.zeros([m, n])
        
        online_tracking_objects = [x for x in self.tracking_objects if
                x.status == "online"]
        
        for i, online_obj in enumerate(online_tracking_objects):
            for j, bbox in enumerate(bboxes):
                p1 = online_obj.centroid
                p2 = (bbox[0]+bbox[2]//2, bbox[1] + bbox[3]//2)
                D[i, j] = _distance(p1, p2)

        # Looping over tracking object:
        # - Update tracking object bbox to the closest bbox in bboxes; remove
        # assigned bbox from list of bboxes
        # - if D[i, j] > thresh, don't update bbox
        
        seen_i = set()
        seen_j = set()
        
        while True:
            i, j = np.where(D == np.amin(D))
            i, j = i[0], j[0]
            
            if (i in seen_i) or (j in seen_j):
                continue

            if D[i,j] < self.THRESH:
                online_tracking_objects[i].update(bboxes[j])
                D[i,j] = 999

            seen_i.add(i)
            seen_j.add(j)

            if len(seen_i) == m or len(seen_j)==n:
                break






