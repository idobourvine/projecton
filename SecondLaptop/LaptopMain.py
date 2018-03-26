import re
import time

import keyboard

import BlochsCode.SecurityVisionData
import Communication.Connection

if __name__ == "__main__":
    print("Server running")

    msg_pattern = re.compile("(^\w*MSG)")
    useless_number_pattern = re.compile("(\d+$)")

    # Booleans that decide if we process the images
    process_security_vision = True

    connection = Communication.Connection.Connection(True)

    security_vision_data = BlochsCode.SecurityVisionData.SecurityVisionData()

    def update_pressed_hotkey(self):
        """
        Function that is called by keyboard to update the flag if the hotkey
        was pressed
        """
        pressed_hotkey = True


    pressed_hotkey = False  # flag if hotkey of ctrl+enter was pressed
    keyboard.add_hotkey('ctrl+enter', update_pressed_hotkey)
    # Starts tracking if hotkey was pressed

    safety_stopped = False

    while True:

        '''Recieving messages'''

        # Currently not working as it is interfering with received images
        '''
        try:
            msg = pi_connection.get_msg()
            if not msg:
                continue

            print("Recieved msg: " + msg)

            messages = msg.split('MESSAGE')
            for real_msg in messages:
                if real_msg == '':
                    continue

                stripped = real_msg.strip()
                removed_useless_num = useless_number_pattern.sub(
                    '', stripped)

                split = msg_pattern.split(removed_useless_num, 1)

                if not split:
                    continue

                msg_type = split[1]
                raw_msg = split[2]
                data = ast.literal_eval(raw_msg)

                if msg_type == "ProcessCarVisionMSG":
                    process_car_vision = data
                    print("Data from pi: process car vision: " + str(data))

                elif msg_type == "ProcessSecurityVisionMSG":
                    process_security_vision = data
                    print("Data from pi: process security vision: " + str(
                        data))
                    security_vision_data.set_working(data)

        except Exception as e:
            print("EXCEPTION CAUGHT")
            print(str(e))
        '''

        '''Sending messages'''

        room_bloons = security_vision_data.get_bloons()
        print "Room bloons:"
        print room_bloons

        if pressed_hotkey:
            pressed_hotkey = False
            safety_stopped = not safety_stopped

        connection.send_msg("MESSAGERoomBloonsMSG" + str(room_bloons))
        connection.send_msg("MESSAGESafetyStoppedMSG" + str(safety_stopped))
        # print "sending..."

        time.sleep(0.5)
