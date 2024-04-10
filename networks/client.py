import socket

# hostname = input("web name: ")

# HOSTIP = socket.gethostbyname(hostname)
HOST = "10.42.0.1"
# print(HOSTIP, type(HOSTIP))
PORT = 6969

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
     while 1:
        msg = input("input: ")
        s.sendto(msg.encode(), (HOST, PORT))
        data = s.recv(1024)

             




print(f"Received {data!r}")
