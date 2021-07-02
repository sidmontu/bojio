from enum import Enum, auto, unique
from dataclasses import dataclass, field

@unique
class PieceColors(Enum) :
    EMPTY = auto()
    BLACK = auto()
    WHITE = auto()

@unique
class PieceNames(Enum) :
    EMPTY = auto()
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

PieceImagePaths = {
    PieceNames.EMPTY : {
        PieceColors.EMPTY : ''
    },
    PieceNames.PAWN : {
        PieceColors.WHITE: './assets/imgs/w_pawn.png',
        PieceColors.BLACK: './assets/imgs/b_pawn.png'
    },
    PieceNames.KNIGHT : {
        PieceColors.WHITE: './assets/imgs/w_knight.png',
        PieceColors.BLACK: './assets/imgs/b_knight.png'
    },
    PieceNames.BISHOP : {
        PieceColors.WHITE: './assets/imgs/w_bishop.png',
        PieceColors.BLACK: './assets/imgs/b_bishop.png'
    },
    PieceNames.ROOK : {
        PieceColors.WHITE: './assets/imgs/w_rook.png',
        PieceColors.BLACK: './assets/imgs/b_rook.png'
    },
    PieceNames.QUEEN : {
        PieceColors.WHITE: './assets/imgs/w_queen.png',
        PieceColors.BLACK: './assets/imgs/b_queen.png'
    },
    PieceNames.KING : {
        PieceColors.WHITE: './assets/imgs/w_king.png',
        PieceColors.BLACK: './assets/imgs/b_king.png'
    }
}

@dataclass()
class Piece :
    color: PieceColors = field(default = PieceColors.EMPTY)
    name: PieceNames = field(default = PieceNames.EMPTY)

    def __post_init__(self) -> None :
        self.img_fpath = PieceImagePaths[self.name][self.color]

    def __str__(self) -> str :
        return str('%s %s' % (self.color.name, self.name.name))

