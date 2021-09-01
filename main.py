import threading 
import time
import random
from queue import Queue
threads = []
buffer = Queue()
fillCount = threading.Semaphore(0)
emptyCount = threading.Semaphore(10)
pLock= threading.Lock()
cLock= threading.Lock()
def producer():
    global buffer
    while True:
        num = random.randint(1,1000)
        emptyCount.acquire()
        pLock.acquire()
        buffer.put(num)
        pLock.release()
        fillCount.release()
        print(f"Producer added {num} => {list(buffer.queue)}, {buffer.qsize()}")
        time.sleep(.5)
        

def consumer():
    global buffer
    while True:
        fillCount.acquire()
        cLock.acquire()
        x = buffer.get()
        cLock.release()
        emptyCount.release()
        print(f"Consumer removed {x} => {list(buffer.queue)}")
        time.sleep(1)



t1 = threading.Thread(target=producer, daemon=True)
t2 = threading.Thread(target=consumer, daemon=True)
t3 = threading.Thread(target=consumer, daemon=True)
t4 = threading.Thread(target=consumer, daemon=True)
threads.append(t1)
threads.append(t2)
threads.append(t3)
threads.append(t4)
[thread.start() for thread in threads]
[thread.join() for thread in threads]
