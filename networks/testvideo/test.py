import socket
import time
import os
import vlc
from time import sleep
import threading as thread
try:
    import pickle
    from picamera2.encoders import H264Encoder, Quality 
    from picamera2 import Picamera2
    from libcamera import controls 
finally:
    pass
HOST = '127.0.0.1'
PORT = 2929
BUFFERSIZE = 1024


def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    inst = vlc.Instance('--no-xlib --demux h264')   
    play = inst.media_player_new()
    media = inst.media_new_fd(s.fileno())
    media.get_mrl = lambda: 'udp://@' + addr[0] + ':2929'
    play.set_media(media)
    play.play()
    while 1:
        data, addr = s.recvfrom(BUFFERSIZE)
        play.next_frame()


def cameraserver():
    cam = Picamera2()
    encoder = H264Encoder()
    output = 'out.h264'
    #output = b""
    cam.start_recording(encoder=encoder, output=output, quality=Quality.LOW)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    data = 0
    size = 0
    file = open("out.h264", "rb")
    while 1:
        data = file.read(BUFFERSIZE)    
        s.sendto(data, ((HOST, PORT)))
        sleep(0.2)
    
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #    s.bind((HOST, PORT))
    data = 0
    file = open("video.h264", "rb")
    size = 0
    while 1:

        if not(data):
            file.seek(0)
        data = file.read(BUFFERSIZE)
        size = s.sendto(data, ((HOST, PORT)))



if __name__ == "__main__":
    t2 = thread.Thread(target=cameraserver)
    t1 = thread.Thread(target=client)
    t1.start()
    time.sleep(0.5)
    t2.start()
    t1.join()
    t2.join()


