import os
from numpy import uint64, uint32
import time
from gpiozero import Button, LED, MCP3002
import socket
import numpy as np
import threading as thread
import vlc
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
LED1 = 6
LED2 = 16
MOSI = 9
MISO = 10
CS0 = 8
CS1 = 7
SCLK = 11


#HOST = "127.0.0.1"
HOST = "10.42.0.1"
PORT1 = 6969
PORT2 = 6968

def startsock(portnum):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def setupcontrol():
    #copy paste control code here
    global sw0, sw1, sw2, pb0, pb1, pb2, pb3, pb4, led0, led1, led2, x1, x2, y1, y2
    sw0 = Button(SW0, pull_up=None, active_state=True)
    sw1 = Button(SW1, pull_up=None, active_state=True)
    sw2 = Button(SW2, pull_up=None, active_state=True)
    pb0 = Button(PB0, pull_up=None, active_state=True)
    pb1 = Button(PB1, pull_up=None, active_state=True)
    pb2 = Button(PB2, pull_up=None, active_state=True)
    pb3 = Button(PB3, pull_up=None, active_state=True)
    pb4 = Button(PB4, pull_up=None, active_state=True)
    led0 = LED(LED0)
    led1 = LED(LED1)
    led2 = LED(LED2)

    x1 = MCP3002(channel=0, clock_pin=SCLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS0)
    x2 = MCP3002(channel=0, clock_pin=SCLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS1)
    y1 = MCP3002(channel=1, clock_pin=SCLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS0)
    y2 = MCP3002(channel=1, clock_pin=SCLK, mosi_pin=MOSI, miso_pin=MISO, select_pin=CS1)

def controlcheck():
    
    packet = 0
    if (sw0.is_pressed):
       print("PACKETYAY")
       packet = packet | 32
    if(sw1.is_pressed):
        packet = packet | 64
    if (sw2.is_pressed):
        packet = packet | 128 
    if (pb0.is_pressed):
        packet = packet | 1
    if (pb1.is_pressed):
        packet = packet | 2
    if (pb2.is_pressed):
        packet = packet | 4
    if (pb3.is_pressed):
        packet = packet | 8
    if (pb4.is_pressed):
        packet = packet | 16

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
    print(packet)
    return packet

def control(timeset):
    setupcontrol()
    while (1):
        packet = controlcheck()
        #        packet = struct.pack('!I', aint) 
        packet = packet.to_bytes(16)
        s.sendto(packet, (HOST, PORT1))
        time.sleep(timeset)

def lcd():
    serial = i2c(port=1, address=0x3c)

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        font = ImageFont.trutype("font.ttf", 14)
        draw.text((x,y), "", fill = "white", font = font)
        sleep(0.5)

if __name__ == "__main__":
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control(0.025)
  #  t1 = thread.Thread(target=control)
    #t2 = thread.Thread(target=video)
  #  t1.start()
  #  t2.start()
  #  t1.join()
 #   t2.join()


