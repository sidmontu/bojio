#!/usr/bin/env python3
"""
Defines function that takes in input board state and outputs all possible legal
moves.
"""

from typing import Dict, List, Tuple

from ch_ss.game_engine.core.piece import Piece, PieceNames
from ch_ss.game_engine.utils.utils import COLUMN_ALPHABETS_IDX


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

    # convert board state to bitboards of each piece
    bitboards_player, bitboards_opp = _state_to_bitboards(state, player_to_move)

    return legal_moves


def _state_to_bitboards(
    state: Dict[str, Piece], player_to_move: str
) -> Tuple[Dict[PieceNames, int], Dict[PieceNames, int]]:
    """
    Converts dictionary board state into bitboards for each piece. Returns two
    dictionaries, where the first one is bitboards of player_to_move, and the
    second one is bitboards of the other player.

    Args:
        state (dict): Board state as a dictionary, where the key is the
        location of the piece, and the value is a Piece object on that
        location.

        player_to_move (str): Player ('black' or 'white') whose turn it is to
        play the next move.

    Returns:
        Dict[PieceNames, int]: Bitboards of all of player_to_move pieces,
        represented as a dictionary where each key is a PieceNames enum, and
        the value is the bitboard represented as a 64-bit integer.

        Dict[PieceNames, int]: Same as the first return above, expect of all
        opponent pieces.
    """

    player_pieces: Dict[PieceNames, int] = {}
    opp_pieces: Dict[PieceNames, int] = {}

    for pos, piece in state.items():
        if piece.color.name.lower() == player_to_move.lower():
            _gen_bitboard(pos, piece.name, player_pieces)
        else:
            _gen_bitboard(pos, piece.name, opp_pieces)

    return player_pieces, opp_pieces


def _gen_bitboard(pos: str, piece_name: PieceNames, player_pieces: Dict[PieceNames, int]):
    """
    Using the piece name enum (e.g. king) and its position, this function
    generates its bitboard integer value and adds it to the player's pieces
    library, which is a dictionary object. If a piece of the same name already
    exists, it updates the bitboard value accordingly such that the bitboard
    captures the positions of all of player's pieces that are of the same type
    (e.g. two knights).

    Args:
        pos (str): Algebraic notation of the piece's position on the board.

        piece_name (PieceNames): Enum of the piece name/type.

        player_pieces (Dict[PieceNames, int]): Library of all player's pieces
        in a dictionary object that is read and updated by this function.

    Returns:
        None
    """

    # Compute the integer for just this piece alone
    mask = 1 << ((int(pos[1]) - 1) * 8 + COLUMN_ALPHABETS_IDX[pos[0]])

    # Check if piece type already exists in player's pieces library
    if piece_name in player_pieces:

        # Bit-wise OR to update the existing bitboard
        player_pieces[piece_name] = player_pieces[piece_name] | mask
    else:
        # Set bitboard to computed mask above
        player_pieces[piece_name] = mask


def _print_bitboard(bitboard: int):
    """
    Pretty-prints bitboard as an 8x8 chess board.

    Args:
        bitboard (int): Bitboard of piece as an integer.

    Returns:
        None
    """
    mask = 0xFF
    v = bitboard
    rows = []
    for _ in range(8):
        rows.append(format(v & mask, "08b")[::-1])
        v = v >> 8
    for i in range(7, -1, -1):
        print(" ".join(list(rows[i])))
