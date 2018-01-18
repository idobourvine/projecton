from Integration.Missions.Mission import Mission
from Integration.Devices.DeviceMap import DeviceMap
import time

class MoveTurretToAngle(Mission):
    def __init__(self, device_map, azimuth, pitch):
        Mission.__init__(self)
        self.azimuth_motor = device_map.azimuth_motor
        self.pitch_motor = device_map.pitch_motor

        self.azimuth = azimuth
        self.pitch = pitch

        self.start_time = 0

        self.duration = 3  # 3 seconds to wait

    def initialize(self):
        self.azimuth_motor.send(self.azimuth, False, False)
        self.pitch_motor.send(self.pitch, False, False)
        self.start_time = time.time()

    def execute(self):
        pass

    def is_finished(self):
        return (time.time() - self.start_time) > self.duration

    def finish(self):
        self.azimuth_motor.send(0, False, False)
        self.pitch_motor.send(0, False, False)

