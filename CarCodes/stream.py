import thread
import time
import cv2
#import GetBalloonOld
#from Helper import *
#import Client
# import picamera
# from picamera.array import PiRGBArray

i = 1

name1, name2 = str(2*i)+".jpg", str(2*i-1)+".jpg"

def Camera1():
    Channel0 = cv2.VideoCapture(0)
    IsOpen0, Image0 = Channel0.read()
    for i in range(100):
        IsOpen0, Image0 = Channel0.read()
        Image0[240, 320] = [0, 255, 0]
        Image0[239, 319] = [0, 255, 0]
        Image0[241, 321] = [0, 255, 0]
        Image0[240, 319] = [0, 255, 0]
        Image0[239, 321] = [0, 255, 0]
        Image0[241, 320] = [0, 255, 0]
        Image0[240, 321] = [0, 255, 0]
        Image0[239, 320] = [0, 255, 0]
        Image0[241, 319] = [0, 255, 0]
        #Image0 = GetBalloonOld.draw(Image0)
        #cv2.imwrite("car.jpg" ,Image0)
        cv2.imshow("1.jpg",Image0)
        cv2.waitKey(10)
    if not IsOpen0:
        time.sleep(0.5)
        print "Error opening Camera1"
    return None

while True:
    Camera1()

def Camera2():
    Channel1 = cv2.VideoCapture(1)
    IsOpen1, Image1 = Channel1.read()
    for i in range(50):
        IsOpen1, Image1 = Channel1.read()
        Image1[240, 320] = [0, 255, 0]
        Image1[239, 319] = [0, 255, 0]
        Image1[241, 321] = [0, 255, 0]
        Image1[240, 319] = [0, 255, 0]
        Image1[239, 321] = [0, 255, 0]
        Image1[241, 320] = [0, 255, 0]
        Image1[240, 321] = [0, 255, 0]
        Image1[239, 320] = [0, 255, 0]
        Image1[241, 319] = [0, 255, 0]
        Image1 = GetBalloonOld.draw(Image1)
        cv2.imwrite(name2 ,Image1)
        cv2.imshow("2.jpg",Image1)
        cv2.waitKey(10)
    if not IsOpen1:
        time.sleep(0.5)
        print "Error opening Camera2"
    return None

def Camera3():
    Channel2 = cv2.VideoCapture(2)
    IsOpen2, Image2 = Channel2.read()
    while IsOpen2:
        IsOpen2, Image2 = Channel2.read()
        cv2.imshow("3.jpg",Image2)
        cv2.waitKey(10)
    if not IsOpen2:
        time.sleep(0.5)
        print "Error opening Camera3"

# def piCam():
#     Channel0 = picamera.PiCamera()
#     Channel0.awb_mode = 'sunlight'
#     raw = PiRGBArray(Channel0, size=(640, 480))
#     Channel0.capture(raw, 'rgb', resize=(640, 480))
#     while True:
#         raw.truncate(0)
#         Channel0.capture(raw, 'rgb', resize=(640, 480))
#         Image0 = raw.array
#         try:
#             cv2.imwrite('pi.jpg', Image0)
#         except Exception as e:
#             print(e)

'''
try:
   thread.start_new_thread(Camera1,())
   thread.start_new_thread(Camera2,())
   # thread.start_new_thread(Camera3,())
   # thread.start_new_thread(piCam,())
except:
   print "Error: unable to start thread"

while 1:
   pass
'''