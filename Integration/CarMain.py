"""
Main class of the car
"""
import time
import threading

from AimAtBalloonInPictureMission import AimAtBalloonInPictureMission
from MissionHandler import MissionHandler


class CarMain(object):
    def __init__(self):
        """
        self init of certain objects
        """
        self.mission_handler = MissionHandler()

    def init_car(self):
        """
        Main initialization code
        Here should be the initialization of other modules, communications,
        physical devices etc.
        :return:
        """
        # Starts the main periodic execution loop
        periodic_loop_thread = threading.Thread(target=self.do_every,
                                              args=(0.02, self.periodic_loop))
        periodic_loop_thread.start()



        # Mission creation and starting them
        aim = AimAtBalloonInPictureMission()
        aim.start()

    def periodic_loop(self):
        """
        Method that will run periodically
        :return:
        """
        self.mission_handler.run()

    def do_every(self, period, f, *args):
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
