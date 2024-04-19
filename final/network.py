import socket
import numpy as np
import cv2
import select
import pickle
from time import sleep
from convert import packetconvert
from picamera2 import Picamera2
import header


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
        req, addr = self.s.recvfrom(header.CONTROLBUFFSIZE) #wait to recvfrom 
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
    def __init__ (self, name = "client", ip = header.HOST, port = 6969):
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
        packet = packet.to_bytes(header.CONTROLBUFFSIZE)
        self.s.sendto(packet, (self.ip, self.port))
        return self.waitfordata(0.0005)

                     


class videoclient(client):
    def __init__(self, name="video", ip='10.42.0.1', port=header.VIDEOPORT):
        super().__init__(name, ip, port) 

    def playvideo(self):
        data, addr = self.s.recvfrom(header.VIDEOBUFFSIZE)
        data = np.frombuffer(data, np.uint8)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("LIVEFEED", data)
        cv2.waitKey(1)


class videoserver(server):
    def __init__(self, name="video", ip='10.42.0.1', port=header.VIDEOPORT):
        super().__init__(name, ip, port)
        self.cam = Picamera2()
        self.cam.start()

    def sendvideo(self, addr):
        while 1:
            im = self.cam.capture_array()
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            ret, buffer = cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 30])
            x = buffer.tobytes()
            self.s.sendto(x, addr)

class beaconserver(server):
    def __init__(self, name="beacon", ip="10.42.0.1", port=header.BEACONPORT):
        super().__init__(name, ip, port)

    def getdata(self):
        data, addr = self.s.recvfrom(header.BEACONBUFFSIZE)
        packet = bytearray(data).decode('utf-8', errors='strict')
        conversion = 160563.2
        x = twos_complement(packet[4:8], 16) / conversion
        y = twos_complement(packet[8:12], 16) / conversion
        z = twos_complement(packet[12:16], 16) / conversion
        return [x,y,z]
        

    def twos_complement(hexstr, bits):
        value = int(hexstr, 16)
        if value & (1 << (bits - 1)):
            value -= 1 << bits
        return value

    def is_hex(d):
        for c in d:
            if c not in set('0123456789abcdefABCDEF'):
                return False
    




