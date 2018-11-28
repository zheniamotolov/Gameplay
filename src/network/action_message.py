import json
import struct


class ActionMessage:
    def __init__(self, action, data=None):
        self.action = action
        self.data = data

    def pack(self):
        if self.data is None:
            json_data = b''
        else:
            json_data = json.dumps(self.data, separators=(',', ':')).encode()

        json_data_len = struct.pack('<i', len(json_data))

        action_code = struct.pack('<i', self.action)
        message = action_code + json_data_len + json_data

        return message
