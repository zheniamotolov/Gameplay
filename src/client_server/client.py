from src.client_server.config import *
from src.client_server.result import Result
from tornado.websocket import WebSocketHandler

class Response:
    def __init__(self, status, length, data):
        self.status = Result.STATUS[status]
        self.length = length
        self.data = data if data != '' else ''


class Client:
    def __init__(self, username=None, password=None):
        self.host = HOST_NAME
        self.port = PORT
        if username is None or password is None:
            username = USERNAME
            password = PASSWORD
