"""
Mission that scans the room and gets an array of balloons
"""
import sys
import threading
import time
import ClearRoom
from Devices.DeviceMap import DeviceMap
from Mission import Mission
from Vision_Processing.BalloonDetection import Webcamera

sys.path.append('..')

class ScanRoom(Mission):
    def __init__(self):
        Mission.__init__(self)

        self.bloons = []
        self.bloonsToAdd = []
        self.canShoot = [0]
        self.didPop = [0]
        self.eg1 = threading.Thread(target=Webcamera,
                                    args=(self.bloonsToAdd, self.canShoot,
                                          self.didPop,))
        self.starting_azimuth = 0
        self.starting_pitch = 0
        self.azimuth = 0
        self.pitch = 0
        self.azimuth_motor = DeviceMap.azimuth_motor
        self.pitch_motor = DeviceMap.pitch_motor
        self.angle_to_move = 15.0

    def initialize(self):
        self.starting_azimuth = self.azimuth_motor.getAngle()
        self.starting_pitch = self.pitch_motor.getAngle()

    def execute(self):
        self.azimuth = self.azimuth_motor.getAngle()
        self.pitch = self.pitch_motor.getAngle()
        if self.bloonsToAdd:
            inner = self.bloonsToAdd[0]
            if inner:
                for bloon in inner:
                    self.bloons.append([bloon[0] + self.azimuth, bloon[1] +
                                        self.pitch])
        self.azimuth_motor.send(self.angle_to_move)
        time.sleep(1)

    def is_finished(self):
        diff = self.starting_azimuth - self.azimuth
        return diff >= 360.0 or diff <= -360.0

    def finish(self):
        clear = ClearRoom.ClearRoom(self.bloons)
        clear.start()