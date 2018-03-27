"""
Serial communication for controlling the turret motors (azimuth or pitch)
"""
import struct
import time

import Utils.Constants
import serial

import Motor


class TurretMotor(Motor.Motor):
    def __init__(self, port, baudrate=2000000):
        Motor.Motor.__init__(self)
        self.port = port
        self.use_devices = Utils.Constants.Constants.use_devices
        if self.use_devices:
            self.ser = serial.Serial(port, baudrate)
            print("opened port " + str(port))
            time.sleep(5)

    def close(self):
        if self.use_devices:
            self.ser.close()

    def send(self, angle, shut, isRel):
        angle1, angle2 = self.pack_to_two_angles(int(angle * 5.825), shut,
                                                 isRel)
        if self.use_devices:
            print(
            "Sending (" + str(angle1) + ", " + str(angle2) + ") to " + str(
                self.port))
            self.ser.write(struct.pack('>B', int(angle1)))
            self.ser.write(struct.pack('>B', int(angle2)))

    def getAngle(self):
        """"""

    def pack_to_two_angles(self, angle, shut, isRel):
        '''
        :param angle: the number of step
        :param shut: the 13 bit is 1 if we need to fire ,else 0
        :param isRel: the 14 bit is 1 if the angle is rel ,else 0
        :return:
        '''
        angle += 2048
        # 8192=2^13
        if shut:
            angle += 4096
        if not isRel:
            # 16384=2^14
            angle += 8192
        # print(int((angle) / 256), int((angle) % 256))
        return (int((angle) / 256), int((angle) % 256))

    def on_target(self):
        """
        Returns whether the motor reached its last setpoint
        """

        # Should be fixed to be based on data from serial
        return True

    def finished_moving(self):
        if (self.ser.inWaiting() > 0):
            a = self.ser.read()
            print True
            return True
        return False
