"""
Pytest unit tests for the chess Piece dataclass.
"""
from os.path import isfile

import pytest

from bojio.game_engine.core.Piece import Piece, PieceColors, PieceNames, PieceValues
from bojio.game_engine.utils.exceptions import IllegalPieceException


def test_empty_piece():
    """
    Very simple test to assert that creating a new Piece instance without any
    arguments creates an empty Piece (i.e. no color/identity).
    """
    piece = Piece()
    assert piece.color == PieceColors.EMPTY
    assert piece.name == PieceNames.EMPTY


def test_piece_img_fpaths_and_values():
    """
    Ensure that each of the supported chess pieces have a non-empty img_fpath
    attribute, and the img_fpath points to a file that actually exists within
    the repo. Also ensures that each of the supported chess pieces have a
    non-negative integer value.
    """

    for color in PieceColors:
        for name in PieceNames:

            # Empty piece
            if color == PieceColors.EMPTY and name == PieceNames.EMPTY:
                piece = Piece(color, name)
                assert piece.img_fpath == ""
                assert piece.value == -1
                continue

            # Illegal piece -- make sure an exception is raised
            if (color == PieceColors.EMPTY and not name == PieceNames.EMPTY) or (
                not color == PieceColors.EMPTY and name == PieceNames.EMPTY
            ):
                err_str = "Illegal piece instantiated: "
                err_str += f"Piece(color={color!r}, name={name!r}), value=-1, img_fpath=''"
                with pytest.raises(IllegalPieceException) as exception_info:
                    piece = Piece(color, name)
                assert str(exception_info.value) == err_str
            else:  # Rest of the pieces

                piece = Piece(color, name)
                assert piece.img_fpath != ""
                assert isfile(piece.img_fpath)
                assert piece.value > 0


def test_piece_values():
    """
    Test if the piece values are assigned as expected.
    """

    for color in PieceColors:
        for name in PieceNames:
            if color == PieceColors.EMPTY or name == PieceNames.EMPTY:
                continue

            piece = Piece(color, name)
            assert piece.value == PieceValues[name]


def test_piece_print():
    """
    Test that the __str__ method prints expected.
    """
    for color in PieceColors:
        for name in PieceNames:
            if color == PieceColors.EMPTY or name == PieceNames.EMPTY:
                continue

            piece = Piece(color, name)
            assert str(piece) == "%s %s" % (color.name, name.name)
