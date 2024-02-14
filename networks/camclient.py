#client code -> controller

from picamera2.encoders import H264Encoder, Quality
import socket
import numpy
import pickle
import threading as thread
from picamera2 import Picamera2
from libcamera import controls

cam = Picamera2()
encoder = H264Encoder()
output = 'out.h264'
cam.start_recording(encoder, output, quality=Quality.MEDIUM)



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
serverip = "127.0.0.1"
serverport = 6969

while True:
    print(output)
    x_as_bytes = pickle.dumps(output)
    s.sendto(x_as_bytes,(serverip , serverport))

