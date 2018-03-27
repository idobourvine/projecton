import Mission
import time

class SeriesMission(Mission.Mission):
    def __init__(self, missions):
        Mission.Mission.__init__(self)  # Critical line in every mission

        self.missions = missions  # List of missions to run

        self.started = [False] * len(self.missions)  # List representing
        # which missions by order have been started
        self.index = 0  # Index of current mission running in the mission list

    def initialize(self):
        self.started = [False] * len(self.missions)
        self.index = 0

    def execute(self):
        if self.index < len(self.missions):  # If there are still missions
            # to run
            mission = self.missions[self.index]  # Current mission
            if not mission.am_i_running():  # If current mission is not
                # running, either it hasnt yet been started, or its finished
                if not self.started[self.index]:  # Case not yet been started
                    mission.start()
                    self.started[self.index] = True
                else:  # Case mission finished
                    self.index += 1  # Inidicates moving on to the next mission
                    time.sleep(5)

    def is_finished(self):
        """
        Returns true after every mission has been started and then finished
        """
        if len(self.missions) == 0:
            return True

        return self.index >= len(self.missions)

    def finish(self):
        # If this mission has been killed stops any running missions
        for mission in self.missions:
            if mission.is_running:
                mission.kill()


