"""
This class contains all of the physical devices of the car, to prevent
attempting to intialize two instances of the same device
"""

import Vision_Processing.VisionData
import TurretMotor


class DeviceMap:
    def __init__(self):
        self.vision_data = \
            Vision_Processing.VisionData.VisionData()

        self.azimuth_motor = TurretMotor.TurretMotor('COM5')
        # serial comm with arduino that controls azimuth motor

        self.pitch_motor = TurretMotor.TurretMotor('COM4')
        # serial comm with arduino that controls pitch motor
