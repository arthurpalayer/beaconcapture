import socket
import threading as thread

PORT = 6969
HOST = '127.0.0.1'
BUFFSIZE = 64

def sendconn(s):
    msg = "conn"
    msg = msg.encode('utf-8')
    s.sendto(msg, (HOST, PORT))

def recvconn(s):
    data, addr = s.recvfrom(BUFFSIZE)
    return addr

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    addr = recvconn(s)
    msg = "received yo shit cuh"
    while 1:
            
        s.sendto(msg.encode('utf-8'), addr)
        

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sendconn(s)
    while 1:
        data, addr = s.recvfrom(BUFFSIZE)
        print(data)

if __name__ == "__main__":
    t1 = thread.Thread(target=server)
    t2 = thread.Thread(target=client)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
