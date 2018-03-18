"""
Mission that drives a distance in a straight line
"""
import sys
import time

import Mission

sys.path.append('..')


class Drive(Mission.Mission):
    def __init__(self, car, length):
        Mission.Mission.__init__(self)
        self.CarDrive = car
        self.length = length

    def initialize(self):
        self.CarDrive.move_distance(self.length)

    def execute(self):
        """"""

    def is_finished(self):
        return self.CarDrive.finished_moving()

    def finish(self):

        """
        do nothing
        :return:
        """
