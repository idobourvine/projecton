from BlochsCode.TaskManager import *
from threading import Thread
import time
import copy


class SecurityVisionData():
    def __init__(self):
        self.bloons = []

        self.car_location = []

        self.process_thread = Thread(target=self.process,
                                     args=())
        self.process_thread.start()

        self.started = False
        self.working = True

    def set_working(self, to_set):
        self.working = to_set

    def process(self):
        startCams()
        self.started = True
        while True:
            if self.working:
                print("Processing security vision data")
                self.bloons = getTargets()
                self.car_location = getCarLocation()
            time.sleep(0.1)

    def get_started(self):
        return self.started

    def get_bloons(self):
        if self.bloons:
            return copy.deepcopy(self.bloons)
        return []

    def get_car_location(self):
        return copy.deepcopy(self.car_location)