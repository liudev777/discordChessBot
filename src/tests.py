from pprint import pp
from model import Model
from settings import Position
from view import *


t = Model() 
# print(board)

t.movePiece((Position(1,0)), Position(1,2))
t.movePiece((Position(1,1)), Position(3,3))
t.movePiece((Position(7,0)), Position(1,5))
t.movePiece((Position(0,7)), Position(3,2))
t.movePiece((Position(3,1)), Position(5,5))
t.movePiece((Position(4,0)), Position(3,2))
t.movePiece((Position(4,1)), Position(7,4))
t.movePiece((Position(5,1)), Position(5,2))
t.movePiece((Position(7,7)), Position(3,3))

board = t.board
t.printBoard()
toFEN(t.board)

# pp(board)

