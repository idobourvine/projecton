import Missions.Car.MoveDistance
import Missions.Car.Rotate
import Missions.SeriesMission
import Missions.NumberedMission
from Utils.UtilFunctions import *


class DriveToPoint(Missions.SeriesMission.SeriesMission):
    def __init__(self, device_map, starting_pos, point):
        """
        Initialization
        :param device_map: the device map
        :param starting_pos: The position the car will start at: tuple of (
        x, y, angle)
        :param point: tuple of (x, y) we want to reach
        """
        Missions.SeriesMission.SeriesMission.__init__(self, list())

        self.security_vision_data = device_map.security_vision_data
        self.starting_pos = starting_pos
        self.point = point

        # These will be initialized by init_missions_list
        self.movement_heading = 0

        self.init_missions_list(device_map=device_map)

    def init_missions_list(self, device_map):

        rel_x = self.point[0] - self.starting_pos[0]
        rel_y = self.point[1] - self.starting_pos[1]

        movement_heading = to_degs(math.atan2(rel_y, rel_x))
        self.movement_heading = movement_heading
        amount_to_rotate = clamp_to_180(movement_heading - self.starting_pos[2])
        self.missions.append(Missions.Car.Rotate.Rotate(
            device_map, amount_to_rotate))

        dist = pythagoras((rel_x, rel_y))
        self.missions.append(
            Missions.Car.MoveDistance.MoveDistance(device_map,
                                                               dist))

        self.missions.append(Missions.NumberedMission.NumberedMission(1, 10))
