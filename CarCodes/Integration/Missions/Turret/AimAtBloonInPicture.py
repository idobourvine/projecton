"""
Mission that aims at closest bloon to the center of car camera
"""
import sys
import time

import Missions.Turret.DestroyBloon
import Missions.Mission

sys.path.append('..')


class AimAtBloonInPicture(Missions.Mission.Mission):
    def __init__(self, device_map):
        Missions.Mission.Mission.__init__(self)  # Critical line in every mission

        self.vision_data = device_map.car_vision_data

        # runs
        self.azimuth_motor = device_map.azimuth_motor
        self.pitch_motor = device_map.pitch_motor

        self.shoot = Missions.Turret.DestroyBloon.DestroyBloon(device_map)
        # Variables for execute loop
        self.min_bloon = None
        self.min_dist = 100000

        self.distance_threshold = 1.3  # Maximum "distance" that the bloon
        #  is allowed to be away from the aiming point (center of camera)
        # The distance is the sum of square of x-angle and y-angle

        self.max_counter = 4  # Number of loops the camera needs to be on
        # target to consider to be finished
        self.counter = 0  # Loop counter that is updated in is_finished method

    def initialize(self):
        """
        To be overriden
        Code that happens when the mission starts
        :return:
        """
        if self.azimuth_motor.is_locked() or self.pitch_motor.is_locked():
            print("Tried to start mission when one of the motors is already "
                  "used by another one")
            self.kill()
        else:
            pass
            # self.azimuth_motor.lock()  # Locks the motor for safety
            # self.pitch_motor.lock()  # Locks the motor for safety

    def execute(self):
        """
        To be overriden
        Code that happens periodically
        :return:
        """
        a = self.vision_data.get_bloons()
        if a:  # Might be empty if no bloons were detected
            inner = a[0]
            if inner:  # Will be empty if no bloons were detected
                self.min_bloon = None  # Object of the bloon that is
                # closest to the center of the picture
                self.min_dist = 100000  # just some big number

                # Loop that finds the min_bloon from the bloons array
                for bloon in inner:
                    dist = bloon[0] ** 2 + bloon[1] ** 2
                    if dist < self.min_dist:
                        self.min_dist = dist
                        self.min_bloon = bloon
                if self.min_bloon:
                    azimuth_angle_to_send = self.min_bloon[0]
                    pitch_angle_to_send = self.min_bloon[1]

                    # This should be log
                    print("angles to send (azimuth, pitch): ({}, " \
                          "{})".format(azimuth_angle_to_send,
                                       pitch_angle_to_send))

                    # Sends angle to arduino, is the angle is small, gives a
                    #  smaller angle
                    """if 1 < abs(azimuth_angle_to_send) < 3:
                        azimuth_angle_to_send *= 0.25
                    elif 0.1 < abs(azimuth_angle_to_send) < 1:
                        azimuth_angle_to_send =
                        0.2*azimuth_angle_to_send/abs(
                            azimuth_angle_to_send)
                    elif abs(azimuth_angle_to_send) < 0.1:
                        azimuth_angle_to_send = 0
                    if 1 < abs(pitch_angle_to_send) < 3:
                        pitch_angle_to_send *= 0.25
                    elif abs(pitch_angle_to_send) < 1:
                        pitch_angle_to_send = 0.2*pitch_angle_to_send / abs(
                            pitch_angle_to_send)
                            """
                    if 1 <= abs(azimuth_angle_to_send) <= 3:
                        azimuth_angle_to_send *= 0.25
                    elif abs(azimuth_angle_to_send) < 1:
                        azimuth_angle_to_send = 0.2 * azimuth_angle_to_send \
                                                / abs(
                            azimuth_angle_to_send)
                    if 1 <= abs(pitch_angle_to_send) <= 3:
                        pitch_angle_to_send *= 0.25
                    elif abs(pitch_angle_to_send) < 1:
                        pitch_angle_to_send = 0.2 * pitch_angle_to_send / \
                                              abs(
                                                  pitch_angle_to_send)
                    self.azimuth_motor.send(azimuth_angle_to_send, False,
                                            True)
                    self.pitch_motor.send(pitch_angle_to_send, False, True)
                    time.sleep(2)
        if self.is_finished():
            self.kill()

    def is_finished(self):
        """
        Finishes when the the bloon is close enough to the aiming point
        (center of camera) for a certain number of loops
        :return:
        """
        a = self.vision_data.get_can_shoot()
        if len(a) > 0:
            return a[0] == 1
        else:
            return False

    def finish(self):
        """
        Stops motors if they happen to be still turning
        :return:
        """
        # self.azimuth_motor.send(0, False, True)
        # self.pitch_motor.send(0, False, True)

        # Unlocks the motors
        self.azimuth_motor.unlock()
        self.pitch_motor.unlock()
        self.shoot.start()
