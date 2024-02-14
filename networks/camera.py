import time
import numpy
import pickle
from picamera2 import Picamera2, Preview

cam = Picamera2()
cam.start(show_preview=True)
time.sleep(1000)
