"""
Mission that shoots the laser and destruction the balloon
"""
import sys
import time

import Mission

sys.path.append('..')


class Destruction(Mission.Mission):
    def __init__(self, device_map):
        Mission.Mission.__init__(self)

        """
        time in order to don't shoot a much more time.
        laser - is clearly
        vision data to know if we finished
        """
        self.old_time = 0
        self.new_time = 0
        self.laser_pointer = device_map.pitch_motor
        self.vision_data = device_map.vision_data

    def initialize(self):
        self.old_time = time.time()
        self.new_time = time.time()
        '''
        send start to laser
        '''
        self.laser_pointer.send(0, True, True)

    def execute(self):
        """"""
        '''
        updata time.
        '''
        self.new_time = time.time()

    def is_finished(self):
        return self.new_time - self.old_time > 5 or self.isBalloonBlassed()


    def finish(self):
        self.laser_pointer.send(0, False, True)
#check me - that the dynamic change doesn't matter
    def isBalloonBlassed(self):
        a = self.vision_data.get_did_pop()
        if len(a) > 0:
            a = a[0]
        else:
            a = False
        return a
