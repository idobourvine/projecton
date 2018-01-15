"""
This class contains all of the physical devices of the car, to prevent
attempting to intialize two instances of the same device
"""

from TurretMotor import TurretMotor


class DeviceMap:
    azimuth_motor = TurretMotor('COM5')  # serial comm with arduino that
    #  controls azimuth motor

    pitch_motor = TurretMotor('COM4')  # serial comm with arduino that
    #  controls pitch motor