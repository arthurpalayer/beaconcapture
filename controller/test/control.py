from gpiozero import MCP3008
from gpiozero import Button
from time import sleep

x1 = MCP3008(0)
y1 = MCP3008(1)
x2 = MCP3008(2)
y2 = MCP3008(3)
A = Button(4, pull_up=None, active_state=True)
B = Button(17, pull_up=None, active_state=True)
C = Button(27, pull_up=None, active_state=True)
D = Button(22, pull_up=None, active_state=True)


while True:
    print("x1: ",int(round(x1.value,3) * 100))
    print("y1: ",int(round(y1.value,3) * 100))
    print("x2: ",int(round(x2.value,3) * 100))
    print("y2: ",int(round(y2.value,3) * 100))
    if (A.is_pressed):
        print("A")
    if (B.is_pressed):
        print("B")
    if (C.is_pressed):
        print("C")
    if (D.is_pressed):
        print("D")
   
    

    sleep(0.2)

