"""
Contains class description of a square on the chessboard.
"""

from dataclasses import dataclass, field

from ch_ss.game_engine.core.piece import Piece


@dataclass(init=True, repr=True, eq=False, order=False, unsafe_hash=False, frozen=False)
class Square:
    """
    Dataclass that defines a square of a chessboard. Each standard chess board
    is made of 64 squares, and each square contains attributes about its
    location, piece, ID, etc.

    Squares should be compared by their x_y coordinates, so we write our own
    equality dunder method. There is no natural ordering between squares, so we
    disable ordering.

    Squares are not frozen, since the chess piece on the square can be changed.
    """

    piece: Piece = field(default=Piece())
    x_y: tuple[int, int] = field(default=(0, 0))
    square_id: str = "a1"
    annotate: bool = False

    def __post_init__(self) -> None:
        """
        Assigns _annotate attribute correctly based on the x_y coordinates of
        the square. The annotate property is helpful when printing the board,
        since we only want to print the square_id on select squares to minimize
        clutter.
        """
        self.annotate = self.x_y[0] == 0 or self.x_y[1] == 0

    def __str__(self) -> str:
        """
        Pretty-print the square, including when the square is empty.
        """
        if self.is_unoccupied():
            return str("[%s,%s] EMPTY SQUARE" % (",".join(map(str, self.x_y)), self.square_id))
        return str(
            "[%s,%s] %s %s"
            % (
                ",".join(map(str, self.x_y)),
                self.square_id,
                self.piece.color.name,
                self.piece.name.name,
            )
        )

    def __eq__(self, other) -> bool:
        """
        Equality check, makes sure other object is of the right type.
        """
        if not isinstance(other, Square):
            raise TypeError("Cannot compare Square object to object of different type")

        return self.x_y == other.x_y

    def print(self) -> str:
        """
        Less verbose print of piece currently on this square.
        """
        if self.is_unoccupied():
            return ""
        return str("%s-%s" % (self.piece.color.name, self.piece.name.name))

    def change_piece(self, new_piece: Piece) -> None:
        """
        Changes the piece currently sitting on this square.
        """
        self.piece = new_piece

    def is_unoccupied(self) -> bool:
        """
        Returns true if a non-empty chess piece is on this square, false
        otherwise.
        """
        return self.piece == Piece()  # Piece() creates an "empty-piece"
