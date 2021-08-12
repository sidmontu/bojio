"""
Contains all the attributes necessary to implement the chess pieces in the game
engine.
"""

from dataclasses import dataclass, field
from enum import Enum, auto, unique

from bojio.game_engine.utils.exceptions import IllegalPieceException


# Enum of piece/player colors
@unique
class PieceColors(Enum):
    EMPTY = auto()
    BLACK = auto()
    WHITE = auto()


# Enum of chess pieces
@unique
class PieceNames(Enum):
    EMPTY = auto()
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()


# Path to images of chess pieces as stored in assets folder
PieceImagePaths = {
    PieceNames.EMPTY: {PieceColors.EMPTY: ""},
    PieceNames.PAWN: {
        PieceColors.WHITE: "./bojio/game_engine/assets/imgs/w_pawn.png",
        PieceColors.BLACK: "./bojio/game_engine/assets/imgs/b_pawn.png",
    },
    PieceNames.KNIGHT: {
        PieceColors.WHITE: "./bojio/game_engine/assets/imgs/w_knight.png",
        PieceColors.BLACK: "./bojio/game_engine/assets/imgs/b_knight.png",
    },
    PieceNames.BISHOP: {
        PieceColors.WHITE: "./bojio/game_engine/assets/imgs/w_bishop.png",
        PieceColors.BLACK: "./bojio/game_engine/assets/imgs/b_bishop.png",
    },
    PieceNames.ROOK: {
        PieceColors.WHITE: "./bojio/game_engine/assets/imgs/w_rook.png",
        PieceColors.BLACK: "./bojio/game_engine/assets/imgs/b_rook.png",
    },
    PieceNames.QUEEN: {
        PieceColors.WHITE: "./bojio/game_engine/assets/imgs/w_queen.png",
        PieceColors.BLACK: "./bojio/game_engine/assets/imgs/b_queen.png",
    },
    PieceNames.KING: {
        PieceColors.WHITE: "./bojio/game_engine/assets/imgs/w_king.png",
        PieceColors.BLACK: "./bojio/game_engine/assets/imgs/b_king.png",
    },
}

# Value of common chess pieces as commonly known in chess literature
PieceValues = {
    PieceNames.EMPTY: -1,
    PieceNames.PAWN: 1,
    PieceNames.KNIGHT: 3,
    PieceNames.BISHOP: 3,
    PieceNames.ROOK: 5,
    PieceNames.QUEEN: 9,
    PieceNames.KING: 100,  # arbitrarily large value
}


@dataclass(init=True, repr=False, eq=True, order=False, unsafe_hash=False, frozen=True)
class Piece:
    """
    Chess piece dataclass defined by its color and name (or type, e.g. PAWN,
    QUEEN, etc). There are two ways to define equality for pieces:

    (1) Equality tests whether it is the same piece by tuple (color,name). In
    this scenario, there is no natural ordering.

    (2) Equality tests whether the piece-values are equal (e.g. Knight/Bishop
    both have value three). In this case, natural-ordering is possible.

    It is potentially dangerous to mix both types of equalities, so we disable
    natural ordering and restrict equality to testing with (1) above. The first
    equality test is conceptually more natural and useful than restricting
    comparisons to piece values. Piece values can be accessed using the class
    property .value instead.
    """

    _color: PieceColors = field(default=PieceColors.EMPTY)
    _name: PieceNames = field(default=PieceNames.EMPTY)
    _value: int = field(default=-1)
    _img_fpath: str = field(default="")

    def __post_init__(self) -> None:
        """
        Error checks to make sure an illegal piece is not instantiated. If
        check passes, then set path to piece's image path based on its color
        and name, and also sets piece value (integer).
        """

        # instantiate img_fpath to an empty string (for error-reporting)
        super().__setattr__("_img_fpath", "")

        if self._color == PieceColors.EMPTY and self._name != PieceNames.EMPTY:
            raise IllegalPieceException("Illegal piece instantiated: %r" % (self))
        if self._color != PieceColors.EMPTY and self._name == PieceNames.EMPTY:
            raise IllegalPieceException("Illegal piece instantiated: %r" % (self))

        # set img_fpath attribute from the asset library dictionary above
        super().__setattr__("_img_fpath", PieceImagePaths[self._name][self._color])

        # set piece value from the piece values dictionary above
        super().__setattr__("_value", PieceValues[self._name])

    @property
    def name(self) -> PieceNames:
        """
        Make private _name variable accessible as a property
        """
        return self._name

    @property
    def color(self) -> PieceColors:
        """
        Make private _color variable accessible as a property
        """
        return self._color

    @property
    def value(self) -> int:
        """
        Make private _value variable accessible as a property
        """
        return self._value

    @property
    def img_fpath(self) -> str:
        """
        Make private _img_fpath variable accessible as a property
        """
        return self._img_fpath

    def __str__(self) -> str:
        """
        Dunder __str__ method for pretty-printing the Piece
        """
        return str("%s %s" % (self.color.name, self.name.name))

    def __repr__(self) -> str:
        """
        Custom dunder __repr__ method that includes img_fpath attribute.
        """
        return str(
            "Piece(color=%r, name=%r), value=%r, img_fpath=%r" % (self.color, self.name, self.value, self.img_fpath)
        )
