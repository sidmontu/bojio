"""
Pytest unit tests for the Square dataclass.
"""
import pytest

from ch_ss.game_engine.core.piece import Piece, PieceColors, PieceNames
from ch_ss.game_engine.core.square import Square


def test_square_init():
    """
    Tests basic square init.
    """

    sq = Square()
    assert sq.piece == Piece()
    assert sq.x_y == (0, 0)
    assert sq.square_id == "a1"
    assert sq.annotate


def test_square_annotate():
    """
    Only first row and first column should have annotate set to true.
    """
    for x, p in enumerate(["a", "b", "c", "d", "e", "f", "g", "h"]):
        for y in range(1, 9):
            sq = Square(Piece(PieceColors.BLACK, PieceNames.PAWN), (x, y), f"{p}{y}")
            if x == 0 or y == 0:
                assert sq.annotate
            else:
                assert not sq.annotate


def test_square_equality():
    """
    Test square equality is only based off x_y coords.
    """

    sq0 = Square(Piece(PieceColors.BLACK, PieceNames.PAWN), (0, 3), "a3")
    sq1 = Square(Piece(PieceColors.WHITE, PieceNames.PAWN), (0, 3), "a4")
    assert sq0 == sq1

    sq2 = Square(Piece(PieceColors.BLACK, PieceNames.PAWN), (1, 3), "a3")
    assert sq0 != sq2

    # Test that comparing Square to another class object raises TypeError
    with pytest.raises(TypeError) as exception_info:
        _ = sq0 == Piece()
    assert str(exception_info.value) == "Cannot compare Square object to object of different type"


def test_square_is_unoccupied():
    """
    Test that .is_unoccupied() method works.
    """
    sq0 = Square(Piece(PieceColors.EMPTY, PieceNames.EMPTY), (0, 3), "a3")
    assert sq0.is_unoccupied()

    sq1 = Square(Piece(PieceColors.BLACK, PieceNames.PAWN), (0, 3), "a3")
    assert not sq1.is_unoccupied()


def test_square_change_piece():
    """
    Test that .change_piece() method works.
    """

    sq = Square(Piece(PieceColors.EMPTY, PieceNames.EMPTY), (0, 3), "a3")

    new_piece = Piece(PieceColors.BLACK, PieceNames.QUEEN)
    sq.change_piece(new_piece)

    assert sq.piece == new_piece


def test_square_print():
    """
    Test that __str__() and .print() methods return expected strings.
    """

    sq = Square(Piece(PieceColors.EMPTY, PieceNames.EMPTY), (0, 3), "a3")

    assert sq.print() == ""
    assert str(sq) == "[0,3,a3] EMPTY SQUARE"

    sq = Square(Piece(PieceColors.WHITE, PieceNames.KING), (0, 3), "a3")
    assert sq.print() == "WHITE-KING"
    assert str(sq) == "[0,3,a3] WHITE KING"
