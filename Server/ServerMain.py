import re
import time

import keyboard

import BlochsCode.SecurityVisionData
import Communication.Connection
import Vision_Processing.CarVisionData

if __name__ == "__main__":
    print("Server running")

    msg_pattern = re.compile("(^\w*MSG)")
    useless_number_pattern = re.compile("(\d+$)")

    # Booleans that decide if we process the images
    process_car_vision = True
    process_security_vision = True

    pi_connection = Communication.Connection.Connection(False)

    car_vision_data = Vision_Processing.CarVisionData.CarVisionData(
        pi_connection)

    security_vision_data = BlochsCode.SecurityVisionData.SecurityVisionData()

    pressed_hotkey = False  # flag if hotkey of ctrl+enter was pressed
    car_working = True
    def update_pressed_hotkey(self):
        """
        Function that is called by keyboard to update the flag if the hotkey
        was pressed
        """
        global pressed_hotkey
        pressed_hotkey = True

    keyboard.add_hotkey('ctrl+enter', update_pressed_hotkey)
    # Starts tracking if hotkey was pressed

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

        car_bloons = car_vision_data.get_bloons()

        # print("Car Bloons: ")
        # print(car_bloons)

        can_shoot = car_vision_data.get_can_shoot()
        did_pop = car_vision_data.get_did_pop()

        room_bloons = security_vision_data.get_bloons()
        print "Room bloons:"
        print room_bloons

        continue_mission = len(room_bloons) > 0

        if pressed_hotkey:
            pressed_hotkey = False
            car_working = not car_working

        pi_connection.send_msg("MESSAGECarBloonsMSG" + str(car_bloons))
        pi_connection.send_msg("MESSAGECanShootMSG" + str(can_shoot))
        pi_connection.send_msg("MESSAGEDidPopMSG" + str(did_pop))
        pi_connection.send_msg("MESSAGERoomBloonsMSG" + str(room_bloons))
        pi_connection.send_msg(
            "MESSAGEContinueMissionMSG" + str(continue_mission))
        pi_connection.send_msg("MESSAGECarWorkingMSG" + str(car_working))
        # print "sending..."

        time.sleep(0.5)
