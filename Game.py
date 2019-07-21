#!/usr/bin/env python3
from collections import namedtuple
import random

from Constants import Agent, BOARD_WIDTH, BOARD_HEIGHT
from Display import *
from GameHelpers import *


# State.win is necessary if you are determining a win by searching the last move
# It is important to do this on very large boards - only searching the last move every turn is more efficient
# (can't afford to search the entire board for a win every turn with a large board)
State = namedtuple("State", "win, turn, board")
Player = namedtuple("Player", "agent, piece")
BoardDims = namedtuple("BoardDims", "w, h")


def emptyBoard(width, height):
    return [Square["EMPTY"]] * (getMaxIndex(width, height) + 1)


def initialiseGameState(width, height):
    return State(win=False,
                 turn=0,
                 board=emptyBoard(width, height))


def setBoardState(state, board):
    return State(state.win, state.turn, board)


def setWinState(state, win):
    return State(win, state.turn, state.board)


def getCurrentPlayerInfo(state, playersInfo):
    return playersInfo[state.turn]


def togglePlayerTurn(state):
    return State(state.win, state.turn ^ 1, state.board)


def getMoveFunctionForPlayer(player):
    return {
        Agent.HUMAN: getMoveFromHuman,
        Agent.AI: getMoveFromAI,
        Agent.RANDOM: getRandomMove
    }.get(player, lambda: print("Invalid agent selected"))  # Default case


# 'Move' functions must have same signature: IO () -> int

def getMoveFromHuman():
    return input("Enter index to place piece:")


# TODO
def getMoveFromAI():
    print("getMoveFromAI() - not yet implemented")
    raise NotImplementedError


def getRandomMove():
    # Ideally would take in width and height as parameters,
    # but need to enforce the function signature IO () -> int
    index = random.randint(0, getMaxIndex(BOARD_WIDTH, BOARD_HEIGHT))
    print("Random index: {}".format(index))

    return index


def getMoveFromPlayer(width, height, playersInfo, state):
    currentPlayer = getCurrentPlayerInfo(state, playersInfo)

    getMoveFunc = getMoveFunctionForPlayer(currentPlayer.agent)

    maxIndex = getMaxIndex(width, height)

    while True:
        try:
            userInput = int(getMoveFunc())
        except ValueError:
            print("Error: Input was not a valid integer.")
            continue
        if userInput < 0:
            print("Error: Index cannot be less than zero.")
            continue
        elif userInput > maxIndex:
            print("Error: Input '{}' exceeds max index '{}' ".format(userInput, maxIndex))
            continue
        elif not squareEmpty(state.board, userInput):
            print("Error: square {} is already taken!".format(userInput))
        else:
            break

    return userInput


# A win for a board of dimensions 'w' x 'h' fulfills one or more of the
# following conditions:
#   w pieces in the horizontal direction
#   h pieces in the vertical direction
#   min(w, h) pieces along a diagonal
def isThereWinInDirection(boardDims, board, lastMove, getPiecesFunc):
    if (
        (getPiecesFunc is getSquaresOnSameDiagonal
            and not isValidDiagonal(boardDims, board, lastMove))
        or (getPiecesFunc is getSquaresOnSameAntiDiagonal
            and not isValidAntiDiagonal(boardDims, board, lastMove))
    ):
        win = False
    else:
        pieces = getPiecesFunc(boardDims, board, lastMove)
        win = allSquaresAreSamePiece(pieces)

    return win


def checkLastMoveForWin(boardDims, state, lastMove):
    getPiecesFuncList = [
        getSquaresOnSameRow,
        getSquaresOnSameColumn,
        getSquaresOnSameDiagonal,
        getSquaresOnSameAntiDiagonal
    ]

    listOfWinsInEachDirection = map(lambda x: isThereWinInDirection(boardDims, state.board, lastMove, x), getPiecesFuncList)

    win = any(winInDirection is True for winInDirection in listOfWinsInEachDirection)

    return setWinState(state, win)


if __name__ == '__main__':

    playersInfo = (
        Player(Agent.RANDOM, Square.O),
        Player(Agent.RANDOM, Square.X)
    )

    boardDims = BoardDims(BOARD_WIDTH, BOARD_HEIGHT)

    state = initialiseGameState(BOARD_WIDTH, BOARD_HEIGHT)

    printHelpGraphic(BOARD_WIDTH, BOARD_HEIGHT)

    # Toggle now so that the game starts with player 1 in the main loop upon first toggle
    state = togglePlayerTurn(state)

    while not (state.win or boardFull(state.board)):
        state = togglePlayerTurn(state)

        currentPlayer = getCurrentPlayerInfo(state, playersInfo)  # Not strictly necessary, but makes code more legible
        printBoard(state.board, BOARD_WIDTH, BOARD_HEIGHT)

        move = getMoveFromPlayer(BOARD_WIDTH, BOARD_HEIGHT, playersInfo, state)

        newBoard = placePiece(state.board, move, currentPlayer.piece)

        state = setBoardState(state, newBoard)

        state = checkLastMoveForWin(boardDims, state, move)

    printBoard(state.board, BOARD_WIDTH, BOARD_HEIGHT)

    print("\nPlayer {} wins".format(state.turn + 1)) if state.win else print("Draw")
