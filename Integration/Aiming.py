import serial
import time

class Aiming:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port)
        time.sleep(5)
        self.ser.baudrate = baudrate

    def close(self):
        self.ser.close()

    def send(self, angle):
        self.ser.write(str(angle%256))







