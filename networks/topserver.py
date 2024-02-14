import socket 
import cv2 as cv
import numpy 
import pickle
import threading as thread


def cam(s):
   s.bind((ip, port))

   while 1:
       x = s.recvfrom(BUFSIZE)
       clientip = x[1][0]
       data = x[0] #clear buf
       data = pickle.loads(data)
       data = cv.imdecode(data, cv.IMREAD_COLOR)


def control(s):


if __name__ == "__main__":
    HOST = "127.0.0.1"
    udpPort = 6002
    tcpPORT = 6001

    sUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    t1 = thread.Thread(target=cam, args=(sUDP,))
    t2 = thread.Thread(target=control, args=(sTCP,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("serverdone")
