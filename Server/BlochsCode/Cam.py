import cv2
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
import triangulation
import WebcamStream


class Cam:
    """A class representing a camera"""

    def __init__(self, Id, campoint, center, left, right, leftPixel, rightPixel, width, height, horAngle, verAngle, i):
        self.Id = Id
        # center of the image in space
        self.center = center
        # two random points seen in the image plane
        self.left = left
        self.right = right
        # the two points locations on the image
        self.leftPixel = [leftPixel[0]-width/2, leftPixel[1]-height/2]
        self.rightPixel = [rightPixel[0] - width/2, rightPixel[1] - height/2]
        # cams location
        self.campoint = campoint
        # size (in pixels) of the image given by the camera
        self.width = width
        self.height = height
        # list of 2D point in the image in which there are balloons (centers
        #   of the balloons)
        self.targets = []
        # list of sizes of each target, by index
        self.sizes = []
        self.horAngle = horAngle
        self.verAngle = verAngle
        # vector pointing from the camera, perpadicular to the image's plane
        self.ver = self.center - self.campoint
        self.stream = WebcamStream.WebcamStream(i)

    def getImage(self):
        """returns the last image saved from this camera"""
        return self.stream.read()

    def getTwoKnownPoints(self):
        """return the (x,y) location on the image of 2 known points, left,
        right (pixel indentation from center"""
        return [self.leftPixel, self.rightPixel]

    def getLines(self):
        """returns list of lines from the camera to the targets"""
        lines = []
        for target in self.targets:
            lines.append(triangulation.findProjectionLine(self, target))
        return lines

    def getPoints(self):
        """return a list of approximated points in space of the targets"""
        points = []
        for i in range(len(self.targets)):
            points.append(triangulation.findPoint(self, self.targets[i],
                                                  self.sizes[i]))
        return points

    def addTarget(self, point):
        """adding a target to the targets list"""
        self.targets.append(point)

    def addSize(self, point):
        """adding a size of target to the sizes list"""
        self.sizes.append(point)

    def closestTarget(self, line):
        """a function that finds the closest target to a 2D line in the
        image plane. returns both the target and it's distance from the line"""
        if len(self.targets) == 0:
            return None
        closest = self.targets[0]
        minDist = line.distanceToPoint(closest)
        for target in self.targets:
            if line.distanceToPoint(target) < minDist:
                closest = target
                minDist = line.distanceToPoint(target)
        return closest, minDist

    def closestTarget(self, line, forbidden):
        """finds the closest target to a 2D line in the image from the
        targets  that do not appear in forbidden"""
        confirmed = []
        for target in self.targets:
            if target not in forbidden:
                confirmed.append(target)
        if len(confirmed) == 0:
            return None
        closest = confirmed[0]
        minDist = line.distanceToPoint(closest)
        for target in confirmed:
            if line.distanceToPoint(target) < minDist:
                closest = target
                minDist = line.distanceToPoint(target)
        return closest, minDist

    def getPlane(self):
        """returns the free parameter (d) in the image's plane's equation"""
        a, b, c, = self.ver[0], self.ver[1], self.ver[2]
        x, y, z = self.center[0], self.center[1], self.center[2]
        d = Symbol('d')
        d = solve(a*x+b*y+c*z+d, d) #important!! z=/=x!!!
        d = d[0]
        return d

    def cutWithPlate(self, vector):
        """finds the cut point between a line connecting the given point
        with  the camera's place, to the image's plane"""
        a, b, c, = self.ver[0], self.ver[1], self.ver[2]
        d = self.getPlane()
        dir = vector - self.campoint
        x, y, z = self.campoint[0], self.campoint[1], self.campoint[2]
        u, v, w = dir[0], dir[1], dir[2]
        t = Symbol('t')
        t = solve(a*(x+t*u)+b*(y+t*v)+c*(z+t*w)+d, t)
        t = t[0]
        return np.array([x+t*u, y+t*v, z+t*w])
