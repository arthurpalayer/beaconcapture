import socket

#define host
HOST = "10.42.0.1"
#define port
PORT = 6969
BUFFSIZE = 64

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
   
    msg = "recvd" 
    
    
    while 1:
        data = s.recvfrom(BUFFSIZE)
        if (len(data[0])):
            sendbuffer = "server received data"
            sendbuffer = str.encode(sendbuffer)
            print("received packet")
            print(data[0])
            addr = data[1]
            print(addr)
            s.sendto(sendbuffer, addr)
            #s.sendall(sendbuffer, addr[0])
         
