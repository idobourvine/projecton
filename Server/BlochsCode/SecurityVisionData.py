from BlochsCode.TaskManager import *
from threading import Thread
import time


class SecurityVisionData():
    def __init__(self):
        self.bloons = []
        self.process_thread = Thread(target=self.process,
                                     args=())
        self.process_thread.start()

    def process(self):
        startCams()
        # Now waits
        while True:
            self.bloons = getTargets()
            time.sleep(0.1)

    def get_bloons(self):
        return