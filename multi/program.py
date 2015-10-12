
import cProfile
import time
import gc

print __name__

def worker():
    time.sleep(5)
    for t in gc.get_objects():
        print t


if __name__ == '__main__':
    import multiprocessing

    x = []
    for i in range(1000000):
        x.append(i)
        #time.sleep(1)

    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()


