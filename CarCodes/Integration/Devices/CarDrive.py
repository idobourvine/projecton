import time

import Utils.Constants
import serial


class CarDrive:
    def __init__(self, port, baudrate=2000000):
        self.use_devices = Utils.Constants.Constants.use_devices
        if self.use_devices:
            self.ser = serial.Serial(port, baudrate)
        time.sleep(5)

    def close(self):
        if self.use_devices:
            self.ser.close()

    """
    def send(self, angle, shut, isRel):
        angle1, angle2 = self.pack_to_two_angles(int(angle*5.825), shut, isRel)
        if self.use_devices:
            self.ser.write(struct.pack('>B', int(angle1)))
            #print(self.ser.read())
            self.ser.write(struct.pack('>B', int(angle2)))
            #print(self.ser.read())

    def pack_to_two_angles(self, angle, shut, isRel):
        '''
        :param angle: the number of step
        :param shut: the 13 bit is 1 if we need to fire ,else 0
        :param isRel: the 14 bit is 1 if the angle is rel ,else 0
        :return:
        '''
        angle += 2048
        #8192=2^13
        if shut:
            angle += 4096
        if not isRel:
            #16384=2^14
            angle += 8192
        print(int((angle) / 256), int((angle) % 256))
        return (int((angle) / 256), int((angle) % 256))
    """

    def move_distance(self, length):
        """
        Sends the arduino a command to drive a certain distance in a
        straight line
        :param length: distance to drive (in meters)
        :return: None
        """
        print ("Moving " + str(length) + " meters")
        pass

        # Sends to arduino to move length

    def rotate(self, angle):
        """
        Rotates in place a given angle
        :param angle: The angle to rotate (positive for counter-clockwise,
        negative for clockwise)
        :return: None
        """
        print ("Rotating " + str(angle) + " degrees")
        pass

        # Sends to arduino to rotate

    def get_gyro_angle(self):
        """
        :return: Current reading from gyro
        """

        return 0

        # returns the read from the serial

    def get_encoder_dist(self):
        """
        :return: Current reading from encoder
        """

        return 0

        # returns the read from the serial

    def finished_moving(self):
        """
        Returns whether the last movement (move distance or rotate) was
        finished
        :return: False if still running, true otherwise
        """

        return True

        # returns the read from the serial
