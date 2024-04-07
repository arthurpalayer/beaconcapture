from msp import MultiWii
from util import push16
import time
import socket

###########################################################
#	64 bit packets
#	47:38 -> x1	37:28 -> y1
#	27:18 -> x2	17:8 -> y2
#	7:5 -> sw	4:0 -> buttons
###########################################################


HOST = "127.0.0.1"		#define Host
PORT = 6969			#define port
BUFFSIZE = 64			#define size of buffer

board = MultiWii("/dev/ttyACM0")
print("Flight controller Connected")

time .sleep(1.0)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
   
    msg = "recvd" 
    
    board.enable_arm()          #enable arming
    board.enable()              #arm the board

    while 1:
        data = s.recvfrom(BUFFSIZE)
        if (len(data[0])):
            sendbuffer = "server received data"
            sendbuffer = str.encode(sendbuffer)
            print("received packet")
            print(data[0])
            addr = data[1]
            print(addr)
            s.sendto(sendbuffer, addr)
            #s.sendall(sendbuffer, addr[0])

            

    board.disarm()          #disarm the board
    
         
