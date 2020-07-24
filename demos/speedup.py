import cv2


if __name__ == "__main__":
    cap = cv2.VideoCapture("output_9am_10am_Jul10.avi")
    out = cv2.VideoWriter("demox16.avi", cv2.VideoWriter_fourcc(*'XVID'), 20,
            (960, 540))
    fcount = 0
    while cap.isOpened():
         
        ret, frame = cap.read()
        fcount += 1
        
        if (fcount % 16) != 0:
            continue
        
        print(fcount)
        if not ret:
            break
        
        out.write(frame)
    
    cap.release()
    out.release()

