import Mission
class Position(Mission.Mission):
    """
    arrival position and destroy all the balloons .
    first go to position - a mission.
    second destroy all the balloons in this position - a mission.
    in this file we go to position and in the finish we do the second.
    """
    def __init__(self,device_map):
        Mission.Mission.__init__(self)
        self.car = device_map.Car

    def initialize(self):
        """

        :return:
        """
    def execute(self):
        """

        :return:
        """

    def is_finished(self):
        """

        :return:
        """

    def finish(self):
        """
        do 'DestroyBalloon'
        :return: none
        """
        m= Mission.DestroyBalloon()
        m.start