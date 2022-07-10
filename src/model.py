from collections import namedtuple
from matplotlib.pyplot import pie
from settings import Position
import numpy as np
from pprint import pp

X_MAX = 8
X_MIN = -1
Y_MAX = 8
Y_MIN = -1

class Piece():
    def __init__(self, color: str, type: str, ver: int, position: Position=None) -> None: 
        if position is None:
            self.position = Position(-1,-1)
        else:
            self.position = position
        self.color = color
        self.type = type
        self.ver = ver
        self.moves = []
        self.isAlive = True
        
    def __str__(self) -> str:
        return (f'color: {self.color}, type: {self.type}, moves: {self.moves}, isAlive: {self.isAlive} position: {self.position}')

    def __repr__(self) -> str:
        return f'{self.color}{self.type}{self.ver}'


class Model():
    def __init__(self) -> None:
        self.whiteTurn = True
        self.currentMove = None
        self.isCheck = False
        self.isCheckmate = False
        self.isStalemate = False
        self.board = [[None for x in range(8)] for y in range(8)]


        """
        we chose to append each piece into their type list so board doesn't have to check all the None types on the board to calculate pieces
        """
        all_pieces = []
        for i in range(16):
            if i < 8:
                all_pieces.append(Piece("w", "P", i+1, Position(i,1)))
            elif i < 16:
                all_pieces.append(Piece("b", "P", i-7, Position(i-8,6)))

        all_pieces.append(Piece("w", "R", 1, Position(0,0)))
        all_pieces.append(Piece("w", "N", 1, Position(1,0)))
        all_pieces.append(Piece("w", "B", 1, Position(2,0)))
        all_pieces.append(Piece("w", "Q", 1, Position(3,0)))
        all_pieces.append(Piece("w", "K", 1, Position(4,0)))
        all_pieces.append(Piece("w", "B", 2, Position(5,0)))
        all_pieces.append(Piece("w", "N", 2, Position(6,0)))
        all_pieces.append(Piece("w", "R", 2, Position(7,0)))

        all_pieces.append(Piece("b", "R", 1, Position(0,7)))
        all_pieces.append(Piece("b", "N", 1, Position(1,7)))
        all_pieces.append(Piece("b", "B", 1, Position(2,7)))
        all_pieces.append(Piece("b", "K", 1, Position(3,7)))
        all_pieces.append(Piece("b", "Q", 1, Position(4,7)))
        all_pieces.append(Piece("b", "B", 2, Position(5,7)))
        all_pieces.append(Piece("b", "N", 2, Position(6,7)))
        all_pieces.append(Piece("b", "R", 2, Position(7,7)))


        self.piece_dict = {
            "P": [],
            "R": [],
            "N": [],
            "B": [],
            "Q": [],
            "K": [],
        }

        for piece in all_pieces:
            self.piece_dict[piece.type].append(piece)

        # iterates through all pieces and places them in board array
        for pieces in self.piece_dict.values():
            for piece in pieces:
                self.board[piece.position.x][piece.position.y] = piece
        
    def __str__(self) -> str:
        return f'{np.matrix(self.board)}'

    def movePiece(self, src: Position, dest: Position):
            if self.board[dest.x][dest.y] != None:
                self.board[dest.x][dest.y].isAlive = False
            self.board[src.x][src.y].position = dest

    def calculateAll(self):
        if self.piece_dict:
            self.calculatePawns(self.piece_dict["P"])
            self.calculateKnights(self.piece_dict["R"])
            self.calculateBishops(self.piece_dict["N"])
            self.calculateRooks(self.piece_dict["B"])
            self.calculateQueens(self.piece_dict["Q"])
            self.calculateKings(self.piece_dict["K"])
                        
    def calculatePawns(self, pieces):
        """
        Plan:
        keep a list of all possible moves made by looping through all the offsets and if it doesn't go out of bound or hits another piece, adds it to the list.
        """
        boardLimit = [-1, 8]

        for piece in pieces:
            curr_pos = piece.position

            forward = 1 if piece.color == "w" else -1 #differentiate white piece from black piece
        
            if not curr_pos.y + forward in boardLimit:
                if not self.board[curr_pos.x][curr_pos.y + forward]:
                    new_pos = Position(curr_pos.x, curr_pos.y + forward)
                    piece.moves.append(new_pos)
                
            # checks for starting position to move 2 spaces
            if piece.color == "w" and piece.position.y == 1 and not self.board[curr_pos.x][curr_pos.y + 2]:
                piece.moves.append(Position(curr_pos.x, curr_pos.y + 2))
            if piece.color == "b" and piece.position.y == 6 and not self.board[curr_pos.x][curr_pos.y - 2]:
                piece.moves.append(Position(curr_pos.x, curr_pos.y - 2))
            
                

    def calculateRooks(self, pieces):
        for piece in pieces:
            position = piece.position
            if position.x < 7:
                for i in range(position.x + 1, X_MAX):
                    if self.board[i][position.y]:
                        break
                    else:
                        piece.moves.append(Position(i, position.y))
            if position.x > 0:    
                for i in range(position.x - 1, X_MIN, -1):
                    if self.board[i][position.y]:
                        break
                    else:
                        piece.moves.append(Position(i, position.y))
            if position.y < 7:
                for i in range(position.y + 1, Y_MAX):
                    if self.board[position.x][i]:
                        break
                    else:
                        piece.moves.append(Position(position.x, i))
            if position.y > 0:
                for i in range(position.y - 1, Y_MIN, -1):
                    if self.board[position.x][i]:
                        break
                    else:
                        piece.moves.append(Position(position.x, i))

    def calculateKnights(self, pieces):
        pass

    def calculateBishops(self, pieces):
        pass

    def calculateQueens(self, pieces):
        self.calculateRooks(pieces)
        self.calculateBishops(pieces)
    
    def calculateKings(self):
        pass

m = Model()
print(m)
pp(m.piece_dict)
