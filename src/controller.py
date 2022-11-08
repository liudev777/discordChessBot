from requests import post
from settings import Position
from model import Model

class Controller():
    def __init__(self, model: Model) -> None:
        self.m = model
        pass

    def checkIsValidMove(self):
        pass
    
    def processInput(self, notation: str):
        validNotation = 'abcdefgh'
        n = notation #ex: Pe4
        targetNotation = n[-2:] #ex: e4
        if targetNotation[0] not in validNotation:
            raise IndexError("invalid row")
        if int(targetNotation[1]) < 1 or int(targetNotation[1]) > 8:
            raise IndexError("invalid column")
        targetPostition = Position(ord(targetNotation[0]) - 97, int(targetNotation[1]) - 1)
        l = len(n)
        if l == 2:
            pieces = self.m.piece_dict["P"]
        if l >= 3:
            pieces = self.m.piece_dict[n[0]] #ex: 'N'
            if l == 4:
                file = n[1]
                if file.isdigit():
                    col = file
                    print ('col', targetPostition)
                else:
                    row = 97 - ord(file)
                    print ('row', targetPostition)
        targetPiece = []
        print("pieces", pieces)
        for piece in pieces:
            if targetPostition in piece.moves:
                print("------contains move!!!------")
                targetPiece.append(piece)

        if len(targetPiece) > 2 and l < 4:
            raise (f"invalid notation, there are multiple {n[0]} pieces that can move to {n[-2:]}!")
        else:
            print(targetPiece)

        # print('process input pieces', pieces)
        # print(targetPostition)


m = Model()
m.calculateAll()
print(m)
c = Controller(m)
c.processInput("e3")
c.processInput("e4")

