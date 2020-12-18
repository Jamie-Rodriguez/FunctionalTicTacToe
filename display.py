#!/usr/bin/env python3
import os


"""
    NOTE: If planning to use BOARD_SIZE > 3, need to adjust printing functions
    used in printHelpGraphic() to account for two (and three?) digit display of
    indexes
"""


def clearConsole():
    if os.name == "posix": # Unix/Linux/MacOS/BSD/etc
        os.system("clear")
    elif os.name in ("nt", "dos", "ce"): # DOS/Windows
        os.system('CLS')
    else: # Other??
        print('\n' * 1000)


def printBoard(board, boardWidth, boardHeight):
    rowNum = 0

    row = __getRow(boardWidth, rowNum, board)

    __printRow(row)
    rowNum += 1

    while rowNum < boardHeight:
        row = __getRow(boardWidth, rowNum, board)

        __printRowSeparator(boardWidth)
        __printRow(row)

        rowNum += 1


def printHelpGraphic(boardWidth, boardHeight):
    print("Enter number to place your move:")
    __helpGraphic(boardWidth, boardHeight - 1)
    print("\n")


# ----------------------------- Private Functions ------------------------------


def __getStartIndexOfRow(boardWidth, rowNum):
    return rowNum * boardWidth


def __getEndIndexOfRow(boardWidth, rowNum):
    return __getStartIndexOfRow(rowNum, boardWidth) + boardWidth - 1


def __getRow(boardWidth, rowNum, board):
    start = __getStartIndexOfRow(boardWidth, rowNum)
    end = __getEndIndexOfRow(boardWidth, rowNum)
    # Slicing in python is over the interval [start, end)
    row = board[start: end + 1]

    return row


def __printRow(row):
    for r in row[:-1]:
        print(" {} |".format(r.value), end="")
    print(" {} ".format(row[-1].value))


def __printRowSeparator(boardWidth):
    for i in range(0, boardWidth - 1):
        print("---+", end="")
    print("---")


def __helpGraphic(boardWidth, rowNum):
    start = __getStartIndexOfRow(boardWidth, rowNum)
    end = __getEndIndexOfRow(boardWidth, rowNum)

    if rowNum == 0:
        __printRowWithIndexes(start, end)
        return
    else:
        __helpGraphic(boardWidth, rowNum - 1)
        __printRowSeparator(boardWidth)
        __printRowWithIndexes(start, end)


def __printRowWithIndexes(start, end):
    for i in range(start, end):
        print(" {} |".format(i), end="")
    print(" {} ".format(i + 1))
