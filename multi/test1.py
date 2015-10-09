from multiprocessing import Process
import time


def ix():

    while True:
        print 'I am Test 1'
        print __name__
        print whos()
         # for name in dir():
         #    myvalue = eval(name)
         #    print name, "is", type(name), "and is equal to ", myvalue
        time.sleep(3)

def run():
    p = Process(target=ix)
    p.start()



