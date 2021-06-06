from dataclasses import dataclass, field
from Piece import Piece, PieceColors, PieceNames

@dataclass()
class Square :
    piece: Piece = field(default = Piece())
    xy: tuple[int] = field(default = (0,0))
    square_id: str = 'a1'
    annotate: bool = False

    def __post_init__(self) -> None :
        self.annotate : bool = True if (self.xy[0] == 0 or self.xy[1] == 0) else False

    def change_piece(self, new_piece : Piece) -> None :
        self.piece = new_piece

    def is_unoccupied(self) -> bool :
        return (self.piece == Piece()) # Piece() creates an "empty-piece"

    def __str__(self) -> str :
        if self.is_unoccupied() :
            return str('[%s,%s] EMPTY SQUARE' % (",".join(map(str,self.xy)), self.square_id))
        return str('[%s,%s] %s %s' % (",".join(map(str,self.xy)), self.square_id, self.piece.color.name, self.piece.name.name))

    def print(self) -> str :
        if self.is_unoccupied() :
            return ''
        return str('%s-%s' % (self.piece.color.name, self.piece.name.name))

if __name__ == "__main__" :
    s0 = Square(Piece(PieceColors.BLACK, PieceNames.QUEEN), (3,2))
    s1 = Square(Piece(PieceColors.WHITE, PieceNames.KING))
    s2 = Square()
    s3 = Square()
    s3.change_piece(Piece(PieceColors.BLACK, PieceNames.PAWN))


