import socket
from threading import Thread

import cv2
import numpy

SIZE_LEN = 10

### Error fixing consts ###
REQUEST_SHOT_MSG = "please take photo"
MOVE_MSG = "move"
RIGHT = "0"
LEFT = "1"
CLOSE = "close"

SERVER_IP = '192.168.137.1'
#SERVER_IP = '127.0.0.1'
SUBNET_MASK = '255.255.255.0'
SEND_TIMEOUT = 20.0  # seconds
LISTEN_TIMEOUT = 1000.0
IM_SIZE = 200000
SENDER = True
LISTENER = False
COMP2_PORT = 5050
PI_PORT = 5060

"""
This class provides sender and receiver TCP services,
sender is nonblocking while receiver obviously is.
"""


class LaptopConnection:
    def __init__(self, port=COMP2_PORT):
        while True:
            try:
                self.timeout = SEND_TIMEOUT
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.timeout)
                # print("Connecting ...")
                s.connect((SERVER_IP, port))
                print("Connected to GUI!")
                self.socket = s
                break
            except Exception as e:
                print(e)
                a = 0
                # print("Failed to connect to GUI!")
        self.thread = None

    def send_image(self, img):
        def really_send(img):
            try:
                self.socket.settimeout(SEND_TIMEOUT)
                str_encode = cv2.imencode('.jpg', img)[1].tostring()
                print('sending img message of size ' + str(len(str_encode)))
                self.send_data(str_encode)
            except:
                print("failed to send image <:-(")

        if not self.thread == None:
            self.thread.join()

        self.thread = Thread(target=really_send, args=(img,))
        self.thread.start()

    def send_msg(self, msg):
        def really_send(msg):
            try:
                self.socket.settimeout(SEND_TIMEOUT)
                encoded_msg = msg.encode()
                # print("Sending encoded msg: " + str(encoded_msg))
                self.send_data(encoded_msg)
            except:
                print("failed to send msg <:-(")

        if not self.thread == None:
            self.thread.join()

        self.thread = Thread(target=really_send, args=(msg,))
        self.thread.start()

    def get_image(self):
        self.socket.settimeout(LISTEN_TIMEOUT)
        while True:
            msg = self.get_msg()
            decoded = numpy.fromstring(msg, numpy.uint8)
            img = cv2.imdecode(decoded,
                               cv2.IMREAD_COLOR)
            if not (img is None):
                return img

    def get_msg(self):
        self.socket.settimeout(LISTEN_TIMEOUT)
        while True:
            msg = str(self.recv_data())
            if not (msg is None):
                return msg

    def send_data(self, data):
        datalen = str(len(data)).ljust(SIZE_LEN)
        data_final = datalen.encode() + data
        len_sent = 0
        while len_sent < SIZE_LEN:
            l = self.socket.send((data_final[len_sent:SIZE_LEN]))
            len_sent = len_sent + l

        while len_sent < len(data_final):
            l = self.socket.send((data_final[len_sent:]))
            len_sent = len_sent + l

    def recv_data(self):
        try:
            tmp_data = self.socket.recv(IM_SIZE)

            while len(tmp_data) < SIZE_LEN:
                tmp_data = tmp_data + self.socket.recv(IM_SIZE)

            msg_size = int(tmp_data[0:SIZE_LEN].decode()) + SIZE_LEN
            while len(tmp_data) < msg_size:
                tmp_data = tmp_data + self.socket.recv(IM_SIZE)

            return tmp_data[SIZE_LEN:]
        except UnicodeDecodeError as e:
            return None
        except ValueError as e:
            return None
