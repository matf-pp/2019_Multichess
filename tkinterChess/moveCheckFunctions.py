# check functions which we will use to make a list of valid moves for each piece
# depending on the current board state

# diagonalCheck and straightsCheck are not hard coded for specific figures since we can use:

# straights check for Rook and Queen (up down letf right any number of tiles)
# diagonal check for Bishop and Queen
# Queens list will be made as ListFromStraightsCheck + ListFromDiagonalCheck

# check functions for pawn, king, knight had to be coded specificaly

# we will call these functions as return values of METHODS of pieces


# lets say board looks like this:

# board is indexed this way


#   0 1 2 3 4 5 6 7

# 0 - - - - - - - -
# 1 - R - - - - - -
# 2 - - - B - - - -
# 3 - X - - - - - -
# 4 - Y - - - X - -
# 5 - - - - - - Y -

# B is bishop, X and Y are some pieces
# we have to make sure that we check diagonal path by incrementing indexes
# and if we come across X on our path, BREAK the loop, coz we cant check Y tile (X is blocking it)
# (same for the pawns if they can make 1 or 2 move (if they are on starting position, and something is right
# in front of them, they cant go on the second tile)
# if X is the opposite color of B, add X tile to the list, otherwise nope
# if there is no piece on the tile we are checking, just add it to the list

# same logic in the straights check (R - X - Y)

def diagonalCheck(Piece, x, y, board):
    list = []

    # down, and to the right check
    for i in range(1, 8):
        # check if tile is out of board bounds
        if x + i >= 8 or y + i >= 8:
            break
        if board.get((x + i, y + i)):
            if board.get((x + i, y + i)).color != Piece.color:
                list.append((x + i, y + i))
            break
        list.append((x + i, y + i))

    # up and to the left (deduce for yourself about the others where they go)
    for i in range(1, 8):
        if x - i < 0 or y - i < 0:
            break
        if board.get((x - i, y - i)):
            if board.get((x - i, y - i)).color != Piece.color:
                list.append((x - i, y - i))
            break
        list.append((x - i, y - i))

    for i in range(1, 8):
        if x + i >= 8 or y - i < 0:
            break
        if board.get((x + i, y - i)):
            if board.get((x + i, y - i)).color != Piece.color:
                list.append((x + i, y - i))
            break
        list.append((x + i, y - i))

    for i in range(1, 8):
        if x - i < 0 or y + i >= 8:
            break
        if board.get((x - i, y + i)):
            if board.get((x - i, y + i)).color != Piece.color:
                list.append((x - i, y + i))
            break
        list.append((x - i, y + i))

    # we return list of possible moves
    return list


def straightsCheck(Piece, x, y, board):
    list = []
    for i in range(x + 1, 8):
        if board.get((i, y)):
            if board.get((i, y)).color != Piece.color:
                list.append((i, y))
            break
        list.append((i, y))

    for i in range(1, x + 1):
        if board.get((x - i, y)):
            if board.get((x - i, y)).color != Piece.color:
                list.append((x - i, y))
            break
        list.append((x - i, y))

    for j in range(y + 1, 8):
        if board.get((x, j)):
            if board.get((x, j)).color != Piece.color:
                list.append((x, j))
            break
        list.append((x, j))

    for j in range(1, y + 1):
        if board.get((x, y - j)):
            if board.get((x, y - j)).color != Piece.color:
                list.append((x, y - j))
            break
        list.append((x, y - j))

    return list

# special checks for special pieces


def kingCheck(Piece, x, y, board):
    list = []
    for elem in [(x+1, y+1), (x+1, y), (x+1, y-1), (x, y+1), (x, y-1), (x-1, y-1), (x-1, y), (x-1, y+1)]:
        if elem[0] >=8 or elem[0] < 0 or elem[1] >= 8 or elem[1] < 0:
            continue
        if board.get(elem):
            if board.get(elem).color != Piece.color:
                list.append(elem)
            continue
        list.append(elem)

    return list


def knightCheck(Piece, x, y, board):
    list = []
    for elem in [(x-2, y-1), (x-2, y+1), (x-1, y-2), (x-1, y+2), (x+1, y-2), (x+1, y+2), (x+2, y-1), (x+2, y+1)]:
        if elem[0] >=8 or elem[0] < 0 or elem[1] >= 8 or elem[1] < 0:
            continue
        if board.get(elem):
            if board.get(elem).color != Piece.color:
                list.append(elem)
            continue
        list.append(elem)

    return list


def pawnCheck(Piece, x, y, board):
    list = []
    if Piece.color == "white":
        # black pieces are UP, and black pawns move TOWARDS BOTTOM ONLY
        if x == 1:     # check if pawn is on the starting position, from which he can go 2 tiles
            for i in range(1,3):
                if x+i >= 8:
                    break
                if board.get((x+i, y)):
                    break
                list.append((x+i, y))
        else:
            if x+1 < 8:
                if board.get((x+1, y)) is None:
                    list.append((x+1, y))

        for elem in [(x+1, y-1), (x+1, y+1)]:
            if elem[0] >= 8 or elem[0] < 0 or elem[1] >= 8 or elem[1] < 0:
                continue
            if board.get(elem) and board.get(elem).color != Piece.color:
                list.append(elem)

    else:
        # white pawns go TOWARDS TOP (index I is decrementing)
        if x == 6:  # check for those on the starting position
            for i in range(1, 3):
                if x-i < 0:
                    break
                if board.get((x - i, y)):
                    break
                list.append((x - i, y))
        else:
            if x - 1 >= 0:
                if board.get((x - 1, y)) is None:
                    list.append((x - 1, y))
        for elem in [(x - 1, y - 1), (x - 1, y + 1)]:
            if elem[0] >= 8 or elem[0] < 0 or elem[1] >= 8 or elem[1] < 0:
                continue
            if board.get(elem) and board.get(elem).color != Piece.color:
                list.append(elem)

    return list
