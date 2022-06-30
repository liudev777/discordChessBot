from collections import namedtuple
from matplotlib.pyplot import pie
from settings import Position
import numpy as np

class Piece(): #piece object
    def __init__(self, color: str, type: str, ver: int, position: Position=None) -> None: 
        if position is None:
            self.position = Position(-1,-1)
        else:
            self.position = position
        self.color = color
        self.type = type
        self.ver = ver
        self.moves = [False]
        self.isAlive = True
        
    def __str__(self) -> str: #print piece info
        return (f'color: {self.color}, type: {self.type}, moves: {self.moves}, isAlive: {self.isAlive} position: {self.position}')

    def __repr__(self) -> str:
        return f'{self.color}{self.type}{self.ver}'


class TempModel():
    def __init__(self) -> None:
        self.whiteTurn = True
        self.currentMove = None
        self.isCheck = False
        self.isCheckmate = False
        self.isStalemate = False

        wP1 = Piece("w", "P", 1, Position(0,1))
        wP2 = Piece("w", "P", 2, Position(1,1))
        wP3 = Piece("w", "P", 3, Position(2,1))
        wP4 = Piece("w", "P", 4, Position(3,1))
        wP5 = Piece("w", "P", 5, Position(4,1))
        wP6 = Piece("w", "P", 6, Position(5,1))
        wP7 = Piece("w", "P", 7, Position(6,1))
        wP8 = Piece("w", "P", 8, Position(7,1))
        
        bP1 = Piece("b", "P", 1, Position(0,6))
        bP2 = Piece("b", "P", 2, Position(1,6))
        bP3 = Piece("b", "P", 3, Position(2,6))
        bP4 = Piece("b", "P", 4, Position(3,6))
        bP5 = Piece("b", "P", 5, Position(4,6))
        bP6 = Piece("b", "P", 6, Position(5,6))
        bP7 = Piece("b", "P", 7, Position(6,6))
        bP8 = Piece("b", "P", 8, Position(7,6))
        

        wR1 = Piece("w", "R", 1, Position(0,0))
        wN1 = Piece("w", "N", 1, Position(1,0))
        wB1 = Piece("w", "B", 1, Position(2,0))
        wQ1 = Piece("w", "Q", 1, Position(3,0))
        wK1 = Piece("w", "K", 1, Position(4,0))
        wB2 = Piece("w", "B", 2, Position(5,0))
        wN2 = Piece("w", "N", 2, Position(6,0))
        wR2 = Piece("w", "R", 2, Position(7,0))

        bR1 = Piece("b", "R", 1, Position(0,7))
        bN1 = Piece("b", "N", 1, Position(1,7))
        bB1 = Piece("b", "B", 1, Position(2,7))
        bK1 = Piece("b", "K", 1, Position(3,7))
        bQ1 = Piece("b", "Q", 1, Position(4,7))
        bB2 = Piece("b", "B", 2, Position(5,7))
        bN2 = Piece("b", "N", 2, Position(6,7))
        bR2 = Piece("b", "R", 2, Position(7,7))

        self.board = [
            [wR1, wN1, wB1, wQ1, wK1, wB2, wN2, wR2],
            [wP1, wP2, wP3, wP4, wP5, wP6, wP7, wP8],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [bP1, bP2, bP3, bP4, bP5, bP6, bP7, bP8],
            [bR1, bN1, bB1, bQ1, bK1, bB2, bN2, bR2]
        ]

        
    def __str__(self) -> str:
        return f'{np.matrix(self.board)}'

    def movePiece(self, src: Position, dest: Position):
            if self.board[dest.y][dest.x] != None:
                self.board[dest.y][dest.x].isAlive = False
            self.board[src.y][src.x].position = dest

print(TempModel())








# class Model():
#     def __init__(self) -> None:
#         #game conditions
#         self.whiteTurn = True
#         self.currentMove = None
#         self.isCheck = False
#         self.isCheckmate = False
#         self.isStalemate = False

#         #initializes all the chess pieces.
#         self.gameBoard = Board()
#         self.pieceArray = [None] * 32
#         for i in range(0, 16):
#             if i < 8:
#                 self.pieceArray[i] = Piece("w", "P", Position(i,1))
#             elif i < 16:
#                 self.pieceArray[i] = Piece("b", "P", Position(i-8,6))

#         self.pieceArray[16] = Piece("w", "R", Position(0,0))
#         self.pieceArray[17] = Piece("w", "N", Position(1,0))
#         self.pieceArray[18] = Piece("w", "B", Position(2,0))
#         self.pieceArray[19] = Piece("w", "Q", Position(3,0))
#         self.pieceArray[20] = Piece("w", "K", Position(4,0))
#         self.pieceArray[21] = Piece("w", "B", Position(5,0))
#         self.pieceArray[22] = Piece("w", "N", Position(6,0))
#         self.pieceArray[23] = Piece("w", "R", Position(7,0))
#         self.pieceArray[24] = Piece("b", "R", Position(0,7))

#         self.pieceArray[25] = Piece("b", "N", Position(1,7))
#         self.pieceArray[26] = Piece("b", "B", Position(2,7))
#         self.pieceArray[27] = Piece("b", "Q", Position(3,7))
#         self.pieceArray[28] = Piece("b", "K", Position(4,7))
#         self.pieceArray[29] = Piece("b", "B", Position(5,7))
#         self.pieceArray[30] = Piece("b", "N", Position(6,7))
#         self.pieceArray[31] = Piece("b", "R", Position(7,7))

#         for piece in self.pieceArray:
#             print(piece)

#         for piece in self.pieceArray: #initializes pieces from pieceArray onto the board
#             self.gameBoard.insertPiece(piece)

    
        