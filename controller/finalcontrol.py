from numpy import uint64, uint32
import time
from gpiozero import Button, LED, MCP3002
import socket
import numpy as np
import threading as thread
import cv2
import pickle

#######64 bit packets 47:38 x1, 37:28 y1, 27:18 x2, 17:8 y2, 7:5 sw, 4:0 buttons

#SHAMTS
X1 = 38
Y1 = 28
X2 = 18
Y2 = 8
SW = 5
PB = 0
bitmask10 = 0x03FF
bitmask = (bitmask10)
PB0 = 14
PB1 = 27
PB2 = 18
PB3 = 17
PB4 = 15
SW0 = 24
SW1 = 23
SW2 = 22
LED0 = 13
LED1 = 16 
LED2 = 6
MOSI = 9
MISO = 10
CS0 = 8
CS1 = 7
SCLK = 11


#HOST = "127.0.0.1"
HOST = "10.42.0.1"
HOSTSERV = "10.42.0.254"
PORT1 = 6969
PORT2 = 6968
VIDBUFFSIZE = 1000000



def setupcontrol():
    #copy paste control code here
    global sw0 
    sw0 = Button(SW0, pull_up=None, active_state=True)
    global sw1 
    sw1 = Button(SW1, pull_up=None, active_state=True)
    global sw2 
    sw2 = Button(SW2, pull_up=None, active_state=True)
    global pb0 
    pb0 = Button(PB0, pull_up=None, active_state=True)
    global    pb1 
    pb1 = Button(PB1, pull_up=None, active_state=True)
    global pb2 
    pb2 = Button(PB2, pull_up=None, active_state=True)
    global pb3 
    pb3 = Button(PB3, pull_up=None, active_state=True)
    global pb4 
    pb4 = Button(PB4, pull_up=None, active_state=True)
    global led0
    led0= LED(LED0)
    global led1
    led1 = LED(LED1)
    global led2
    led2= LED(LED2)

    global x1
    x1 = MCP3002(channel=0, clock_pin=SCLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS0)
    global x2
    x2= MCP3002(channel=0, clock_pin=SCLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS1)
    global y1
    y1 = MCP3002(channel=1, clock_pin=SCLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS0)
    global y2
    y2= MCP3002(channel=1, clock_pin=SCLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS1)

def controlcheck():

    packet = 0
    dataset = []
    if (sw0.is_pressed):
      # print("PACKETYAY")
        packet = packet | 32
        dataset.append("Switch 0: ON")
    if(sw1.is_pressed):
        packet = packet | 64
        led1.on()
        dataset.append("SWITCH 1: ON")
    if (sw2.is_pressed):
        dataset.append("SWITHC 2: ON")
        led2.on()
        packet = packet | 128 
    if (pb0.is_pressed):
        dataset.append("PB0 : ON")
        packet = packet | 1
    if (pb1.is_pressed):
        dataset.append("PB1 : ON")
        packet = packet | 2
    if (pb2.is_pressed):
        dataset.append("PB2: ON")
        packet = packet | 4
    if (pb3.is_pressed):
        dataset.append("PB3: ON")
        packet = packet | 8
    if (pb4.is_pressed):
        dataset.append("PB4: ON")
        packet = packet | 16

    dataset.clear()
    x1u = int(x1.value * 1024) #percentage of 1024, can decrease granularity here 
    x1u = x1u & bitmask #truncate bits  
    packet = (x1u << (X1)) 
    x2u = int(x2.value * 1024)
    x2u = x2u & bitmask
    packet = packet | (x2u << (X2))
    y1u = int(y1.value * 1024)
    y1u = (y1u & bitmask)
    packet = packet | (y1u << (Y1))
    y2u = int(y2.value * 1024)
    y2u = y2u & bitmask
    packet = packet | (y2u << (Y2))
    packet = int(packet)
    return packet

def control():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    setupcontrol()
    timeset = 0.005
    while (1):
        packet = controlcheck()
        #        packet = struct.pack('!I', aint) 
        packet = packet.to_bytes(16)
        led1.off()
        s.sendto(packet, (HOST, PORT2))
        led1.on()
        time.sleep(timeset )

def lcd():
    serial = i2c(port=1, address=0x3c)

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        if (sw0.is_pressed()):
            status = "MANUAL MODE"
        else:
            status = "AUTO"
        font = ImageFont.trutype("font.ttf", 14)
        draw.text((x,y), status, fill = "white", font = font)
        sleep(0.5)

def makeconns(s):
    msg = "utf"
    s.sendto(msg.encode('utf-8'), (HOST, VIDPORT))

def videosocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    makeconns(s)
    while 1:
        data, addr = s.recvfrom(VIDBUFFSIZE)
        data = pickle.loads(data)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("LIVE FEED", data)
        
def donothing():
    time.sleep(0.2)

if __name__ == "__main__":
    global s
    t1 = thread.Thread(target=donothing)
    t2 = thread.Thread(target=videosocket)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


