import json
import socket
import struct
from json import dumps

from src.client.action_message import ActionMessage
from src.client.config import *
from src.client.response_message import ResponseMessage
from src.client.result import Result
from src.constants import BYTES_SIZE


class Client:
    def __init__(self, username=None, password=None):
        self.host = HOST_NAME
        self.port = PORT
        self.timeout = 5

        if username is None or password is None:
            self.username = USERNAME
            self.password = PASSWORD
        else:
            self.username = username
            self.password = password
        self.connection = None

    def make_request(self, action):
        request_message = action.action_code + action.data_length + action.data
        self.connection.send(request_message)

    def receive_data(self):
        response_message = ResponseMessage()
        result_code = struct.unpack('<i', self.connection.recv(BYTES_SIZE))[0]
        if result_code != 0:
            pass
        response_message.result_code = result_code
        response_message.data_length = struct.unpack('<i', self.connection.recv(BYTES_SIZE))[0]
        data = self.connection.recv(response_message.data_length)
        while len(data) < response_message.data_length:
            data += self.connection.recv(response_message.data_length)
        data = data.decode('utf8').replace("\n", '').replace(" ", '')
        data = json.loads(data)
        response_message.data = data
        return response_message

    def login(self, password=None, num_players=None, game=None):
        self.connection = socket.create_connection((self.host, self.port), self.timeout)
        data = {'name': self.username}
        if password is not None:
            data['password'] = password
        if num_players is not None:
            data['num_players'] = num_players
        if game is not None:
            data['game'] = game
        action_code = 1
        action = ActionMessage(action_code.to_bytes(BYTES_SIZE, byteorder='little'),
                               len(dumps(data)).to_bytes(BYTES_SIZE, byteorder='little'),
                               dumps(data).encode())
        self.make_request(action)
        print(self.receive_data().data)

    def move(self, line_idx, speed, train_idx):
        action_code = 3
        data = {'line_idx': line_idx, 'speed': speed, 'train_idx': train_idx}
        action = ActionMessage(action_code.to_bytes(BYTES_SIZE, byteorder='little'),
                               len(dumps(data)).to_bytes(BYTES_SIZE, byteorder='little'),
                               dumps(data).encode())
        self.make_request(action)
        return self.receive_data()

    def player(self):
        action_code = 6
        data=''
        action = ActionMessage(action_code.to_bytes(BYTES_SIZE, byteorder='little'),
                               len(dumps(data)).to_bytes(BYTES_SIZE, byteorder='little'),
                               dumps(data).encode())
        self.make_request(action)
        return self.receive_data()

    def turn(self):
        action_code = 5
        data = ''
        action = ActionMessage(action_code.to_bytes(BYTES_SIZE, byteorder='little'),
                               len(dumps(data)).to_bytes(BYTES_SIZE, byteorder='little'),
                               dumps(data).encode())
        self.make_request(action)
        return self.receive_data()
