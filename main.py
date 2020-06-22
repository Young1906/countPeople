import cv2
import numpy as np
import copy
from track import O

H, W = 1080, 1920


def processFrame(frame):
    _frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _frame = cv2.resize(_frame, (W//2, H//2))
    return _frame

backSub = cv2.createBackgroundSubtractorKNN()

if __name__ == "__main__":

    cap = cv2.VideoCapture("dat.mp4")
    frames = []
    
    prv_cnts = []
    contour_objects = list()

    while (cap.isOpened()):
        ret, frame = cap.read()
        _frame = processFrame(frame)
        fgMask = backSub.apply(_frame)
        
        _fgMask = cv2.dilate(fgMask, None, iterations=1)

        cnts = cv2.findContours(_fgMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]



        for c in cnts:
            if cv2.contourArea(c) < 250:
                continue
            
            x, y, w, h = cv2.boundingRect(c)
            a = cv2.contourArea(c)
            cx, cy = x + w/2, y + h/2
            px = _frame[x:x+w, y:y+h]
            hist, bins = np.histogram(px.ravel(), 256, [0,256])
            
            # Condition to initialize an contour object:
            _co = O(x, y, w, h, cx, cy, hist)
            
            con, id = _co.exists(10, contour_objects)

            if not con:
                contour_objects.append(_co)

            
            






            
            cv2.rectangle(_frame, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.imshow("mask", _frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()