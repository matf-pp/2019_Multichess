from moveCheckFunctions import straightsCheck
from moveCheckFunctions import diagonalCheck
from moveCheckFunctions import kingCheck
from moveCheckFunctions import knightCheck
from moveCheckFunctions import pawnCheck

# superclass
class Piece:

    def __init__(self, color):
        self.color = color


################################

# uppercase letters for white pieces, lowercase for black pieces

#################################


class Rook(Piece):

    def toString(self):
        if self.color == "white":
            return "R"
        else:
            return "r"

    # method gives us list of available moves, using check functions
    def validMovesList(self, x, y, board):
        return straightsCheck(self, x, y, board)


class Knight(Piece):

    def toString(self):
        if self.color == "white":
            return "K"
        else:
            return "k"

    def validMovesList(self, x, y, board):
        return knightCheck(self, x, y, board)


class Bishop(Piece):

    def toString(self):
        if self.color == "white":
            return "B"
        else:
            return "b"

    def validMovesList(self, x, y, board):
        return diagonalCheck(self, x, y, board)


class Queen(Piece):

    def toString(self):
        if self.color == "white":
            return "Q"
        else:
            return "q"

    # queen uses diagonal and straights check functions and concatenates those lists
    def validMovesList(self, x, y, board):
        return diagonalCheck(self, x, y, board) + straightsCheck(self, x, y, board)


class King(Piece):

    def toString(self):
        if self.color == "white":
            return "W"
        else:
            return "w"

    def validMovesList(self, x, y, board):
        return kingCheck(self, x, y, board)


class Pawn(Piece):

    def toString(self):
        if self.color == "white":
            return "P"
        else:
            return "p"

    def validMovesList(self, x, y, board):
        return pawnCheck(self, x, y, board)


# chessboard will be map with {(i,j) : chessPiece} format
# for example: board = { (1,1) : Rook("white"), (2,4) : Bishop("black") .... }
# better than first attempt: array of arrays, where we had to define each one of 64 tiles
# this way, we dont need to define tiles that contain no chess piece

board = {}


# populate it with figures
for j in range(0, 8):
    board[(1, j)] = Pawn("black")
    board[(6, j)] = Pawn("white")

# using this list so we dont have to put each piece individualy

mainFiguresWhite = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"),
                    Bishop("white"), Knight("white"), Rook("white")]

mainFiguresBlack = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"),
                    Bishop("black"), Knight("black"), Rook("black")]

for j in range(0, 8):
    board[(0, j)] = mainFiguresBlack[j]
    board[(7, j)] = mainFiguresWhite[j]

################################

# display the board
# "-" for empty black tiles, "+" for empty white tiles

for i in range(0, 8):
    for j in range(0, 8):
        # if that board tile contains a chess piece, use its toString method to write it out
        if board.get((i, j)):
            print(board.get((i, j)).toString(), end=" ")
        else:
            # if there is no chess piece, put '-' or '+'
            if (i + j) % 2 == 0:
                print("+", end=" ")
            else:
                print("-", end=" ")
    print()


###############################################################################################
#  OVO MI JE TVRDO KODIRANJE DA BIH PROVERAVAO DA LI SAM DOBRO IMPLEMENTIRAO FUNKCIJE PROVERA ITD
board[(3,4)] = Pawn("white")
board[(2,5)] = Bishop("white")
#######################################################################################
#######################################################################################
# tvrdo kodiranje da proveravam da li mi validMovesList funkcije vracaju dobre rezultate za specificna polja
# moz koristis ovo, i ono iznad da se igras i proveravas

for i in range(0, len(board.get((1,4)).validMovesList(1, 4, board))):
    print("(" + str(board.get((1,4)).validMovesList(1, 4, board)[i][0]) + ", " + str(board.get((1,4)).validMovesList(1, 4, board)[i][1]) + ")", end=" ")