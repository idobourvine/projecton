from MissionHandler import MissionHandler


class Mission(object):

    def __init__(self):
        self.is_running = False

    def init(self):
        """
        To be overriden
        Code that happens when the mission starts
        :return:
        """

    def execute(self):
        """
        To be overriden
        Code that happens periodically
        :return:
        """

    def is_finished(self):
        """
        To be overriden
        True if the mission is finished, false otherwise
        :return:
        """

        return False

    def finish(self):
        """
        To be overriden
        Code that happends at termination of mission
        :return:
        """

    def am_i_running(self):
        return self.is_running

    def start(self):
        MissionHandler.add_mission(self)
