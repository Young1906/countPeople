import cv2
import numpy as np
import os 

def getfn():
    ls = os.listdir("videos")
    for fn in ls:
        yield f"videos/{fn}"

def preProcess(frame):
    o_frame = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return o_frame, frame



if __name__ == "__main__":
    
    # Getting list of videos to process
    l_fn = getfn()
    fn = next(l_fn)
    
    # App start here
    cap = cv2.VideoCapture(fn)
    

    #cv2 Background Estimator:
    bg = cv2.createBackgroundSubtractorKNN()

l
    while cap.isOpened():

        ret, frame = cap.read()
        o_frame, frame = preProcess(frame)
        
        bgFrame = bg.apply(frame)
        bgFrame = cv2.dilate(bgFrame, None, iterations=2)

        contours = cv2.findContours(bgFrame.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[0]
        

        bboxes = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c)
                > 500]
        
        for bbox in bboxes:
            x, y, w, h = bbox
            cv2.rectangle(o_frame, (x, y), (x+w, y+h), (0, 255, 0), 1)


        if not ret:
            break

        key = cv2.waitKey(0) & 0xFF

        if key not in (ord("q"), ord("k")):
            key = cv2.waitKey(0) & 0xFF

        if key == ord("q"):
            break

        cv2.imshow("Original", bgFrame)

    cap.release()
    cv2.destroyAllWindows()
