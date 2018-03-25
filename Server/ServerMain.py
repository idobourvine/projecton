import time

import Communication.Connection
import Vision_Processing.CarVisionData
import BlochsCode.SecurityVisionData

if __name__ == "__main__":
    print("Server running")

    pi_connection = Communication.Connection.Connection(False)

    car_vision_data = Vision_Processing.CarVisionData.CarVisionData(pi_connection)

    security_vision_data = BlochsCode.SecurityVisionData.SecurityVisionData()

    while True:
        car_bloons = car_vision_data.get_bloons()
        can_shoot = car_vision_data.get_can_shoot()
        did_pop = car_vision_data.get_did_pop()

        room_bloons = security_vision_data.get_bloons()
        print("Room Bloons:")
        print(room_bloons)

        continue_mission = len(room_bloons) > 0

        pi_connection.send_msg("MESSAGEBCarBloonsMSG" + str(car_bloons))
        pi_connection.send_msg("MESSAGEBCanShootMSG" + str(can_shoot))
        pi_connection.send_msg("MESSAGEBDidPopMSG" + str(did_pop))
        pi_connection.send_msg("MESSAGEBRoomBloonsMSG" + str(room_bloons))
        pi_connection.send_msg("MESSAGEBContinueMissionMSG" + str(continue_mission))
        # print "sending..."
        time.sleep(0.5)
