import enum


class Result(enum.IntEnum):
    OKEY = 0,
    BAD_COMMAND = 1,
    RESOURCE_NOT_FOUND = 2,
    ACCESS_DENIED = 3,
    NOT_READY = 4,
    TIMEOUT = 5,
    INTERNAL_SERVER_ERROR = 500