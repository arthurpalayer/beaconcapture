from drone import packetconvert
from util import push16
import time 
import video
import socket
import threading as thread

HOST = "10.42.0.1"		#define Host
PORT = 6969			#define port
BUFFSIZE = 64			#define size of buffer
HOSTSERV = "10.42.0.254"


def control():
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		flag = 1
		while flag != 0: #handling ip not functioning
			try:
				s.bind((HOST, PORT))
				flag = 0
				print("conection")
			except: 
				time.sleep(0.05)
				print("no connection")

		print("arming")		
		try: 
			while 1:
				data, addr = s.recvfrom(BUFFSIZE)
				data = int.from_bytes(data)
				converted_data = packetconvert(data)

				#converted data[0] encoding scheme:
				#                     0x1F = disarm
				#                     0x1 = Manual
				#                     0x2 = AUTO
				#                     0x4 = HOVER
				#

				if(converted_data[0] == 0xF):
					print("RECEIVED KILL")
					break

				elif (converted_data[0] == 0x1):
					rudder = converted_data[2] / 1024           #left x axis
					throttle = converted_data[4] / 1024         #left y axis
					aileron = converted_data[3] / 1024          #right x axis
					elevator = converted_data[5] / 1024         #right y axis
					print(rudder, throttle, elevator, aileron)
					push16(buf, rudder * 1000 + 1000)
					push16(buf, throttle * 1000 + 1000)
					push16(buf, aileron * 1000 + 1000)
					push16(buf, elevator * 1000 + 1000)
					print(buf)
				elif(not converted_data[0] == 0x2):
					print("Manual control off")
				
		except KeyboardInterrupt:
			print("DISARMING DUE TO SIGINT")
#			landing(board)
	return
def testpush16():
    stat = 0.01
    while 1:
        buf = []
        push16(buf, int(stat * 1000) + 1000)
        push16(buf, int(stat * 900) + 1000)
        push16(buf, int(stat * 800) + 1000)
        push16(buf, int(stat * 700) + 1000)
        push16(buf,int( stat * 600) + 1000)
        push16(buf, 1500)
        push16(buf, 1400)
        stat = stat + 0.01
        time.sleep(0.5)
        print(buf)
def testswitch():
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.bind((HOST, PORT))
		while 1:
			data, addr = s.recvfrom(BUFFSIZE)
			data = int.from_bytes(data)
			converted_data = packetconvert(data)
			print(converted_data[0])
			print(converted_data[1])

if __name__ == "__main__":
	testpush16()
		
