from gpiozero import MCP3002
from gpiozero import Button
from time import sleep
from gpiozero import LED

#define pins
PB0 = 14 #8
PB1 = 27 #13
PB2 = 18 #12
PB3 = 17 #11
PB4 = 15 #10
SW0 = 24 #18
SW1 = 22 #15
SW2 = 23 #16
LED0 = 13 #33
LED1 = 6 #31
LED2 = 16 #3i6

x1 = MCP3002(0, device=0)
y1 = MCP3002(1, device=0)
x2 = MCP3002(0, device=1)
y2 = MCP3002(1,device=1)


pb0 = Button(PB0, pull_up=None, active_state=True)
pb1 = Button(PB1, pull_up=None, active_state=True)
pb2 = Button(PB2, pull_up=None, active_state=True)
pb3 = Button(PB3, pull_up=None, active_state=True)
pb4 = Button(PB4, pull_up=None, active_state=True)
sw0 = Button(SW0, pull_up=None, active_state=True)
sw1 = Button(SW1, pull_up=None, active_state=True)
sw2 = Button(SW2, pull_up=None, active_state=True)
led0 = LED(LED0)
led1 = LED(LED1)
led2 = LED(LED2)
while (1):
    print("x1: ", int(round(x1.value,3) * 100))
    print("x2: ", int(round(x2.value,3) * 100))
    print("y1: ", int(round(y1.value,3) * 100))
    print("y2: ", int(round(y2.value,3) * 100))
    if (pb0.is_pressed == True):
        print("A")
    if (pb1.is_pressed == True):
        print("B")
    if (pb2.is_pressed == True):
        print("C")
    if (pb3.is_pressed == True):
        print("d")
    if (pb4.is_pressed == True):
        print("E")
    if (sw0.is_pressed):
        print("SW0")
    if (sw1.is_pressed):
        print("SW1")
    if (sw2.is_pressed):
        print("SW2")

    led0.on
    led1.on
    led2.on
    sleep(0.2)

