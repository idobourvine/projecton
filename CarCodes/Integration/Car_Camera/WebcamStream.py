import Queue
from threading import Thread
from Utils.Constants import *
import cv2


class WebcamStream:
    def __init__(self, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        if Constants.use_devices:
            self.stream = cv2.VideoCapture(0)

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

            if Constants.use_devices:
                (grabbed, frame) = self.stream.read()
                # print("Read frame")
            else:
                frame = cv2.imread("1.jpg")

            if self.Q.full():
                # read the next frame from the file
                self.Q.get()
            self.Q.put(frame)

    def read(self):
        # return next frame in the queue
        return self.Q.get()

    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
