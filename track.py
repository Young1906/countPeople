import uuid 
from numpy import dot
from numpy.linalg import norm

def cos_sim(a,b):
    return dot(a, b)/(norm(a)*norm(b))

class O:
    """
    P: object with following attribute:
    - Bounding box
    - Contour area
    - Centroid
    
    ---

    Goal is to trace same object between 2 frames
    """
    def __init__(self,x, y, w, h, cx, cy, hist):
        self.id = uuid.uuid4()
        self.x, self.y, self.w, self.h = x, y, w, h
        self.cx, self.cy = cx, cy
        self.coor = []
        self.status = "tracking" # online / offline
        self.hist = hist

    def exists(self, R, ls):
        return 0
        """
        Check if object is already exist in list of online object
        if yes: 
            return 1, +id 
        if no: 
            retunr 0, None

        --- 
        Condition of existency:
        - centroid within radius R
        - 
        """
        ls = [o for o in ls if o.status=="online"]
        # List of objects having centroid within radious of R
        _ls = [o for o in ls if (o.x - self.x)**2 + (o.y - self.y)**2 < R**2]

        if not _ls:
            return 0, None
        
        _ls_sim = [cos_sim(self.hist, o.hist) for o in ls]
        print(_ls_sim)

        return 1, "Test"
        


            

    

if __name__ == "__main__":
    p1 = P()
    print(p1.id)