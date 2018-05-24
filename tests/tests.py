from unittest import TestCase
from itertools import starmap

from Game import *


testBoard = [Square.O, Square.EMPTY, Square.EMPTY,
             Square.X, Square.X, Square.EMPTY,
             Square.O, Square.EMPTY, Square.X]


# TODO!
"""
Can't test anything that reads from BOARD_SIZE in a general case as
they rely on size of board, which is a hard-coded, compile-time constant.
This breaks the referential transparency of the functions

TODO: fix the following functions to remain pure: The basic functions that read from BOARD_SIZE, i.e.
    getRowNum
    getColNum
    nextIndexInRow
    nextIndexInColumn
    nextIndexInDiagonal
    nextIndexInAntiDiagonal

The following functions are affected as a consequence of this impurity:
    isValidDiagonal()
    isValidAntiDiagonal()
    getSquaresOnSameRow()
    getSquaresOnSameColumn()
    getSquaresOnSameDiagonal()
    getSquaresOnSameAntiDiagonal()
    isThereWinInDirection()
    checkLastMoveForWin()
"""


class TestCoordinates(TestCase):

    def mapAssertionHelper(self, expectedOutputs, inputs, f):
        # map converts list into iterable map object, cast back
        self.assertEqual(expectedOutputs, list(map(lambda x: f(x), inputs)))

    def test_getRowNum3x3(self):
        inputs = range(9)
        expectedOutputs = [0, 0, 0, 1, 1, 1, 2, 2, 2]

        self.mapAssertionHelper(expectedOutputs, inputs, getRowNum)

    def test_getColNum3x3(self):
        inputs = range(9)
        expectedOutputs = [0, 1, 2, 0, 1, 2, 0, 1, 2]

        self.mapAssertionHelper(expectedOutputs, inputs, getColNum)

    def test_nextIndexInRow3x3(self):
        inputs = range(9)
        expectedOutputs = [1, 2, 0, 4, 5, 3, 7, 8, 6]

        self.mapAssertionHelper(expectedOutputs, inputs, nextIndexInRow)

    def test_nextIndexInColumn3x3(self):
        inputs = range(9)
        expectedOutputs = [3, 4, 5, 6, 7, 8, 0, 1, 2]

        self.mapAssertionHelper(expectedOutputs, inputs, nextIndexInColumn)

    """
    Can't test isValidDiagonal() or isValidAntiDiagonal() in a general case as
    they rely on size of board, which is a hard-coded, compile-time constant.
    Number of pieces in a row for the diagonal and anti-diagonal directions varies with BOARD_SIZE.
    TODO: Remove isValidDiagonal() and isValidAntiDiagonal()'s dependence on BOARD_SIZE
    """
    def test_nextIndexInDiagonal3x3(self):
        inputs = range(9)
        expectedOutputs = [4, 5, 2, 7, 8, 1, 6, 3, 0]

        self.mapAssertionHelper(expectedOutputs, inputs, nextIndexInDiagonal)

    def test_nextIndexInAntiDiagonal3x3(self):
        inputs = range(9)
        expectedOutputs = [0, 3, 4, 1, 6, 7, 2, 5, 8]

        self.mapAssertionHelper(expectedOutputs, inputs, nextIndexInAntiDiagonal)


class TestGameHelpers(TestCase):

    def isValidDiagAntiDiagHelper(self, expectedOutputs, f, inputs):
        # map converts list into iterable map object, cast back
        self.assertEqual(expectedOutputs, list(map(lambda x: f(x), inputs)))

    def getPiecesHelper(self, expectedOutputs, f, inputBoard):
        actualOutputs = list(starmap(lambda i, x: f(inputBoard, i), enumerate(inputBoard)))

        self.assertEqual(expectedOutputs, actualOutputs)

    def test_placePiece(self):
        input = [Square.EMPTY, Square.EMPTY, Square.EMPTY]
        expectedOutput = [Square.EMPTY, Square.O, Square.X]

        actualOutput = placePiece(input, 1, Square.O)
        actualOutput = placePiece(actualOutput, 2, Square.X)

        self.assertEqual(expectedOutput, actualOutput)

    def test_getPieceOnSquare(self):
        input = [Square.EMPTY, Square.O, Square.X]

        self.assertEqual(Square.EMPTY, getPieceOnSquare(input, 0))
        self.assertEqual(Square.O, getPieceOnSquare(input, 1))
        self.assertEqual(Square.X, getPieceOnSquare(input, 2))

    # squareEmpty() does not need to be tested because it's just an equivalence...

    def test_boardFull(self):
        emptyBoard = [Square.EMPTY, Square.EMPTY, Square.EMPTY]
        nonEmptyBoard = [Square.EMPTY, Square.O, Square.X]
        fullBoard = [Square.X, Square.O, Square.X]

        self.assertEqual(False, boardFull(emptyBoard))
        self.assertEqual(False, boardFull(nonEmptyBoard))
        self.assertEqual(True, boardFull(fullBoard))

    def test_allSquaresAreSamePiece(self):
        nonHomogeneousBoard = [Square.EMPTY, Square.O, Square.X]
        homogeneousBoard = [Square.X] * 3

        self.assertEqual(False, allSquaresAreSamePiece(nonHomogeneousBoard))
        self.assertEqual(True, allSquaresAreSamePiece(homogeneousBoard))

    def test_isValidDiagonal3x3(self):
        inputs = range(9)
        expectedOutputs = [True, False, False, False, True, False, False, False, True]

        self.isValidDiagAntiDiagHelper(expectedOutputs, isValidDiagonal, inputs)

    def test_isValidAntiDiagonal3x3(self):
        inputs = range(9)
        expectedOutputs = [False, False, True, False, True, False, True, False, False]

        self.isValidDiagAntiDiagHelper(expectedOutputs, isValidAntiDiagonal, inputs)

    def test_getPiecesOnRow3x3(self):
        expectedRow = [
            [Square.O, Square.EMPTY, Square.EMPTY],
            [Square.EMPTY, Square.EMPTY, Square.O],
            [Square.EMPTY, Square.O, Square.EMPTY],
            [Square.X, Square.X, Square.EMPTY],
            [Square.X, Square.EMPTY, Square.X],
            [Square.EMPTY, Square.X, Square.X],
            [Square.O, Square.EMPTY, Square.X],
            [Square.EMPTY, Square.X, Square.O],
            [Square.X, Square.O, Square.EMPTY]
        ]

        self.getPiecesHelper(expectedRow, getSquaresOnSameRow, testBoard)

    def test_getPiecesOnColumn3x3(self):
        expectedCol = [
            [Square.O,     Square.X,     Square.O],
            [Square.EMPTY, Square.X,     Square.EMPTY],
            [Square.EMPTY, Square.EMPTY, Square.X],
            [Square.X, Square.O, Square.O],
            [Square.X, Square.EMPTY, Square.EMPTY],
            [Square.EMPTY, Square.X, Square.EMPTY],
            [Square.O, Square.O, Square.X],
            [Square.EMPTY, Square.EMPTY, Square.X],
            [Square.X, Square.EMPTY, Square.EMPTY]
        ]

        self.getPiecesHelper(expectedCol, getSquaresOnSameColumn, testBoard)

    def test_getPiecesOnDiagonal3x3(self):
        expectedDiag = [
            [Square.O, Square.X, Square.X],
            [Square.EMPTY, Square.EMPTY],
            [Square.EMPTY],
            [Square.X, Square.EMPTY],
            [Square.X, Square.X, Square.O],
            [Square.EMPTY, Square.EMPTY],
            [Square.O],
            [Square.EMPTY, Square.X],
            [Square.X, Square.O, Square.X]
        ]

        self.getPiecesHelper(expectedDiag, getSquaresOnSameDiagonal, testBoard)

    def test_getPiecesOnAntiDiagonal3x3(self):
        expectedAntiDiag = [
            [Square.O],
            [Square.EMPTY, Square.X],
            [Square.EMPTY, Square.X, Square.O],
            [Square.X, Square.EMPTY],
            [Square.X, Square.O, Square.EMPTY],
            [Square.EMPTY, Square.EMPTY],
            [Square.O, Square.EMPTY, Square.X],
            [Square.EMPTY, Square.EMPTY],
            [Square.X]
        ]

        self.getPiecesHelper(expectedAntiDiag, getSquaresOnSameAntiDiagonal, testBoard)


class TestGame(TestCase):
    def test_initialiseGame(self):
        expectedOutput = State(
                            win=False,
                            turn=0,
                            board=emptyBoard()
                        )

        self.assertEqual(expectedOutput, initialiseGame())

    def test_setBoardState(self):
        inputState = State(
                        win=False,
                        turn=0,
                        board=[Square["EMPTY"]] * 3
                    )

        inputBoard = [Square.EMPTY, Square.EMPTY, Square.X]

        expectedOutput = State(
                            win=False,
                            turn=0,
                            board=inputBoard
                        )

        self.assertEqual(expectedOutput, setBoardState(inputState, inputBoard))

    def test_setWinState(self):
        inputState = State(
            win=False,
            turn=0,
            board=[Square.EMPTY, Square.EMPTY, Square.X]
        )

        expectedOutput = State(
            win=True,
            turn=inputState.turn,
            board=inputState.board
        )

        self.assertEqual(expectedOutput, setWinState(inputState, True))

    def test_getCurrentPlayerInfo(self):
        inputState = State(
            win=False,
            turn=1,
            board=[Square.EMPTY, Square.EMPTY, Square.X]
        )

        inputPlayersInfo = (
            Player(Agent.HUMAN,  Square.O),
            Player(Agent.RANDOM, Square.X)
        )

        expectedOutput = inputPlayersInfo[inputState.turn]

        self.assertEqual(expectedOutput, getCurrentPlayerInfo(inputState, inputPlayersInfo))

    def test_togglePlayerTurn(self):
        inputState = State(
            win=False,
            turn=1,
            board=[Square.EMPTY, Square.EMPTY, Square.X]
        )

        actualOutput = togglePlayerTurn(inputState)

        expectedOutput = State(
            win=inputState.win,
            turn=0,
            board=inputState.board
        )

        self.assertEqual(expectedOutput, actualOutput)

        actualOutput = togglePlayerTurn(actualOutput)

        expectedOutput = State(
            win=inputState.win,
            turn=1,
            board=inputState.board
        )

        self.assertEqual(expectedOutput, actualOutput)

    def test_getMoveFunctionForPlayer(self):
        self.assertEqual(getMoveFromHuman, getMoveFunctionForPlayer(Agent.HUMAN))

        self.assertEqual(getMoveFromAI, getMoveFunctionForPlayer(Agent.AI))

        self.assertEqual(getRandomMove, getMoveFunctionForPlayer(Agent.RANDOM))

        # Can't compare anonymous function in default case...

    """
    Can't test checkLastMoveForWin() in a general case as it relies on
    isValidDiagonal() and isValidAntiDiagonal() which read compile-time constant BOARD_SIZE
    See note above test_nextIndexInDiagonal3x3()
    """