import socket

#define host
HOST = "127.0.0.1"
#define port
PORT = 6001


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    msg = "recvd" 
    
    conn, addr = s.accept()
    while 1:
        data = conn.recv(512)
        if (len(data)):
            sendbuffer = "server received data"
            conn.send(sendbuffer.encode())
            print(data)
        if conn.timeout 
