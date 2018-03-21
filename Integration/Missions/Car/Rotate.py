"""
Mission that drives a distance in a straight line
"""
import sys
import time

import Integration.Missions.Mission

sys.path.append('..')


class Rotate(Integration.Missions.Mission.Mission):
    def __init__(self, device_map, angle):
        Integration.Missions.Mission.Mission.__init__(self)
        self.car_drive = device_map.car_drive
        self.angle = angle

    def initialize(self):
        self.car_drive.rotate(self.angle)

    def execute(self):
        pass

    def is_finished(self):
        return self.car_drive.finished_moving()

    def finish(self):

        """
        do nothing
        :return:
        """


