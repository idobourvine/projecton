from BlochsCode.TaskManager import *
from threading import Thread
import time
import copy


class SecurityVisionData():
    def __init__(self):
        self.bloons = []
        self.process_thread = Thread(target=self.process,
                                     args=())
        self.process_thread.start()

        self.started = False

    def process(self):
        startCams()
        self.started = True
        while True:
            self.bloons = getTargets()
            time.sleep(0.1)

    def get_started(self):
        return self.started

    def get_bloons(self):
        if self.bloons:
            return copy.deepcopy(self.bloons)
        return []