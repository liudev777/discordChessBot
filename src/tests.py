from pprint import pp
from model import Model
from settings import Position
from view import *


m = Model() 
# print(board)
m.movePiece((Position(1,0)), Position(1,2))
m.movePiece((Position(1,1)), Position(3,3))
m.movePiece((Position(7,0)), Position(1,5))
m.movePiece((Position(0,7)), Position(3,2))
m.movePiece((Position(3,1)), Position(5,5))
m.movePiece((Position(4,0)), Position(3,2))
m.movePiece((Position(4,1)), Position(7,4))
m.movePiece((Position(5,1)), Position(5,2))
m.movePiece((Position(7,7)), Position(3,3))

n = Model()

n.movePiece((Position(2,0)), Position(3,2))
n.movePiece((Position(1,1)), Position(3,3))
n.movePiece((Position(2,0)), Position(1,5))
n.movePiece((Position(0,7)), Position(3,2))
n.movePiece((Position(3,3)), Position(5,5))
n.movePiece((Position(4,0)), Position(3,2))
n.movePiece((Position(4,1)), Position(7,4))
n.movePiece((Position(4,2)), Position(5,2))
n.movePiece((Position(7,7)), Position(3,3))

pp(n.board)
print(toURL(toFEN(n.board), 'w'))


# pp(board)

