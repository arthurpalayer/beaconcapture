import gpiozero
import numpy as np
from numpy import uint64
import threading as thread
import time
import socket
import pickle
from picamera2.encoders import H264Encoder, Quality
from picamera2 import picamera2
import struct
from msp import MultiWii
from util import push16

X1 = 38
X2 = 18
Y1 = 28
Y2 = 8


PORT0 = 6968
PORT1 = 6969
HOST = "" #fill
BUFFERSIZE = 4096 
CTLBUFSIZE = 8

def videosocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cam.start(show_preview=True)
    while 1:
        im = cam.capture_array()
        ret, buffer = cv2.imencode(".jpg", im, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        x = pickle.dumps(buffer)
        s.sendto(x, (HOST, PORT0))

def recvcontrol():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.bind((HOST, PORT1))
    while 1:
        data,addr =  s.recvfrom(CTLBUFSIZE)
        data = packetconvert(packet) 

def packetconvert(packet):
    #packet here is a packed struct 
    #    bindata = struct.unpack('!I', packet)[0]
    bindata = packet
    bitmask10 = (0x3FF)
    bitmask5 = (0x1F) 
    bitmask3 = (0x7)
    bitmask1 = (0x1)
    data[0] = (bindata & bitmask5) #pb0 - ph4
    data[1] = (bindata & bitmask3)#switches
    data[2] = (bindata & (bitmask10 << (X1))) #x1
    data[3] = (bindata & (bitmask10 << (X2)))#x2
    data[4] = (bindata & (bitmask10 << (Y1)))#y1
    data[5] = (bindata & (bitmask10 << (Y2)))#y2
    return data

def send_command(data, board): 
    rudder = converted_data[2] / 1024           #left x axis
    throttle = converted_data[4] / 1024         #left y axis
    aileron = converted_data[3] / 1024          #right x axis
    elevator = converted_data[5] / 1024         #right y axis

    buf = []
    push16(buf, int(aileron * 1000 + 1000))		    # aileron
    push16(buf, int(elevator * 1000 + 1000))	    # elevator
    push16(buf, int(throttle * 1000 + 1000))	    # throttle
    push16(buf, int(rudder * 1000 + 1000))		    # rudder
    push16(buf, 1500)		                        # aux1
    push16(buf, 1000)		                        # aux2
    push16(buf, 1000)		                        # aux3
    push16(buf, 1000)		                        # aux4
    board.sendCMD(MultiWii.SET_RAW_RC, buf)

    time.sleep(0.025)

if __name__ = "__main__":
    t1 = thread.Thread(target=videosocket)
    t2 = thread.Thread(target=recvcontrol)
    t1.start()
    t2.start()
    t1.join()
    t2.join()



