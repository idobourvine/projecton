import select, socket, sys, Queue
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

LAPTOP_IP = '192.168.137.1'
SUBNET_MASK = '255.255.255.0'
SEND_TIMEOUT = 20.0  # seconds
LISTEN_TIMEOUT = 1000.0
IM_SIZE = 8192000
SENDER = True
LISTENER = False
PORT = 5000

"""
This class provides sender and receiver TCP services,
sender is nonblocking while receiver obviously is.
"""

class ServerConnection:
    def __init__(self, port=PORT):
        while True:
            try:
                ## fix ip ##
                # call("netsh interface ip set address name=\"Wireless "
                #      "Network"
                #      "Connection 2\" static " +LAPTOP_IP + " " +
                #      SUBNET_MASK + " " + GATEWAY)
                self.timeout = LISTEN_TIMEOUT

                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                server.setblocking(0)
                server.bind(("", port))

                self.sock = server
                self.sock.settimeout(self.timeout)
                self.sock.listen(1)

                print "listening"

                self.inputs = [server]
                self.outputs = []
                self.message_queues = {}

                while self.inputs:
                    readable, writable, exceptional = select.select(
                        self.inputs, self.outputs, self.inputs)
                    for s in readable:
                        if s is server:
                            connection, client_address = s.accept()
                            print("Successfully connected to address: ",
                                  client_address)

                            connection.setblocking(0)

                            self.inputs.append(connection)
                            self.message_queues[connection] = Queue.Queue()
                        else:
                            data = s.recv(1024)
                            if data:
                                self.message_queues[s].put(data)
                                if s not in self.outputs:
                                    self.outputs.append(s)
                            else:
                                if s in self.outputs:
                                    self.outputs.remove(s)
                                    self.inputs.remove(s)
                                s.close()
                                del self.message_queues[s]

                    for s in writable:
                        try:
                            next_msg = self.message_queues[s].get_nowait()
                        except Queue.Empty:
                            self.outputs.remove(s)
                        else:
                            s.send(next_msg)

                    for s in exceptional:
                        self.inputs.remove(s)
                        if s in self.outputs:
                            self.outputs.remove(s)
                        s.close()
                        del self.message_queues[s]

                break
            except:
                a = 0
                # print("Failed to connect to GUI!")
        self.thread = None

    def send_image(self, param_socket, img):
        def really_send(img):
            try:
                param_socket.settimeout(SEND_TIMEOUT)
                str_encode = cv2.imencode('.jpg', img)[1].tostring()
                print('sending img message of size ' + str(len(str_encode)))
                self.send_data(param_socket, str_encode)
            except:
                print("failed to send image <:-(")

        if not self.thread == None:
            self.thread.join()

        self.thread = Thread(target=really_send, args=(img,))
        self.thread.start()

    def send_msg(self, param_socket, msg):
        def really_send(msg):
            try:
                param_socket.settimeout(SEND_TIMEOUT)
                encoded_msg = msg.encode()
                # print("Sending encoded msg: " + str(encoded_msg))
                self.send_data(param_socket, encoded_msg)
            except:
                print("failed to send msg <:-(")

        if not self.thread == None:
            self.thread.join()

        self.thread = Thread(target=really_send, args=(msg,))
        self.thread.start()

    def get_image(self, param_socket):
        param_socket.settimeout(LISTEN_TIMEOUT)
        while True:
            msg = self.get_msg(param_socket)
            decoded = numpy.fromstring(msg, numpy.uint8)
            img = cv2.imdecode(decoded,
                               cv2.IMREAD_COLOR)
            if not (img is None):
                return img

    def get_msg(self, param_socket):
        param_socket.settimeout(LISTEN_TIMEOUT)
        while True:
            msg = str(self.recv_data())
            if not (msg is None):
                return msg

    def send_data(self, param_socket, data):
        datalen = str(len(data)).ljust(SIZE_LEN)
        data_final = datalen.encode() + data
        len_sent = 0
        while len_sent < SIZE_LEN:
            l = param_socket.send((data_final[len_sent:SIZE_LEN]))
            len_sent = len_sent + l

        while len_sent < len(data_final):
            l = param_socket.send((data_final[len_sent:]))
            len_sent = len_sent + l

    def recv_data(self, param_socket):
        try:
            tmp_data = param_socket.recv(IM_SIZE)

            while len(tmp_data) < SIZE_LEN:
                tmp_data = tmp_data + param_socket.recv(IM_SIZE)

            msg_size = int(tmp_data[0:SIZE_LEN].decode()) + SIZE_LEN
            while len(tmp_data) < msg_size:
                tmp_data = tmp_data + param_socket.recv(IM_SIZE)

            return tmp_data[SIZE_LEN:]
        except UnicodeDecodeError as e:
            return None
        except ValueError as e:
            return None
