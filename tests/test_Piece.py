"""
Pytest unit tests for the chess Piece dataclass.
"""
import pytest
from bojio.game_engine.core.Piece import Piece, PieceColors, PieceNames


def test_empty_piece():
    """
    Very simple test to assert that creating a new Piece instance without any
    arguments creates an empty Piece (i.e. no color/identity).
    """
    piece = Piece()
    assert piece.color == PieceColors.EMPTY
    assert piece.name == PieceNames.EMPTY


def test_piece_img_fpaths():
    """
    Ensure that each of the supported chess pieces have a non-empty img_fpath
    attribute, and the img_fpath points to a file that actually exists within
    the repo.
    """

    for color in PieceColors:
        for name in PieceNames:
            piece = Piece(color, name)
            # if color == PieceColors.EMPTY:
