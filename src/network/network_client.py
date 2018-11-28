import asyncio
import functools
import json
import struct

from action import Action
from action_message import ActionMessage
from result import Result
from response_message import ResponseMessage


def request(func):
    @functools.wraps(func)
    async def wrapper_request(self, *args, **kwargs):
        message = await func(self, *args, **kwargs)

        await self.write_message(message)
        response_message = await self.read_message()

        return response_message
    return wrapper_request


def disconnect(func):
    @functools.wraps(func)
    async def wrapper_disconnect(self, *args, **kwargs):
        value = await func(self, *args, **kwargs)

        self.writer.close()
        await self.writer.wait_closed()

        return value
    return wrapper_disconnect


class NetworkClient:
    SERVER_HOST = 'wgforge-srv.wargaming.net'
    SERVER_PORT = 443

    def __init__(self):
        self.writer = None
        self.reader = None

    async def write_message(self, message):
        self.writer.write(message.pack())
        await self.writer.drain()

    async def read_message(self):
        result_code = struct.unpack(
            '<i', await self.reader.readexactly(4))[0]
        json_data_len = struct.unpack(
            '<i', await self.reader.readexactly(4))[0]

        if json_data_len == 0:
            data = None
        else:
            json_data = await self.reader.readexactly(json_data_len)
            data = json.loads(json_data)

        return ResponseMessage(Result(result_code), data)

    async def login(self, username, password=None):
        self.reader, self.writer = await asyncio.open_connection(
            self.SERVER_HOST, self.SERVER_PORT)

        message_data = {'name': username}

        if password is not None:
            message_data['password'] = password

        request_message = ActionMessage(Action.LOGIN, message_data)
        await self.write_message(request_message)

        response_message = await self.read_message()
        return response_message

    @disconnect
    @request
    async def logout(self):
        return ActionMessage(Action.LOGOUT)

    @request
    async def move_train(self, line_idx, speed, train_idx):
        return ActionMessage(
            Action.UPGRADE,
            {'line_idx': line_idx, 'speed': speed, 'train_idx': train_idx})

    @request
    async def upgrade_objects(self, posts, trains):
        return ActionMessage(
            Action.UPGRADE, {'posts': posts, 'trains': trains})

    @request
    async def force_next_turn(self):
        return ActionMessage(Action.TURN)

    @request
    async def get_player_info(self):
        return ActionMessage(Action.PLAYER)

    @request
    async def get_static_objects(self):
        return ActionMessage(Action.MAP, {'layer': 0})

    @request
    async def get_dynamic_objects(self):
        return ActionMessage(Action.MAP, {'layer': 1})
