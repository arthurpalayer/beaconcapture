import socket
import vlc
import time
import threading as thread

BUFFSIZE = 1024


if __name__ == "__main__":
    t1 = thread.thread(server)
    t2 = thread.thread(client)
    t1.start()
    sleep(1)
    t2.start()
    t1.join()
    t2.join()


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, IP))

    while 1:

def client():
    data, addr = s.recvfrom(BUFFSIZE)
    
