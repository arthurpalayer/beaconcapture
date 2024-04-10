import socket
import time
import os
import vlc
from time import sleep
import threading as thread
from picamera2.outputs import FileOutput
import io
import cv2

try:
    import pickle
    from picamera2.encoders import H264Encoder, Quality 
    from picamera2 import Picamera2
    from libcamera import controls 
finally:
    pass
HOST = '127.0.0.1'
PORT = 2929
BUFFERSIZE = 100000

def clientnotvlc():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    while 1:
        x = s.recvfrom(BUFFERSIZE)
        data = x[0]
        data = pickle.loads(data)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("yomama", data)

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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cam.start(show_preview=True)
    img_counter = 0
    while True:
        im = cam.capture_array()
        ret, buffer = cv2.imencode(".jpg", im, [int(cv2.IMWRITE_JPEG_QUALITY),30])
        x = pickle.dumps(buffer)
        s.sendto(x, (HOST, PORT))


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
    t1 = thread.Thread(target=clientnotvlc)
    t1.start()
    time.sleep(0.5)
    t2.start()
    t1.join()
    t2.join()


