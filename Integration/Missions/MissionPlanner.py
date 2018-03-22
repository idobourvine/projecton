# import keyboard

import time
import Test
import ClearStandpoint


class MissionPlanner:
    def __init__(self, device_map):
        self.device_map = device_map

        # self.pressed_hotkey = False  # flag if hotkey of ctrl+enter was pressed
        self.current_mission = None
        """
        def update_pressed_hotkey():
        """
        """
            Function that is called by keyboard to update the flag if the hotkey
            was pressed
        """
        """
            self.pressed_hotkey = True
        """
        # keyboard.add_hotkey('ctrl+enter', update_pressed_hotkey)
        # Starts tracking if hotkey was pressed

    def manage_missions(self):
        """
        Decides if new missions are to be taken out each iteration
        """
        # Before starting the first mission, waits some time for
        # system initialization to take place
        if not self.current_mission:
            time.sleep(10)

        if not self.current_mission or \
                self.current_mission.finished_called_since_start():
            if self.device_map.vision_data.continue_mission():
                # if self.pressed_hotkey:

                # print("Initiated new mission in mission manager")

                # self.pressed_hotkey = False

                # self.current_mission.start()
                self.current_mission = Test.Test(self.device_map)
                self.current_mission.start()

    def return_next_mission(self, device_map):
        mis = ClearStandpoint.ClearStandpoint(device_map, [[-65, 0], [-65, 35],
                                                           [-85, 5],
                                                           [-105, 0]])
        return mis
