import cv
import numpy as np
from track import Tracker, Object

class TrackerEngine:
    def __init__(self):
        
        # Initiate tracker objects
        self.nTracker = Tracker()

        # Yolo
        self.net = cv2.dnn.readNet("yolo/yolov3.weights", "yolo/yolov3.cfg")
        with open("yolo/coco.name", "r") as f:
            self.class = [line.strip() for line in f.readlines()]
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in \
                net.getUnconnectedOutLayers()]

        
