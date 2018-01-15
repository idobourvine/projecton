from Mission import Mission


class ParallelMission(Mission):
    def __init__(self, missions):
        Mission.__init__(self)  # Critical line in every mission

        self.missions = missions

        self.started = [False] * len(self.missions)

    def initialize(self):
        self.started = [False] * len(self.missions)

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
        Returns true if all missions have been started and each of them
        finished
        """
        return all(self.started) and all([not mission.am_i_running() for
                                          mission in self.missions])

    def finish(self):
        # If this mission has been killed stops any running missions
        for mission in self.missions:
            if mission.is_running:
                mission.kill()
