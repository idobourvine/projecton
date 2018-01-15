"""
Main class of the car
"""
import threading
import time

import Devices.DeviceMap
import Missions.MissionHandler
import Missions.MissionPlanner
import Vision_Processing.VisionData


class CarMain:
    """
    Main class of the car
    """

    """
    self init of certain objects
    """
    device_map = Devices.DeviceMap.DeviceMap()
    vision_data = Vision_Processing.VisionData.VisionData()

    mission_handler = Missions.MissionHandler.MissionHandler()
    mission_planner = Missions.MissionPlanner.MissionPlanner(
        device_map=device_map, vision_data=vision_data)

    @classmethod
    def init_car(cls):
        """
        Main initialization code
        Here should be the initialization of other modules, communications,
        physical devices etc.
        :return:
        """
        # Starts the main periodic execution loop
        periodic_loop_thread = threading.Thread(target=cls.do_every,
                                                args=(0.02, cls.periodic_loop))
        periodic_loop_thread.start()

        print("All set, let's go!")

    @classmethod
    def periodic_loop(cls):
        """
        Method that will run periodically
        """

        cls.mission_planner.manage_missions()
        cls.mission_handler.run()

    @classmethod
    def do_every(cls, period, f, *args):
        """
        Calls a function every period of time
        :param period: In seconds
        :param f: function to call
        :param args: arguments to pass the function
        :return: None
        """

        def g_tick():
            t = time.time()
            count = 0
            while True:
                count += 1
                yield max(t + count * period - time.time(), 0)

        g = g_tick()
        while True:
            time.sleep(next(g))
            f(*args)


if __name__ == "__main__":
    car = CarMain()
    car.init_car()
