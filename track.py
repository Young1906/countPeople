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
        self.MAX_DISAPPEAR = 10
        self.c = 0

    def deregister(self):
        self.c+=1
        if self.c > self.MAX_DISAPPEAR:
            self.status = "offline"
    
    def update(self,bbox):
        self.bbox = bbox
        x, y, w, h = bbox
        self.centroid = x + w//2, y + h//2

class Tracker:
    def __init__(self):
        self._is_inited = False
        self.tracking_objects = []
        self.THRESH = 100
    def clean(self):
        for obj in tracking_objects:
            if obj.status == "offline":
                del obj


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

        online_tracking_objects = [x for x in self.tracking_objects if
                x.status == "online"]
        
        m, n = len(online_tracking_objects), len(bboxes)
        D = np.zeros([m, n])
        
        for i, online_obj in enumerate(online_tracking_objects):
            for j, bbox in enumerate(bboxes):
                p1 = online_obj.centroid
                p2 = (bbox[0]+bbox[2]//2, bbox[1] + bbox[3]//2)
                D[i, j] = _distance(p1, p2)
        
         
        seen_i = set()
        seen_j = set()
        
        terminate = False
        
        counter = 0
        counter2 = 0

        while not terminate:

            i, j = np.where(D == np.amin(D))
            i, j = i[0], j[0]
            
            if (i in seen_i) or (j in seen_j):
                # print("skip")
                D[i, j] = 9999
                continue
            
            # print(D)
            
            if D[i,j] < self.THRESH:
                online_tracking_objects[i].update(bboxes[j])
                D[i,j] = 9999
                counter += 1
                seen_i.add(i)
                seen_j.add(j)

            counter2 += 1
            if counter >=  min(m,n) or counter2 > max(m,n):
                terminate = True
        
        # index of tracking objects without match
        unseen_i = set(range(m)) - seen_i

        for i in unseen_i:
            online_tracking_objects[i].deregister()

        
        # index of bbox without match
        unseen_j = set(range(n)) - seen_j
        for j in unseen_j:
            self.tracking_objects.append(Object(bboxes[j]))

        self.clean()
