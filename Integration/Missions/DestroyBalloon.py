"""
Mission that shoots the laser
"""
import sys
import time

import Mission

sys.path.append('..')


class DestroyBalloon(Mission.Mission):
    def __init__(self):
        Mission.Mission.__init__(self)

        import Integration.Devices.DeviceMap
        import Integration.CarMain

        self.old_time = 0
        self.new_time = 0

        self.laser_pointer = Integration.Devices.DeviceMap.DeviceMap.pitch_motor
        self.vision_data = Integration.CarMain.CarMain.vision_data

    def initialize(self):
        self.old_time = time.time()
        self.new_time = time.time()
        time.sleep(3)
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
        return self.new_time - self.old_time > 5 or a

    def finish(self):
        self.laser_pointer.send(0, False, True)
