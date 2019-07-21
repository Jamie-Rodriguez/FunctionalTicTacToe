#!/usr/bin/env python3
from Constants import Square
from Coordinates import *


def placePiece(board, index, piece):
    # Is there a way to create newBoard in a functional way in python?
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


def isValidDiagonal(boardDims, board, index):
    return __scoringDiagInternal(getSquaresOnSameDiagonal, boardDims, board, index)


def isValidAntiDiagonal(boardDims, board, index):
    return __scoringDiagInternal(getSquaresOnSameAntiDiagonal, boardDims, board, index)


def getSquaresOnSameRow(boardDims, board, index):
    return __getSquaresInDirection(nextIndexInRow, boardDims, board, index)


def getSquaresOnSameColumn(boardDims, board, index):
    return __getSquaresInDirection(nextIndexInColumn, boardDims, board, index)


def getSquaresOnSameDiagonal(boardDims, board, index):
    return __getSquaresInDirection(nextIndexInDiagonal, boardDims, board, index)


def getSquaresOnSameAntiDiagonal(boardDims, board, index):
    return __getSquaresInDirection(nextIndexInAntiDiagonal, boardDims, board, index)


# ----------------------------- Private Functions ------------------------------


def __getSquaresInDirection(nextIndexFunc, dims, board, index):
    return __getSquaresInDirectionInternal(nextIndexFunc, dims, board, index, index)


"""
    Parameters:
        nextIndexFunc        Function that returns the next index to check;
                             the direction to iterate indexes
        board                Game board to check against
                             width and height are required by nextIndexFunc
        index                Index to be iterated on during looping; iterator
                             Also defines the starting index to loop on
        finalIndex           Stop looping once the next index = finalIndex; the base case
                             Normally defined as the final index = starting index
                             See example.

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
        getPiecesInDirectionInternal(nextIndexInRow, state, 4, 4)
"""


def __getSquaresInDirectionInternal(nextIndexFunc, dims, board, finalIndex, index):
    if nextIndexFunc(dims.w, dims.h, index) == finalIndex:
        return [getPieceOnSquare(board, index)]

    return [getPieceOnSquare(board, index)] + \
           __getSquaresInDirectionInternal(nextIndexFunc,
                                           dims,
                                           board,
                                           finalIndex,
                                           nextIndexFunc(dims.w, dims.h, index))


def __scoringDiagInternal(findSquaresInDirectionFunc, boardDims, board, index):
    squaresFoundOnDiagonal = findSquaresInDirectionFunc(boardDims, board, index)

    if len(squaresFoundOnDiagonal) >= min(boardDims):
        isValid = True
    else:
        isValid = False

    return isValid
