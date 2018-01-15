"""
Generic mission class that is run by the mission handler
"""
from MissionHandler import MissionHandler


class Mission(object):

    def __init__(self):
        """
        This needs to be called explicitly in the __init__ of every
        inheriting mission
        """
        self.is_running = False
        self.kill_flag = False

    def initialize(self):
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

    def set_running(self):
        self.is_running = True

        # Should be log
        """print (self.__class__.__name__ + " set running")  # Debugging"""

    def stop_running(self):
        self.is_running = False
        self.kill_flag = False

        # Should be log
        """print (self.__class__.__name__ + " stopped running")  # Debugging"""

    def kill(self):
        """
        Indicates to the mission handler to kill this mission
        """
        if self.am_i_running():
            self.kill_flag = True

    def get_kill_flag(self):
        return self.kill_flag

    def start(self):
        """
        Starts the mission by adding it to the mission handler
        :return: None
        """
        MissionHandler.add_mission(self)
