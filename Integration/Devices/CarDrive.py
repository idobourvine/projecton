import struct
import time
import serial
import Utils.Constants

class CarDrive():

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

        pass

        # Sends to arduino to move length

    def finished_moving(self):
        """
        Returns whether the last movement (move distance or rotate) was
        finished
        :return: False if still running, true otherwise
        """

        pass

        # returns the read from the serial

    # TODO:
    # Add methods: rotate, get gyro angle, get encoder reading

