import time

import Communication.Connection
import Vision_Processing.CarVisionData

if __name__ == "__main__":
    print("Server running")

    pi_connection = Communication.Connection.Connection(False)

    car_vision_data = Vision_Processing.CarVisionData.CarVisionData(pi_connection)



    while True:
        _bloons = car_vision_data.get_bloons()
        _can_shoot = car_vision_data.get_can_shoot()
        _did_pop = car_vision_data.get_did_pop()

        pi_connection.send_msg("BloonsMSG" + str(_bloons))
        pi_connection.send_msg("CanShootMSG" + str(_can_shoot))
        pi_connection.send_msg("DidPopMSG" + str(_did_pop))
        # print "sending..."
        time.sleep(0.5)
