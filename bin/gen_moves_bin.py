#!/usr/bin/env python3
"""
Binary for running the gen_moves function.
"""

from ch_ss.game_engine.core.piece import Piece, PieceColors, PieceNames
from ch_ss.game_engine.utils.gen_moves import gen_moves


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

    # Create board state as a dictionary
    board_state = {
        "a8": Piece(PieceColors.BLACK, PieceNames.ROOK),
        "c1": Piece(PieceColors.WHITE, PieceNames.BISHOP),
        "d2": Piece(PieceColors.WHITE, PieceNames.PAWN),
        "d4": Piece(PieceColors.WHITE, PieceNames.KNIGHT),
        "d5": Piece(PieceColors.BLACK, PieceNames.KNIGHT),
        "e1": Piece(PieceColors.WHITE, PieceNames.KING),
        "e8": Piece(PieceColors.BLACK, PieceNames.KING),
        "f7": Piece(PieceColors.BLACK, PieceNames.PAWN),
    }

    # Specify players' castling states
    # black_castle_vec = (False, True, True)
    white_castle_vec = (False, False, False)

    # Specify player to move
    player_to_move = "white"

    # Specify last move of opponent (black)
    last_move = "Nb6d5"

    # Run gen_moves()
    legal_moves = gen_moves(board_state, player_to_move, white_castle_vec, last_move)

    print(f"Found {len(legal_moves)} legal moves.")


if __name__ == "__main__":
    _main()
