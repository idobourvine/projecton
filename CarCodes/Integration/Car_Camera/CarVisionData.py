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
        self.car_bloons = []  # Array of balloons detected by vision processing
        self.can_shoot = [0]
        self.did_pop = [0]

        self.room_bloons_1 = []

        self.room_bloons_2 = []

        self.stream = WebcamStream.WebcamStream(queueSize=2).start()

        self.connection = connection

        self.send_images_thread = threading.Thread(target=self.send_messages,
                                                   args=(self.connection,
                                                         self.stream))  # Thread that runs
        self.send_images_thread.start()

        self.parse_messages_thread = threading.Thread(
            target=self.read_messages,
            args=(self.connection,))
        self.parse_messages_thread.start()

        self.msg_pattern = re.compile("(^\w*MSG)")
        self.useless_number_pattern = re.compile("(\d+$)")

        self.process_car_vision = True  # Process car camera or not
        self.process_security_vision = True  # Process security cameras or not

        self.car_working = True  # True if car is working, false if it was
        # stopped

    def get_car_bloons(self):
        return copy.deepcopy(self.car_bloons)

    def get_can_shoot(self):
        return copy.deepcopy(self.can_shoot)

    def get_did_pop(self):
        return copy.deepcopy(self.did_pop)

    def get_room_bloons_1(self):
        return copy.deepcopy(self.room_bloons_1)

    def get_room_bloons_2(self):
        return copy.deepcopy(self.room_bloons_2)

    def get_room_bloons(self):
        return self.get_room_bloons_1() + self.get_room_bloons_2()

    def get_car_position(self):
        return (360, 180, 30)

    def get_continue_mission(self):
        return copy.deepcopy(self.continue_mission)

    def continue_mission(self):
        """
        Should return whether there are more balloons to pop in the room
        :return:
        """
        return True

    def set_process_car_vision(self, bool):
        self.process_car_vision = bool

    def set_process_security_vision(self, bool):
        self.process_security_vision = bool

    def send_messages(self, connection, stream):
        time.sleep(5)

        while True:

            # Currently sending does not work

            # Sending relevant processes types
            '''
            connection.send_msg(
                "MESSAGEProcessCarVisionMSG" + str(self.process_car_vision))
            connection.send_msg(
                "MESSAGEProcessSecurityVisionMSG" + str(
                    self.process_security_vision))
            '''

            if stream.more():
                if Constants.use_devices:
                    next_img = stream.read()
                else:
                    next_img = cv2.imread("1.jpg")

                connection.send_image(next_img)

                # print("Showing image")
                cv2.imshow('Kavitz', next_img)

                cv2.waitKey(150)

    def read_messages(self, connection):
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

                    if msg_type == "CarBloonsMSG":
                        self.car_bloons = data
                        print("Data from server: bloons: " + str(data))

                    elif msg_type == "CanShootMSG":
                        self.can_shoot = data
                        print("Data from server: can shoot: " + str(data))

                    elif msg_type == "DidPopMSG":
                        self.did_pop = data
                        print("Data from server: did pop: " + str(data))

                    elif msg_type == "RoomBloons1MSG":
                        self.room_bloons_1 = data
                        print("Data from server: room bloons 1: " + str(
                        data))

                    elif msg_type == "RoomBloons2MSG":
                        self.room_bloons_2 = data
                        print("Data from server: room bloons 2: " + str(
                        data))

                    elif msg_type == "CarWorkingMSG":
                        self.car_working = data
                        print("Data from server: car working: " + str(data))

            except Exception as e:
                print("EXCEPTION CAUGHT")
                print(str(e))
