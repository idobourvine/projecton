import ast
import copy
import re
import threading
import time

import cv2
from Utils.Constants import *

import WebcamStream


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

        self.send_images_thread = threading.Thread(target=self.send_images,
                                                   args=(self.connection,
                                                         self.stream))  # Thread that runs
        self.send_images_thread.start()

        self.parse_messages_thread = threading.Thread(
            target=self.read_messages,
            args=(self.connection,
                  self.bloons,
                  self.can_shoot,
                  self.did_pop))
        self.parse_messages_thread.start()

        self.msg_pattern = re.compile("(^\w*MSG)")
        self.useless_number_pattern = re.compile("(\d+$)")

    def get_bloons(self):
        return copy.deepcopy(self.bloons)

    def get_can_shoot(self):
        return copy.deepcopy(self.can_shoot)

    def get_did_pop(self):
        return copy.deepcopy(self.did_pop)

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
                connection.send_image(next_img)
                # cv2.imshow('Kavitz', next_img)
                cv2.waitKey(150)

    def read_messages(self, connection, bloons, can_shoot, did_pop):
        while True:
            try:
                msg = connection.get_msg()
                if not msg:
                    continue

                messages = msg.split('MESSAGE')
                for real_msg in messages:
                    if real_msg == '':
                        continue

                    stripped = real_msg.strip()
                    removed_useless_num = self.useless_number_pattern.sub(
                        '', stripped)

                    split = self.msg_pattern.split(removed_useless_num, 1)

                    if not split:
                        continue

                    msg_type = split[1]
                    raw_msg = split[2]
                    data = ast.literal_eval(raw_msg)

                    if msg_type == "BloonsMSG":
                        self.bloons = data

                    elif msg_type == "CanShootMSG":
                        self.can_shoot = data

                    elif msg_type == "DidPopMSG":
                        self.did_pop = data

                    print(str(data))

            except Exception as e:
                print("EXCEPTION CAUGHT")
                print(e)
