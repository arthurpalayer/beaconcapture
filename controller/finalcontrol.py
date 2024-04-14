from numpy import uint64, uint32
import time
from gpiozero import Button, LED, MCP3002
import socket
import numpy as np
import threading as thread
import cv2
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
import pickle
import video
#######64 bit packets 47:38 x1, 37:28 y1, 27:18 x2, 17:8 y2, 7:5 sw, 4:0 buttons

#SHAMTS
X1 = 38
Y1 = 28
X2 = 18
Y2 = 8
SW = 5
PB = 1
bitmask10 = 0x03FF
bitmask = (bitmask10)
PB0 = 14
PB1 = 27
PB2 = 18
PB3 = 17
PB4 = 15
SW0 = 24
SW1 = 22
SW2 = 23
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
PORT1 = 6969
PORT2 = 6969
VIDBUFFSIZE = 1000000
VIDPORT = 6967

sens = 3
manualmode = False
automode = False
hovermode = False
disarmnow = False

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

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial)

def controlcheck():
    packet = 0
    dataset = []
    if (sw0.is_pressed):
        packet = packet | 32
        dataset.append("Switch 0: ON")
    if(sw1.is_pressed):
        packet = packet | 64
        dataset.append("SWITCH 1: ON")
    if (sw2.is_pressed):
        packet = packet | 128 
        dataset.append("SWITHC 2: ON")
    if (pb0.is_pressed):
        dataset.append("PB0 : ON")
        global manualmode = ~manualmode
    if (pb1.is_pressed):
        dataset.append("PB1 : ON")
        global automode = ~automode
    if (pb2.is_pressed):
        dataset.append("PB2: ON")
        global hovermode = ~hovermode
    if (pb3.is_pressed):
        dataset.append("PB3: ON")
        global disarmnow = ~disarmnow 
    if (pb4.is_pressed):
        dataset.append("PB4: ON")
        packet = packet | 16

    global status = ""


    if (disarmnow == True):
        status = "DISARM" 
        packet = packet | 0x1F
        led0.on()
        led1.on()
        led2.on()
    elif (manualmode == True):
        status = "MANUAL MODE"
        packet = packet | 0x1
        led0.on()
        led1.off()
        led2.off()
    elif (automode == True):
        status = "AUTO MODE"
        packet = packet | 0x2
        led0.off()
        led1.on()
        led2.off()
    elif (hovermode == True):
        status = "HOVER MODE"
        packet = packet | 0x4
        led0.off()
        led1.off()
        led2.on() 
 
    #print(dataset)
   # print(packet)
    dataset.clear()
    x1u = int(round(x1.value, sens) * 1024) #percentage of 1024, can decrease granularity here 
    x1u = x1u & bitmask #truncate bits  
    packet = packet | (x1u << (X1)) 
    x2u = int(round(x2.value, sens) * 1024)
    x2u = x2u & bitmask
    packet = packet | (x2u << (X2))
    y1u = int(round(y1.value, sens) * 1024)
    y1u = (y1u & bitmask)
    packet = packet | (y1u << (Y1))
    y2u = int(round(y2.value, sens) * 1024)
    y2u = y2u & bitmask
    packet = packet | (y2u << (Y2))
    packet = int(packet)
    
    return (packet, status)

def control():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    draw = canvas(device)
    while (1):
        packet, status = controlcheck()
        packet = packet.to_bytes(16)
        try: 
            s.sendto(packet, (HOST, PORT2))
            print("SEND SUCCESS")
        except:
            status = "no connection"
            pass
        lcd(status, draw)

def lcd(status, draw):
    x = 2
    y = 15
    
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    font = ImageFont.trutype("font.ttf", 14)
    draw.text((x,y), status, fill = "white", font = font)


if __name__ == "__main__":
    try:
        if (0 == 1):
            t1 = thread.Thread(target=control)
            t2 = thread.Thread(target=video.videorecv)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        else:
            control()
    except KeyboardInterrupt:
        pass


    time.sleep(1)



