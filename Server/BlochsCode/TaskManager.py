import numpy as np
import cv2
import copy
# import GetBalloonOld
import Line
import Cam
import Vision_Processing.GetBalloon
import math
from sympy.solvers import solve
from sympy import Symbol
from Helper import *
import time

CAR_Z = 40.0


def startCams():
    for cam in CAMS:
        cam.stream.start()
    time.sleep(6)


def stopCams():
    for cam in CAMS:
        cam.stream.stop()


def getTargetsPlaces(points):
    cams = CAMS
    for i in range(2):
        cams[i].targets = []
        for point in points[i]:
            cams[i].addTarget(point)
    targets = triangulate()
    return targets


def getCarLocation():
    """returns 2D location of the car (looking from the ceiling)"""
    cams = CAMS
    img1, img2 = cams[0].getImage(), cams[1].getImage()
    potint1op, point2op = GetBalloonOld.getCar(img1), GetBalloonOld.getCar(
        img2)
    for j in range(len(point1op)):
        point1op[j] = np.array(np.array([point1op[j][0], point1op[j][1]]))
    for j in range(len(point2op)):
        point2op[j] = np.array(np.array([point2op[j][0], point2op[j][1]]))
    if len(point1op) == 0 or len(point2op) == 0:
        return None
    points = [[point1op[0]], [point2op[0]]]
    car = getTargetsPlaces(copy.deepcopy(points))[0]
    diff = abs(car[2] - CAR_Z)
    for op1 in point1op:
        for op2 in point2op:
            testPoint = [[op1], [op2]]
            testCar = getTargetsPlaces(copy.deepcopy(testPoint))[0]
            testDiff = abs(testCar[2] - CAR_Z)
            if testDiff < diff:
                diff = testDiff
                car = testCar
    return car


def getTargets():
    """return 3D points in space of the targets"""
    cams = CAMS
    for cam in cams:
        cam.resetTargets()
        cam.resetSizes()
        image = cam.getImage()
        # print("Time before getting enemies: " + str(time.time()))
        bloons, sizes = Vision_Processing.GetBalloon.getEnemies(image)
        # print("Time after getting enemies: " + str(time.time()))



        points = []
        for bloon in bloons:
            points.append(np.array([bloon[0], bloon[1]]))
        for i in range(len(bloons)):
            cam.addTarget(points[i])
            cam.addSize(sizes[i])

    targets = triangulate()
    # print("Time after triangulation: " + str(time.time()))
    # print "getTargets"
    # print targets
    # targets = cartesianToSpheric(targets, place, orientation)
    return targets


def getInnocents():
    """return 3D points in space of the friendly balloons"""

    cams = CAMS
    for cam in cams:
        image = cam.getImage()
        bloons, sizes = Vision_Processing.GetBalloon.getFriends(image)
        points = []
        for bloon in bloons:
            points.append(np.array([bloon[0], bloon[1]]))
        for i in range(len(bloons)):
            cam.addTarget(points[i])
            cam.addSize(sizes[i])
    targets = triangulate()
    # targets = cartesianToSpheric(targets, place, orientation)
    return targets


def getImage(cam):
    """takes an image from one of the cameras"""

    return cam.getImage()


def didPop(img1, img2):
    """return true if balloon popped, false otherwise"""

    return Vision_Processing.GetBalloon.didPop(img1, img2, True)


def getAngles():
    img = cv2.imread("pi.jpg")
    return Vision_Processing.GetBalloon.getAngles(img, True)


def getAnglesFriend():
    img = cv2.imread("pi.jpg")
    return Vision_Processing.GetBalloon.getAnglesFriend(img, True)
