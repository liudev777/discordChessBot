from settings import Position
import model

class Controller():
    def __init__(self) -> None:
        self.count = 0
        pass

    def checkIsValidMove(self):
        pass

    def ping(self):
        self.count += 1
        return self.count
    