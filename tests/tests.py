from unittest import TestCase
from itertools import starmap

from game import *


testBoard = [Square.O, Square.EMPTY, Square.EMPTY,
             Square.X, Square.X, Square.EMPTY,
             Square.O, Square.EMPTY, Square.X]


class TestCoordinates(TestCase):

    def mapAssertionHelper(self, expectedOutputs, width, inputs, f):
        self.assertEqual(expectedOutputs, list(map(lambda x: f(width, x), inputs)))

    def test_getMaxIndex(self):
        width = 3
        height = 5
        expectedOutput = 14

        self.assertEqual(expectedOutput, getMaxIndex(width, height))

    def test_getRowNum3x3(self):
        width = 3
        inputs = range(9)
        expectedOutputs = [0, 0, 0, 1, 1, 1, 2, 2, 2]

        outputs = list(map(lambda x: getRowNum(width, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_getColNum3x3(self):
        width = 3
        inputs = range(9)
        expectedOutputs = [0, 1, 2, 0, 1, 2, 0, 1, 2]

        outputs = list(map(lambda x: getColNum(width, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_isLeftColumn3x3(self):
        width = 3
        inputs = range(width * width)
        expectedOutputs = [True, False, False, True, False, False, True, False, False]

        outputs = list(map(lambda x: isLeftColumn(width, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_isRightColumn3x3(self):
        width = 3
        inputs = range(width * width)
        expectedOutputs = [False, False, True, False, False, True, False, False, True]

        outputs = list(map(lambda x: isRightColumn(width, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_isBottomRow3x3(self):
        width = 3
        height = 3
        inputs = range(width * width)
        expectedOutputs = [False, False, False, False, False, False, True, True, True]

        outputs = list(map(lambda x: isBottomRow(width, height, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_nextIndexInRow3x3(self):
        width = 3
        height = 3
        inputs = range(9)
        expectedOutputs = [1, 2, 0, 4, 5, 3, 7, 8, 6]

        outputs = list(map(lambda x: nextIndexInRow(width, height, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_nextIndexInColumn3x3(self):
        width = 3
        height = 3
        inputs = range(9)
        expectedOutputs = [3, 4, 5, 6, 7, 8, 0, 1, 2]

        outputs = list(map(lambda x: nextIndexInColumn(width, height, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_nextIndexInDiagonal3x3(self):
        width = 3
        height = 3
        inputs = range(9)
        expectedOutputs = [4, 5, 2, 7, 8, 1, 6, 3, 0]

        outputs = list(map(lambda x: nextIndexInDiagonal(width, height, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_nextIndexInDiagonal5x3(self):
        width = 5
        height = 3
        inputs = range(15)
        expectedOutputs = [6, 7, 8, 9, 4, 11, 12, 13, 14, 3, 10, 5, 0, 1, 2]

        outputs = list(map(lambda x: nextIndexInDiagonal(width, height, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_nextIndexInDiagonal3x5(self):
        width = 3
        height = 5
        inputs = range(15)
        expectedOutputs = [4, 5, 2, 7, 8, 1, 10, 11, 0, 13, 14, 3, 12, 9, 6]

        outputs = list(map(lambda x: nextIndexInDiagonal(width, height, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_nextIndexInAntiDiagonal3x3(self):
        width = 3
        height = 3
        inputs = range(9)
        expectedOutputs = [0, 3, 4, 1, 6, 7, 2, 5, 8]

        outputs = list(map(lambda x: nextIndexInAntiDiagonal(width, height, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_nextIndexInAntiDiagonal5x3(self):
        width = 5
        height = 3
        inputs = range(15)
        expectedOutputs = [0, 5, 6, 7, 8, 1, 10, 11, 12, 13, 2, 3, 4, 9, 14]

        outputs = list(map(lambda x: nextIndexInAntiDiagonal(width, height, x), inputs))

        self.assertEqual(expectedOutputs, outputs)

    def test_nextIndexInAntiDiagonal3x5(self):
        width = 3
        height = 5
        inputs = range(15)
        expectedOutputs = [0, 3, 4, 1, 6, 7, 2, 9, 10, 5, 12, 13, 8, 11, 14]

        outputs = list(map(lambda x: nextIndexInAntiDiagonal(width, height, x), inputs))

        self.assertEqual(expectedOutputs, outputs)


class TestGameHelpers(TestCase):

    def isValidDiagAntiDiagHelper(self, expectedOutputs, f, dims, board, inputs):
        actualOutputs = list(map(lambda i: f(dims, board, i), inputs))
        
        self.assertEqual(expectedOutputs, actualOutputs)

    def getPiecesHelper(self, expectedOutputs, f, dims, inputBoard):
        actualOutputs = list(starmap(lambda i, x: f(dims, inputBoard, i), enumerate(inputBoard)))

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

    def test_squareEmpty(self):
        input = [Square.X, Square.O, Square.EMPTY]

        self.assertEqual(False, squareEmpty(input, 1))
        self.assertEqual(True, squareEmpty(input, 2))

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
        boardDims = BoardDims(3, 3)
        inputs = range(9)
        expectedOutputs = [True, False, False, False, True, False, False, False, True]

        self.isValidDiagAntiDiagHelper(expectedOutputs, isValidDiagonal, boardDims, testBoard, inputs)

    def test_isValidAntiDiagonal3x3(self):
        boardDims = BoardDims(3, 3)
        inputs = range(9)
        expectedOutputs = [False, False, True, False, True, False, True, False, False]

        self.isValidDiagAntiDiagHelper(expectedOutputs, isValidAntiDiagonal, boardDims, testBoard, inputs)

    def test_getPiecesOnRow3x3(self):
        boardDims = BoardDims(3, 3)
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

        self.getPiecesHelper(expectedRow, getSquaresOnSameRow, boardDims, testBoard)

    def test_getPiecesOnColumn3x3(self):
        boardDims = BoardDims(3, 3)
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

        self.getPiecesHelper(expectedCol, getSquaresOnSameColumn, boardDims, testBoard)

    def test_getPiecesOnDiagonal3x3(self):
        boardDims = BoardDims(3, 3)
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

        self.getPiecesHelper(expectedDiag, getSquaresOnSameDiagonal, boardDims, testBoard)

    def test_getPiecesOnAntiDiagonal3x3(self):
        boardDims = BoardDims(3, 3)
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

        self.getPiecesHelper(expectedAntiDiag, getSquaresOnSameAntiDiagonal, boardDims, testBoard)


class TestGame(TestCase):
    defaultPlayersInfo = [Player(Agent.RANDOM, Square.O),
                          Player(Agent.RANDOM, Square.X)]

    def test_initialiseGame(self):
        width = 3
        height = 3
        expectedOutput = State(playersInfo=self.defaultPlayersInfo,
                               win=False,
                               turn=0,
                               board=[Square["EMPTY"]] * 9)

        self.assertEqual(expectedOutput, initialiseGameState(width, height))

    def test_setBoardState(self):
        inputState = State(playersInfo=self.defaultPlayersInfo,
                           win=False,
                           turn=0,
                           board=[Square["EMPTY"]] * 3)

        inputBoard = [Square.EMPTY, Square.EMPTY, Square.X]

        expectedOutput = State(playersInfo=self.defaultPlayersInfo,
                               win=False,
                               turn=0,
                               board=inputBoard)

        self.assertEqual(expectedOutput, setBoardState(inputState, inputBoard))


    def test_togglePlayerTurn(self):
        inputState = State(playersInfo=self.defaultPlayersInfo,
                           win=False,
                           turn=1,
                           board=[Square.EMPTY, Square.EMPTY, Square.X])

        actualOutput = togglePlayerTurn(inputState)

        expectedOutput = State(playersInfo=self.defaultPlayersInfo,
                               win=inputState.win,
                               turn=0,
                               board=inputState.board)

        self.assertEqual(expectedOutput, actualOutput)

        actualOutput = togglePlayerTurn(actualOutput)

        expectedOutput = State(playersInfo=self.defaultPlayersInfo,
                               win=inputState.win,
                               turn=1,
                               board=inputState.board)

        self.assertEqual(expectedOutput, actualOutput)


    def test_setWinState(self):
        inputState = State(playersInfo=self.defaultPlayersInfo,
                           win=False,
                           turn=0,
                           board=[Square.EMPTY, Square.EMPTY, Square.X])

        expectedOutput = State(playersInfo=self.defaultPlayersInfo,
                               win=True,
                               turn=inputState.turn,
                               board=inputState.board)

        self.assertEqual(expectedOutput, setWinState(inputState, True))


    def test_applyMoveToState(self):
        boardDims = BoardDims(3, 3)
        inputBoard = [Square.EMPTY, Square.EMPTY, Square.EMPTY,
                      Square.O,     Square.EMPTY, Square.O,
                      Square.EMPTY, Square.X,     Square.X]
        inputState = State(playersInfo=self.defaultPlayersInfo,
                      win=False,
                      turn=1,
                      board=inputBoard)

        noWinMove = 4
        noWinBoard = [Square.EMPTY, Square.EMPTY, Square.EMPTY,
                      Square.O,     Square.X,     Square.O,
                      Square.EMPTY, Square.X,     Square.X]
        winningMove = 6
        winBoard = [Square.EMPTY, Square.EMPTY, Square.EMPTY,
                    Square.O,     Square.EMPTY, Square.O,
                    Square.X,     Square.X,     Square.X]

        expectedOutputNoWin = State(playersInfo=self.defaultPlayersInfo,
                                    win=False,
                                    turn=0,
                                    board=noWinBoard)
        expectedOutputWin = State(playersInfo=self.defaultPlayersInfo,
                                  win=True,
                                  turn=1,
                                  board=winBoard)

        self.assertEqual(expectedOutputNoWin,
                         applyMoveToState(boardDims, inputState, noWinMove))
        self.assertEqual(expectedOutputWin,
                         applyMoveToState(boardDims, inputState, winningMove))


    def test_getCurrentPlayerInfo(self):
        inputState = State(playersInfo=self.defaultPlayersInfo,
                           win=False,
                           turn=1,
                           board=[Square.EMPTY, Square.EMPTY, Square.X])

        expectedOutput = Player(Agent.RANDOM, Square.X)

        self.assertEqual(expectedOutput, getCurrentPlayerInfo(inputState))


    def test_getMoveFunctionForPlayer(self):
        self.assertEqual(getMoveFromHuman, getMoveFunctionForPlayer(Agent.HUMAN))
        self.assertEqual(getMoveFromAI, getMoveFunctionForPlayer(Agent.AI))
        self.assertEqual(getRandomMove, getMoveFunctionForPlayer(Agent.RANDOM))
        # Can't test the default (error) case in this way

    # Can't test getMoveFromHuman(), getMoveFromAI() or getRandomMove()
    # and as a result, also can't test getMoveFromPlayer()


    def test_getAvailableMoves(self):
        inputBoard = [Square.EMPTY, Square.X, Square.EMPTY]
        expectedOutput = [0, 2]
        actualOutput = getAvailableMoves(inputBoard)

        self.assertEqual(expectedOutput, actualOutput)


    def test_createPreRecordedPlayer(self):
        getMove = createPreRecordedPlayer([2, 5])
        self.assertEqual(getMove(), 2)
        self.assertEqual(getMove(), 5)


    def test_isThereWinInDirection3x3(self):
        boardDims = BoardDims(3, 3)
        board = [Square.EMPTY, Square.O, Square.X,
                 Square.EMPTY, Square.O, Square.O,
                 Square.X,     Square.X, Square.X]
        lastMove = 7

        self.assertEqual(True,
                         isThereWinInDirection(boardDims,
                                               board,
                                               lastMove,
                                               getSquaresOnSameRow))
        self.assertEqual(False,
                         isThereWinInDirection(boardDims,
                                               board,
                                               lastMove,
                                               getSquaresOnSameColumn))
        self.assertEqual(False,
                         isThereWinInDirection(boardDims,
                                               board,
                                               lastMove,
                                               getSquaresOnSameDiagonal))
        self.assertEqual(False,
                         isThereWinInDirection(boardDims,
                                               board,
                                               lastMove,
                                               getSquaresOnSameAntiDiagonal))

    def test_isThereWinInDirection4x3(self):
        boardDims = BoardDims(4, 3)
        board = [Square.EMPTY, Square.O, Square.EMPTY, Square.X,
                 Square.X,     Square.X, Square.X,     Square.X,
                 Square.O,     Square.O, Square.EMPTY, Square.O]
        lastMove = 5

        self.assertEqual(True,
                         isThereWinInDirection(boardDims,
                                               board,
                                               lastMove,
                                               getSquaresOnSameRow))
        self.assertEqual(False,
                         isThereWinInDirection(boardDims,
                                               board,
                                               lastMove,
                                               getSquaresOnSameColumn))
        self.assertEqual(False,
                         isThereWinInDirection(boardDims,
                                               board,
                                               lastMove,
                                               getSquaresOnSameDiagonal))
        self.assertEqual(False,
                         isThereWinInDirection(boardDims,
                                               board,
                                               lastMove,
                                               getSquaresOnSameAntiDiagonal))

    def test_checkLastMoveForWin3x3(self):
        boardDims = BoardDims(3, 3)

        noWinBoard = [Square.EMPTY, Square.O,     Square.X,
                      Square.EMPTY, Square.O,     Square.O,
                      Square.X,     Square.EMPTY, Square.X]
        inputStateNoWin = State(self.defaultPlayersInfo, False, 1, noWinBoard)
        lastMoveNoWin = 6

        winBoard = [Square.EMPTY, Square.O, Square.X,
                    Square.EMPTY, Square.O, Square.O,
                    Square.X,     Square.X, Square.X]
        inputStateWin = State(self.defaultPlayersInfo, False, 1, winBoard)
        lastMoveWin = 7

        expectedNoWinState = State(self.defaultPlayersInfo, False, 0, noWinBoard)
        expectedWinState = State(self.defaultPlayersInfo, True, 1, winBoard)

        self.assertEqual(expectedNoWinState,
                         checkLastMoveForWin(boardDims,
                                             inputStateNoWin,
                                             lastMoveNoWin))
        self.assertEqual(expectedWinState,
                         checkLastMoveForWin(boardDims,
                                             inputStateWin,
                                             lastMoveWin))

    def test_checkLastMoveForWin4x3(self):
        boardDims = BoardDims(4, 3)

        noWinBoard = [Square.X,     Square.O,     Square.O,     Square.O,
                      Square.EMPTY, Square.X,     Square.EMPTY, Square.EMPTY,
                      Square.X,     Square.EMPTY, Square.EMPTY, Square.EMPTY]
        inputStateNoWin = State(self.defaultPlayersInfo, False, 0, noWinBoard)
        lastMoveNoWin = 3

        winBoard = [Square.X,     Square.O,     Square.O,     Square.O,
                    Square.EMPTY, Square.X,     Square.EMPTY, Square.EMPTY,
                    Square.X,     Square.EMPTY, Square.X,     Square.EMPTY]
        inputStateWin = State(self.defaultPlayersInfo, False, 1, winBoard)
        lastMoveWin = 10

        expectedNoWinState = State(self.defaultPlayersInfo, False, 1, noWinBoard)
        expectedWinState = State(self.defaultPlayersInfo, True, 1, winBoard)

        self.assertEqual(expectedNoWinState,
                         checkLastMoveForWin(boardDims,
                                             inputStateNoWin,
                                             lastMoveNoWin))
        self.assertEqual(expectedWinState,
                         checkLastMoveForWin(boardDims,
                                             inputStateWin,
                                             lastMoveWin))
