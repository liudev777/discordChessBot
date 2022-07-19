from collections import namedtuple
from matplotlib.pyplot import pie
from settings import Position
import numpy as np
from pprint import pp

MAX = 8
MIN = -1


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

    def __del__(self):
        pass


class Model():
    def __init__(self) -> None:
        self.whiteTurn = True
        self.currentMove = None
        self.isCheck = False
        self.isCheckmate = False
        self.isStalemate = False
        self.canCastle = False

        self.pawns = [None] * 16
        self.knights = [None] * 4
        self.bishops = [None] * 4
        self.rooks = [None] * 4
        self.queens = [None] * 2
        self.kings = [None] * 2

        self.board = [[None for x in range(8)] for y in range(8)]


        """
        we chose to append each piece into their type list so board doesn't have to check all the None types on the board to calculate pieces
        """
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



        self.piece_dict = {
            "P": self.pawns,
            "R": self.rooks,
            "N": self.knights,
            "B": self.bishops,
            "Q": self.queens,
            "K": self.kings,
        }
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

    """
    Plan:
    keep a list of all possible moves made by looping through all the offsets and if it doesn't go out of bound or hits another piece, adds it to the list.
    """                   
    def calculatePawns(self, pieces):
       
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
        offsetRange = [
            (0, 1),
            (0, -1),
            (-1, 0),
            (-1, -0)
        ]
        for piece in pieces:
            curr_pos = piece.position
            for rang in offsetRange:
                new_y = curr_pos.y + rang[1]
                new_x = curr_pos.x + rang[0]
                while True: #loops through empty space until out of bound or hit another piece
                    try:
                        if not (new_x > MIN and new_x < MAX and new_y > MIN and new_y < MAX): # check for out of bound
                            break
                        if self.board[new_x][new_y]: #adds opposite color piece coord into moveset
                            if self.board[new_x][new_y].color != piece.color:
                                print(self.board[new_x][new_y].color)
                                piece.moves.append(Position(new_x, new_y))  
                                break
                        if not self.board[new_x][new_y]: #add to move if board is empty and increment x y
                            piece.moves.append(Position(new_x, new_y))
                            new_x += rang[0]
                            new_y += rang[1]
                        else:
                            break
                    except:
                        break

    def calculateKnights(self, pieces):
        offsetRange = [
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),
            (-1, 2)
        ]
        for piece in pieces:
            curr_pos = piece.position # current position
            for rang in offsetRange:
                new_x = curr_pos.x + rang[0]
                new_y = curr_pos.y + rang[1]
                if new_x > MIN and new_x < MAX and new_y > MIN and new_y < MAX: # check for out of bound
                    try:
                        if self.board[new_x][new_y] == None: # add to move
                            piece.moves.append(Position(new_x, new_y))
                        elif self.board[new_x][new_y].color != piece.color: #add to move is other piece is diff color
                            piece.moves.append(Position(new_x, new_y))
                    except IndexError:
                        pass

    def calculateBishops(self, pieces):
        offsetRange = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1)
        ]
        for piece in pieces:
            curr_pos = piece.position
            for rang in offsetRange:
                new_y = curr_pos.y + rang[1]
                new_x = curr_pos.x + rang[0]
                while True: #loops through empty space until out of bound or hit another piece
                    try:
                        if not (new_x > MIN and new_x < MAX and new_y > MIN and new_y < MAX): # check for out of bound
                            break
                        if self.board[new_x][new_y]: #adds opposite color piece coord into moveset
                            if self.board[new_x][new_y].color != piece.color:
                                print(self.board[new_x][new_y].color)
                                piece.moves.append(Position(new_x, new_y))  
                                break
                        if not self.board[new_x][new_y]: #add to move if board is empty and increment x y
                            piece.moves.append(Position(new_x, new_y))
                            new_x += rang[0]
                            new_y += rang[1]
                        else:
                            break
                    except:
                        break
            

    def calculateQueens(self, pieces):
        self.calculateRooks(pieces)
        self.calculateBishops(pieces)
    
    def calculateKings(self, pieces):
        offsetRange = [
            (-1, -1),
            (-1, 1),
            (1, 1),
            (1, -1),
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0)
        ]
        for piece in pieces:
            curr_pos = piece.position
            for rang in offsetRange:
                new_x = curr_pos.x + rang[0]
                new_y = curr_pos.y + rang[1]
                try:
                    if not self.board[new_x][new_y]:
                        piece.moves.append(Position(new_x, new_y))
                except IndexError:
                    print('out of bound')


            
            

m = Model()
pp(m.piece_dict)
print(m)


"""
TO DO:
update board after every move
"""