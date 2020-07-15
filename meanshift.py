#!env/bin/python

import cv2
import numpy

class Meanshift_tracker():
    def __init__(self):
        pass
        
if __name__ == "__main__":
    
    cap = cv2.VideoCapture("videos/test.mp4")
    ret, frame = cap.read()
        
    while cap.isOpened():
        bbox = cv2.selectROI(frame)
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Frame", frame)



    cap.release()
    cv2.destroyAllWindows()
