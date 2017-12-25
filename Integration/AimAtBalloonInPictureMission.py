from Mission import Mission
import threading
from Vision_Processing.BalloonDetection import Webcamera

class AimAtBalloonInPictureMission (Mission):
    def init(self):
        """
        To be overriden
        Code that happens when the mission starts
        :return:
        """
        self.bloons1 = []
        eg1 = threading.Thread(target=Webcamera,
                               args=(self.bloons1,))
        eg1.start()

    def execute(self):
        """
        To be overriden
        Code that happens periodically
        :return:
        """

        print(self.bloons1)

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
        pass