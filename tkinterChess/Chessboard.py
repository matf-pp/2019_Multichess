from tkinterChess.Pieces import *
from copy import deepcopy
import sys

# FEN_PATTERN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w 1'

# class board extends dict type (we are implementing board as dictionary)


class InvalidMove(Exception): pass


class NotYourTurn(Exception): pass


class Check(Exception): pass


class CheckMate(Exception): pass


class Draw(Exception): pass


class Board(dict):

    turn = "white"
    captured_pieces = {'white': [], 'black': []}


    # kingsSafety = {}
    # kingsSafety['white'] = True
    # kingsSafety['black'] = True

    def __init__(self):
        # populate it with figures
        for j in range(0, 8):
            self[(1, j)] = Pawn("white", self)
            self[(6, j)] = Pawn("black", self)

        # using this list so we dont have to put each piece individualy

        mainFiguresWhite = [Rook("white", self), Knight("white", self), Bishop("white", self), Queen("white", self),
                            King("white", self), Bishop("white", self), Knight("white", self), Rook("white", self)]

        mainFiguresBlack = [Rook("black", self), Knight("black", self), Bishop("black", self), Queen("black", self),
                            King("black", self), Bishop("black", self), Knight("black", self), Rook("black", self)]

        for j in range(0, 8):
            self[(0, j)] = mainFiguresWhite[j]
            self[(7, j)] = mainFiguresBlack[j]

    def shift(self, coord1, coord2):
        # no need to check if there is one on coord1, we did that in gui.py
        piece = self[coord1]
        if piece.color != self.turn:
            raise NotYourTurn
        if coord2 not in piece.validMovesList(coord1[0], coord1[1], self):
            raise InvalidMove
        # if u check urself after the move, its invalid move
        # we perform move on the deepcopy of the board, and act accordingly
        boardCopy = deepcopy(self)
        boardCopy.move(coord1, coord2)
        if boardCopy.isInCheck(self.turn):
            raise Check
        if not self.allPossibleMoves(self.turn) and self.isInCheck(self.turn):
            raise CheckMate
        elif not self.allPossibleMoves(self.turn):
            raise Draw
        else:
            self.move(coord1, coord2)

    def move(self, coord1, coord2):
        piece = self[coord1]
        del self[coord1]
        self[coord2] = piece
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    # all available moves for one player (will be used when we check for Check and stuff like that)
    def allPossibleMoves(self, color):
        moves = []
        for (x, y), piece in self.items():
            if piece.color == color:
                moves += piece.validMovesList(x, y, self)
        return moves

    # define occupied(self, color):
    #   result = []
    #   for coord in self:
    #        if self[coord].color == color:
    #            result.append(coord)
    #   return result

    # find the king

    def kingsPositions(self):
        kings = {}
        for position, piece in self.items():
            if type(piece) == King:
                kings[piece.color] = position
        return kings

    def isInCheck(self, color):
        kingPos = self.kingsPositions()[color]
        for (x, y), piece in self.items():
            if kingPos in piece.validMovesList(x, y, self):
                return True
        return False

    # check if any of the pieces has the King of certain color in its list of available moves
    # (if any of the pieces 'sees' opponents king (if its check))
    # and change the kingsSafety dictionary accordingly

    # def isCheck(self, kingsSafety):
    #    kingsSafety['white'] = True
    #    kingsSafety['black'] = True
    #    for kingColor, kingPos in self.kingsPositions().items():
    #        for position, piece in self.items():
    #            if kingPos in piece.validMovesList(position[0], position[1], self):
    #                kingsSafety[kingColor] = False

    # makes the (startX, startY) -> (targetX, targetY) move, checks if its valid
    # if its not, returns the board to its previous state
    # and returns true/false depending on whether the move was made or not

    # def movePiece(self, startX, startY, targetX, targetY, turn, kingsSafety):
    #    tmp = self.get((targetX, targetY))
    #    self[(targetX, targetY)] = self.get((startX, startY))
    #    del self[(startX, startY)]

        # if the player who is on the move revealed his king to opponent, the move is not valid:
        # return pieces as they were and return false

    #   self.isCheck(kingsSafety)
    #    if kingsSafety.get(turn) is False:
    #        self[(startX, startY)] = self[(targetX, targetY)]
    #        if tmp is not None:
    #            self[(targetX, targetY)] = tmp
    #        else:
    #            del self[(targetX, targetY)]
    #        return

        # if the player who is on the move checked opponent, write it out
    #    for color, pos in kingsSafety.items():
    #        if color != turn and kingsSafety[color] is False:
    #            print(color.capitalize() + " check.")

    #    if turn == 'white':
    #        self.turn = 'black'
    #    else:
    #        self.turn = 'white'
        # if everything was okay, return true
    #    return

    # check if there is any valid move for the player whose turn it is,
    # and if not, check if its checkmate, or pat

    # def isCheckMate(self, kingsSafety, turn):
    #    self.isCheck(kingsSafety)
    #    for position, piece in self.items():
    #        if piece.color == turn:
    #            for move in piece.validMovesList(position[0], position[1], self):
                     # use copies, so you dont actually do anything with the board, or kingsSafety dictionary
    #                boardCopy = copy.deepcopy(self)
    #              kingsSafetyCopy = copy.deepcopy(kingsSafety)
    #               if boardCopy.movePiece(position[0], position[1], move[0], move[1], turn, kingsSafetyCopy):
    #                    return "notCheckMate"

    #    if kingsSafety[turn] is True:
    #        return "pat"
    #    return "checkMate"
