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
        n = notation
        pieces = self.m.piece_dict[n[0]]
        targetNotation = n[-2:]
        targetPostition = Position(97 - ord(targetNotation[0]), targetNotation[1])
        l = len(n)
        if l > 3:
            if l == 4:
                file = n[1]
                if file.isdigit():
                    col = file
                    print ('col', targetPostition)
                else:
                    row = 97 - ord(file)
                    print ('row', targetPostition)


        # print('process input pieces', pieces)
        # print(targetPostition)


        
c = Controller(Model())
c.processInput("N7e3")
c.processInput("Pec7")