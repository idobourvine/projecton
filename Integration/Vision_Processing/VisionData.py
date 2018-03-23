import threading
import time
import WebcamStream
import cv2

class VisionData:
    """
    Wrapper class for the data that comes from vision processing
    """
    def __init__(self, connection):
        self.bloons = []  # Array of balloons detected by vision processing
        self.can_shoot = [0]
        self.did_pop = [0]

        self.stream = WebcamStream.WebcamStream(queueSize=2).start()

        self.connection = connection

        self.eg1 = threading.Thread(target=self.manage_connection,
                                    args=(self.connection, self.stream,
                                          self.bloons,
                                          self.can_shoot,
                                          self.did_pop))  # Thread that runs
        self.eg1.start()

    def get_bloons(self):
        return self.bloons[:]

    def get_can_shoot(self):
        return self.can_shoot[:]

    def get_did_pop(self):
        return self.did_pop[:]

    def continue_mission(self):
        """
        Should return whether there are more balloons to pop in the room
        :return:
        """
        return True

    def manage_connection(self, connection, stream, bloons, can_shoot,
                          did_pop):
        time.sleep(5)
        
        while True:
            if stream.more():
                next_img = stream.read()
                cv2.imshow('Kavitz', next_img)
                connection.send_image(next_img)
                cv2.waitKey(50)
