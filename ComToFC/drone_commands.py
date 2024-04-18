from msp import MultiWii
from util import push16
from drone import packetconvert
from drone_server_example import get_accel
import time 
import video
import socket
import threading as thread

HOST = "10.42.0.1"		#define Host
PORT = 6969			#define port
IMU_PORT = 6970
BUFFSIZE = 64			#define size of buffer
HOSTSERV = "10.42.0.254"
HOVER = 1250

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
    aileron = int(ail * 1000 + 1375)
    rudder = int((rud * 1000) + 1250)
    elevator = int((elv * 1000) + 1375)
    thrust = (int((thr - 0.5) * 1000 + 1000))

    if (thrust < 1000):
        thrust = 1000

    print("AIL: ",aileron, " RUDDER: ", rudder, " ELV: ", elevator, " THR: ", thrust)

    push16(buf, int(aileron))
    push16(buf, elevator)
    push16(buf, thrust)
    push16(buf, rudder)
    
    push16(buf, 1500)
    push16(buf, 1000)
    push16(buf, 1000)
    push16(buf, 1000)
    board.sendCMD(MultiWii.SET_RAW_RC, buf)

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
        
def auto(board, accel):
    #elevator x axis
    #aileron y axis
    x_accel = accel[0]
    y-accel = accel[1]
    aileron = int(x_accel * 100) + 1500
    elevator = int(y_accel * 100) + 1500

    buf = []
    push16(buf, aileron)
    push16(buf, elevator)
    push16(buf, HOVER)
    push16(buf, 1500)
    push16(buf, 1500)
    push16(buf, 1000)
    push16(buf, 1000)
    push16(buf, 1000)

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
        notarmed = 1 
        msg = "READY"
        msg = msg.encode()

        while (notarmed):
            data, addr = s.recvfrom(BUFFSIZE)
            s.sendto(msg, addr)
            data = int.from_bytes(data)
            if (data & 32 != 0 | data & 128 != 0):
                notarmed = 0
            else:
                notarmed = 1
        msg = "ARMING"
        print("arming")
        msg = msg.encode()
        s.sendto(msg, addr)
        time.sleep(2)
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
                if(converted_data[0] == 0x1F):
                    msg = "DISARMING"
                    s.sendto(msg.encode(), addr)
                    landing(board)
                    board.disarm()
                    board.disable_arm()
                    msg = "DISARMED"
                    s.sendto(msg.encode(), addr)
                    break

                elif (converted_data[0] == 0x1):
                    print("CONVERSION")
                    msg = "MANUAL"
                    s.sendto(msg.encode(), addr)
                    rudder = converted_data[4] / (1023 * 2)           #left x axis
                    throttle = converted_data[2] / (1023)   #left y axis
                    aileron = converted_data[3] / (1023 * 4)         #right x axis
                    elevator = converted_data[5] /( 1023 * 4)        #right y axis
                    sendspeed(board, aileron, elevator, throttle, rudder)

                elif(converted_data[0] == 0x2 '''| converted_data[0] == 0x4'''):
                    print("Manual control off")
                    msg = "AUTOHOVER"
                    s.sendto(msg.encode(), addr)
                    sendspeed(board, 0.5, 0.5, 0.25, 0.5)

                elif(converted_data[0] == 0x4):
                    print("Autonomous mode on")
                    msg = "AUTONOMOUS")
                    s.sendto(msg.encode(), addr)
                    accel = get_accel(HOST, IMU_PORT)
                    auto(board, accel)

                else:
                    print("else")
                    msg = "ELSE"
                    s.sendto(msg.encode(), addr)
                    sendspeed(board, 0.5, 0.5, 0.25, 0.5)	


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
    control()
    #t1 = thread.Thread(target=control)
    #t2 = thread.Thread(target=video.videoserver)
    #t1.start()
    #t2.start()
    #t1.join()
    #t2.join()

