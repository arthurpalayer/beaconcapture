from gpiozero import MCP3002
from time import sleep

x1 = MCP3002(channel=0, clock_pin=11, mosi_pin=9, miso_pin=10, select_pin=8)
x2 = MCP3002(channel=0, clock_pin=11, mosi_pin=9, miso_pin=10, select_pin=7)
y1 = MCP3002(channel=1, clock_pin=11, mosi_pin=9, miso_pin=10, select_pin=8)
y2 = MCP3002(channel=1, clock_pin=11, mosi_pin=9, miso_pin=10, select_pin=7)
count = 0

while (1):


    print(count)
    print("x1: ", x1.value)
    print("x2: ", x2.value)
    print("y1: ", y1.value)
    print("y2; ", y2.value)
    sleep(0.5)
    count = count + 1
