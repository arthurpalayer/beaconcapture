#client code -> controller
import cv2 as cv
import socket
import numpy
import pickle
import threading as thread

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
serverip = "127.0.0.1"
serverport = 6969

cap = cv.VideoCapture(0)

while True:
    ret, photo = cap.read()
    cv.imshow('clientside', photo)
    ret, buffer = cv.imencode(".jpg", photo, [int(cv.IMWRITE_JPEG_QUALITY),30])
    x_as_bytes = pickle.dumps(buffer)
    s.sendto(x_as_bytes,(serverip , serverport))
    if cv.waitKey(10) == 13:
        break

cv.destroyAllWindwos()
cap.release()
