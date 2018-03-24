import threading
import time

from BloonDetection import Webcamera
import WebcamStream
import cv2
import copy
import collections

from Utils.Constants import *

class CarVisionData:
    """
    Wrapper class for the data that comes from vision processing
    """
    def __init__(self, connection):
        self.bloons = []  # Array of balloons detected by vision processing
        self.can_shoot = [0]
        self.did_pop = [0]

        self.stream = WebcamStream.WebcamStream(queueSize=2).start()

        self.connection = connection

        self.eg1 = threading.Thread(target=self.send_images,
                                    args=(self.connection, self.stream))  # Thread that runs
        self.eg1.start()

        self.eg2 = threading.Thread(target=self.read_messages,
                                    args=(self.connection,))  # Thread that
        self.eg2.start()
        # runs

    def get_bloons(self):
        return []

    def get_can_shoot(self):
        return []

    def get_did_pop(self):
        return []

    def continue_mission(self):
        """
        Should return whether there are more balloons to pop in the room
        :return:
        """
        return True

    def send_images(self, connection, stream):
        time.sleep(5)
        
        while True:
            if stream.more():
                next_img = stream.read()
                cv2.imshow('Kavitz', next_img)
                connection.send_image(next_img)
                cv2.waitKey(150)
                
    def read_messages(self, connection):
        while True:
            try:
                msg = connection.get_msg()
                if msg:
                    print(str(msg))
            except Exception as e:
                print("EXCEPTION CAUGHT")
                print(e)
