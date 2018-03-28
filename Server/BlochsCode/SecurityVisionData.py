from BlochsCode.TaskManager import *
from threading import Thread
import time
import copy


class SecurityVisionData():
    def __init__(self):
        self.bloons = []

        self.car_location = []
        self.friends = []
        self.process_thread = Thread(target=self.process,
                                     args=())
        self.process_thread.start()

        self.started = False

        self.working = True
        # self.working = False

    def set_working(self, to_set):
        self.working = to_set


    def process(self):
        startCams()
        self.started = True
        while True:
            if self.working:
                print("Processing security vision data")
                try:
                    self.bloons = getTargets()
                    self.car_location = getCarLocation()
                    self.friends = getInnocents()
                except Exception, err:
                    print("Exception from security process")
                    print(err)
                    print(err.args)
                    print(err.__class__)

            time.sleep(0.1)


    def get_started(self):
        return self.started


    def get_bloons(self):
        if len(self.bloons) > 0:
            return copy.deepcopy(self.bloons)
        return []


    def get_car_location(self):
        return copy.deepcopy(self.car_location)


    def get_friends(self):
        if len(self.friends) > 0:
            return copy.deepcopy(self.friends)
        return []
