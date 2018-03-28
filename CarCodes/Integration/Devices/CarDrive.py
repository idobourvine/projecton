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

        self.curr_ori = 270  # Starting orientation

    def close(self):
        if self.use_devices:
            self.ser.close()

    def get_curr_ori(self):
        return self.curr_ori

    def set_curr_ori(self, to_set):
        self.curr_ori = to_set

    def move_distance(self, length):
        """
        Sends the arduino a command to drive a certain distance in a
        straight line
        :param length: distance to drive (in meters)
        :return: None
        """

        length *= -1  # Distances are reversed

        if length < 0:
            self.send(0, abs(length), 1)
        else:
            self.send(0, length, 0)

    def rotate(self, angle):
        """
        Sends the arduino a command to drive a certain distance in a
        straight line
        :param length: distance to drive (in meters)
        :return: None
        """

        self.curr_ori += angle

        self.send(-1 * angle, 0, 0)

    def finished_moving(self):
        """
        Returns whether the last movement (move distance or rotate) was
        finished
        :return: False if still running, true otherwise
        """
        if (self.ser.inWaiting() > 0):
            a = self.ser.read()
            return True
        return False

    def send_data(self, numToSend):
        '''
        :param numToSend: send to arduino
        :return: void
        '''
        temp = numToSend
        b1 = int(temp / (2 ** 18))
        # print "b1 - " + str(b1)
        temp = temp % (2 ** 18)
        b2 = int(temp / (2 ** 11))
        # print "b2 - " + str(b2)
        temp = temp % (2 ** 11)
        b3 = int(temp / (2 ** 4))
        # print "b3 - " + str(b3)
        temp = temp % (2 ** 4)
        b4 = temp
        # print "b4 - " + str(b4)
        # send the data devided to half-bytes
        # print b1
        self.ser.write((chr(b1)))
        # print b2
        self.ser.write((chr(b2)))
        # print b3
        self.ser.write((chr(b3)))
        # print b4
        self.ser.write((chr(b4)))

        # print(b1,b2,b3)

    def send(self, angle, distance, isReverse):
        """
        :param angle: the angle to send
        :param distance: the distance in cm include dir
        :return: void
        """
        temp = int(abs(angle)) * 5 * 4096 + distance % 2048
        if (isReverse):
            temp = temp + 2048
        if angle < 0:
            temp += 8388608
        self.send_data(temp)
        print temp
