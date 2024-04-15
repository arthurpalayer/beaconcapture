from msp import MultiWii
from util import push16
from drone import packetconvert
import time 
import video
import socket
import threading as thread

HOST = "10.42.0.1"		#define Host
PORT = 6969			#define port
BUFFSIZE = 64			#define size of buffer
HOSTSERV = "10.42.0.254"

def low_motor(board, speed):
	buf = []
	push16(buf, speed)
	push16(buf, speed)
	push16(buf, 1000)
	push16(buf, speed)
	push16(buf, 1500)
	push16(buf, 1000)
	push16(buf, 1000)
	push16(buf, 1000)
	board.sendCMD(MultiWii.SET_RAW_RC, buf)

def sendspeed(board, ail, elv, thr, rud):
	buf = []
	push16(buf, int(ail * 1000) + 1000)
	push16(buf, int(elv * 1000) + 1000)
	push16(buf, int(thr * 1000) + 1000)
	push16(buf, int((rud) * 1000) + 1000)
	push16(buf, 1500)
	push16(buf, 1000)
	push16(buf, 1000)
	push16(buf, 1000)
	board.sendCMD(MultiWii.SET_RAW_RC, buf)
	print(buf)

def landing(board):
	for x in range(20):
		buf = [] 
		push16(buf, 1500)
		push16(buf, 1500)
		push16(buf, 1100)
		push16(buf, 1500)
		push16(buf, 1500)
		push16(buf, 1000)
		push16(buf, 1000)
		push16(buf, 1000)
		board.sendCMD(MultiWii.SET_RAW_RC, buf)
		time.sleep(0.025)

def control():
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		flag = 1
		while flag != 0:
			try:
				s.bind((HOST, PORT))
				flag = 0
				print("conection")
			except: 
				time.sleep(0.05)
				print("bind fail")
				pass
            
		board = MultiWii("/dev/ttyACM0")
		time.sleep(1.0)
		board.enable_arm()          #enable arming
		board.arm()              #arm the board
	    #MOTORS CANNOT STOP SPINNING	
		try:	
			buf = []
			while 1:
				data, addr = s.recvfrom(BUFFSIZE)
				data = int.from_bytes(data)
				converted_data, msg = packetconvert(data)

				#converted data[0] encoding scheme:
				#                     0x1F = disarm
				#                     0x1 = Manual
				#                     0x2 = AUTO
				#                     0x4 = HOVER
				#
				if(converted_data[0] >= 0xF):
					board.disarm()
					board.disable_arm()
					msg = "DISARMING"
					s.sendto(msg.encode(), addr)
					landing(board)
                    
					break
				elif (converted_data[0] == 0x1):
					print("CONVERSION")

					rudder = converted_data[4] / 1023           #left x axis
					throttle = converted_data[2] / 1023   #left y axis
					throttle = throttle * 0.5
					aileron = converted_data[3] / 1023         #right x axis
					elevator = converted_data[5] / 1023         #right y axis
					sendspeed(board, aileron, elevator, throttle, rudder)
					msg = "MANUAL"
					time.sleep(0.025)



				elif(converted_data[0] == 0x2 | converted_data[0] == 0x4):
					print("Manual control off")
					sendspeed(board, 0.5, 0.5, 0.25, 0.5)	
					msg = "AUTOHOVER"
					time.sleep(0.025)
				else:
					print("else")
					sendspeed(board, 0.5, 0.5, 0.25, 0.5)
					msg = "ELSE"
					time.sleep(0.025)
				s.sendto(msg.encode(), addr)

		except KeyboardInterrupt:
#			landing(board)
			board.disarm()          #disarm the board
			board.disable_arm()
	return

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
#	t1 = thread.Thread(target=control)
	#t2 = thread.Thread(target=video.videoserver)
#	t1.start()
	#t2.start()
#	t1.join()
	#t2.join()
	control()
