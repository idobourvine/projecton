"""
Main class of the car
"""
import threading
import time

import Devices.DeviceMap
import Integration.Missions.Planning.MissionPlanner
import Missions.MissionHandler


class CarMain:
    """
    Main class of the car
    """

    """
    self init of global objects
    """
    device_map = Devices.DeviceMap.DeviceMap()

    @classmethod
    def init_car(cls):
        """
        Main initialization code
        Here should be the initialization of other modules, communications,
        physical devices etc.
        :return:
        """

        cls.mission_handler = Missions.MissionHandler.MissionHandler()
        cls.mission_planner = Integration.Missions.Planning.MissionPlanner.MissionPlanner(
            device_map=cls.device_map)

        def periodic_loop():
            """
            Method that will run periodically
            """
            cls.mission_planner.manage_missions()
            cls.mission_handler.run()

        # Starts the main periodic execution loop
        periodic_loop_thread = threading.Thread(target=cls.do_every,
                                                args=(0.02, periodic_loop))
        periodic_loop_thread.start()

        print("All set, let's go!")


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
