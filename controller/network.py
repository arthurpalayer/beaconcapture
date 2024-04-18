import socket
import numpy as np
import cv2
import select
import pickle
from time import sleep
from drone import packetconvert

CONTROLLERBUFFSIZE = 16
VIDEOBUFFSIZE = 32768
BEACONBUFFSIZE = 64
BUFFSIZE = 64
PORT = 6969
HOST = '127.0.0.1'
VIDEOPORT = 6967


class server():
    
    def __init__(self, name = "server", ip = '127.0.0.1', port = 6969):
        self.name = name
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        flag = 1
        while flag != 0:
            try:
                self.s.bind((self.ip, self.port))
                flag = 0
                print(self.name, " BIND SUCCESS")
            except:
                time.sleep(2)
                print(self.name, " BIND FAIL")
                flag = 1

    def waitfordata(self,timeout):
        #run select to wait for data
        ready = select.select([self.s], [], [], timeout)
        if ready[0]:
            data, addr = self.s.recvfrom(16)
            data = data.decode()
        else:
            data = "Not Ready"

        print(self.name, data)
        return data

    def makeconn(self):
        #establish connection by receiving conn REQ and reply with ACK
        req, addr = self.s.recvfrom(BUFFSIZE) #wait to recvfrom 
        msg = "ACK".encode()
        self.s.sendto(msg, addr) #send ACK #send 1
        print(self.name, " CONN CHECK")
        return req, addr 

    def controlrecv(self,buffersize=4096, msg = "CONTROL ACK"):
        data, addr = self.s.recvfrom(buffersize)
        data = int.from_bytes(data)
        self.s.sendto(msg.encode(), addr)
        data, status = packetconvert(data)
        return data, addr





class client():
    def __init__ (self, name = "client", ip = HOST, port = 6969):
        self.name = name
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def waitfordata(self, timeout):
        ready = select.select([self.s], [], [], timeout)
        if ready[0]:
            data, addr = self.s.recvfrom(16)
            data = data.decode()
        else:
            data = "server not ready"
            
        print(self.name,": ", data)
        return data

    def makeconn(self):
        #the client needs to send and wait for an ACK
        noACK = 1
        while noACK != 0:
            print("sending connection req")
            self.s.sendto("CONN".encode(), (self.ip, self.port))
            ret = self.waitfordata(0.05)
            if (ret == "ACK"):
                noACK = 0
            else:
                noACK = 1
        return ret
    
    def sendcontrol(self, packet):
        packet = packet.to_bytes(CONTROLLERBUFFSIZE)
        self.s.sendto(packet, (self.ip, self.port))

                     


class videoclient(client):
    def __init__(self, name="video", ip='10.42.0.1', port=VIDEOPORT):
        super().__init__(name, ip, port) 

    def playvideo():
        data, addr = s.recvfrom(VIDEOBUFFSIZE)
        data = np.frombuffer(data, np.uint8)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("LIVEFEED", data)
        cv2.waitKey(1)


class videoserver(server):
    def __init__(self, name="video", ip='10.42.0.1', port=VIDEOPORT):
        super().__init__(name, ip, port)
        cam = Picamera2()
        cam.start()

    def sendvideo(self, addr):
        while 1:
            im = cam.capture_array()
            ret, buffer = cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 30])
            x = buffer.tobytes()
            self.s.sendto(x, addr)



