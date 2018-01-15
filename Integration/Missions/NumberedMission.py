import time
from random import *

from Mission import Mission


class NumberedMission(Mission):
    def __init__(self, num):
        Mission.__init__(self)  # Critical line in every mission
        self.num = num
        self.start_time = time.time()
        self.duration = random()

    def initialize(self):
        print("Numbered mission " + str(self.num) + " initialized")

        self.start_time = time.time()
        self.duration = random()

    def execute(self):
        print("Current time: " + str(time.time()))

    def is_finished(self):
        return (time.time() - self.start_time) > self.duration

    def finish(self):
        print("Numbered mission " + str(self.num) + " finished after " +
              str(self.duration))
