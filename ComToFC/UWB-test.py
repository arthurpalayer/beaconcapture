import serial
import time

DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)
print("Connected to " + DWM.name)
DWM.write(b'\r\r')
res = DWM.read(10)
time.sleep(0.5)
DWM.write(b'lec\r')
time.sleep(1)
while True:
    time.sleep(.5)
    try:
        line = DWM.readline()
        if(line):
            if len(line)>=10:
                print(line)
                parse=line.decode().split(",")
                distance = parse[parse.index("AN0") + 5]
                print(distance)
            else:
                print("Distance not calculated")
    except Exception as ex:
        print(ex)
        break

DWM.write("\r".encode())
DWM.close()

