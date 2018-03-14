"""
Responsible for executing all of the missions
"""


class MissionHandler(object):
    active_missions = list()  # List of currently active missions

    @classmethod
    def add_mission(cls, mission):
        """
        Adds a new mission to the list of active missions
        :param mission: the mission to add
        :return: None
        """
        cls.active_missions.append(mission)

    @classmethod
    def run(cls):
        """
        Periodically called to run all of the missions
        :return: None
        """
        for mission in cls.active_missions:
            # If this is the first execution of this mission - it needs to
            # be initialized
            if not mission.am_i_running():
                mission.set_running()
                mission.initialize()
                print("Mission " + str(mission.__class__) + " initialize")
            if not mission.get_kill_flag():
                # Normal execution of the mission
                mission.execute()
            else:
                print("Mission " + str(mission.__class__) + " was killed")

            # If the mission is ready to finish it will return true
            if mission.is_finished() or mission.get_kill_flag():
                mission.finish()  # call finish code
                mission.stop_running()
                print("Mission " + str(mission.__class__) + " finished")
                cls.active_missions.remove(mission)

    @classmethod
    def close_all(cls):
        """
        Interrupts and finishes all currently active missions
        :return: None
        """
        for mission in cls.active_missions:
            mission.finish()
            mission.stop_running()
