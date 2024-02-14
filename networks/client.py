import socket

# hostname = input("web name: ")

# HOSTIP = socket.gethostbyname(hostname)
HOST = "127.0.0.1"
# print(HOSTIP, type(HOSTIP))
PORT = 6001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     while 1:
        msg = input("input: ")
        s.sendall(msg.encode())
        data = s.recv(1024)

             




print(f"Received {data!r}")
