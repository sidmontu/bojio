from PIL import Image, ImageDraw, ImageFont
from Square import Square
from Piece import Piece, PieceColors, PieceNames
from pprint import pprint
from utils import COLUMN_ALPHABETS
import re, sys

class Board :
    def __init__(self, board_config : str = 'standard') -> None :
        sqs = {}
        for j in range(8) :
            for i, alphabet in enumerate(COLUMN_ALPHABETS) :
                sq = Square(xy = (7-j,i), square_id = alphabet + str(j+1))
                sqs[alphabet + str(j+1)] = sq
        self.squares = sqs

        if board_config == 'standard' :
            self.init_standard()
        elif board_config == 'empty' :
            pass
        else :
            self.put_piece_by_sid('e2', Piece(PieceColors.EMPTY, PieceNames.EMPTY))
            self.put_piece_by_sid('e4', Piece(PieceColors.WHITE, PieceNames.PAWN))

        # global settings for printing board image
        self.board_len = 800
        self.margin = 10
        self.colors = ['#23de74', '#f7f7d5']
        self.font = ImageFont.truetype("assets/fonts/arial.ttf", 16)

        # calculated settings for printing board image -- don't change this
        self.w, self.h = self.board_len+(self.margin*2), self.board_len+(self.margin*2) # margin 10px each 
        self.square_len = self.board_len / 8

    def init_standard(self) -> None :

        # white/black pawns
        for alphabet in ['a','b','c','d','e','f','g','h'] :
            self.put_piece_by_sid(alphabet + '2', Piece(PieceColors.WHITE, PieceNames.PAWN))
            self.put_piece_by_sid(alphabet + '7', Piece(PieceColors.BLACK, PieceNames.PAWN))

        # white pieces
        self.put_piece_by_sid('a1', Piece(PieceColors.WHITE, PieceNames.ROOK))
        self.put_piece_by_sid('b1', Piece(PieceColors.WHITE, PieceNames.KNIGHT))
        self.put_piece_by_sid('c1', Piece(PieceColors.WHITE, PieceNames.BISHOP))
        self.put_piece_by_sid('d1', Piece(PieceColors.WHITE, PieceNames.QUEEN))
        self.put_piece_by_sid('e1', Piece(PieceColors.WHITE, PieceNames.KING))
        self.put_piece_by_sid('f1', Piece(PieceColors.WHITE, PieceNames.BISHOP))
        self.put_piece_by_sid('g1', Piece(PieceColors.WHITE, PieceNames.KNIGHT))
        self.put_piece_by_sid('h1', Piece(PieceColors.WHITE, PieceNames.ROOK))

        # black pieces
        self.put_piece_by_sid('a8', Piece(PieceColors.BLACK, PieceNames.ROOK))
        self.put_piece_by_sid('b8', Piece(PieceColors.BLACK, PieceNames.KNIGHT))
        self.put_piece_by_sid('c8', Piece(PieceColors.BLACK, PieceNames.BISHOP))
        self.put_piece_by_sid('d8', Piece(PieceColors.BLACK, PieceNames.QUEEN))
        self.put_piece_by_sid('e8', Piece(PieceColors.BLACK, PieceNames.KING))
        self.put_piece_by_sid('f8', Piece(PieceColors.BLACK, PieceNames.BISHOP))
        self.put_piece_by_sid('g8', Piece(PieceColors.BLACK, PieceNames.KNIGHT))
        self.put_piece_by_sid('h8', Piece(PieceColors.BLACK, PieceNames.ROOK))

    def get_pieces_by_color(self, color: str) -> dict :

        pieces = {}
        to_match = PieceColors.WHITE if color == 'white' else PieceColors.BLACK
        for sid, square in self.squares.items() :
            if square.piece.color == to_match :
                pieces[sid] = square.piece

        return pieces

    def get_piece_by_sid(self, sid: str) -> Piece :

        assert sid in self.squares, str('Error: get_pieces_by_sid() called but sid does not exist: %s' % (sid))
        return self.squares[sid].piece

    def clear_square_by_sid(self, square_id: str) -> None :
        self.put_piece_by_sid(square_id, Piece(PieceColors.EMPTY, PieceNames.EMPTY))

    def put_piece_by_sid(self, square_id : str, piece : Piece) -> None :
        self.squares[square_id].change_piece(piece)

    def make_move(self, move: str, color: str) -> None :
        pprint('Attempting to make move %s' % (move))
        if move[0] in ['R','B','N','Q','K'] : # non-pawn moves
            sq_from = move[1:3]
            if move[3] == 'x' :
                sq_to = move[4:6]
            else :
                sq_to = move[3:5]
            piece = self.get_piece_by_sid(sq_from)
            self.clear_square_by_sid(sq_from)
            self.clear_square_by_sid(sq_to)
            self.put_piece_by_sid(sq_to, piece)
        elif move == 'O-O' : # castling move
            row = 8 if color == 'black' else 1
            rsq_from = str('h%d' % (row))
            ksq_from = str('e%d' % (row))
            rsq_to = str('f%d' % (row))
            ksq_to = str('g%d' % (row))
            rook = self.get_piece_by_sid(rsq_from)
            king = self.get_piece_by_sid(ksq_from)
            self.clear_square_by_sid(rsq_from)
            self.clear_square_by_sid(ksq_from)
            self.put_piece_by_sid(rsq_to, rook)
            self.put_piece_by_sid(ksq_to, king)
        elif move == 'O-O-O' :
            row = 8 if color == 'black' else 1
            rsq_from = str('a%d' % (row))
            ksq_from = str('e%d' % (row))
            rsq_to = str('d%d' % (row))
            ksq_to = str('c%d' % (row))
            rook = self.get_piece_by_sid(rsq_from)
            king = self.get_piece_by_sid(ksq_from)
            self.clear_square_by_sid(rsq_from)
            self.clear_square_by_sid(ksq_from)
            self.put_piece_by_sid(rsq_to, rook)
            self.put_piece_by_sid(ksq_to, king)
        else : # must be a pawn move
            sq_from = move[0:2]
            piece = self.get_piece_by_sid(sq_from)
            if '=' in move : # pawn promotion
                promoted_to = move.split('=')[1]
                color = PieceColors.BLACK if color == 'black' else PieceColors.WHITE
                if promoted_to == 'Q' :
                    piece = Piece(color, PieceNames.QUEEN)
                elif promoted_to == 'R' :
                    piece = Piece(color, PieceNames.ROOK)
                elif promoted_to == 'B' :
                    piece = Piece(color, PieceNames.BISHOP)
                elif promoted_to == 'N' :
                    piece = Piece(color, PieceNames.KNIGHT)
                else :
                    print('Error: unknown piece to promote pawn to: %s' % (promoted_to))
                    sys.exit()

            if move[2] == 'x' :
                sq_to = move[3:5]
                captured_piece = self.get_piece_by_sid(sq_to)
                if captured_piece.name == PieceNames.EMPTY : # must be an en-passant capture
                    pawn_to_capture = str('%s%s' % (sq_to[0],sq_from[1]))
                    assert self.get_piece_by_sid(pawn_to_capture).name == PieceNames.PAWN, str('Error: en-passant capture detected, but pawn-to-capture not found at %s' % (pawn_to_capture))
                    self.clear_square_by_sid(sq_from)
                    self.clear_square_by_sid(pawn_to_capture)
                    self.put_piece_by_sid(sq_to, piece)
                else :
                    self.clear_square_by_sid(sq_from)
                    self.clear_square_by_sid(sq_to)
                    self.put_piece_by_sid(sq_to, piece)
            else :
                sq_to = move[2:4]
                self.clear_square_by_sid(sq_from)
                self.clear_square_by_sid(sq_to)
                self.put_piece_by_sid(sq_to, piece)

    def to_image(self, out_file : str = 'board_position.jpg', flipped : bool = False) -> None :

        # global settings
        board_len, margin, colors, font = self.board_len, self.margin, self.colors, self.font

        # calculated settings
        w, h, square_len = self.w, self.h, self.square_len

        # creating new Image object
        img = Image.new("RGB", (w, h), (255,255,255,0))
        d = ImageDraw.Draw(img)

        # create board with pieces
        row = margin
        col = margin
        c = 1

        for square_id, square in self.squares.items() :

            # calculate (x,y) coordinates, and colors
            i, j = square.xy
            if flipped :
                top_left_x = margin + (7-j) * square_len
                top_left_y = margin + (7-i) * square_len
            else :
                top_left_x = margin + j * square_len
                top_left_y = margin + i * square_len
            color = colors[0] if ((i+j)%2) else colors[1]
            shape = [(top_left_x, top_left_y), (top_left_x + square_len, top_left_y + square_len)]

            # draw the rectangle
            d.rectangle(shape, fill = color, outline = "black")

            # paste piece image on the square
            if not square.is_unoccupied() :
                # load the piece image and get the size of the image
                piece_img = Image.open(square.piece.img_fpath)
                px, py = piece_img.size

                # we need to resize it programmatically, since each piece has different height/width
                ratio = py/70
                px, py = int(px/ratio), 70
                piece_img = piece_img.resize((px,py))

                # calculate the location of the piece based on current square and piece image's height/width
                loc_x = int(top_left_x+(square_len/2)-int(px/2))
                loc_y = int(top_left_y+(square_len/2)-int(py/2))
                img.paste(piece_img, (loc_x, loc_y), mask = piece_img)

            # write square ids in the corner squares
            char = 'h' if flipped else 'a'
            num = '8' if flipped else '1'
            if num in square_id :
                text = re.sub(num, '', square_id)
                loc_x = top_left_x + 5
                loc_y = top_left_y + square_len - 20
                d.text((loc_x,loc_y), text, '#3b3b3b', font = font)
            if char in square_id :
                text = re.sub(char, '', square_id)
                loc_x = top_left_x + 5
                loc_y = top_left_y + 5
                d.text((loc_x,loc_y), text, '#3b3b3b', font = font)

        # save the image
        img.save(out_file)

if __name__ == "__main__" :
    board = Board()
    board.to_image(flipped = False)

