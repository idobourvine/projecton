import copy
import threading
import time
import cv2
import GetBloon


def Webcamera(stream, bloons, canShoot, didPop):
    Image0 = None
    start_time = -1
    temp = []
    while not stream.stopped:
        if stream.more():
            Image1 = stream.read()
            if Image0 is None:
                Image0 = copy.deepcopy(Image1)
            try:
                cv2.imshow('image', Image1)
            except Exception as e:
                print(e)
            del temp[:]
            temp.append(GetBloon.getBloon(Image1))
            temp = temp[0]
            del bloons[:]
            bloons.append(temp[1])
            if len(bloons) > 0:
                bloons = bloons[0]
            del canShoot[:]
            canShoot.append(temp[0])
            # does so if bloon is popped it will say so for 3 seconds,
            # so we won't miss it
            del didPop[:]
            if start_time > 0 and time.time() - start_time <= 3:
                didPop.append(1)
            else:
                didPop.append(GetBloon.didPop(Image0, Image1))
                if len(didPop) > 0 and didPop[0] == 1:
                    start_time = time.time()
            cv2.waitKey(10)
            Image0 = copy.deepcopy(Image1)


    if stream.stopped:
        time.sleep(0.5)
        print "Stream died"