

class SecurityVisionData:
    """
    Wrapper class for the data that comes from vision processing
    """
    def __init__(self):
        """
        Init method of this object
        """

        # Need to add relevant attributes

    def get_bloons(self):
        """
        Returns a list of the balloons in the room
        each balloon is a tuple of [stuff] (such as id, x, y, z, alignment)
        # Alignment is whether or not the balloon is hostile
        :return: List of all balloons
        """

        pass


    def get_car_position(self):
        """
        Returns the location and heading of the car
        :return: tuple of (x, y, theta)
        """

        pass


    def get_did_pop(self):
        """
        :return: Whether there was a balloon popped
        """

        pass

    def continue_mission(self):
        """
        Should return whether there are more balloons to pop in the room
        :return:
        """
        return True
