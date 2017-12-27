from Mission import Mission
import threading
from Vision_Processing.BalloonDetection import Webcamera


class AimAtBalloonInPictureMission (Mission):

    def __init__(self):
        Mission.__init__(self)
        self.bloons1 = []
        self.eg1 = threading.Thread(target=Webcamera,
                               args=(self.bloons1,))

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
                min_dist = 90000  # just some big number
                for balloon in inner:
                    dist = balloon[0] ** 2 + balloon[1] ** 2
                    if dist < min_dist:
                        min_dist = dist
                        min_balloon = balloon
                if min_balloon:
                    print("Minimum balloon found: " + str(min_balloon))

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

