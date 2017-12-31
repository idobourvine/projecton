"""
Serial communication for controlling the azimuth motor
"""
import serial
import time
import struct


class Aiming:
    def __init__(self, port, baudrate=2000000):
        self.ser = serial.Serial(port,baudrate)
        time.sleep(5)


    def close(self):
        self.ser.close()

    def send(self, angle):
        angle1, angle2 = self.pack_to_two_angles(angle)
        self.ser.write(struct.pack('>B',int(angle1)))
        print(self.ser.read())
        self.ser.write(struct.pack('>B', int(angle2)))
        print(self.ser.read())

    def pack_to_two_angles(self, angle):
        angle = angle + 512
        print(int((angle)/256),int((angle)%256))
        return (int((angle)/256),int((angle)%256))








