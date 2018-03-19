"""
This class contains all of the physical devices of the car, to prevent
attempting to intialize two instances of the same device
"""

import Integration.Car_Camera.CarVisionData
import Integration.Security_Cameras.SecurityVisionData
import CarDrive
import TurretMotor


class DeviceMap:
    def __init__(self):
        self.car_vision_data = \
            Integration.Car_Camera.CarVisionData.CarVisionData()
        self.security_vision_data = \
            Integration.Security_Cameras.SecurityVisionData.SecurityVisionData()

        self.azimuth_motor = TurretMotor.TurretMotor('COM5')
        # serial comm with arduino that controls azimuth motor

        self.pitch_motor = TurretMotor.TurretMotor('COM4')
        # serial comm with arduino that controls pitch motor

        self.car_drive = CarDrive.CarDrive('COM6') # Need to check port
        # Serial communication with car arduino
