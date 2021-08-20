#!/usr/bin/env python3
"""
Defines function that takes in input board state and outputs all possible legal
moves.
"""

from typing import Dict, List, Tuple

from ch_ss.game_engine.core.piece import Piece


def gen_moves(
    state: Dict[str, Piece], player_to_move: str, castle_vec: Tuple[bool, bool, bool], last_move: str
) -> List[str]:
    """
    Generates legal moves based on input board state and the player to move.
    The player can only be either 'white' or 'black'.

    Args:

        state (dict): Board state as a dictionary, where the key is the
        location of the piece, and the value is a Piece object on that
        location.

        player_to_move (str): Player ('black' or 'white') whose turn it is to
        play the next move.

        castle_vec (Tuple[bool, bool, bool]): Length-3 tuple of booleans that
        capture the state of castling for the player_to_move. The booleans
        represent the following states, from left-to-right: (O-O rook not
        moved, King not moved, O-O-O rook not moved).

        last_move (str): Last move played, expressed in our custom algebraic
        notation.

    Returns:
        List[str]: List of legal moves the player can make, expresed in our
        custom algebraic notation.
    """

    legal_moves: List[str] = []

    return legal_moves
