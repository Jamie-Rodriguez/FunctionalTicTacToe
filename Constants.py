#!/usr/bin/env python3
from enum import Enum

BOARD_WIDTH = 3
BOARD_HEIGHT = 3


class Agent(Enum):
    HUMAN, AI, RANDOM = range(0, 3)


# Values are used when printing the board state to the console
class Square(Enum):
    EMPTY = " "
    O = "O"
    X = "X"
