import Queue
from threading import Thread

import cv2


class PiStream:
    def __init__(self, connection, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.connection = connection
        self.stopped = False

        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue.Queue(maxsize=queueSize)

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return

            frame = self.connection.get_image()

            if self.Q.full():
                # read the next frame from the file
                self.Q.get()
            self.Q.put(frame)

    def read(self):
        # return next frame in the queue
        return self.Q.queue[0]

    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
