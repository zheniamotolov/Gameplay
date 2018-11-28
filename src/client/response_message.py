class ResponseMessage:
    def __init__(self, result_code=None, data_length=None, data=None):
        self.__result_code = result_code
        self.__data_length = data_length
        self.__data = data

    @property
    def result_code(self):
        return self.__result_code

    @result_code.setter
    def result_code(self, result_code):
        self.__result_code = result_code

    @property
    def data_length(self):
        return self.__data_length

    @data_length.setter
    def data_length(self, data_length):
        self.__data_length = data_length

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data
