from collections import namedtuple
from settings import Position

class Piece():
    def __init__(self, color: str, type: str, position: Position=None) -> None:
        if position is None:
            self.position = Position(-1,-1)
        else:
            self.position = position
        self.color = color
        self.type = type
        self.moves = [False]
        self.isAlive = True
        
    def __str__(self) -> str: #print info
        return (f'color: {self.color}, type: {self.type}, moves: {self.moves}, isAlive: {self.isAlive}')

class Model():
    def __init__(self) -> None:
        self.whiteTurn = True
        self.currentMove = None
        self.isCheck = False
        self.isCheckmate = False
        self.isStalemate = False
        self.pieceArray = [None] * 32
        for i in range(0, 15):
            if i < 8:
                self.pieceArray[i] = Piece("w", "P", Position(i,1))
            elif i < 16:
                self.pieceArray[i] = Piece("b", "P", Position(i-8,6))

        self.pieceArray[16] = Piece("w", "R", Position(0,0))
        self.pieceArray[17] = Piece("w", "R", Position(7,0))
        self.pieceArray[18] = Piece("b", "R", Position(0,7))
        self.pieceArray[19] = Piece("b", "R", Position(7,7))

        self.pieceArray[20] = Piece("w", "N", Position(1,0))
        self.pieceArray[21] = Piece("w", "N", Position(6,0))
        self.pieceArray[22] = Piece("b", "N", Position(1,7))
        self.pieceArray[23] = Piece("b", "N", Position(6,7))

        self.pieceArray[24] = Piece("w", "B", Position(2,0))
        self.pieceArray[25] = Piece("w", "B", Position(5,0))
        self.pieceArray[26] = Piece("b", "B", Position(2,7))
        self.pieceArray[27] = Piece("b", "B", Position(5,7))

        self.pieceArray[28] = Piece("w", "Q", Position(3,0))
        self.pieceArray[29] = Piece("w", "K", Position(4,0))
        self.pieceArray[30] = Piece("b", "Q", Position(3,7))
        self.pieceArray[31] = Piece("b", "K", Position(4,7))


