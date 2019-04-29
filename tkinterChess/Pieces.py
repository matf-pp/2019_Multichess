from moveCheckFunctions import *


class Piece():
    # we handle the color here, because it is common feature for every piece
    def __init__(self, color, board):
        self.board = board
        self.color = color
        if self.color == "black":
            self.name = self.name.lower()
        else:
            self.name = self.name.upper()


class Rook(Piece):
    name = 'R'

    # method returns list of valid moves depending on the current board state,
    # using functions from moveCheckFunctions
    def validMovesList(self, x, y, board):
        return straightsCheck(self, x, y, board)


class Knight(Piece):
    name = 'N'

    def validMovesList(self, x, y, board):
        return knightCheck(self, x, y, board)


class Bishop(Piece):
    name = 'B'

    def validMovesList(self, x, y, board):
        return diagonalCheck(self, x, y, board)


class King(Piece):
    name = 'K'

    def validMovesList(self, x, y, board):
        return kingCheck(self, x, y, board)

class Queen(Piece):
    name = 'Q'

    def validMovesList(self, x, y, board):
        return diagonalCheck(self, x, y, board) + straightsCheck(self, x, y, board)


class Pawn(Piece):
    name = 'P'

    def validMovesList(self, x, y, board):
        return pawnCheck(self, x, y, board)
