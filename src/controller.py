from requests import post
from settings import Position
from model import Model

class Controller():
    def __init__(self, model: Model) -> None:
        self.m = model
        pass

    def checkIsValidMove(self):
        pass
    
    def processInput(self, notation: str): # reads the input from the discord side and converts it into a command
        validFiles = 'abcdefgh'
        capture = False
        n = notation #ex: Ne4
        origin = None
        rank = None
        file = None
        count = 0

        destinationNotation = n[-2:] #ex: e2
        targetPiece = [] #potential pieces that can move that the destination

        # checks if notation is in bound
        if destinationNotation[0] not in validFiles:
            raise IndexError("invalid destination column")
        if int(destinationNotation[1]) < 1 or int(destinationNotation[1]) > 8:
            raise IndexError("invalid destination row")
        destination = Position(ord(destinationNotation[0]) - 97, int(destinationNotation[1]) - 1) 
        l = len(n) # length of the notation

        if l == 2: #e4
            """
            still deciding if we want to split piece array into b and w
            """
            pieces = [c for p in self.m.piece_dict["P"] for c in p]
            print("pieces:", pieces) #del
            
            for piece in pieces: 
                    if destination in piece.moves:
                        count += 1
                        if count == 2:
                            raise ("ambiguous notation")
                        origin = piece.position
        
        if n[0] in validFiles: #exd5
            for piece in pieces:
                    if piece.position.y == rank or piece.position.x == file:
                        origin = piece.position

        if l >= 3: #Nf3, Rdf8, R1a3, Qh4e1, Bxc6, Rdxf8, R1xa3, Qh4xe1
            pieces = [c for p in self.m.piece_dict[n[0]] for c in p] #ex: 'K'
            print ("pieces2 : ", pieces)
            if n[-3] == "x": #checks if user wants to take, speeds up taking process. If there is no valid piece to take, send error. (Note user doesn't need 'x' to take)
                l -= 1
                capture = True
            if l == 3:
                for piece in pieces: 
                    if destination in piece.moves:
                        count += 1
                        if count == 2:
                            raise ("ambiguous notation")
                        origin = piece.position
            if l == 4:
                if n[1].isnumeric():
                    col = n[1]
                else:
                    row = 97 - ord(n[1])
                for piece in pieces:
                        if piece.position.y == rank or piece.position.x == file:
                            origin = piece.position
            if not origin or origin.x == None or origin.y == None:
                raise ("specified piece doesn't exist")
            if l == 5: #ex: Qc3d4
                origin = Position(ord(n[1]) - 97, int(n[2]) - 1)
                if not m.board[origin.x][origin.y]:
                    raise ("specified piece doesn't exist")
                # add code
        #print("pieces", pieces)
        print(f"origin: {origin}")
        print(f"destination: {destination}")

        #if len(targetPiece) > 2 and l < 4: #checks if only one piece has the destination, otherwise throw error.
        #    raise (f"ambiguous notation, there are multiple {n[0]} pieces that can move to {n[-2:]}!")
        #else:
        #    print(targetPiece)

        # print('process input pieces', pieces)
        # print(targetPostition)


m = Model()
m.calculateAll()
print(m)
c = Controller(m)
c.processInput("e4")
c.processInput("e5")
c.processInput("Nf3")
c.processInput("Nc6")
# c.processInput("Bb5")
# c.processInput("a6")
# c.processInput("Bxc6")

