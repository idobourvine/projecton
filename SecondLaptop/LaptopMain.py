import re
import time

import keyboard

import BlochsCode.SecurityVisionData
import Communication.LaptopConnection

if __name__ == "__main__":
    print("Laptop running")

    msg_pattern = re.compile("(^\w*MSG)")
    useless_number_pattern = re.compile("(\d+$)")

    # Booleans that decide if we process the images
    process_security_vision = True

    connection = Communication.LaptopConnection.LaptopConnection()

    if process_security_vision:
        security_vision_data = BlochsCode.SecurityVisionData.SecurityVisionData()

    pressed_hotkey = False  # flag if hotkey of ctrl+enter was pressed


    def update_pressed_hotkey():
        """
        Function that is called by keyboard to update the flag if the hotkey
        was pressed
        """
        global pressed_hotkey
        pressed_hotkey = True


    keyboard.add_hotkey('ctrl+enter', update_pressed_hotkey)
    # Starts tracking if hotkey was pressed

    safety_stopped = False

    while True:

        '''Sending messages'''

        if process_security_vision:
            room_bloons = security_vision_data.get_bloons()
            print "Room bloons:"
            print room_bloons

            connection.send_msg("MESSAGERoomBloons2MSG" + str(room_bloons))

        if pressed_hotkey:
            print("Changing safety stop to " + str(not safety_stopped))
            pressed_hotkey = False
            safety_stopped = not safety_stopped

        connection.send_msg("MESSAGESafetyStopped2MSG" + str(safety_stopped))
        # print "sending..."

        time.sleep(0.2)
