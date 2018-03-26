"""
Mission that destroys all bloons from an array
"""
import sys

import AimAtBloonInPicture
import Missions.SeriesMission
import MoveTurretByAngle
import DestroyBloon
from Utils.UtilFunctions import *

sys.path.append('..')


class ClearStandpoint(Missions.SeriesMission.SeriesMission):
    def __init__(self, device_map, bloons, position, orientation):
        """
        Initialization
        :param device_map: the device map
        :param position: the position the car will be at: tuple (x, y, angle)
        :param bloons: list of bloon tuples (x, y, z, alignment)
        """
        Missions.SeriesMission.SeriesMission.__init__(self, list())

        self.security_vision_data = device_map.security_vision_data

        self.bloons = bloons
        self.position = position  # Starting position (x, y, z)
        self.orientation = orientation  # Starting orientation (theta)

        self.init_missions_list(device_map, self.bloons)

    def init_missions_list(self, device_map, bloons):
        self.missions = list()

        # TODO: figure out starting angles better
        # Assumes starting pitch is 0 and azimuth as car
        last_angles = (self.orientation, 0)
        print("Bloons to be popped at: ")
        print(bloons)
        for bloon in bloons:
            angles = self.convert_bloon_to_angles(bloon)

            diff_azimuth = - clamp_to_0_360(angles[0] - last_angles[0])
            # Azimuth motor is moving reversed relative to normal angles in
            # a mathematical plane

            diff_pitch = clamp_to_180(angles[1] - last_angles[1])

            print("Going to move angles: " + str((diff_azimuth, diff_pitch)))

            self.missions.append(
                MoveTurretByAngle.MoveTurretByAngle(device_map,
                                                    diff_azimuth, True,
                                                    diff_pitch, True))
            self.missions.append(
                AimAtBloonInPicture.AimAtBloonInPicture(
                    device_map))

            self.missions.append(DestroyBloon.DestroyBloon(device_map))

            last_angles = angles

    def convert_bloon_to_angles(self, bloon):
        """
        Recieves a bloon with x, y, z coordinates in the room, and returns
        the azimuth/pitch angles that the turret needs to turn
        :param bloon: A tuple of a bloon
        :return: A tuple of (azimuth_angle, pitch_angle)
        """

        # This function assumes that the bloon is a tuple of the following
        #  form: (id, x, y, z, alignment)
        # The balloons are (x,y,z) only!!!!
        # Computes bloon location relative to the given position,
        # in coordinates aligned with the room
        rel_x = bloon[0] - self.position[0]
        rel_y = bloon[1] - self.position[1]
        rel_z = bloon[2] - self.position[2]

        # Distance on ground between bloon and car
        ground_dist = pythagoras((rel_x, rel_y))

        # Pitch angle is arctan(z / (x^2 + y^2) )
        pitch_angle = to_degs(math.atan(rel_z / ground_dist))

        # Azimuth angle (in room coordinates) is arctan(y/x)
        room_azimuth_angle = to_degs(math.atan2(rel_y, rel_x))

        azimuth_angle = clamp_to_0_360(room_azimuth_angle)

        return azimuth_angle, pitch_angle


"""
    def initialize(self):
        self.azimuth_motor.send(self.bloons[self.index][0], False, False)
        self.pitch_motor.send(self.bloons[self.index][1], False, False)
        time.sleep(3)
        self.aim = AimAtBloonInPictureMission()
        self.aim.start()

    def execute(self):
        if self.aim.is_finished():
            self.aim_done = True
        if self.aim_done and self.aim.shoot.is_finished():
            if self.index < len(self.bloons) - 1:
                self.azimuth_motor.send(self.bloons[self.index + 1][0], False,
                                        False)
                self.pitch_motor.send(self.bloons[self.index + 1][1], False,
                                      False)
                time.sleep(3)
                self.aim =  \
                    AimAtBloonInPictureMission.AimAtBloonInPictureMission()
                self.aim_done = False
                self.aim.start()
                self.index += 1
            else:
                self.index += 1

    def is_finished(self):
        return self.index >= len(self.bloons)

    def finish(self):
        self.azimuth_motor.send(0, False, False)
        self.pitch_motor.send(0, False, False)
"""
