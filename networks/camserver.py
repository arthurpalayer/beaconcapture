#server code


import cv2 as cv
import socket
import numpy
import pickle   

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "127.0.0.1"
port = 6969
s.bind((ip, port))

while True:
    x = s.recvfrom(1000000000)
    clientip = x[1][0]
    data = x[0]
    data = pickle.loads(data)
    data = cv.imdecode(data, cv.IMREAD_COLOR)
    cv.imshow('serverside', data)
    if cv.waitKey(10) == 13:
        break
cv.destroyAllWindows()


