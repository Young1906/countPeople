import multiprocessing as mp
import cv2
import time

_DONE = False

def gen():
    global q 
    i = 0
    while True:

        if q.qsize() < 10:
            q.put(i)
            print(f"sent {i}")
            i+=1

        if i > 20:
            break

def p():
    global q, _DONE

    while True:
        
        if _DONE==True:
            print("This")
            break


        i = q.get()
        print(f"received {i}")
        q.task_done()
        time.sleep(1)
        
if __name__ == "__main__":
    q = mp.JoinableQueue(10)

    sender = mp.Process(target=gen)
    receiver = mp.Process(target=p)

    sender.start()
    receiver.start()
    
    sender.join()
    q.join()
    _DONE = True
    receiver.join()
