import socket
import time
import os
import vlc
import threading as thread
HOST = '127.0.0.1'
PORT = 2929
BUFFERSIZE = 1024


def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    inst = vlc.Instance('--no-xlib --demux h264')   
    play = inst.media_player_new()
    while 1:
        data, addr = s.recvfrom(BUFFERSIZE)
        media = inst.media_new_fd(s.fileno())
        media.get_mrl = lambda: 'udp://@' + addr[0] + ':2929'
        play.set_media(media)
        play.play()


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #    s.bind((HOST, PORT))
    data = 0
    file = open("video.h264", "rb")
    size = 0
    while 1:

        if (size < BUFFERSIZE):
            file.seek(0)
        data = file.read(BUFFERSIZE)
        
        size = s.sendto(data, ((HOST, PORT)))
        print(size)

if __name__ == "__main__":
    client()


