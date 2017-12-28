"""
Serial communication for controlling the azimuth motor
"""
import serial
import time


class Aiming:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port)
        time.sleep(5)  # Need to wait for the port to open before addressing
        #  the ser
        self.ser.baudrate = baudrate  # Bandwidth of the serial comm

    def close(self):
        self.ser.close()

    def send(self, angle):
        """
        Sends an angle to the arduino
        :param angle: angle to make the azimuth motor turn
        :return: None
        """

        # Should be log
        """print ("about to send: " + str(angle % 256))"""
        self.ser.write(str(angle % 256))  # Code at arduino currently
        # expects a single byte







