#!/usr/bin/env python3
from collections import namedtuple
from secrets import randbelow

from Display import *
from GameHelpers import *

# State.win is necessary if you are determining a win by searching the last move
# It is important to do this on very large boards - only searching the last move every turn is more efficient
# (can't afford to search the entire board for a win every turn with a large board)
State = namedtuple("State", "win, turn, board")
Player = namedtuple("Player", "agent, piece")


def emptyBoard():
    return [Square["EMPTY"]] * (MAX_INDEX + 1)


def initialiseGame():
    return State(
        win=False,
        turn=0,
        board=emptyBoard()
    )


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


def getMoveFromHuman():
    return input("Enter index to place piece:")


# TODO
def getMoveFromAI():
    print("getMoveFromAI() - not yet implemented")


def getRandomMove():
    number = randbelow(MAX_INDEX + 1)
    print("Random index: {}".format(number))

    return number


def getMoveFromPlayer(state, playersInfo):
    currentPlayer = getCurrentPlayerInfo(state, playersInfo)

    getMoveFunc = getMoveFunctionForPlayer(currentPlayer.agent)

    while True:
        try:
            userInput = int(getMoveFunc())
        except ValueError:
            print("Error: User input was not a valid integer.")
            continue
        if userInput < 0:
            print("Error: Index cannot be less than zero.")
            continue
        elif userInput > MAX_INDEX:
            print("Error: User input '{}' exceeds max index '{}' ".format(userInput, MAX_INDEX))
            continue
        elif not squareEmpty(state.board, userInput):
            print("Error: square {} is already taken!".format(userInput))
        else:
            break

    return userInput


def isThereWinInDirection(board, lastMove, getPiecesFunc):
    if (
            (getPiecesFunc is getSquaresOnSameDiagonal and not isValidDiagonal(lastMove)) or
            (getPiecesFunc is getSquaresOnSameAntiDiagonal and not isValidAntiDiagonal(lastMove))
    ):
        win = False
    else:
        pieces = getPiecesFunc(board, lastMove)
        win = allSquaresAreSamePiece(pieces)

    return win


def checkLastMoveForWin(state, lastMove):
    getPiecesFuncList = [
        getSquaresOnSameRow,
        getSquaresOnSameColumn,
        getSquaresOnSameDiagonal,
        getSquaresOnSameAntiDiagonal
    ]

    listOfWinsInEachDirection = map(lambda x: isThereWinInDirection(state.board, lastMove, x), getPiecesFuncList)

    win = any(winInDirection is True for winInDirection in listOfWinsInEachDirection)

    return setWinState(state, win)


if __name__ == '__main__':

    playersInfo = (
        Player(Agent.RANDOM, Square.O),
        Player(Agent.RANDOM, Square.X)
    )

    state = initialiseGame()

    printHelpGraphic()

    # Toggle now so that the game starts with player 1 in the main loop upon first toggle
    state = togglePlayerTurn(state)

    while not (state.win or boardFull(state.board)):
        state = togglePlayerTurn(state)

        currentPlayer = getCurrentPlayerInfo(state, playersInfo)  # Not strictly necessary, but makes code more legible
        printBoard(state.board)

        move = getMoveFromPlayer(state, playersInfo)

        newBoard = placePiece(state.board, move, currentPlayer.piece)

        state = setBoardState(state, newBoard)

        state = checkLastMoveForWin(state, move)

    printBoard(state.board)

    print()
    print("Player {} wins".format(state.turn + 1)) if state.win else print("Draw")
