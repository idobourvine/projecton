"""
This class contains all of the physical devices of the car, to prevent
attempting to intialize two instances of the same device
"""

import Integration.Communication.Connection
import Integration.Car_Camera.CarVisionData
import Integration.Security_Cameras.SecurityVisionData
import CarDrive
import TurretMotor

class DeviceMap:
    def __init__(self):
        self.connection = Integration.Communication.Connection.Connection(True)

        self.car_vision_data = \
            Integration.Car_Camera.CarVisionData.CarVisionData(self.connection)

        self.security_vision_data = \
            Integration.Security_Cameras.SecurityVisionData.SecurityVisionData()

        # serial comm with arduino that controls azimuth motor
        # self.azimuth_motor = TurretMotor.TurretMotor('COM5')  # PC port
        self.azimuth_motor = TurretMotor.TurretMotor('/dev/ttyUSB1')  # Pi port

        # serial comm with arduino that controls pitch motor
        # self.pitch_motor = TurretMotor.TurretMotor('COM4')  # PC port
        self.pitch_motor = TurretMotor.TurretMotor('/dev/ttyUSB0')  # Pi port

        # self.car_drive = CarDrive.CarDrive('/dev/ttyUSB2')  # Pi port
        # Serial communication with car arduino
