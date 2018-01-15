"""
Mission that shoots the laser
"""
import sys
import threading
import time

from Devices.DeviceMap import DeviceMap
from Mission import Mission
from Vision_Processing.BalloonDetection import Webcamera

sys.path.append('..')

class DestroyBalloon(Mission):
    def __init__(self):
        Mission.__init__(self)

        self.laser_pointer = DeviceMap.pitch_motor
        self.old_time = 0
        self.new_time = 0
        self.bloons1 = []  # Array of balloons detected by vision processing
        self.canShoot = [0]
        self.didPop = [0]
        self.eg1 = threading.Thread(target=Webcamera,
                                    args=(self.bloons1, self.canShoot,
                                          self.didPop,))  # Thread that runs
    def initialize(self):
        self.eg1.start()
        self.old_time = time.time()
        self.new_time = time.time()
        time.sleep(3)
        self.laser_pointer.send(0, True, True)
        time.sleep(3)

    def execute(self):
        """"""
        self.new_time = time.time()

    def is_finished(self):
        a = self.didPop[:]
        if len(a) > 0:
            a = a[0]
        else:
            a = False
        return self.new_time - self.old_time > 5 or a

    def finish(self):
        self.laser_pointer.send(0, False, True)
