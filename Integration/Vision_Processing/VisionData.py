import threading

from BalloonDetection import Webcamera


class VisionData:
    """
    Wrapper class for the data that comes from vision processing
    """
    def __init__(self):
        self.bloons = []  # Array of balloons detected by vision processing
        self.canShoot = [0]
        self.didPop = [0]

        self.eg1 = threading.Thread(target=Webcamera,
                                    args=(self.bloons, self.canShoot,
                                          self.didPop,))  # Thread that runs
        self.eg1.start()

    def get_bloons(self):
        return self.bloons[:]

    def get_can_shoot(self):
        return self.canShoot[:]

    def get_did_pop(self):
        return self.didPop[:]

    def continue_mission(self):
        """
        Should return whether there are more balloons to pop in the room
        :return:
        """
        return True