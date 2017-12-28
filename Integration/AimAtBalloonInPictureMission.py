from Mission import Mission
import threading
from Vision_Processing.BalloonDetection import Webcamera
from Aiming import Aiming

import sys

sys.path.append('..')
import keyboard


class AimAtBalloonInPictureMission (Mission):

    def __init__(self):
        Mission.__init__(self)
        self.bloons1 = []
        self.eg1 = threading.Thread(target=Webcamera,
                               args=(self.bloons1,))
        self.aiming = Aiming(2, 9600)
        self.pressed_hotkey = False
        keyboard.add_hotkey('ctrl+enter', self.update_pressed_hotkey)

    def update_pressed_hotkey(self):
        self.pressed_hotkey = True

    def initialize(self):
        """
        To be overriden
        Code that happens when the mission starts
        :return:
        """

        self.eg1.start()
        print("initiated")

    def execute(self):
        """
        To be overriden
        Code that happens periodically
        :return:
        """
        if self.bloons1:
            inner = self.bloons1[0]
            if inner:
                min_balloon = None
                min_dist = 100000  # just some big number
                for balloon in inner:
                    dist = balloon[0] ** 2 + balloon[1] ** 2
                    if dist < min_dist:
                        min_dist = dist
                        min_balloon = balloon
                if min_balloon:
                    if self.pressed_hotkey:
                        self.pressed_hotkey = False
                        print("Minimum balloon found: " + str(min_balloon))
                        self.aiming.send(10 * int(round(min_balloon[0])))

    def is_finished(self):
        """
        To be overriden
        True if the mission is finished, false otherwise
        :return:
        """

        return False

    def finish(self):
        """
        To be overriden
        Code that happends at termination of mission
        :return:
        """
        self.aiming.close()

