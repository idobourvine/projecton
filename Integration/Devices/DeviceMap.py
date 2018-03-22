"""
This class contains all of the physical devices of the car, to prevent
attempting to intialize two instances of the same device
"""

import Car_Camera.CarVisionData
import Security_Cameras.SecurityVisionData
import CarDrive
import TurretMotor


class DeviceMap:
    def __init__(self):
        self.car_vision_data = \
            Car_Camera.CarVisionData.CarVisionData()

        self.security_vision_data = \
            Security_Cameras.SecurityVisionData.SecurityVisionData()

        # self.azimuth_motor = TurretMotor.TurretMotor('COM5')  # PC Port
        self.azimuth_motor = TurretMotor.TurretMotor('/dev/ttyUSB1')  # Pi Port
        # serial comm with arduino that controls azimuth motor

        # self.pitch_motor = TurretMotor.TurretMotor('COM4')  # PC Port
        self.pitch_motor = TurretMotor.TurretMotor('/dev/ttyUSB0')  # Pi Port

        # serial comm with arduino that controls pitch motor

        # self.car_drive = CarDrive.CarDrive('COM6') # Need to check port  # PC Port
        # Serial communication with car arduino
