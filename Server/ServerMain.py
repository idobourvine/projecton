import time
import Communication.Connection
import Vision_Processing.VisionData

if __name__ == "__main__":
    print("Server running")

    #pi_connection = Communication.Connection.Connection(False)

    #vision_data = Vision_Processing.VisionData.VisionData()

    while True:

        # _bloons = vision_data.get_bloons()
        # _can_shoot = vision_data.get_can_shoot()
        # _did_pop = vision_data.get_did_pop()
        #pi_connection.send_msg("MESSAGEBloonsMSG" + str(_bloons))
        #pi_connection.send_msg("MESSAGECanShootMSG" + str(_can_shoot))
        #pi_connection.send_msg("MESSAGEDidPopMSG" + str(_did_pop))
        # print "sending..."
        time.sleep(0.5)
