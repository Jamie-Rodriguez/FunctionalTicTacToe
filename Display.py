#!/usr/bin/env python3
import os
from Constants import BOARD_SIZE

"""
    NOTE: If planning to use BOARD_SIZE > 3, need to adjust printing functions
    used in printHelpGraphic() to account for two (and three?) digit display of
    indexes
"""


def clearConsole():
    if os.name == "posix":  # Unix/Linux/MacOS/BSD/etc
        os.system("clear")
    elif os.name in ("nt", "dos", "ce"):  # DOS/Windows
        os.system('CLS')
    else:  # Other??
        print('\n' * 1000)


def printBoard(board):
    rowNum = 0

    row = __getRow(board, rowNum)

    __printRow(row)
    rowNum += 1

    while rowNum < BOARD_SIZE:
        row = __getRow(board, rowNum)

        __printRowSeparator()
        __printRow(row)

        rowNum += 1


def printHelpGraphic():
    print("Enter number to place your move:")
    __helpGraphic(BOARD_SIZE - 1)
    print("\n")


# ----------------------------- Private Functions ------------------------------


def __getRow(board, rowNum):
    start = rowNum * BOARD_SIZE
    end = (rowNum + 1) * BOARD_SIZE - 1
    # Slicing in python is over the interval [start, end)
    row = board[start: end + 1]

    return row


def __printRow(row):
    for r in row[:-1]:
        print(" {} |".format(r.value), end="")
    print(" {} ".format(row[-1].value))


def __printRowSeparator():
    for i in range(0, BOARD_SIZE - 1):
        print("---+", end="")
    print("---")


def __helpGraphic(rowNum):
    start = rowNum * BOARD_SIZE
    end = start + BOARD_SIZE - 1

    if rowNum == 0:
        __printRowWithIndexes(start, end)
        return
    else:
        __helpGraphic(rowNum - 1)
        __printRowSeparator()
        __printRowWithIndexes(start, end)


def __printRowWithIndexes(start, end):
    for i in range(start, end):
        print(" {} |".format(i), end="")
    print(" {} ".format(i + 1))
