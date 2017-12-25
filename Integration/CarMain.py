import time
from MissionHandler import MissionHandler


class CarMain(object):

        def __init__(self):
            self.mission_handler = MissionHandler()

        def init_car(self):
            """
            Initialization code
            :return:
            """
            self.do_every(0.02, self.periodic_loop)

        def periodic_loop(self):
            """
            Method that will run periodically every 10 ms
            :return:
            """

            self.mission_handler.run()

        def do_every(self, period, f, *args):
            def g_tick():
                t = time.time()
                count = 0
                while True:
                    count += 1
                    yield max(t + count*period - time.time(), 0)
            g = g_tick()
            while True:
                time.sleep(next(g))
                f(*args)


if __name__ == "__main__":
    car = CarMain()
    car.init_car()

