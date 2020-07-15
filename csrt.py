import cv2
import copy

class Id:
    def __init__(self):
        self.id = 0

    def getId(self):
        _id = copy.deepcopy(self.id)
        self.id += 1
        return _id



class Tracked_Object:
    def __init__(self, bbox, _id):
        self.id = _id
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(frame, bbox)

    def update(self, frame):
        ret, bbox = self.tracker.update(frame)
        
        

class MotherTracker:
    def __init__(self, bboxes):
        self.trackers = []

        

    def update(self):
        pass

if __name__ == "__main__":
    cap = cv2.VideoCapture("videos/test.mp4")
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        key = cv2.waitKey(0) & 0xFF

        if key not in (ord("q"), ord("k")):
            key = cv2.waitKey(0) & 0xFF

        if key == ord("q"):
            break

        cv2.imshow("Frame", frame)


        # Loop termination condition
        if not ret:
            break
    
    cap.release()
    cv2.destroyAllWindows()

