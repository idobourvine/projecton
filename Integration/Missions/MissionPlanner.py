import keyboard

import ClearRoom
from NumberedMission import NumberedMission
from SeriesMission import SeriesMission
from ParallelMission import ParallelMission

class MissionPlanner:
    def __init__(self):
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
        Decides if new missions are to be taken ou
        t each iteration
        """
        if self.pressed_hotkey:
            print("Initiated mission")
            self.pressed_hotkey = False

            """
            aim = ClearRoom.ClearRoom([[-65, 0], [-65, 35], [-85, 5], [-105,
                                                                       0]])
            # aim = ClearRoom.ClearRoom([[-70, 0], [-100, 0], [-86, 0]])
            aim.start()
            """
