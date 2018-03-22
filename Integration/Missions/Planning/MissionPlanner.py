import time

import Missions.Car.DriveToPoint
import Missions.SeriesMission
import Missions.Turret.ClearStandpoint
import Missions.Turret.MoveTurretToAngle
from Utils.Constants import *
from Utils.UtilFunctions import *


class MissionPlanner:
    MAX_SHOOTING_RANGE = 4  # In meters

    def __init__(self, device_map):
        self.device_map = device_map

        self.current_mission = None

        """
        Attribute describing current operating state
        0:
        Testing mode

        1:
        Starting state - destroy all bloons that are in range of
        starting position

        2:
        Travelling between preset central points in the room,
        destroying from each point all possible bloons

        3:
        Targeted elimination - so long as there are bloons, travels
        to the closest one and destroys all bloons from position
        """
        self.mission_state = 0

        # For testing state
        self.entered_state_0 = False

        # For state 2
        self.preset_standpoint = [(1, 2.5), (0, 1), (1, 0)]
        self.entered_state_2 = False
        # These numbers are munfatsim

    def manage_missions(self):
        """
        Decides if new missions are to be taken out each iteration
        """
        # Before starting the first mission, waits some time for
        # system initialization to take place
        if not self.current_mission:
            if Constants.use_devices:
                time.sleep(10)

        if not self.current_mission or \
                self.current_mission.finished_called_since_start():
            if self.device_map.security_vision_data.continue_mission():
                self.current_mission = self.return_next_mission(
                    self.device_map)
                if not self.current_mission:
                    print("No mission returned, going to sleep")
                    time.sleep(1)
                else:
                    self.current_mission.start()
                    print("Initiated new mission in mission manager")

    def return_next_mission(self, device_map):
        """
        Returns the next mission to perform, according to the current
        mission state and the current information from car and security vision
        data
        Should be called only when we want to issue a new mission

        The mission returned will be a complex mission - driving to a
        standpoint and clearing bloons from it

        :param device_map: The device map
        :return: A new mission to perform
        """
        curr_position = self.device_map.security_vision_data.get_car_position()
        curr_bloons = self.device_map.security_vision_data.get_bloons()

        if self.mission_state == 0:
            if not self.entered_state_0:
                # Testing mode
                print("Running tests")
                print()
                print("Testing Tzidud 20, Tzidud 10, Tzidud 5, Tzidud -20, "
                      "Tzidud -10, Tzidud -5")

                tzidud0 = Missions.Turret.MoveTurretToAngle.MoveTurretToAngle(
                    self.device_map, 20, 0)
                tzidud1 = Missions.Turret.MoveTurretToAngle.MoveTurretToAngle(
                    self.device_map, 10, 0)
                tzidud2 = Missions.Turret.MoveTurretToAngle.MoveTurretToAngle(
                    self.device_map, 5, 0)

                tzidud3 = Missions.Turret.MoveTurretToAngle.MoveTurretToAngle(
                    self.device_map, -20, 0)
                tzidud4 = Missions.Turret.MoveTurretToAngle.MoveTurretToAngle(
                    self.device_map, -10, 0)
                tzidud5 = Missions.Turret.MoveTurretToAngle.MoveTurretToAngle(
                    self.device_map, -5, 0)

                mis = Missions.SeriesMission.SeriesMission([
                    tzidud0, tzidud1, tzidud2, tzidud3, tzidud4, tzidud5])

                return mis

            else:
                return None

        elif self.mission_state == 1:
            bloons_to_destroy = self.get_bloons_relevant_for_standpoint(
                curr_bloons, curr_position)

            mis = Missions.Turret.ClearStandpoint.ClearStandpoint(
                device_map, bloons_to_destroy, curr_position)

            self.mission_state = 2  # Next mission that will be returned
            # will be clearing preset standpoints

            return mis

        elif self.mission_state == 2:
            if len(self.preset_standpoint) == 0:
                # Meaning we went through all preset points
                # Time to go to targeted elimination
                self.mission_state = 3

            else:
                # Checking if should start the preset points from start to end
                # or in reversed order
                # Should only do this check when entering state 2
                if not self.entered_state_2:
                    self.entered_state_2 = True
                    # Now this check won't happen again

                    dist_to_first = pythagoras(
                        (curr_position[0] - self.preset_standpoint[0][0],
                         curr_position[1] - self.preset_standpoint[0][1]))

                    dist_to_last = pythagoras(
                        (curr_position[0] - self.preset_standpoint[-1][0],
                         curr_position[1] - self.preset_standpoint[-1][1]))

                    # Each time the last bloon in the array is popped out of
                    #  the list
                    # So we want to reverse the order if the first is close
                    # than the last
                    if dist_to_last > dist_to_first:
                        self.preset_standpoint.reverse()

                next_standpoint = self.preset_standpoint.pop()
                driving_mission = \
                    Missions.Car.DriveToPoint.DriveToPoint(
                        device_map, curr_position, next_standpoint)

                # A position is a tuple of (x, y, angle)
                next_position = (next_standpoint[0], next_standpoint[1],
                                 driving_mission.movement_heading)

                bloons_to_destroy = self.get_bloons_relevant_for_standpoint(
                    curr_bloons, next_standpoint)

                clear_standpoint_mission = \
                    Missions.Turret.ClearStandpoint.ClearStandpoint(
                        device_map, bloons_to_destroy, next_position)

                mis = Missions.SeriesMission.SeriesMission([
                    driving_mission, clear_standpoint_mission])
                return mis

        elif self.mission_state == 3:
            # State is 3 and next mission was asked - meaning there are
            # still bloons in the room
            hostile_bloons = \
                self.device_map.security_vision_data.get_hostile_bloons()

            # If there are no more bloons and we got here - there's a problem
            if len(hostile_bloons) == 0:
                return None

            # Chooses next bloon arbitrarily
            next_bloon = hostile_bloons[0]

    def get_bloons_relevant_for_standpoint(self, bloons, standpoint):
        """
        Returns hostile bloons that are to be destroyed from a standpoint
        :param bloons: An iterable of all bloons to look at
        :param standpoint: The position the car will be at: tuple of (x, y) 
        :return: A list of relevant bloons
        """

        # A relevant bloon is defined to be hostile and in shooting range

        hostile_relevant_bloons = [bloon for bloon in bloons
                                   if bloon[4] == Constants.b_hostile and
                                   pythagoras((standpoint[0] - bloon[1],
                                               standpoint[1] - bloon[2],
                                               bloon[3])) <
                                   MissionPlanner.MAX_SHOOTING_RANGE]

        return hostile_relevant_bloons
