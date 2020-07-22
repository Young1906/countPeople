import cv2
import numpy as np
from track import Tracker, Object

class MotherTracker:
    def __init__(self, path):
        self.feed = cv2.VideoCapture(path)

    def release(self):
        self.feed.release()
        cv2.destroyAllWindows()

    def preprocess(self, frame):
        return frame
   
    def getFrame(self):
        
        print("This")
        
        if not self.feed.isOpened():
            self.release()
        
        ret, frame = self.feed.read()
        print(ret, frame)
        return self.preprocess(frame)
