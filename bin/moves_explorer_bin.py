#!/usr/bin/env python3

"""
Binary for testing/developing with the MovesExplorer class.
"""

from ch_ss.game_engine.core.moves_explorer import MovesTree
from ch_ss.game_engine.core.piece import Piece, PieceColors, PieceNames


def _main():
    """
    e.g. board configuration:

         ___ ___ ___ ___ ___ ___ ___ ___
        |BR |   |   |   |BK |   |   |   |
      8 |___|___|___|___|___|___|___|___|
        |   |   |   |   |   |BP |   |   |
      7 |___|___|___|___|___|___|___|___|
        |   |   |   |   |   |   |   |   |
      6 |___|___|___|___|___|___|___|___|
        |   |   |   |BN |   |   |   |   |
      5 |___|___|___|___|___|___|___|___|
        |   |   |   |WN |   |   |   |   |
      4 |___|___|___|___|___|___|___|___|
        |   |   |   |   |   |   |   |   |
      3 |___|___|___|___|___|___|___|___|
        |   |   |   |WP |   |   |   |   |
      2 |___|___|___|___|___|___|___|___|
        |   |   |WB |   |WK |   |   |   |
      1 |___|___|___|___|___|___|___|___|
          a   b   c   d   e   f   g   h

    """

    player_color = "white"
    player_pieces = [
        ("e1", Piece(PieceColors.WHITE, PieceNames.KING)),
        ("c1", Piece(PieceColors.WHITE, PieceNames.BISHOP)),
        ("d2", Piece(PieceColors.WHITE, PieceNames.PAWN)),
        ("d4", Piece(PieceColors.WHITE, PieceNames.KNIGHT)),
    ]
    opp_pieces = [
        ("e8", Piece(PieceColors.BLACK, PieceNames.KING)),
        ("a8", Piece(PieceColors.BLACK, PieceNames.ROOK)),
        ("f7", Piece(PieceColors.BLACK, PieceNames.PAWN)),
        ("d5", Piece(PieceColors.BLACK, PieceNames.KNIGHT)),
    ]

    all_pieces = player_pieces + opp_pieces

    moves_tree = MovesTree(player_color, depth=1, max_delta=14.0)
    print(moves_tree)
    moves_tree.build_tree(all_pieces)
