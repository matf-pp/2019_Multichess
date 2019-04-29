from tkinter import *
from PIL import ImageTk
from tkinterChess.Chessboard import Board
import sys


class GUI:
    # data for our chess board gui
    rows = 8
    columns = 8
    color1 = 'linen'
    color2 = 'dark goldenrod'
    highlightcolor = 'yellow'
    # dimension of chess tile
    dim = 60
    images = {}

    # we will keep track of remaining pieces on board, piece selected by the mouse click
    # and list of possible moves for selected piece
    pieces = {}
    selectedPiece = None
    focused = None

    # root is passed so we can create Canvas within it
    # in the main function, root will be our Tk() window
    def __init__(self, root, board):
        self.root = root
        self.chessboard = board
        # dimensions of Canvas (num of tiles * size of tile)
        canvasHeight = self.rows * self.dim
        canvasWidth = self.columns * self.dim
        # we use canvas widget as container for tiles and pieces
        # canvas provides the ability to do stuff based on mouse clicks etc
        self.canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
        # packs the canvas into the root window
        self.canvas.pack()
        # call the drawBoard and drawPieces when initializing GUI
        self.drawBoard()
        self.drawPieces()
        # event handler: bind the left click, which we will use to move pieces (to invoke tile_clicked method)
        self.canvas.bind('<Button 1>', self.tileClicked)

    def drawBoard(self):
        color = self.color1
        for i in range(0, 8):
            if color == self.color1:
                color = self.color2
            else:
                color = self.color1
            for j in range(0, 8):
                x1 = j * self.dim
                y1 = (7 - i) * self.dim
                x2 = x1 + self.dim
                y2 = y1 + self.dim

                if self.focused is not None and (i, j) in self.focused:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.highlightcolor, tags='tile')
                # create_rectangle(x1, y1, x2, y2) where (x1,y1) and (x2,y2) are diagonal points in our tile
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags='tile')

                # change color everytime in J loop, and I loop
                if color == self.color1:
                    color = self.color2
                else:
                    color = self.color1

        #for name in self.pieces:
        #    #self.pieces[name] = (self.pieces[name][0], self.pieces[name][1])
        #    x0 = (self.pieces[name][1] * self.dim) + int(self.dim / 2)
        #    y0 = ((7 - self.pieces[name][0]) * self.dim) + int(self.dim / 2)
        #    self.canvas.coords(name, x0, y0)
        #self.canvas.tag_raise('occupied')
        #self.canvas.tag_lower('tile')



            # NEDOVRSENO

    def drawPieces(self):
        self.canvas.delete("occupied")
        for (x, y), piece in self.chessboard.items():
            filename = "../tkinterChess/Artwork/%s%s.png" % (piece.name.upper(), piece.color[0].upper())
            # piecename = ex. R01 (white rook, (0, 1)) or n23 (black knight, (2, 3))
            piecename = "%s%s%s" % (piece.name, x, y)
            if filename not in self.images:
                # add images to the map in format: {...path/BK.png : ImageTk.image}
                self.images[filename] = ImageTk.PhotoImage(file=filename)
            # anchor the image we create to the center ('C'), tag it with piecename, and 'occupied'
            # we use tags to adjust elements on canvas
            self.canvas.create_image(0, 0, image=self.images[filename], tags=(piecename, 'occupied'), anchor='c')
            x0 = (y * self.dim) + int(self.dim / 2)
            y0 = ((7 - x) * self.dim) + int(self.dim / 2)
            #self.pieces[piecename] = (x, y)
            # changes the starting throwaway coords of object with tag PIECENAME (which is string B02 or r12)
            # (which is our image) to the calculated coords
            self.canvas.coords(piecename, x0, y0)

    def tileClicked(self, event):
        colSize = rowSize = self.dim
        selectedColumn = int(event.x / colSize)
        selectedRow = 7 - int(event.y / rowSize)
        coord = (selectedRow, selectedColumn)
        # try - except block - if user click on a tile with a piece, assing it to 'piece'
        #try:
        #    piece = self.chessboard[coord]
        #except:
        #    pass
        # we need to deal with 2 possible 'clicks'
        # 1. if there is no selected piece, click is selecting the piece which user wants to play with
        # 2. if there is selected piece, click chooses the targeted tile
        # we stored this info in pieces, selectedPiece, possibleMoves in GUI class
        if self.selectedPiece:
            self.shift(self.selectedPiece[1], coord)
            self.selectedPiece = None
            self.focused = None
            self.pieces = {}
            self.drawBoard()
            self.drawPieces()
        # else: ??
        self.focus(coord)
        # why this call? to highlight possible moves? draw fresh board? why?
        self.drawBoard()
        self.drawPieces()

    def shift(self, coord1, coord2):
        piece = self.chessboard[coord1]
        try:
            target = self.chessboard[coord2]
        except:
            target = None
        if target is None or target.color != piece.color:
            try:
                # implementiraj shift metod za board klasu
                self.chessboard.shift(coord1, coord2)
            except:
                pass

    def focus(self, pos):
        try:
            piece = self.chessboard[pos]
        except:
            piece = None
        if piece is not None and (piece.color == self.chessboard.turn):
            self.selectedPiece = (self.chessboard[pos], pos)
            self.focused = piece.validMovesList(pos[0], pos[1], self.chessboard)


def main():
    # create root window, and GUI (which will, by the definition of GUI constructor method)
    # call the drawBoard method
    root = Tk()
    root.title("Multichess")
    gui = GUI(root, Board())
    root.mainloop()

# if our program is called from other .py file, it will execute main()
if __name__ == "__main__":
    main()

# The FEN record for starting position of a chess game is written as:
# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
