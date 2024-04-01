from gpiozero import MCP3002
from time import sleep
from gpiozero import LED, Button
import socket
from numpy import uint64
import numpy as np
#######64 bit packets 47:38 x1, 37:28 y1, 27:18 x2, 17:8 y2, 7:5 sw, 4:0 buttons

#SHAMTS
X1 = 38
Y1 = 28
X2 = 18
Y2 = 8
SW = 5
PB = 0
bitmask10 = 0x03FF
bitmask = uint64(bitmask10)
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
count = 0

#startserver()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = '10.42.0.1'
PORT = 6001
packet = uint64(0)
while (1):
        
    print(count)
    if (sw0.is_pressed):
        print("0") 
    if(sw1.is_pressed):
        print("0") 
    if (sw2.is_pressed):
        print("0") 
    if (pb0.is_pressed):
        print("0")
    if (pb1.is_pressed):
        print("1")
    if (pb2.is_pressed):
        print("2")
    if (pb3.is_pressed):
        print("3")
    if (pb4.is_pressed):
        print("4")

    x1u = uint64(x1.value * 1024)
    x1u = x1u & bitmask 
    packet = (x1u << uint64(X1))
    x2u = uint64(x2.value * 1024)
    x2u = x2u & bitmask
    packet = packet | (x2u << uint64(X2))
    y1u = uint64(y1.value * 1024)
    y1u = y1u & bitmask
    packet = packet | (y1u << uint64(Y1))
    y2u = uint64(y2.value * 1024)
    y2u = y2u & bitmask
    packet = packet | (y2u << uint64(Y2))
    sleep(0.2)
    count = count + 1
    packet = str(packet)
    print(packet)
    packet = packet.encode('utf_8')
    s.sendto(packet, (HOST, PORT))
 
