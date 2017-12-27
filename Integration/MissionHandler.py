

class MissionHandler(object):

    active_missions = list()

    @classmethod
    def add_mission(cls, mission):
        cls.active_missions.append(mission)

    @classmethod
    def run(cls):
        for mission in cls.active_missions:
            if not mission.am_i_running():
                mission.set_running()
                mission.initialize()

            mission.execute()

            if mission.is_finished():
                mission.finish()
                mission.stop_running()
                cls.active_missions.remove(mission)
