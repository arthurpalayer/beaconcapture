import gpiozero
import header
import numpy as np
from numpy import uint64
import threading as thread
import time
import socket
import pickle
from picamera2 import Picamera2
import struct
from msp import MultiWii
from util import push16
import cv2


X1 = 38
X2 = 18
Y1 = 28
Y2 = 8

def recvcontrol():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.bind((HOST, CTRLPORT))

    board = MultiWii("dev/ttyACM0")
    time.sleep(1.0)

    board.enable_arm()
    board.arm()

    while 1:
        addr, data =  s.recvfrom(CTLBUFSIZE)
        data = packetconvert(packet) 
        send_command(data, board)

    board.disarm

def send_command(data, board): 
    rudder = converted_data[2] / 1023           #left x axis
    throttle = converted_data[4] / 1023         #left y axis
    aileron = converted_data[3] / 1023          #right x axis
    elevator = converted_data[5] / 1023         #right y axis

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

if __name__ == "__main__":
    t1 = thread.Thread(target=videoserver)
    t2 = thread.Thread(target=recvcontrol)
    t1.start()
    t2.start()
    t1.join()
    t2.join()



