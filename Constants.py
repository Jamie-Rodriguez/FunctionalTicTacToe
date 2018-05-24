#!/usr/bin/env python3
from enum import Enum

BOARD_SIZE = 3
MAX_INDEX = BOARD_SIZE ** 2 - 1


class Agent(Enum):
    # Don't care about values...
    HUMAN, AI, RANDOM = range(0, 3)


# Values are used in printing the board state to the console
class Square(Enum):
    EMPTY = " "
    O = "O"
    X = "X"
