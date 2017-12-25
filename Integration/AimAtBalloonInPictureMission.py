from Integration.Mission import Mission

class AimAtBalloonInPictureMission (Mission):
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

        print("running")

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
        pass