#!/usr/bin/env python3
import math

"""
    Coordinate system for grid of size 3:

     0 | 1 | 2
    ---+---+---
     3 | 4 | 5
    ---+---+---
     6 | 7 | 8
"""

def getMaxIndex(width, height):
    return width * height - 1


def getRowNum(width, index):
    return math.floor(index / width)


def getColNum(width, index):
    return index % width


def isLeftColumn(width, index):
    return index % width == 0


def isRightColumn(width, index):
    return isLeftColumn(width, index + 1)


def isBottomRow(width, height, index):
    return width * (height - 1) <= index and index < width * height

"""
    IMPORTANT NOTE
    The next________Index() functions wrap around the edges of the board

    i.e. on a grid of size 3:
        nextIndexInRow(5) = 3
        nextIndexInColumn(7) = 1
        nextIndexInDiagonal(8) = 0
        nextIndexInAntiDiagonal(6) = 2
"""


# NOTE: height is not used
# but requires the same signature as the nextIndexIn____ functions
def nextIndexInRow(w, h, i):
    rowNum = getRowNum(w, i)
    nextIndex = i + 1

    if getRowNum(w, nextIndex) != rowNum:
        nextIndex -= w

    return nextIndex


def nextIndexInColumn(w, h, i):
    maxIndex = getMaxIndex(w, h)
    nextIndex = i + w

    if nextIndex > maxIndex:
        nextIndex -= maxIndex + 1

    return nextIndex


def nextIndexInDiagonal(w, h, i):
    if isRightColumn(w, i):
        if i <= (w+1)*(w-1):
            nextIndex = int((1/w) * (-i + pow(w, 2) - 1))
        else: # w < h
            nextIndex = i - (pow(w, 2) - 1)
    elif isBottomRow(w, h, i):
        if i <= (w+1)*(h-1):
            nextIndex = w * (-i + (w+1)*(h-1))
        else: # w > h
            nextIndex = i - (w+1)*(h-1)
    else:
        nextIndex = i + w + 1

    return nextIndex


def nextIndexInAntiDiagonal(w, h, i):
    if isLeftColumn(w, i):
        if i <= w*(w-1):
            nextIndex = int(i/w)
        else: # w < h
            nextIndex = i - pow(w-1, 2)
    elif isBottomRow(w, h, i):
        if i >= h*(w-1):
            nextIndex = w*i - (w-1)*(w*h - 1)
        else: # w > h
            nextIndex = i - (w-1)*(h-1)
    else:
        nextIndex = i + w - 1

    return nextIndex
