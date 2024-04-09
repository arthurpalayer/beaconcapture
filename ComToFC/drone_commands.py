from msp import MultiWii
from util import push16
from drone import packetconvert
import time
import socket

###########################################################
#	64 bit packets
#	47:38 -> x1	37:28 -> y1
#	27:18 -> x2	17:8 -> y2
#	7:5 -> sw	4:0 -> buttons
###########################################################


HOST = "10.42.0.1"		#define Host
PORT = 6969			#define port
BUFFSIZE = 64			#define size of buffer

board = MultiWii("/dev/ttyACM0")
print("Flight controller Connected")

time .sleep(1.0)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
   
    msg = "recvd" 
    
    board.enable_arm()          #enable arming
    board.arm()              #arm the board

    while 1:
	    data, addr = s.recvfrom(BUFFSIZE)
	    data = int.from_bytes(data)
	    converted_data = packetconvert(data)
			
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
	    if(converted_data[1] == 1):
	        break

    board.disarm()          #disarm the board
    
         
