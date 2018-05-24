#!/usr/bin/env python3
from Constants import *

"""
    Coordinate system for grid of size 3:

     0 | 1 | 2
    ---+---+---
     3 | 4 | 5
    ---+---+---
     6 | 7 | 8
"""


def getRowNum(index):
    return index // BOARD_SIZE


def getColNum(index):
    return index % BOARD_SIZE


"""
    IMPORTANT NOTE
    The next________Index() functions wrap around the edges of the board
    
    i.e. on a grid of size 3:
        nextIndexInRow(5) = 3
        nextIndexInColumn(7) = 1
        nextIndexInDiagonal(8) = 0
        nextIndexInAntiDiagonal(6) = 2
"""


def nextIndexInRow(currentIndex):
    rowNum = getRowNum(currentIndex)
    nextIndex = currentIndex + 1

    if getRowNum(nextIndex) != rowNum:
        nextIndex -= BOARD_SIZE

    return nextIndex


def nextIndexInColumn(currentIndex):
    nextIndex = currentIndex + BOARD_SIZE

    if nextIndex > MAX_INDEX:
        nextIndex -= MAX_INDEX + 1

    return nextIndex


def nextIndexInDiagonal(currentIndex):
    # Right-most column
    if (currentIndex + 1) % BOARD_SIZE == 0:
        nextIndex = -1 * (currentIndex + 1) // BOARD_SIZE + BOARD_SIZE
    # Bottom row, excluding bottom-right corner (because of previous if-statement)
    elif currentIndex >= BOARD_SIZE * (BOARD_SIZE - 1):
        nextIndex = -1 * BOARD_SIZE * (currentIndex - BOARD_SIZE ** 2 + 1)
    else:
        nextIndex = currentIndex + BOARD_SIZE + 1

    return nextIndex


def nextIndexInAntiDiagonal(currentIndex):
    # Left-most column
    if currentIndex % BOARD_SIZE == 0:
        nextIndex = currentIndex // BOARD_SIZE
    # Bottom row, excluding bottom-left corner (because of previous if-statement)
    elif currentIndex >= BOARD_SIZE * (BOARD_SIZE - 1) + 1:
        nextIndex = BOARD_SIZE * currentIndex - (BOARD_SIZE + 1) * (BOARD_SIZE - 1) ** 2
    else:
        nextIndex = currentIndex + BOARD_SIZE - 1

    return nextIndex
