#!/usr/bin/env python

from msp import MultiWii
import time
board = MultiWii("/dev/ttyACM0")
while True:
    board.getData(MultiWii.RAW_IMU)
    print(board.rawIMU)

    #board.getData(MultiWii.ALTITUDE)
    #print(board.altitude)


    
