#!/usr/bin/env python

from msp import MultiWii
from util import push16
import time

board = MultiWii("/dev/ttyACM0")
time.sleep(1.0)

board.enable_arm()
board.arm()
try:
    while True:
        buf = []
        push16(buf, 1500)		# aileron
        push16(buf, 1500)		# elevator
        push16(buf, 1500)		# throttle
        push16(buf, 1500)		# rudder
        push16(buf, 1500)		# aux1
        push16(buf, 1000)		# aux2
        push16(buf, 1000)		# aux3
        push16(buf, 1000)		# aux4
        board.sendCMD(MultiWii.SET_RAW_RC, buf)
    
        time.sleep(0.05)
except KeyboardInterrupt:
	board.disarm()
	board.disable_arm()

