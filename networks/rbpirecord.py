import socket
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

serverip = "10.42.0.1"
serverport = 6968



picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (400, 240)})
picam2.configure(video_config)
encoder = H264Encoder(5000)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	s.connect((serverip, serverport))
	stream = s.makefile("wb")
	picam2.start_preview(True)
	picam2.start_recording(encoder, FileOutput(stream))
	time.sleep(1000)
	picam2.stop_recording()
