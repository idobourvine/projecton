"""
Mission that shoots the laser
"""
import sys
import time

import Missions.Mission

sys.path.append('..')


class DestroyBloon(Missions.Mission.Mission):
    def __init__(self, device_map, countdown = 5):
        Missions.Mission.Mission.__init__(self)

        self.old_time = 0
        self.new_time = 0

        self.laser_pointer = device_map.pitch_motor
        self.vision_data = device_map.car_vision_data

        self.countdown = countdown

    def initialize(self):
        self.old_time = time.time()
        self.new_time = time.time()
        self.laser_pointer.send(0, True, True)
        time.sleep(3)

    def execute(self):
        """"""
        self.new_time = time.time()

    def is_finished(self):
        a = self.vision_data.get_did_pop()
        if len(a) > 0:
            a = a[0]
        else:
            a = False
        return self.new_time - self.old_time > self.countdown or a

    def finish(self):
        self.laser_pointer.send(0, False, True)
