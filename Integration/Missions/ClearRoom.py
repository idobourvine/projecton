"""
Mission that destroys all balloons from an array
"""
import sys
import time

from Devices.DeviceMap import DeviceMap

import AimAtBalloonInPictureMission
from Mission import Mission

sys.path.append('..')

class ClearRoom(Mission):
    def __init__(self, balloons):
        Mission.__init__(self)
        self.azimuth_motor = DeviceMap.azimuth_motor
        self.pitch_motor = DeviceMap.pitch_motor
        self.bloons = balloons
        self.index = 0
        self.aim = None
        self.aim_done = False

    def initialize(self):
        self.azimuth_motor.send(self.bloons[self.index][0], False, False)
        self.pitch_motor.send(self.bloons[self.index][1], False, False)
        time.sleep(3)
        self.aim = AimAtBalloonInPictureMission.AimAtBalloonInPictureMission()
        self.aim.start()

    def execute(self):
        if self.aim.is_finished():
            self.aim_done = True
        if self.aim_done and self.aim.shoot.is_finished():
            if self.index < len(self.bloons) - 1:
                self.azimuth_motor.send(self.bloons[self.index + 1][0], False,
                                        False)
                self.pitch_motor.send(self.bloons[self.index + 1][1], False,
                                      False)
                time.sleep(3)
                self.aim =  \
                    AimAtBalloonInPictureMission.AimAtBalloonInPictureMission()
                self.aim_done = False
                self.aim.start()
                self.index += 1
            else:
                self.index += 1

    def is_finished(self):
        return self.index >= len(self.bloons)

    def finish(self):
        self.azimuth_motor.send(0, False, False)
        self.pitch_motor.send(0, False, False)
