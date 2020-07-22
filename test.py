#!env/bin/python

from multiprocessing import Process, Queue
import os, cv2
from matplotlib import pyplot as plt
import numpy as np

def info(title):
    print(f"{title}: ppid={os.getppid()}, pid={os.getpid()}")

class Feed:
    def __init__(self, path):
        info("Video Feeder")
        self.frame_id = 0
        self.cap = cv2.VideoCapture(path)

    def get_frame(self):
        if not self.cap.isOpened():
            self.cap.release()
            return "END"

        ret, frame = self.cap.read()
        
        if not ret:
            self.cap.release()
            return "ERR"
        
        rs = self.frame_id, frame
        self.frame_id += 1

        return rs

def Detect(frame, threshold=.5):
    H, W, _ = frame.shape
    # Read YOLO pretrain weights
    net = cv2.dnn.readNet("yolo/yolov3.weights", "yolo/yolov3.cfg")

    classes = []
    with open("yolo/coco.names","r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True,\
            crop=False)

    net.setInput(blob)

    # Inference
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    classes_ = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence  = scores[class_id]
            
            if confidence > threshold:
                
                # Bbox
                cx, cy = int(detection[0] * W), int(detection[1] * H)
                w, h = int(detection[2] * W), int(detection[3] * H)
                
                x, y = cx - w // 2, cy - h//2
                
                # Appending to result
                boxes.append((x, y, w, h))
                confidences.append(confidence)
                classes_.append(classes[class_id])
    
    #TODO: non-max suppression here
    classes_, confidences, boxes = NMS(classes_, confidences, boxes, .5)
    return classes_, confidences, boxes

def NMS(C, S, B, N):
    C_, S_, B_ = [],[],[]


    while len(B) > 0:
        i = np.argmax(S)
        
        c_ = C.pop(i) # Class
        s_ = S.pop(i) # Score
        b_ = B.pop(i) # BBox
        
        C_.append(c_)
        S_.append(s_)
        B_.append(b_)

        for i, b in enumerate(B):
            print(IoU(b_, b))
            if IoU(b_, b) > N:
                print("pop")
                B.pop(i)
                S.pop(i)
                C.pop(i)

    return C_, S_, B_

def IoU(b1, b2):
    x1, y1, w1, h1 = b1
    x2, y2, w2, h2 = b2

    if x1 > x2 + w2 or x2 > w1 + w1:
        ix = 0
    else:
        ix = min(x1 + w1, x2 + w2) - max(x1, x2)
    
    if y1 > y2 + h2 or y2 > y1 + h1:
        iy = 0
    else:
        iy = min(y1 + h1, y2 + h2) - max(y1, y2)

    I = ix * iy
    U = w1 * h1 + w2 * h2 - I

    return float(I)/float(U)
        


def main():
    feed = Feed("videos/test.mp4")
    fid, frame = feed.get_frame()
    classes, probs, bboxes = Detect(frame, .5)
    
    for c, p, b in zip(classes, probs, bboxes):
        x, y, w, h = b
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.putText(frame,f"{c}:{str(p)[:4]}", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    cv2.imshow("Detection", frame)
    cv2.waitKey(0) & 0xFF

if __name__ == "__main__":
    main()
