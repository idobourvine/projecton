import threading
import PiStream
import copy
import collections
from BalloonDetection import Webcamera

class VisionData:
    """
    Wrapper class for the data that comes from vision processing
    """
    def __init__(self, connection):
        self.bloons = []  # Array of balloons detected by vision processing
        self.can_shoot = [0]
        self.did_pop = [0]

        self.stream = PiStream.PiStream(queueSize=2).start()
        print("Started image stream from pi")

        self.connection = connection

        self.eg1 = threading.Thread(target=Webcamera,
                                    args=(self.connection, self.stream,
                                          self.bloons,
                                          self.can_shoot,
                                          self.did_pop))  # Thread that runs
        self.eg1.start()

    def get_bloons(self):
        temp = self.flatten(copy.deepcopy(self.bloons))
        pairs = []
        for i in range(int(len(temp) / 2)):
            pairs.append([temp[2*i], temp[2*i+1]])
        return pairs

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

    def flatten(self, x):
        if isinstance(x, collections.Iterable):
            return [a for i in x for a in self.flatten(i)]
        else:
            return [x]