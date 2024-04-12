import threading as thread
from picamera2 import Picamera2
import cv2
import pickle
import socket
from time import sleep

HOST = '127.0.0.1'
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

def videoserver():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, VIDPORT))
    addr = makeconn(s) #establish connection to get address to send video to
    cam = Picamera2()
    cam.start(show_preview=True)
    while 1:
        im = cam.capture_array()
        ret, buffer = cv2.imencode(".jpg", im, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        x = pickle.dumps(buffer)
        s.sendto(x, addr)

def videorecv():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sendconn(s)
    while 1:
        data, addr = s.recvfrom(VIDBUFFSIZE)
        data = pickle.loads(data)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("LIVEFEED", data)


if __name__ == "__main__":
    t1 = thread.Thread(target=videoserver)
    t2 = thread.Thread(target=videorecv)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
