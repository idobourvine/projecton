import cv2
import numpy as np
import Line
from sympy.solvers import solve
from sympy import Symbol
import math
FACTOR_OF_ERROR = 1.1

def findPartialCenter(first, second, part, dist):
    """finds the weighted average of 2 vectors"""

    r = part*second+(dist-part)*first
    r = 1.0/dist*r
    return r


def findProjectionPoint(cam, point):
    """given a 2D point in the image, finds it's 3D point in space on the
    camera's plane"""

    xVector = findPartialCenter(cam.aVector, cam.bVector, point[0], cam.width)
    yVector = findPartialCenter(cam.aVector, cam.cVector, point[1], cam.height)
    r = xVector + yVector - cam.aVector
    return r

# def findProjectionLine(cam, target):
#     w = cam.center-cam.campoint
#     u = cam.cutWithPlate(cam.right)-cam.cutWithPlate(cam.left)
#     v = np.cross(u, w)
#     sizeV = (v[0]**2 + v[1]**2 + v[2]**2)**0.5
#     v /= sizeV
#     sizeU = (u[0]**2 + u[1]**2 + u[2]**2)**0.5
#     v = v*(cam.height/cam.width)*sizeU
#     direction = target - np.array([320, 240])
#     realVec = w + (float(direction[0])/cam.width)*u + (float(direction[
#                                                               1])/cam.height)*v
#     return Line.Line(cam.campoint, realVec)

def findProjectionLine(cam, target):
    """returns a line from a camera to a target"""
    target[0] -= cam.width/2
    target[1] -= cam.height/2
    p1 = cam.cutWithPlate(cam.left)
    p2 = cam.cutWithPlate(cam.right)
    delta1 = p1 - cam.center
    delta2 = p2 - cam.center
    [[x1, y1], [x2, y2]] = cam.getTwoKnownPoints()
    a = np.array([[x1, x2], [y1, y2]])
    b = np.array([target[0], target[1]])
    x = np.linalg.solve(a, b)
    pTar = cam.center + x[0]*delta1+x[1]*delta2
    # pTar = [cam.center[0] + x[0]*delta1[0] + x[1]*delta2[0], cam.center[1] +
    #         x[0]*delta1[1] + x[1]*delta2[1], cam.center[2] + x[0]*delta1[2]
    #         + x[1]*delta2[2]]
    dir1 = pTar - cam.campoint
    start = cam.campoint
    return Line.Line(start, dir1)

# ToDO find these constants - Experiments
x0 = 1
S0 = 1

def isPointInImage(cam, point):
    """checks if a point should be visible
    from a camera"""
    # pointOnPlane = cam.cutWithPlate(point)
    # vecOnPlane = pointOnPlane - cam.center
    # p1 = cam.cutWithPlate(cam.left)
    # p2 = cam.cutWithPlate(cam.right)
    # delta1 = p1 - cam.center
    # delta2 = p2 - cam.center
    # [[x1, y1], [x2, y2]] = cam.getTwoKnownPoints()
    # a = np.array([[delta1[0], delta2[0]], [delta1[1], delta2[1]], [delta1[2],
    #                                                               delta2[2]]])
    # b = np.array([vecOnPlane[0], vecOnPlane[1], vecOnPlane[2]])
    # x = np.linalg.solve(a, b)
    # xTot = x[0] * x1 + x[1] * x2
    # yTot = x[0] * y1 + x[1] * y2
    # if abs(xTot * 2) > cam.width * FACTOR_OF_ERROR or abs(yTot * 2) > \
    #                 cam.height * FACTOR_OF_ERROR:
    #     return False
    # else:
    #     return True
    return True

def findPoint(cam, target, size):
    """gives an approximation on the location of a target from one camera,
    using its size"""
    line1 = findProjectionLine(cam, target)
    dist = findDist(x0, S0, size)
    start = line1.start
    dir1 = line1.dir
    point = start + dist*dir1
    return point


def findDist(x0, S0, S):
    """gives the estimated distance of object with size S from the camera,
    with a starting object with S0 size from distance x0, relying on the
    fact that the size goes like 1/x^2"""
    return x0*math.pow(S0/S, 0.5)

def triangulate(cam1, cam2, point1, point2):
    """given 2 cameras and 2 points in each of their images, find the 3D
    point of the balloon in space"""

    l1 = findProjectionPoint(cam1, point1)
    l2 = findProjectionPoint(cam2, point2)
    r = l1.intersect(l2)
    return r
