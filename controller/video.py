import threading as thread
import numpy as np
from picamera2 import Picamera2
import cv2
import pickle
import socket
from time import sleep

HOST = '10.42.0.1'
#HOST = '127.0.0.1'
VIDPORT = 6967
VIDBUFFSIZE = 100000
PACKETSIZE = 8

def makeconn(s):
    data, addr = s.recvfrom(PACKETSIZE)
    return addr

def sendconn(s):
    msg = "conn" 
    msg = msg.encode('utf-8')
    s.sendto(msg, (HOST, VIDPORT))

def waitdata(s, timeout):
    ready = select.select([s], [], [], timeout)
    if ready[0]:
        data, addr = s.recvfrom(16)
        print("RECVCONNREQ")
        notconn = 0
    else:
        print("NOMSG")
        noconn = 1

    return noconn

def videoserver():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, VIDPORT))
    addr = makeconn(s) #establish connection to get address to send video to
    print("Made conn")
    cam = Picamera2()
    cam.start()
    while 1:
        im = cam.capture_array()
        ret, buffer = cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 30])
        x = buffer.tobytes()
        s.sendto(x, addr)

def videorecv():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    notconn = 1
    while notconn:
        notconn = sendconn(s)
    print("MADECONN")
    while 1:
        data, addr = s.recvfrom(VIDBUFFSIZE)
        data = np.frombuffer(data, np.uint8)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("LIVEFEED", data)
        cv2.waitKey(1)


if __name__ == "__main__":
    try:
        while 0:
                        
            t1 = thread.Thread(target=videoserver)
            t2 = thread.Thread(target=videorecv)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        videoserver()
    except KeyboardInterrupt:
        pass
