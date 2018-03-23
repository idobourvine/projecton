from Utils.Constants import *


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
        Returns a list of the bloons in the room
        each bloon is a tuple of (id, x, y, z, alignment)
        # Alignment is whether or not the bloon is hostile
        :return: List of all bloons
        """

        return list()

    def get_hostile_bloons(self):
        """
        Returns a list of the hostile bloons in the room
        each bloon is a tuple of (id, x, y, z, alignment)
        # Alignment is whether or not the bloon is hostile
        :return: List of all bloons with hostile alignment
        """

        return [bloon for bloon in self.get_bloons()
                if bloon[4] == Constants.b_hostile]

    def get_car_position(self):
        """
        Returns the location and heading of the car
        :return: tuple of (x, y, theta)
        """

        return (0, 0, 0)

    def get_did_pop(self):
        """
        :return: Whether there was a bloon popped
        """

        return False

    def continue_mission(self):
        """
        Should return whether there are more bloons to pop in the room
        :return:
        """
        return True
