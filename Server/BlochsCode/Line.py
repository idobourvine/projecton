import numpy as np
import math
from Helper import *
from sympy.solvers import solve
from sympy import Symbol

# ToDo - remeasure
ROOM_X = 640
ROOM_Y = 480
ROOM_Z = 220

class Line:
    """"A line class representing the connection between a camera and a
    balloon"""

    def outOfRoom(self, balloon):
        """returns True if the approximated point is outside the room and False otherwise"""
        if balloon[0] > 1.1 * ROOM_X or balloon[0] < -0.1 * ROOM_X:
            return True
        elif balloon[1] > 1.1 * ROOM_Y or balloon[1] < -0.1 * ROOM_Y:
            return True
        elif balloon[2] > 1.1 * ROOM_Z or balloon[2] < -0.1 * ROOM_Z:
            return True
        return False

    def __init__(self, start, dir):
        self.start = start
        self.dir = dir
        self.connected = False

    def distanceToLine(self, line):
        """the function gets a line in space and returns the distance
        between  the lines"""

        a = self.findClosest(line)
        b = line.findClosest(self)
        balloon = np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2])
        if self.outOfRoom(balloon):
            return 1000
        else:
            parallel = np.cross(self.dir, line.dir)
            a, b, c = parallel[0], parallel[1], parallel[2]
            d = -a * line.start[0] - b * line.start[1] - c * line.start[2]
            x, y, z = self.start[0], self.start[1], self.start[2]
            dist = abs(a * x + b * y + c * z + d) / math.sqrt(a * a + b * b
                                                              + c * c)
            return dist

    def __eq__(self, other):
        a = self.start[0] == other.start[0]
        b = self.start[1] == other.start[1]
        c = self.start[2] == other.start[2]
        d = self.dir[0] == other.dir[0]
        e = self.dir[1] == other.dir[1]
        f = self.dir[2] == other.dir[2]
        return a and b and c and d and e and f

    def getClosestLine(self, lines, forbidden):
        """given a list of line, finds the one whose closest to our line"""
        new = []
        for line in lines:
            new.append(line)
        lines = new
        for line in forbidden:
            for l in lines:
                if line.__eq__(l):
                    lines.remove(line)
        if len(lines) == 0:
            return None
        line = lines[0]
        dist = self.distanceToLine(line)
        for l in lines:
            if self.distanceToLine(l) < dist:
                line = l
                dist = self.distanceToLine(l)
        return line

    def distanceToPoint(self, point):
        """the function gets a point in space and returns the distance
        between  the line to the point"""

        t = Symbol('t')
        vec = self.start + t * self.dir
        t = solve(vec.dot(point - vec), t)
        t = t[0]
        vec = self.start + t * self.dir
        return np.linalg.norm(point - vec)

    def intersect(self, l):
        """the function gets a line and returns the point in space who'se
        the  sum of it's distances from both of the lines is minimal"""

        a = self.findClosest(l)
        b = l.findClosest(self)
        c = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
        r = np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2])
        return r

    def findClosest(self, l):
        """the function gets a line and finds the point in our line that is
         closest to the given line"""

        parallel = np.cross(self.dir, l.dir)
        ver = np.cross(l.dir, parallel)
        a, b, c = ver[0], ver[1], ver[2]
        d = -a * l.start[0] - b * l.start[1] - c * l.start[2]
        t = Symbol('t')
        x, y, z = self.start[0], self.start[1], self.start[2]
        u, v, w = self.dir[0], self.dir[1], self.dir[2]
        t = solve(a * (x + t * u) + b * (y + t * v) + c * (z + t * w) + d, t)
        t = t[0]
        return np.array([x + t * u, y + t * v, z + t * w])