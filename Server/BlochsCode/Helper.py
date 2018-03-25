import numpy as np
import math
import Cam
import cv2
import itertools
from sympy.solvers import solve
from sympy import Symbol
import triangulation

BIG_INT = 999999
MIN_DIST = 10
# Right camera
CAM1 = Cam.Cam(0, np.array([-49.0, 108.5, 128.0]), np.array([668.5 ,206.5 ,
                                                             116.0]),
               np.array([668.5, 240.0, 69.5]), np.array([668.5 , 60.0, 54.5]), [272, 294], [475, 310],
               640.0,
               480.0, 30.0, 25.0, 1)
# Left camera
CAM2 = Cam.Cam(1, np.array([-57.0, 252.0, 135.0]), np.array([669.0, 117.0,
                                                              139.0]),
               np.array([668.5, 240.0, 69.5]), np.array([668.5, 60.0, 54.5]), [179, 310], [378, 335],
               640.0,
               480.0, 30.0, 25.0, 0)

CAM3 = Cam.Cam(2, np.array([664.0, 28.0, 128.0]), np.array([-57.0 , 222.0, 135.0]),
               np.array([-56.0, 60.0, 80.5]), np.array([-57.0, 240.0, 50.5]), [141.0, 295.0], [334.0, 331.0],
               640.0,
               480.0, 30.0, 25.0, 1)
# Left camera
CAM4 = Cam.Cam(3, np.array([664.0, 269.0, 120.0]), np.array([-57.0 ,170. ,
                                                             120.0]),
               np.array([-56.0, 60.0, 80.5]), np.array([-57.0, 240.0, 50.5]), [205.0, 274.0], [395.0, 321.0],
               640.0,
               480.0, 30.0, 25.0, 0)


CAMS = [CAM1, CAM2]

# ToDo - remeasure
ROOM_X = 640
ROOM_Y = 480
ROOM_Z = 220


def outOfRoom(balloon):
    """returns True if the approximated point is outside the room and False otherwise"""
    if balloon[0] > 1.1 * ROOM_X or balloon[0] < -0.1 * ROOM_X:
        return True
    elif balloon[1] > 1.1 * ROOM_Y or balloon[1] < -0.1 * ROOM_Y:
        return True
    elif balloon[2] > 1.1 * ROOM_Z or balloon[2] < -0.1 * ROOM_Z:
        return True
    return False


def locateCar(theta1, theta2):
    """gets the angle diffs between 2 tuples of corners, and returns the car's place on the floor"""
    cosAlpha = Symbol('c')
    sinAlpha = Symbol('s')
    sinAlpha = solve(cosAlpha ** 2 + sinAlpha ** 2 - 1, sinAlpha)
    sinAlpha = sinAlpha[1]
    up = ROOM_X * (sinAlpha * math.cos(theta1) + cosAlpha * math.sin(theta1))
    down = ROOM_Y * (cosAlpha * math.cos(theta2) + sinAlpha * math.sin(theta2))
    const = math.sin(theta1) / math.sin(theta2)
    cosAlpha = solve(up / down - const, cosAlpha)
    cosAlpha = cosAlpha[0]
    sinAlpha = math.sqrt(1 - cosAlpha ** 2)
    l = ROOM_X * (
    sinAlpha * math.cos(theta1) + cosAlpha * math.sin(theta1)) / math.sin(
        theta1)
    x = l * cosAlpha
    y = l * sinAlpha
    return np.array([x, y])


def getOtherIndex(i):
    if i == 0:
        return 1
    else:
        return 0


def filterLines(cam1, cam2):
    """given 2 cameras, gets the lines from them to the target, and then filters those line (so far, only by checking if
     a target from one camera should be visible from the other)"""
    cams = [cam1, cam2]
    lines = []
    if(len(cams[0].sizes) == 0 or len(cams[1].sizes) == 0):
        lines.append(cams[0].getLines())
        lines.append(cams[1].getLines())
        return lines
    for i in range(2):
        camLines = cams[i].getLines()
        camPoints = cams[i].getPoints()
        goodPoints = []
        for j in range(len(camPoints)):
            # checks if the cams point appears in the other camera
            if (triangulation.isPointInImage(cams[getOtherIndex(i)],
                                             camPoints[j])):
                goodPoints.append(j)
        # picks only the good lines - ones that the point is supposed to be
        # on the other cameras image
        goodLines = [camLines[k] for k in goodPoints]
        lines.append(goodLines)
    return lines


def dist(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (
    point1[2] - point2[2]) ** 2) ** 0.5


def connectTargets():
    cams = CAMS
    return connectTargets1(cams)


def connectTargets1(cams1):
    """picks the best-worst combination of lines between 2 cameras"""
    cams = cams1
    lines = filterLines(cams[0], cams[1])
    if len(lines[0]) == 0 or len(lines[1]) == 0:
        return []
    linesDists = []
    min1 = 0
    max1 = 1
    if len(lines[0]) > len(lines[1]):
        min1 = 1
        max1 = 0
    for line in lines[min1]:
        lineDists = []
        for line1 in lines[max1]:
            lineDists.append(line.distanceToLine(line1))
        linesDists.append(lineDists)
    listMin = range(len(lines[min1]))
    listMax = range(len(lines[max1]))
    combs = [zip(x, listMin) for x in
             itertools.permutations(listMax, len(listMin))]
    scores = []
    # make a list of all the bad pairs, eliminate each comb with a pair from
    #  the list
    forbidenTuples = []
    for comb in combs:
        flag = False  # if the comb is bad
        for tup in forbidenTuples:
            if tup in comb:
                scores.append(BIG_INT)
                flag = True
                break
        if flag:
            continue
        dists = []
        for tup in comb:
            # if 2 lines intersect outside the room, eliminate the combination
            if outOfRoom(lines[min1][tup[1]].intersect(lines[max1][tup[0]])):
                dists.append(BIG_INT)
                forbidenTuples.append(tup)
            else:
                dists.append(linesDists[tup[1]][tup[0]])
        scores.append(max(dists))
    best_worst_comb = combs[scores.index(min(scores))]
    if min1 == 0:
        best_worst_comb = [(x, y) for (y, x) in best_worst_comb]
    best_worst_comb = [(lines[0][x], lines[1][y]) for (x, y) in best_worst_comb]
    return best_worst_comb


def connectTargets1Test(lines1):
    """"picks the best-worst combination of lines between 2 cameras"""
    lines = lines1
    linesDists = []
    min1 = 0
    max1 = 1
    if len(lines[0]) > len(lines[1]):
        min1 = 1
        max1 = 0
    for line in lines[min1]:
        lineDists = []
        for line1 in lines[max1]:
            lineDists.append(line.distanceToLine(line1))
        linesDists.append(lineDists)
    listMin = range(len(lines[min1]))
    listMax = range(len(lines[max1]))
    combs = [zip(x, listMin) for x in
             itertools.permutations(listMax, len(listMin))]
    scores = []
    # make a list of all the bad pairs, eliminate each comb with a pair from
    #  the list
    forbidenTuples = []
    for comb in combs:
        flag = False  # if the comb is bad
        for tup in forbidenTuples:
            if tup in comb:
                scores.append(BIG_INT)
                flag = True
                break
        if flag:
            continue
        dists = []
        for tup in comb:
            # if 2 lines intersect outside the room, eliminate the combination
            if outOfRoom(lines[min1][tup[1]].intersect(lines[max1][tup[0]])):
                dists.append(BIG_INT)
                forbidenTuples.append(tup)
            else:
                dists.append(linesDists[tup[1]][tup[0]])
        scores.append(max(dists))
    best_worst_comb = combs[scores.index(min(scores))]
    if min1 == 0:
        best_worst_comb = [(x, y) for (y, x) in best_worst_comb]
    return best_worst_comb


"""
def getAngle(point1, point2):
    slope1_1 = (point1[1] - point2[1]) / (point1[0] - point2[0])
    theta1_1 = np.arctan(slope1_1)
    if slope1_1 < 0:
        theta1_1 += np.pi
    return theta1_1

def getSlope(point1, point2):
    slope1_1 = (point1[1] - point2[1]) / (point1[0] - point2[0])
    return slope1_1

def findPointOutOfRoom(point, dir):
    i = 0.1
    while True:
        if outOfRoom([point[0] + dir[0] * i, point[1] + dir[1] * i, point[2]]):
            return [point[0] + dir[0] * i, point[1] + dir[1] * i, point[2]]
        i += 0.1

def findCriticalAzis(cam1, cam2):
    slope1_left = getSlope(cam1.campoint[0:1], cam1.left[0:1])
    slope1_right = getSlope(cam1.campoint[0:1], cam1.right[0:1])

"""


def triangulate():
    """given tuples of lines, finds the 3D point in space represented by
    each line"""

    targets = []
    connections = connectTargets()
    for connection in connections:
        point = connection[0].intersect(connection[1])
        isIn = False
        for target in targets:
            if (target[0] - point[0]) ** 2 + (target[1] - point[1]) ** 2 + (
                        target[2] - point[2]) ** 2 < 25:
                isIn = True
        if not isIn:
            targets.append(point.tolist())
    return targets


def radToDeg(rad):
    deg = rad * 180
    deg = deg / math.pi
    return deg


def cartesianToSpheric(targetsCartesian, place, orientation):
    """gets the list of the targets in Cartesian coordinates, as well ae the car's place and it's orientation (current theta, phi).
    returns the list of the targets in Spheric coordinates."""

    targetsSpheric = []
    [theta0, phi0] = orientation
    for target in targetsCartesian:
        print target
        direction = target - place
        x, y, z = direction[0], direction[1], direction[2]
        theta = math.atan2(y,x)
        theta = theta - theta0
        theta = radToDeg(theta)
        phi = math.atan2(z, math.sqrt(x**2+y**2))
        phi = phi - phi0
        phi = radToDeg(phi)
        targetsSpheric.append([theta, phi])
    return targetsSpheric
