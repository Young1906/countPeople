import cv2
import numpy as np
from track import Tracker, Object


nTracker = Tracker()


def process(img):
    img = cv2.resize(img, dsize= (0,0), fx=.5, fy=.5)
    return img

if __name__ == "__main__":
    
    # Read YOLO pretrain weights
    net = cv2.dnn.readNet("yolo/yolov3.weights", "yolo/yolov3.cfg")
    
    classes = []
    with open("yolo/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # Demo output:
    output = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'XVID'), 20,
            (960, 540))


    # Capture Video
    cap = cv2.VideoCapture("videos/NVR@ch6@main_20200710085959_20200710095958.avi")
    # cap = cv2.VideoCapture("videos/test.mp4")
    while cap.isOpened():

        ok, img = cap.read()
        img = process(img)
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        height, width, channels = img.shape
        if not ok:
            break 

        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop = False)
        net.setInput(blob)

        outs = net.forward(output_layers)
        
        # import pdb; pdb.set_trace()
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
    
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
        
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                        
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        # import pdb; pdb.set_trace()
        # Tracking
        _bboxes = []
        for i in range(len(boxes)):
            if i in indexes:
                label = str(classes[class_ids[i]])
                if label == "person":
                    _bboxes.append(boxes[i])

        nTracker.fit(_bboxes)
        
        for obj in nTracker.tracking_objects:
            if obj.status == "online":
               if len(obj.bboxes) > 1:
                    for i in range(1, len(obj.bboxes)):
                        x1, y1, w1, h1 = obj.bboxes[i - 1]
                        x2, y2, w2, h2 = obj.bboxes[i]

                        # cv2.line(img, (x1+ w1//2, y1 + h1//2), (x2+w2//2,
                        #     y2+h2//2), (0, 255, 0), 2)
            
            cross = obj.is_cross((490, 308), (613, 532), (396, 467))
            
            if cross == "in":
                nTracker._in += 1
            if cross == "out":
                nTracker._out += 1

        cv2.line(img, (490, 308), (613, 532), (0, 255, 255), 2)
        cv2.putText(img, "In", (396, 467), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,
            0 ,255), 1) 
        cv2.putText(img, f"In: {nTracker._in}", (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.putText(img, f"Out: {nTracker._out}", (0, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)


       

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 1, color, 1)
                    
        cv2.imshow("Image", img)
        output.write(img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    output.release()
    cv2.destroyAllWindows()
