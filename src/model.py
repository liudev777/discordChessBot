from collections import namedtuple
from matplotlib.pyplot import pie
from settings import Position
import numpy as np

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
        self.pawns = [None] * 16
        self.knights = [None] * 4
        self.bishops = [None] * 4
        self.rooks = [None] * 4
        self.queens = [None] * 2
        self.kings = [None] * 2
        self.piece_lists = [self.pawns, self.knights, self.bishops, self.rooks, self.queens, self.kings]
        self.board = [[None for x in range(8)] for y in range(8)]

        for i in range(len(self.pawns)):
            if i < 8:
                self.pawns[i] = Piece("w", "P", i+1, Position(i,1))
            elif i < 16:
                self.pawns[i] = Piece("b", "P", i-7, Position(i-8,6))

        self.rooks[0] = Piece("w", "R", 1, Position(0,0))
        self.knights[0] = Piece("w", "N", 1, Position(1,0))
        self.bishops[0] = Piece("w", "B", 1, Position(2,0))
        self.queens[0] = Piece("w", "Q", 1, Position(3,0))
        self.kings[0] = Piece("w", "K", 1, Position(4,0))
        self.bishops[1] = Piece("w", "B", 2, Position(5,0))
        self.knights[1] = Piece("w", "N", 2, Position(6,0))
        self.rooks[1] = Piece("w", "R", 2, Position(7,0))

        self.rooks[2] = Piece("b", "R", 1, Position(0,7))
        self.knights[2] = Piece("b", "N", 1, Position(1,7))
        self.bishops[2] = Piece("b", "B", 1, Position(2,7))
        self.kings[1] = Piece("b", "K", 1, Position(3,7))
        self.queens[1] = Piece("b", "Q", 1, Position(4,7))
        self.bishops[3] = Piece("b", "B", 2, Position(5,7))
        self.knights[3] = Piece("b", "N", 2, Position(6,7))
        self.rooks[3] = Piece("b", "R", 2, Position(7,7))

        self.rooks.append(Piece("w", "R", 3, Position(4,3)))
        self.rooks.append(Piece("b", "R", 4, Position(4,4)))

        # iterates through all pieces and places them in board array
        for pieces in self.piece_lists:
            for piece in pieces:
                self.board[piece.position.x][piece.position.y] = piece
        
    def __str__(self) -> str:
        return f'{np.matrix(self.board)}'

    def movePiece(self, src: Position, dest: Position):
            if self.board[dest.x][dest.y] != None:
                self.board[dest.x][dest.y].isAlive = False
            self.board[src.x][src.y].position = dest

    def calculateAll(self):
        if self.piece_lists:
            self.calculatePawns(self.piece_lists[0])
            self.calculateKnights(self.piece_lists[1])
            self.calculateBishops(self.piece_lists[2])
            self.calculateRooks(self.piece_lists[3])
            self.calculateQueens(self.piece_lists[4])
            self.calculateKings(self.piece_lists[5])
                        
    def calculatePawns(self, pieces):
        """
        Plan:
        keep a list of all possible moves made by looping through all the offsets and if it doesn't go out of bound or hits another piece, adds it to the list.
        """
        for piece in pieces:
            possible_moves = []
            boardLimit = [-1, 8]
            curr_pos = piece.position

            forward = 1 if piece.color == "w" else -1 #differentiate white piece from black piece
            offsets = [(0, forward)] #regular move forward
            specialOffset = [(0, forward * 2)] #move two square at start
            takeOffset = [(-1, forward), (1, forward)] #take diagonally

            for offset in offsets:
                x_inc = offset[0]
                y_inc = offset[1]
                new_pos = Position(curr_pos.x, curr_pos.y)
                print('new_pos', new_pos)
                if self.board[new_pos.x + x_inc][new_pos.y + y_inc]:
                    print("here 2") # delete
                    break
                new_pos = Position(curr_pos.x + x_inc, curr_pos.y + y_inc)
                possible_moves.append(new_pos)
            
        return possible_moves
                

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
        pass
    
    def calculateKings(self):
        pass

test = Model()
print(test)
test.calculateRooks(test.piece_lists[3])
print(test.piece_lists[3][4].moves)