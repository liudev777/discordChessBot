from pprint import pp
from model import Model

m = Model()
board = m.board
# board[0][3] = None
# board[0][4] = None
# board[0][5] = None

def toFEN(board): #converts board to FEN
    board = [[board[j][i] for j in range(len(board))] for i in range(len(board[0])-1, -1, -1)]
    pp(board)
    fen = []
    none_count = 0
    for row in board:
        fen_row = []
        for piece in row:
            if piece:
                if none_count:
                    fen_row.append(str(none_count))
                    none_count = 0
                if piece.color == 'w':
                    notation = piece.type.upper()
                elif piece.color == 'b':
                    notation = piece.type.lower()
                fen_row.append(notation)
            else:
                none_count += 1
        if none_count:
            fen_row.append(str(none_count))
            none_count = 0
        fen.append(fen_row)
    return fen

def toURL(board, turn):
    fen = toFEN(board)
    fen = '/'.join([''.join(row) for row in fen])
    # newlist = "/".join(fen)
    if (turn % 2 == 0):
        color = 'w'
    else:
        color = 'b'
    url = f"https://fen2png.com/api/?fen={fen}%20{color}%20-%20-&raw=true"
    return url

