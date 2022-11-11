from dataclasses import dataclass

@dataclass
class Position:
    x: int
    y: int

    # def __eq__(self, other) -> bool:
        # return other.x == self.x and other.y == self.y

    # def getX(self):
    #     return int(self.x)
    # def getY(self):
    #     return int(self.y)