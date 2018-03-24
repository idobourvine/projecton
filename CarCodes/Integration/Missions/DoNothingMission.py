import time
from random import *

import Mission


class DoNothingMission(Mission.Mission):
    def __init__(self):
        Mission.Mission.__init__(self)  # Critical line in every mission

    def initialize(self):
        print("Doing nothing mission")

    def execute(self):
        pass

    def is_finished(self):
        return False

    def finish(self):
        print("Going to do stuff")