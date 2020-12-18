#!/usr/bin/env python3
from collections import namedtuple
import random

from Constants import Agent, BOARD_WIDTH, BOARD_HEIGHT
from Display import *
from GameHelpers import *


# State.win is necessary if you are determining a win by searching the last move
# It is important to do this on very large boards - only searching the last move every turn is more efficient
# (can't afford to search the entire board for a win every turn with a large board)
State = namedtuple("State", "playersInfo, win, turn, board")
Player = namedtuple("Player", "agent, piece")
BoardDims = namedtuple("BoardDims", "w, h")


def emptyBoard(width, height):
    return [Square["EMPTY"]] * (getMaxIndex(width, height) + 1)


def initialiseGameState(width, height):
    return State(playersInfo=[Player(Agent.RANDOM, Square.O),
                              Player(Agent.RANDOM, Square.X)],
                 win=False,
                 turn=0,
                 board=emptyBoard(width, height))


def setBoardState(state, board):
    return State(state.playersInfo, state.win, state.turn, board)


def togglePlayerTurn(state):
    return State(state.playersInfo, state.win, state.turn ^ 1, state.board)


def setWinState(state, win):
    return State(state.playersInfo, win, state.turn, state.board)


# This function will place the piece according to the current turn in state
# This function will then update the turn afterwards (see checkLastMoveForWin())
def applyMoveToState(boardDims, state, move):
    currentTurn = state.turn
    currentPiece = state.playersInfo[currentTurn].piece
    board = placePiece(state.board, move, currentPiece)

    newState = setBoardState(state, board)

    return checkLastMoveForWin(boardDims, newState, move)


def getCurrentPlayerInfo(state):
    return state.playersInfo[state.turn]


def getMoveFunctionForPlayer(player):
    return {
        Agent.HUMAN: getMoveFromHuman,
        Agent.AI: getMoveFromAI,
        Agent.RANDOM: getRandomMove
    }.get(player, lambda: print("Invalid agent selected"))  # Default case


def getAvailableMoves(board):
    return [i for i in range(len(board)) if board[i] == Square.EMPTY]


# 'Move' functions must have same signature: IO () -> int

def getMoveFromHuman():
    return input("Enter index to place piece:")


def createPreRecordedPlayer(moves):
    def createPreRecordedMoveGenerator(moves):
        for i in range(len(moves)):
            yield moves[i]

    preRecordedPlayer = createPreRecordedMoveGenerator(moves)

    return lambda: next(preRecordedPlayer)


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


def getMoveFromPlayer(width, height, state):
    currentPlayer = getCurrentPlayerInfo(state)

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


# Note: Updates the turn
def checkLastMoveForWin(boardDims, state, lastMove):
    getPiecesFuncList = [
        getSquaresOnSameRow,
        getSquaresOnSameColumn,
        getSquaresOnSameDiagonal,
        getSquaresOnSameAntiDiagonal
    ]

    listOfWinsInEachDirection = map(lambda x: isThereWinInDirection(boardDims, state.board, lastMove, x), getPiecesFuncList)

    win = any(winInDirection is True for winInDirection in listOfWinsInEachDirection)

    return setWinState(state, win) if win else togglePlayerTurn(setWinState(state, win))


def playGame(state):
    if state.win or boardFull(state.board):
        return state

    boardDims = BoardDims(BOARD_WIDTH, BOARD_HEIGHT)

    printBoard(state.board, BOARD_WIDTH, BOARD_HEIGHT)

    move = getMoveFromPlayer(BOARD_WIDTH, BOARD_HEIGHT, state)

    return playGame(applyMoveToState(boardDims, state, move))


if __name__ == '__main__':
    initialState = initialiseGameState(BOARD_WIDTH, BOARD_HEIGHT)

    printHelpGraphic(BOARD_WIDTH, BOARD_HEIGHT)

    finalState = playGame(initialState)

    printBoard(finalState.board, BOARD_WIDTH, BOARD_HEIGHT)

    print("\nPlayer {} wins".format(finalState.turn + 1)) if finalState.win else print("Draw")
