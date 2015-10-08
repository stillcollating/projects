from multiprocessing import Process
from multiprocessing import Pipe

import time

def ix(conn):
    running = True

    while running:
        time.sleep(10)
        conn.send('hello')


if __name__ == '__main__':
    from kivympd2 import KivyMpd2
    k = KivyMpd2()
    a, b = Pipe()
    k.p = a
    x = Process(target=ix,args=(b,))
    x.start()
    k.run()

