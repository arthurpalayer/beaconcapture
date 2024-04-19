import gpiozero
import numpy as np
import threading as thread
import time
import socket
import cv2


X1 = 38
X2 = 18
Y1 = 28
Y2 = 8


def packetconvert(packet):
    #packet here is a packed struct 
    #    bindata = struct.unpack('!I', packet)[0]
    bindata = packet
    bitmask10 = 0x3FF
    bitmask5 = 0x1F 
    bitmask3 = 0x7
    bitmask1 = 0x1

    usermode = False
    automode = False
    disarmnow = False
    hovermode = False
#    print(bindata)
 #   print(type(bindata))
    data = [0,[0,0,0], 0, 0, 0, 0, 0]
    #data[0] = [bindata & 1, bindata & 2, bindata & 4, bindata & 8, bindata & 16] #pb0 - ph4
    data[0] = bindata & 0x1F
    msg = ""
    if (data[0] == 0x1):
        msg = "MANUAL"
    elif (data[1] == 0x2):
        msg = "AUTO"
    elif (data[0] == 0x4):
        msg = "HOVER"
    elif (data[0] == 0x1F):
        msg = "DISARMING"
    else:
        msg = "FOUND"

    data[1] = [bindata & 32, bindata & 64, bindata & 128]#switches
    data[2] = (bindata & (bitmask10 << (X1))) >> X1 #x1
    data[3] = (bindata & (bitmask10 << (X2))) >> X2#x2
    data[4] = (bindata & (bitmask10 << (Y1))) >> Y1#y1
    data[5] = (bindata & (bitmask10 << (Y2))) >> Y2#y2
    
    #print(bindata)

    return data, msg



