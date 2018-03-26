"""
Moves turret to given azimuth and pitch angles
the angles are relative to the car, and represent the actual setpoints for
the turret (rather than change in angles)
"""

import time

import Missions.Mission


class MoveTurretByAngle(Missions.Mission.Mission):
    def __init__(self, device_map, azimuth, azimuth_rel, pitch, pitch_rel):

        Missions.Mission.Mission.__init__(self)

        self.azimuth_motor = device_map.azimuth_motor
        self.pitch_motor = device_map.pitch_motor

        self.azimuth = azimuth
        self.pitch = pitch

        self.azimuth_rel = azimuth_rel
        self.pitch_rel = pitch_rel

        self.start_time = 0

        self.duration = 3  # 3 seconds to wait

    def initialize(self):
        print("moving angles: " + str(self.azimuth, self.azimuth_rel,
                                      self.pitch, self.pitch_rel))
        if self.azimuth != 0:
            self.azimuth_motor.send(self.azimuth, False, self.azimuth_rel)
        if self.pitch != 0:
            self.pitch_motor.send(self.pitch, False, self.pitch_rel)
        self.start_time = time.time()

    def execute(self):
        pass

    def is_finished(self):
        return (time.time() - self.start_time) > self.duration

    def finish(self):
        self.azimuth_motor.send(0, False, True)
        self.pitch_motor.send(0, False, True)
