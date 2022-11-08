from ast import Raise
from collections import namedtuple
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
            
            self.canTakes = []
            self.canEnPassant = []
            self.isAlive = True
            
    def __str__(self) -> str:
        return f'{self.color}{self.type}{self.ver}'

    def __repr__(self) -> str:
        return f'{self.color}{self.type}{self.ver}'

    def __del__(self):
        pass


class Model():
    def __init__(self) -> None:
        self.turn = 0
        self.whiteTurn = True
        self.currentMove = None
        self.isCheck = False
        self.isCheckmate = False
        self.isStalemate = False
        self.canCastle = False


        self.wPawns = [None] * 8
        self.wKnights = [None] * 2
        self.wBishops = [None] * 2
        self.wRooks = [None] * 2
        self.wQueens = [None] * 1
        self.wKings = [None] * 1

        self.bPawns = [None] * 8
        self.bKnights = [None] * 2
        self.bBishops = [None] * 2
        self.bRooks = [None] * 2
        self.bQueens = [None] * 1
        self.bKings = [None] * 1

        self.board = [[None for x in range(8)] for y in range(8)]


        """
        we chose to append each piece into their type list so board doesn't have to check all the None types on the board to calculate pieces
        """
        for i in range(len(self.wPawns)):
            if i < 8:
                self.wPawns[i] = Piece("w", "P", i+1, Position(i,1))

        for i in range(len(self.bPawns)):
            if i < 8:
                self.bPawns[i] = Piece("b", "P", i+1, Position(i,6))
           

        self.wRooks[0] = Piece("w", "R", 1, Position(0,0))
        self.wKnights[0] = Piece("w", "N", 1, Position(1,0))
        self.wBishops[0] = Piece("w", "B", 1, Position(2,0))
        self.wQueens[0] = Piece("w", "Q", 1, Position(3,0))
        self.wKings[0] = Piece("w", "K", 1, Position(4,0))
        self.wBishops[1] = Piece("w", "B", 2, Position(5,0))
        self.wKnights[1] = Piece("w", "N", 2, Position(6,0))
        self.wRooks[1] = Piece("w", "R", 2, Position(7,0))

        self.bRooks[0] = Piece("b", "R", 1, Position(0,7))
        self.bKnights[0] = Piece("b", "N", 1, Position(1,7))
        self.bBishops[0] = Piece("b", "B", 1, Position(2,7))
        self.bKings[0] = Piece("b", "K", 1, Position(3,7))
        self.bQueens[0] = Piece("b", "Q", 1, Position(4,7))
        self.bBishops[1] = Piece("b", "B", 2, Position(5,7))
        self.bKnights[1] = Piece("b", "N", 2, Position(6,7))
        self.bRooks[1] = Piece("b", "R", 2, Position(7,7))



        self.piece_dict = {
            "P": [self.wPawns, self.bPawns],
            "R": [self.wRooks, self.bRooks],
            "N": [self.wKnights, self.bKnights],
            "B": [self.wBishops, self.bBishops],
            "Q": [self.wQueens, self.bQueens], 
            "K": [self.wKings, self.bKings]
        }
        # iterates through all pieces and places them in board array
        for coloredPieces in self.piece_dict.values():
            for pieces in coloredPieces:
                for piece in pieces:
                    self.board[piece.position.y][piece.position.x] = piece
        
    def __str__(self) -> str:
        return f'{np.matrix(np.array(self.board).transpose())}'

    def printBoard(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        matrix = self.board
        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    def deletePiece(self, position: Position): #deletes piece at a given position
        try:
            piece = self.board[position.x][position.y]
            if piece == None:
                print("The square is empty")
            else:
                if piece:
                    print(piece)    
                    self.piece_dict[piece.type].remove(piece)
                    self.board[position.x][position.y] = None
        except IndexError:
            print("out of bound range")

    def movePiece(self, src: Position, dest: Position):
            if self.board[dest.x][dest.y] != None:
                self.board[dest.x][dest.y].isAlive = False
            self.board[src.x][src.y].position = dest

    def calculateWhite(self):
        if self.piece_dict:
            self.calculatePawns(self.piece_dict["P"][0])
            self.calculateKnights(self.piece_dict["N"][0])
            self.calculateBishops(self.piece_dict["B"][0])
            self.calculateRooks(self.piece_dict["R"][0])
            self.calculateQueens(self.piece_dict["Q"][0])
            self.calculateKings(self.piece_dict["K"][0])

    def calculateBlack(self):
        if self.piece_dict:
            self.calculatePawns(self.piece_dict["P"][1])
            self.calculateKnights(self.piece_dict["N"][1])
            self.calculateBishops(self.piece_dict["B"][1])
            self.calculateRooks(self.piece_dict["R"][1])
            self.calculateQueens(self.piece_dict["Q"][1])
            self.calculateKings(self.piece_dict["K"][1])
    def calculateAll(self):
        self.calculateWhite()
        self.calculateBlack()

    """
    Plan:
    keep a list of all possible moves made by looping through all the offsets and if it doesn't go out of bound or hits another piece, adds it to the list.
    """                   
    def calculatePawns(self, pieces):
        for piece in pieces:
            piece.canBeEnPassant = False
            curr_pos = piece.position
            forward = 1 if piece.color == "w" else -1 #differentiate white piece from black piece
            new_y = curr_pos.y + forward
            if new_y > MIN and new_y < MAX: # check for out of bound
                try:
                    if self.board[curr_pos.x][new_y] == None: # add to move
                        piece.moves.append(Position(curr_pos.x, new_y))

                    
                    def addDiagonalTake(piece, diag_x, new_y): #checks if the forward diagonal of the pawn contain takable pieces
                        if diag_x > MIN and diag_x < MAX and new_y > MIN and new_y < MAX:
                            if self.board[diag_x][new_y]:
                                if self.board[diag_x][new_y].color != piece.color:
                                    piece.canTakes.append(Position(diag_x, new_y))
                    addDiagonalTake(piece, curr_pos.x + 1, new_y)
                    addDiagonalTake(piece, curr_pos.x - 1, new_y)

                    """
                    enpassant
                    """
                    
            

                except IndexError:
                    raise ("out of board")
            

            # def addEnPassantTake(piece, curr_pos, dir_x):
            #     square = self.board[dir_x][curr_pos.y]
            #     target_square = self.board[dir_x][curr_pos.y + forward]
            #     if square:
            #         if square.color != piece.color and square.type == "P" and square in self.enPassantablePawns:
            #             if target_square == None:
            #                 piece.canEnPassant.append(target_square)


            # if (piece.color == "w" and piece.position.y == 4) or (piece.color == "b" and piece.position.y == 3):
            #     if (piece.position.x-1 > MIN):
            #         addEnPassantTake(piece, curr_pos, piece.position.x-1)
            #     if (piece.position.x+1 < MAX):
            #         addEnPassantTake(piece, curr_pos, piece.position.x+1)
                
        

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
                                piece.canTakes.append(Position(new_x, new_y))  
                                break
                        if not self.board[new_x][new_y]: #add to move if board is empty and increment x y
                            piece.moves.append(Position(new_x, new_y))
                            new_x += rang[0]
                            new_y += rang[1]
                        else:
                            break
                    except:
                        raise ("out of board")

                

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
                            piece.canTakes.append(Position(new_x, new_y))
                    except IndexError:
                        raise ("out of board")

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
                                piece.canTakes.append(Position(new_x, new_y))  
                                break
                        if not self.board[new_x][new_y]: #add to move if board is empty and increment x y
                            piece.moves.append(Position(new_x, new_y))
                            new_x += rang[0]
                            new_y += rang[1]
                        else:
                            break
                    except:
                        raise ("out of board")
            

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
                if not (new_x > MIN and new_x < MAX and new_y > MIN and new_y < MAX): # check for out of bound
                    try:
                        if self.board[new_x][new_y] == None: # add none space to move
                            piece.moves.append(Position(new_x, new_y))
                        elif self.board[new_x][new_y].color != piece.color:
                            piece.canTakes.append(Position(new_x, new_y))  
                            break
                    except IndexError:

                        pass
                        # print('out of bound')


Model().printBoard()
print(Model().board)

"""
TO DO:
update board after every move
"""