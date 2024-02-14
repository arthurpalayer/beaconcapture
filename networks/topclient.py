import socket
import numpy
import pickle
import threading as thread
import cv2 as cv

def control(s):
    s.connect((HOST, PORT))
    while 1:
        msg = input("input: ")
        s.sendall(msg.encode())
        data = s.recv(1024)


    print(f"received {data!r}")
    
def video(s):
    cap = cv.VideoCapture(0)
    
    while 1:
        ret, photo = cap.read()
        cv.imshow('clientside', photo)
        ret, buffer = cv.imencode(".jpg", photo, [int(cv.IMWRITE_JPEG_QUALITY), 30])
        x_as_bytes = pickle.dumps(buffer)
        s.sendto(x_as_bytes,(serverip, serverport))
        if cv.waitKey(10) == 13:
            break
        
    cv.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 6000

    sUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    t1 = thread.Thread(target=control, args =(sTCP,))
    t2 = thread.Thread(target=video, args=(sUDP,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("exit")
