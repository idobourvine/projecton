import keyboard

import ClearRoom

class MissionPlanner:
    def __init__(self, device_map, vision_data):
        self.device_map = device_map
        self.vision_data = vision_data

        self.pressed_hotkey = False  # flag if hotkey of ctrl+enter was pressed

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
        if self.vision_data.continue_mission():
            if self.pressed_hotkey:
                print("Initiated mission")
                self.pressed_hotkey = False

                aim = ClearRoom.ClearRoom([[-65, 0], [-65, 35], [-85, 5],
                                           [-105, 0]])
                # aim = ClearRoom.ClearRoom([[-70, 0], [-100, 0], [-86, 0]])
                aim.start()
