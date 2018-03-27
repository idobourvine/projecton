"""
This class contains all of the physical devices of the car, to prevent
attempting to intialize two instances of the same device
"""

import Communication.Connection
import Car_Camera.CarVisionData
import CarDrive
import TurretMotor
from Utils.Constants import *

class DeviceMap:
    def __init__(self):
        self.connection = Communication.Connection.Connection(True)

        self.car_vision_data = \
            Car_
        Camera.CarVisionData.CarVisionData(self.connection)

        if Constants.car_or_turret:
            self.car_drive = CarDrive.CarDrive('/dev/ttyUSB0')  # Pi port
            # Serial communication with car arduino

        else:
            # serial comm with arduino that controls azimuth motor
            # self.azimuth_motor = TurretMotor.TurretMotor('COM5')  # PC port
            self.azimuth_motor = TurretMotor.TurretMotor('/dev/ttyUSB0')  # Pi port

            # serial comm with arduino that controls pitch motor
            # self.pitch_motor = TurretMotor.TurretMotor('COM4')  # PC port
            self.pitch_motor = TurretMotor.TurretMotor('/dev/ttyUSB1')  # Pi port


