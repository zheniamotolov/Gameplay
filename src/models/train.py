import enum


class MoveDirection(enum.IntEnum):
    BACKWARD = -1
    NEITHER = 0
    FORWARD = 1


class Train:
    def __init__(self, idx, line_idx, player_idx, position, speed):
        self.idx = idx
        self.line_idx = line_idx
        self.player_idx = player_idx
        self.position = position
        self.speed = speed

    def move(self, direction, line_idx=None):
        self.speed = direction
        if line_idx is not None:
            self.line_idx = line_idx
