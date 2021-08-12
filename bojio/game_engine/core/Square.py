"""
Contains class description of a square on the chessboard.
"""

from dataclasses import dataclass, field
from bojio.game_engine.core.Piece import Piece, PieceColors, PieceNames


@dataclass(init=True, repr=True, eq=False, order=False, unsafe_hash=False, frozen=False)
class Square:
    """
    Dataclass that defines a square of a chessboard. Each standard chess board
    is made of 64 squares, and each square contains attributes about its
    location, piece, ID, etc.

    Squares should be compared by their xy coordinates, so we write our own
    equality dunder method. There is no natural ordering between squares, so we
    disable ordering.

    Squares are not frozen, since the chess piece on the square can be changed.
    """

    _piece: Piece = field(default=Piece())
    _xy: tuple[int] = field(default=(0, 0))
    _square_id: str = "a1"
    _annotate: bool = False

    def __post_init__(self) -> None:
        """
        Assigns _annotate attribute correctly based on the xy coordinates of
        the square. The annotate property is helpful when printing the board,
        since we only want to print the square_id on select squares to minimize
        clutter.
        """
        self._annotate = True if (self._xy[0] == 0 or self._xy[1] == 0) else False

    def __str__(self) -> str:
        """
        Pretty-print the square, including when the square is empty.
        """
        if self.is_unoccupied():
            return str(
                "[%s,%s] EMPTY SQUARE" % (",".join(map(str, self._xy)), self._square_id)
            )
        return str(
            "[%s,%s] %s %s"
            % (
                ",".join(map(str, self._xy)),
                self._square_id,
                self._piece.color.name,
                self._piece.name.name,
            )
        )

    def __eq__(self, other) -> bool:
        """
        Equality check, makes sure other object is of the right type.
        """
        if not isinstance(other, Square):
            raise TypeError("Cannot compare Square object to object of different type")

        return self._xy == other._xy

    def print(self) -> str:
        """
        Less verbose print of piece currently on this square.
        """
        if self.is_unoccupied():
            return ""
        return str("%s-%s" % (self._piece.color.name, self._piece.name.name))

    def change_piece(self, new_piece: Piece) -> None:
        """
        Changes the piece currently sitting on this square.
        """
        self._piece = new_piece

    def is_unoccupied(self) -> bool:
        """
        Returns true if a non-empty chess piece is on this square, false
        otherwise.
        """
        return self._piece == Piece()  # Piece() creates an "empty-piece"
