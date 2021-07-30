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
