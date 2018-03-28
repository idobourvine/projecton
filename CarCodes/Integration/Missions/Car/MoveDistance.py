"""
Mission that drives a distance in a straight line
"""
import sys
import time

import Missions.Mission

sys.path.append('..')


class MoveDistance(Missions.Mission.Mission):
    def __init__(self, device_map, length):
        Missions.Mission.Mission.__init__(self)
        self.car_drive = device_map.car_drive
        self.length = length

    def initialize(self):
        self.car_drive.move_distance(self.length)

    def execute(self):
        """"""
        pass

    def is_finished(self):
        return self.car_drive.finished_moving()

    def finish(self):
        """
        do nothing
        :return:
        """
        pass

