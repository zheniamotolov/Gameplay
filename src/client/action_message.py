class ActionMessage:
    def __init__(self, action_code, data_length, data):
        self.action_code = action_code
        self.data_length = data_length
        self.data = data
