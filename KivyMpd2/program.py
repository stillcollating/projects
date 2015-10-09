from multiprocessing import Process
from multiprocessing import Pipe

import time


#if __name__ != '__main__':


def ix(p_mpd_send, p_mpd_recv):
    running = True

    while running:
        time.sleep(10)
        p_mpd_send.send('hello')
        print p_mpd_recv.recv()


if __name__ == '__main__':
    from kivympd2 import KivyMpd2
    k = KivyMpd2()
    p_mpd_send, p_gui_recv = Pipe()
    p_gui_send, p_mpd_recv = Pipe()
    k.p_gui_send = p_gui_send
    k.p_gui_recv = p_gui_recv
    x = Process(target=ix,args=(p_mpd_send, p_mpd_recv))
    x.start()
    k.run()

