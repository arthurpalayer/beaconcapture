import time 
import socket
from picamera2 import Picamera2
import subprocess

cmd1 = "--"


ip = "10.42.0.254"
port = 6968

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
s.bind((ip, port))
obj = s.makefile("rb")
player = subprocess.Popen(['vlc','--demux', 'h264' ,'-'], stdin=subprocess.PIPE)
count = 0;
while (1):
	data = obj.read(16384)
	player.stdin.write(data)
