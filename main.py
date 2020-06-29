#!env/bin/python

import cv2
import numpy as np
import copy
from track import Tracker, Object

np.set_printoptions(precision=2)

def preProcess(frame):
    frame = cv2.resize(frame, dsize= (0,0), fx=.5, fy=.5)
    sframe = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    return sframe, frame

nTracker = Tracker()

def app():
    cap = cv2.VideoCapture("videos/test.mp4")
    bg = cv2.createBackgroundSubtractorKNN()
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            return 0
        
        # Substracting backgroud
        sframe, _frame = preProcess(frame)
        _frame = bg.apply(_frame)

        # dilating the mask
        _frame = cv2.dilate(_frame, None, iterations = 2)
        
        contours = cv2.findContours(_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            
        # with given frame, we calculated a tuple of bounding box of current frames
        bboxes = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 500]
        
        # initializing list of object in current frame
        # objects = [Object(bbox) for bbox in bboxes]
        nTracker.fit(bboxes)

        # Fit this bounding box to tracker:
        # The tracker will:
        # - object matching with prv frame using distance matrix: Object Matching Based on Distance Matrix (https://sci-hub.tw/10.1109/icist.2013.6747840)      
        
        """
        for bbox in bboxes:
            x, y, w, h = bbox
            cv2.rectangle(sframe, (x, y), (x+w, y+h), (0, 0, 255), 2)
        """

        for obj in nTracker.tracking_objects:
            
            if obj.status == "online":
                """x, y, w, h = obj.bbox
                cv2.rectangle(sframe, (x, y), (x+w, y+h), (0, 255, 255), 2)
                cv2.putText(sframe, str(obj.id),\
                    (x ,y),\
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX,\
                    fontScale = .5, \
                    color=(255, 0, 0))
                """
                if len(obj.coor) >= 2:
                    for i in range(1, len(obj.coor)):
                        cv2.line(sframe, obj.coor[i-1], obj.coor[i], (0, 0,
                            255), 2)

	
        # out.write(sframe)

        cv2.imshow("bgSubtracted", _frame)
        cv2.imshow("Original", sframe)
        
            
        
        key  = cv2.waitKey(1) & 0xFF
        
        while key not in [ord('q'), ord('k')]:
           key = cv2.waitKey(0)
        
        # Quit when 'q' is pressed
        if key == ord('q'):
            break


    # out.release()
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    app()
