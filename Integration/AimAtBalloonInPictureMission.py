"""
Mission that aims at closest balloon to the center of car camera
"""
import sys
import threading

import keyboard

from Aiming import Aiming
from Integration.Vision_Processing.BalloonDetection import Webcamera
from Mission import Mission

sys.path.append('..')


class AimAtBalloonInPictureMission (Mission):

    def __init__(self):
        Mission.__init__(self)  # Critical line in every mission

        self.bloons1 = []  # Array of balloons detected by vision processing
        self.eg1 = threading.Thread(target=Webcamera,
                               args=(self.bloons1,))  # Thread that runs
        self.aiming = Aiming(2)  # Object of serial comm to

        self.pressed_hotkey = False  # flag if hotkey of ctrl+enter was pressed
        keyboard.add_hotkey('ctrl+enter', self.update_pressed_hotkey)
        # Starts tracking if hotkey was pressed

    def update_pressed_hotkey(self):
        """
        Function that is called by keyboard to update the flag if the hotkey
        was pressed
        """
        self.pressed_hotkey = True

    def initialize(self):
        """
        To be overriden
        Code that happens when the mission starts
        :return:
        """

        self.eg1.start()  # Starts the vision processing thread

    def execute(self):
        """
        To be overriden
        Code that happens periodically
        :return:
        """
        if self.bloons1:  # Might be empty if no balloons were detected
            inner = self.bloons1[0]
            if inner:  # Will be empty if no balloons were detected
                min_balloon = None  # Object of the balloon that is closest
                # to the center of the picture
                min_dist = 100000  # just some big number

                # Loop that finds the min_balloon from the bloons array
                for balloon in inner:
                    dist = balloon[0] ** 2 + balloon[1] ** 2
                    if dist < min_dist:
                        min_dist = dist
                        min_balloon = balloon
                if min_balloon:
                    if self.pressed_hotkey:
                        self.pressed_hotkey = False
                        # Tried to unmark the flag even in case min_balloon
                        # is not found
                        # Turns out it doesn't work smoothly
                        # This just means that care should be taken when
                        # pressing hotkey with no balloon present in picture
                        # Might cause system to move unexpectedly

                        angle_to_send = int(round(min_balloon[0]))

                        # This should be log
                        print("angle to send: " + str(angle_to_send))

                        # Sends angle to arduino
                        self.aiming.send(angle_to_send)

    def is_finished(self):
        """
        To be overriden
        True if the mission is finished, false otherwise
        :return:
        """

        # Currently the mission never finishes
        # Should finish when min_balloon detected is close enough to the
        # aiming point (center of picture)
        return False

    def finish(self):
        """
        To be overriden
        Code that happends at termination of mission
        :return:
        """
        self.aiming.close()

