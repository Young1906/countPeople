import multiprocessing as mp
import cv2
import time
from all_function import Detect 

MAX_Q_LEN = 10

def time_this(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        rs = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time() - t0}")
        return rs
    return wrapper

def Feed(path, nterminate):
    global q

    cap = cv2.VideoCapture(path)
    
    fid = 0 
    while cap.isOpened():
        if q.qsize() < MAX_Q_LEN:
            ret, frame = cap.read()
            fid += 1
            if not ret:
                q.put((-1, None1))
                break
            
            if fid > 100:
                q.put((-1, None))
                break

            q.put((fid, frame))
            #print(f"send frame {fid}")
    for i in range(nterminate):
        q.put((-1, None))
    
    cap.release()

def Detect_(name):
    global q
    
    while True:
        fid, frame = q.get()
        
        if fid == -1:
            break
        
        classes_, confidence, boxes = Detect(frame, threshold = .5)
        
        #print(f"{name}: {classes_}")
        q.task_done()

@time_this
def main(N_CONSUMMER):

    Pfeed = mp.Process(target = Feed , args
            = ("videos/NVR@ch6@main_20200710085959_20200710095958.avi",
                N_CONSUMMER, ))
    PDetect_ = []

    for i in range(N_CONSUMMER):
        PDetect_.append(mp.Process(target = Detect_, args=(f"Process {i}", )))
    
    Pfeed.start()
    
    for p in PDetect_:
        p.start()

    Pfeed.join()
    
    for p in PDetect_:
        p.join()



if __name__ == "__main__":
    q = mp.JoinableQueue(MAX_Q_LEN)
    
    for i in range(2, 20):
        print(i)
        main(i)
