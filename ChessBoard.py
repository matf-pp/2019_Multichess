from moveCheckFunctions import straightsCheck
from moveCheckFunctions import diagonalCheck
from moveCheckFunctions import kingCheck
from moveCheckFunctions import knightCheck
from moveCheckFunctions import pawnCheck

import copy

import pygame

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
            return "N"
        else:
            return "n"

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
            return "K"
        else:
            return "k"

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


def createBoard():
    board = {}
    # populate it with figures
    for j in range(0, 8):
        board[(1, j)] = Pawn("black")
        board[(6, j)] = Pawn("white")

    # using this list so we dont have to put each piece individualy

    mainFiguresWhite = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"),
                        Bishop("white"), Knight("white"), Rook("white")]

    mainFiguresBlack = [Rook("black"), Knight("black"), Bishop("black"), King("black"), Queen("black"),
                        Bishop("black"), Knight("black"), Rook("black")]

    for j in range(0, 8):
        board[(0, j)] = mainFiguresBlack[j]
        board[(7, j)] = mainFiguresWhite[j]

    return board
    ################################

# display the board
# "-" for empty black tiles, "+" for empty white tiles


def displayBoard(board):
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


# returns dictionary: {black : position of black king, white : position of white king}

def kingsPositions(board):
    kings = {}
    for position, piece in board.items():
        if type(piece) == King:
            kings[piece.color] = position
    return kings


# check if any of the pieces has the King of certain color in its list of available moves
# (if any of the pieces 'sees' opponents king (if its check))
# and change the kingsSafety dictionary accordingly

def isCheck(board, kingsSafety):
    kingsSafety['white'] = True
    kingsSafety['black'] = True
    for kingColor, kingPos in kingsPositions(board).items():
        for position, piece in board.items():
            if kingPos in piece.validMovesList(position[0], position[1], board):
                kingsSafety[kingColor] = False


# makes the (startX, startY) -> (targetX, targetY) move, checks if its valid
# if its not, returns the board to its previous state
# and returns true/false depending on whether the move was made or not

def movePiece(startX, startY, targetX, targetY, board, turn, kingsSafety):
    tmp = board.get((targetX, targetY))
    board[(targetX, targetY)] = board.get((startX, startY))
    del board[(startX, startY)]

    # if the player who is on the move revealed his king to opponent, the move is not valid:
    # return pieces as they were and return false

    isCheck(board, kingsSafety)
    if kingsSafety.get(turn) is False:
        board[(startX, startY)] = board[(targetX, targetY)]
        if tmp is not None:
            board[(targetX, targetY)] = tmp
        else:
            del board[(targetX, targetY)]
        return False

    # if the player who is on the move checked opponent, write it out
    for color, pos in kingsSafety.items():
        if color != turn and kingsSafety[color] is False:
            print(color.capitalize() + " check.")

    # if everything was okay, return true
    return True


# check if there is any valid move for the player whose turn it is,
# and if not, check if its checkmate, or pat

def isCheckMate(board, kingsSafety, turn):
    isCheck(board, kingsSafety)
    for position, piece in board.items():
        if piece.color == turn:
            for move in piece.validMovesList(position[0], position[1], board):
                # use copies, so you dont actually do anything with the board, or kingsSafety dictionary
                boardCopy = copy.deepcopy(board)
                kingsSafetyCopy = copy.deepcopy(kingsSafety)
                if movePiece(position[0], position[1], move[0], move[1], boardCopy, turn, kingsSafetyCopy):
                    return "notCheckMate"

    if kingsSafety[turn] is True:
        return "pat"
    return "checkMate"


def main():
    turn = "white"

    kingsSafety = {}
    kingsSafety['white'] = True
    kingsSafety['black'] = True

    board = createBoard()

    print("----------------------------------------")

    while True:

        outcome = isCheckMate(board, kingsSafety, turn)
        if outcome == "checkMate":
            print(turn.capitalize() + " loses. Checkmate. GGWP")
            exit()
        elif outcome == "pat":
            print("Pat position. GGWP")
            exit()

        displayBoard(board)

        data = input(turn.capitalize() + " is on the move. Enter data in format: x y X Y for (x, y) -> (X, Y) move\n").split(" ")
        if len(data) != 4:
            print("Invalid number of arguments\n")
            continue

        startX = int(data[0])
        startY = int(data[1])
        targetX = int(data[2])
        targetY = int(data[3])

        if targetY > 7 or targetY < 0 or targetX > 7 or targetX < 0:
            print("Invalid target tile")
            continue

        if board.get((startX, startY)) is None:
            print("Invalid starting tile")
            continue

        if board.get((startX, startY)).color != turn:
            print(turn.capitalize() + " is on the move.")
            continue

        if kingsSafety[turn] is False:
            kings = kingsPositions(board)
            if (startX, startY) != kings[turn]:
                print("Your king is not safe. Play again\n")

        if (targetX, targetY) in board[(startX, startY)].validMovesList(startX, startY, board):
            if movePiece(startX, startY, targetX, targetY, board, turn, kingsSafety) is False:
                print("Invalid move\n")
                continue
        else:
            print("Invalid move\n")
            continue

        if turn == "white":
            turn = "black"
        else:
            turn = "white"

        

main()