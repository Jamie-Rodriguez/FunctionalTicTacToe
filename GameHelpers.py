#!/usr/bin/env python3
from Coordinates import *


def placePiece(board, index, piece):
    # deep copy list
    newBoard = list(board)

    newBoard[index] = piece

    return newBoard


def getPieceOnSquare(board, index):
    return board[index]


def squareEmpty(board, index):
    return board[index] == Square["EMPTY"]


def boardFull(board):
    return Square.EMPTY not in board


def allSquaresAreSamePiece(listOfPieces):
    return len(set(listOfPieces)) == 1


def isValidDiagonal(index):
    return index % (BOARD_SIZE + 1) == 0


# Need to exclude 0 and MAX_INDEX
def isValidAntiDiagonal(index):
    return (index % (BOARD_SIZE - 1) == 0) and (index % MAX_INDEX != 0)


def getSquaresOnSameRow(board, index):
    return __getSquaresInDirection(board, index, nextIndexInRow)


def getSquaresOnSameColumn(board, index):
    return __getSquaresInDirection(board, index, nextIndexInColumn)


def getSquaresOnSameDiagonal(board, index):
    return __getSquaresInDirection(board, index, nextIndexInDiagonal)


def getSquaresOnSameAntiDiagonal(board, index):
    return __getSquaresInDirection(board, index, nextIndexInAntiDiagonal)


# ----------------------------- Private Functions ------------------------------


def __getSquaresInDirection(board, index, nextIndexFunc):
    return __getSquaresInDirectionInternal(board, index, index, nextIndexFunc)


"""
    Parameters:
        board            Game board state to check against
        index            Index to be iterated on during looping; iterator
                         Also defines the starting index to loop on
        finalIndex       Stop looping once the next index = finalIndex; the base case
                         Normally defined as the final index = starting index
                         See example.
        nextIndexFunc    Function that returns the next index to check;
                         the direction to iterate indexes

    Assumptions:
        nextIndexFunc loops index in a cyclic pattern i.e. 0, 4, 8, 0, 4, 8, ...

    Description:
        Normally initialised with finalIndex = starting index in order to consume the whole board for that direction
        Specific sub ranges can be defined however...
        Recursively calls itself until base case is hit, relying on nextIndexFunc looping index back around
        Base case = reached last index,
            where last index is such that the next index = original index,
            due to the assumed wrapping property of nextIndexFunc
        Once base case is hit, begin returning a list of each piece on each indexed square

    Returns:
        List of the pieces present along the direction defined by nextIndexFunc
        
    Example Usage:
        getPiecesInDirectionInternal(state, 4, 4, nextIndexInRow)
"""


def __getSquaresInDirectionInternal(board, index, finalIndex, nextIndexFunc):
    if nextIndexFunc(index) == finalIndex:
        return [getPieceOnSquare(board, index)]

    return [getPieceOnSquare(board, index)] + __getSquaresInDirectionInternal(board, nextIndexFunc(index), finalIndex,
                                                                              nextIndexFunc)
