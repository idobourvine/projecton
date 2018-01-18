from Mission import Mission


class ParallelMission(Mission):
    def __init__(self, missions):
        Mission.__init__(self)  # Critical line in every mission

        self.missions = missions  # List of missions

        self.started = [False] * len(self.missions)  # Flags of was mission
        # started

    def initialize(self):
        self.started = [False] * len(self.missions)  # Inits all mission
        # flags to be not started

    def execute(self):
        """
        Makes sure all missions are started if they have not yet been started
        """
        for index in range(len(self.missions)):
            mission = self.missions[index]
            if not mission.am_i_running():
                if not self.started[index]:
                    mission.start()
                    self.started[index] = True

    def is_finished(self):
        """
        Returns true if all missions have been started and the finish of
        each has been called since being started
        """
        return all(self.started) and all(
            [mission.finished_called_since_start() for mission in
             self.missions])

    def finish(self):
        # If this mission has been killed stops any running missions
        for mission in self.missions:
            if mission.is_running:
                mission.kill()