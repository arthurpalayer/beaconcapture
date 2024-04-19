import header
from msp import MultiWii
from util import push16
import time 
import threading as thread
import network
import uwb

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
    y_accel = accel[1]
    aileron = int(x_accel * 1000) + 1500
    elevator = int(y_accel * 1000) + 1500
    if aileron < 1375:
        aileron = 1375
    if aileron > 1625:
        aileron = 1625
    if elevator < 1375:
        elevator = 1375
    if elevator > 1625:
        elevator = 1625
    '''
    if(thresh_dist < uwb.distance):
        aileron = int(x_accel * 100) + 1500
        elevator = int(y_accel * 100) + 1500
    else:
        aileron = 1500
        elevator = 1500
    '''
    print(aileron)
    print(elevator)
    buf = []
    push16(buf, aileron)
    push16(buf, elevator)
    push16(buf, 1250)
    push16(buf, 1500)
    push16(buf, 1500)
    push16(buf, 1000)
    push16(buf, 1000)
    push16(buf, 1000)
    board.sendCMD(MultiWii.SET_RAW_RC, buf)

def control():
    controlserver = network.server("control", header.HOST, header.CONTROLPORT)
    controlserver.makeconn()
    beaconserver = network.beaconserver("beacon", header.HOST, header.BEACONPORT)
    #beaconserver = network.server("beacon", header.HOST, header.BEACONPORT)
    #beaconserver.makeconn()

    notarmed = 1
    first_auto = 1
    msg = "READY"
    msg = msg.encode()

    while (notarmed):
        data, addr = controlserver.controlrecv(16, "READY")
        if data[1][2] == 128:
            notarmed = 0
        else:
            notarmed = 1

    msg = "ARMING"
    print("arming")
    msg = msg.encode()
    controlserver.s.sendto(msg, addr)
    board = MultiWii("/dev/ttyACM0")
    time.sleep(1.0)
    board.enable_arm()          #enable arming
    board.arm()              #arm the board
    #MOTORS CANNOT STOP SPINNING	
    try:	
        buf = []
        while 1:
            converted_data, addr = controlserver.controlrecv(header.CONTROLBUFFSIZE, "TAKINGDATA")
            #converted data[0] encoding scheme:
            #                     0x1F = disarm
            #                     0x1 = Manual
            #                     0x2 = AUTO
            #                     0x4 = HOVER
            #
            if(converted_data[0] == 0x1F):
                msg = "DISARMING"
                controlserver.s.sendto(msg.encode(), addr)
                landing(board)
                board.disarm()
                board.disable_arm()
                msg = "DISARMED"
                controlserver.s.sendto(msg.encode(), addr)
                break

            elif (converted_data[0] == 0x1):
                print("CONVERSION")
                msg = "MANUAL"
                controlserver.s.sendto(msg.encode(), addr)
                rudder = converted_data[4] / (1023 * 2)           #left x axis
                throttle = converted_data[2] / (1023)   #left y axis
                aileron = converted_data[3] / (1023 * 4)         #right x axis
                elevator = converted_data[5] /( 1023 * 4)        #right y axis
                sendspeed(board, aileron, elevator, throttle, rudder)

            elif(converted_data[0] == 0x2):
                '''if(first_auto):
                    global dist_thresh = uwb.distance
                    first_auto = 0'''
                print("Autonomous mode on")
                msg = "AUTONOMOUS"
                controlserver.s.sendto(msg.encode(), addr)
                xyz = beaconserver.getdata()
                print(xyz)
                #accel = get_accel(HOST, IMU_PORT)
                auto(board, xyz)

            elif(converted_data[0] == 0x4):
                print("Manual control off")
                msg = "AUTOHOVER"
                controlserver.s.sendto(msg.encode(), addr)
                sendspeed(board, 0.125, 0.125, 0.25, 0.25)

            else:
                print("else")
                msg = "ELSE"
                controlserver.s.sendto(msg.encode(), addr)
                sendspeed(board, 0.125, 0.125, 0.25, 0.25)	


    except KeyboardInterrupt:
        #			landing(board)
        board.disarm()          #disarm the board
        board.disable_arm()
    return

def video():
    videoserver = network.videoserver("camera", header.HOST, header.VIDEOPORT)
    req, addr = videoserver.makeconn()
    videoserver.sendvideo(addr)

if __name__ == "__main__":
    try:
        #uwb.intitialze_uwb()
        if (1 == 1):
            t1 = thread.Thread(target=control)
            t2 = thread.Thread(target=video)
            #t3 = thread.Thread(target=uwb.read_uwb)
            t1.start()
            t2.start()
            #t3.start()
            t1.join()
            t2.join()
            #t3.join()
    except KeyboardInterrupt:
        pass

    #control()
    #t1 = thread.Thread(target=control)
    #t2 = thread.Thread(target=video.videoserver)
    #t1.start()
    #t2.start()
    #t1.join()
    #t2.join()

