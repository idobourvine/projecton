`       """
Mission that shoots the laser
"""
import sys
import time

import Mission

sys.path.append('..')


class Drive(Mission.Mission,):
    def __init__(self, car,length):
        Mission.Mission.__init__(self)
        self.CarDrive = car
        self.length=length

    def initialize(self):
        self.CarDrive.move(self.length)

    def execute(self):
        """"""


    def is_finished(self):
        return self.CarDrive.isNotMove()

    def finish(self):

        """
        do nothing
        :return:
        """
