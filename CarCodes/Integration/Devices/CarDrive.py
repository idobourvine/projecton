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

    def move_distance(self, length):
        """
        Sends the arduino a command to drive a certain distance in a
        straight line
        :param length: distance to drive (in meters)
        :return: None
        """
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
        self.send(angle,0,0)

    def finished_moving(self):
        """
        Returns whether the last movement (move distance or rotate) was
        finished
        :return: False if still running, true otherwise
        """
        if(self.ser.inWaiting() > 0):
            a = self.ser.read()
            print str(a)
            return True
        return False

    def send_data(self,numToSend):
        '''
        :param numToSend: send to arduino
        :return: void
        '''
        temp = numToSend
        b1 = int(temp / (2 ** 17))
        temp = temp % (2 ** 17)
        b2 = int(temp / (2 ** 10))
        temp = temp % (2 ** 10)
        b3 = int(temp / (2 ** 3))
        temp = temp % (2 ** 3)
        b4 = temp
        #send the data devided to half-bytes
        #print b1
        self.ser.write((chr(b1)))
        #print b2
        self.ser.write((chr(b2)))
        #print b3
        self.ser.write((chr(b3)))
        #print b4
        self.ser.write((chr(b4)))

        # print(b1,b2,b3)

    def send(self, angle, distance, isReverse):
        """
        :param angle: the angle to send
        :param distance: the distance in cm include dir
        :return: void
        """
        temp = int(angle) * 5 * 4096 + distance % 2048
        if (isReverse):
            temp = temp + 2048
        self.send_data(temp)
        print temp
