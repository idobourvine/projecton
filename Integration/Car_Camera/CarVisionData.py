import threading

from BalloonDetection import Webcamera
import WebcamStream

class CarVisionData:
    """
    Wrapper class for the data that comes from vision processing
    """
    def __init__(self):
        self.bloons = []  # Array of balloons detected by vision processing
        self.canShoot = [0]
        self.didPop = [0]

        self.stream = WebcamStream.WebcamStream(queueSize=2).start()

        self.eg1 = threading.Thread(target=Webcamera,
                                    args=(self.stream, self.bloons,
                                          self.canShoot,
                                          self.didPop))  # Thread that runs
        self.eg1.start()

    def get_hostile_bloons(self):
        """
        Returns a list of the balloons in the car camera that are hostile
        each balloon is a tuple of azimuth angle and pitch angle
        :return:
        """
        return self.bloons[:]

    def get_can_shoot(self):
        return self.canShoot[:]

    def get_did_pop(self):
        return self.didPop[:]

