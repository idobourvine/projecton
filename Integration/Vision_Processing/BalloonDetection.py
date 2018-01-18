import copy
import threading
import time

import cv2.cv2 as cv2

import GetBalloon


def Webcamera(stream, bloons, canShoot, didPop):
    Image0 = None
    while not stream.stopped:
        if stream.more():
            Image1 = stream.read()
            if Image0 is None:
                Image0 = copy.deepcopy(Image1)
            try:
                cv2.imshow('image', Image1)
            except Exception as e:
                print(e)
            del didPop[:]
            didPop.append(GetBalloon.didPop(Image0, Image1))
            del bloons[:]
            bloons.append(GetBalloon.getBall(Image1))
            del canShoot[:]
            canShoot.append(GetBalloon.canShoot(Image1))
            cv2.waitKey(10)

            Image0 = copy.deepcopy(Image1)

    if stream.stopped:
        time.sleep(0.5)
        print "Stream died"


def Panasonic(bloons):
    Channel1 = cv2.VideoCapture(1)
    Channel1.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
    Channel1.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
    IsOpen1, Image1 = Channel1.read()
    while IsOpen1:
        IsOpen1, Image1 = Channel1.read()
        j = len(bloons)
        for i in range(j):
            del bloons[i]
        bloons.append(GetBalloon.getBall(Image1))
        cv2.waitKey(10)
    if not IsOpen1:
        time.sleep(0.5)
        print "Error opening Panasonic"

def Dancig(bloons):
    Channel2 = cv2.VideoCapture(2)
    Channel2.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
    Channel2.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
    IsOpen2, Image2 = Channel2.read()
    while IsOpen2:
        IsOpen2, Image2 = Channel2.read()
        j = len(bloons)
        for i in range(j):
            del bloons[i]
        bloons.append(GetBalloon.getBall(Image2))
        cv2.waitKey(10)
    if not IsOpen2:
        time.sleep(0.5)
        print "Error opening Dancig"

if __name__ == "__main__":
    try:
        bloons1 = []
        canShoot1 = [0]
        bloons2 = []
        bloons3 = []
        eg1 = threading.Thread(target=Webcamera, args=(bloons1,canShoot1,))
        eg2 = threading.Thread(target=Panasonic, args=(bloons2,))
        eg3 = threading.Thread(target=Dancig, args=(bloons3,))
        eg1.start()
        eg2.start()
        eg3.start()

    except:
        print "Error: unable to start thread"
    while 1:
        pass

