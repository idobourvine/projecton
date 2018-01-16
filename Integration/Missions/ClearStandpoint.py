"""
Mission that destroys all balloons from an array
"""
import sys

import AimAtBalloonInPictureMission
import MoveTurretToAngle
import SeriesMission

sys.path.append('..')


class ClearStandpoint(SeriesMission.SeriesMission):
    def __init__(self, balloons):
        SeriesMission.SeriesMission.__init__(self, list())
        self.bloons = balloons
        self.init_missions_list(self.bloons)

    def init_missions_list(self, balloons):
        self.missions = list()
        for balloon in balloons:
            self.missions.append(
                MoveTurretToAngle.MoveTurretToAngle(balloon[0], balloon[1]))
            self.missions.append(
                AimAtBalloonInPictureMission.AimAtBalloonInPictureMission())


"""
    def initialize(self):
        self.azimuth_motor.send(self.bloons[self.index][0], False, False)
        self.pitch_motor.send(self.bloons[self.index][1], False, False)
        time.sleep(3)
        self.aim = AimAtBalloonInPictureMission()
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
                    AimAtBalloonInPictureMission.AimAtBalloonInPictureMission()
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
