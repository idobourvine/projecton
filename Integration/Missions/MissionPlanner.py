import keyboard

import ClearStandpoint


class MissionPlanner:
    def __init__(self, device_map, vision_data):
        self.device_map = device_map
        self.vision_data = vision_data

        self.pressed_hotkey = False  # flag if hotkey of ctrl+enter was pressed
        self.current_mission = None

        def update_pressed_hotkey():
            """
            Function that is called by keyboard to update the flag if the hotkey
            was pressed
            """
            self.pressed_hotkey = True

        keyboard.add_hotkey('ctrl+enter', update_pressed_hotkey)
        # Starts tracking if hotkey was pressed

    def manage_missions(self):
        """
        Decides if new missions are to be taken out each iteration
        """
        if self.current_mission and \
                self.current_mission.finished_called_since_start():
            if self.vision_data.continue_mission():
                # if self.pressed_hotkey:
                print("Initiated new mission in mission manager")
                # self.pressed_hotkey = False

                self.current_mission = self.return_next_mission()
                self.current_mission.start()

    def return_next_mission(self):
        mis = ClearStandpoint.ClearStandpoint([[-65, 0], [-65, 35], [-85, 5],
                                               [-105, 0]])
        return mis
