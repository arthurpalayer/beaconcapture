from gpiozero import MCP3002
from time import sleep
from gpiozero import LED, Button

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

while (1):

    
    print(count)
    if (sw0.is_pressed):
        led0.on()
    else:
        led0.off()
    if(sw1.is_pressed):
        led1.on()
    else:
        led1.off()
    if (sw2.is_pressed):
        led2.on()
    else:
        led2.off()

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

    print("x1: ", x1.value)
    print("x2: ", x2.value)
    print("y1: ", y1.value)
    print("y2; ", y2.value)
    sleep(0.2)
    count = count + 1
