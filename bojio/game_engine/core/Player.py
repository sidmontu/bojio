import copy
import random
import sys
from pprint import pprint
from typing import Callable

from bojio.game_engine.core.Piece import Piece, PieceColors, PieceNames
from bojio.game_engine.utils.utils import COLUMN_ALPHABETS


class Player:
    def __init__(self, name: str, print_board_state_func: Callable[[dict, dict, str, str], None]) -> None:

        self.name = name.lower()
        self.opponent_point_of_view = False
        self.print_board_state_func = print_board_state_func
        self.under_check = False

    def naive(self, moves: list[str]) -> str:
        idx = random.randint(0, len(moves) - 1)
        return moves[idx]

    def capturebot5000(self, moves: list[str]) -> str:
        capture_moves = [move for move in moves if "x" in move]
        if len(capture_moves) > 0:
            idx = random.randint(0, len(capture_moves) - 1)
            return capture_moves[idx]
        else:
            idx = random.randint(0, len(moves) - 1)
            return moves[idx]

    def evaluate_move(self, strategy: str, moves: list[str]) -> str:
        move = ""
        if len(moves) == 0:  # handle checkmate/stalemate
            if self.under_check:
                move = "checkmate"
            else:
                move = "stalemate"
        else:
            # makes a random move
            if strategy == "naive":
                move = self.naive(moves)

            # prioritises capture moves over everything else
            if strategy == "capturebot5000":
                move = self.capturebot5000(moves)

        return move

    def tick(
        self, states: dict, my_pieces: dict, opp_pieces: dict, strategy: str = "naive"
    ) -> tuple[tuple[str, bool], list, str]:

        # see if player is under check
        self.under_check = self.check_if_under_check(my_pieces, opp_pieces)
        if self.under_check:
            print("-> %s is under check!" % (self.name))

        # get all legal moves that player can make in this tick
        moves = self.get_all_legal_moves(states, my_pieces, opp_pieces)

        # make sure only moves that don't end with king in check are legal
        moves = self.filter_moves(moves, my_pieces, opp_pieces)

        # pick a move
        move = self.evaluate_move(strategy, moves)
        assert move != ""

        # update global states based on picked move
        en_passant_offered = self.check_en_passant_offered(move, opp_pieces)
        opp_king_sq = [(key, opp_pieces[key]) for key in opp_pieces if opp_pieces[key].name == PieceNames.KING]
        assert len(opp_king_sq) == 1, f"Error: Unexpected number of opponent kings {len(opp_king_sq)}"

        castling_states = states["castling"]
        if move[0] == "R":  # is a rook move
            sq_from = move[1:3]
            if sq_from == "h8" and castling_states[0]:
                castling_states[0] = False
            if sq_from == "a8" and castling_states[2]:
                castling_states[2] = False
        if move[0] == "K":
            castling_states[1] = False
        if move[0] == "O":  # castling
            castling_states = [False, False, False]

        # return en-passant offered, player's castling vector, and picked move
        return en_passant_offered, castling_states, move

    def check_if_under_check(self, my_pieces: dict, opp_pieces: dict) -> bool:

        squares_attacked_by_opp = self.get_squares_attacked_by_opp(my_pieces, opp_pieces)
        my_king_sq = [key for key in my_pieces if my_pieces[key].name == PieceNames.KING]
        assert len(my_king_sq) == 1, str("Error: Unexpected number of my kings: %d" % (len(my_king_sq)))
        if my_king_sq[0] in squares_attacked_by_opp:
            return True
        return False

    def filter_moves(self, moves: list, my_pieces: dict, opp_pieces: dict) -> list:
        legal_moves = []
        for move in moves:
            my_pieces_copy, opp_pieces_copy = self.soft_execute_move(move, my_pieces, opp_pieces)
            if not self.check_if_under_check(my_pieces_copy, opp_pieces_copy):
                legal_moves.append(move)

        return legal_moves

    def soft_execute_non_pawn_moves(self, move: str, my_pieces: dict, opp_pieces: dict) -> tuple[dict, dict]:
        sq_from = move[1:3]
        if move[3] == "x":
            sq_to = move[4:6]
            del opp_pieces[sq_to]
        else:
            sq_to = move[3:5]
        piece = my_pieces[sq_from]
        del my_pieces[sq_from]
        my_pieces[sq_to] = piece

        return my_pieces, opp_pieces

    def soft_execute_o_o_moves(self, my_pieces: dict) -> dict:
        king_sq = [x for x in my_pieces if my_pieces[x].name == PieceNames.KING]
        assert len(king_sq) == 1, str("Error: Unexpected number of kings = %d" % (len(king_sq)))
        assert king_sq[0][0] == "e", str("Error: Trying O-O, king not on e[x] square! = %s" % (king_sq))
        king_row = int(king_sq[0][1])
        rook_sq = str("h%d" % (king_row))
        assert rook_sq in my_pieces and my_pieces[rook_sq].name == PieceNames.ROOK, str(
            "Error: Trying O-O, rook missing at %s!" % (rook_sq)
        )
        rook = my_pieces[rook_sq]
        king = my_pieces[king_sq[0]]
        del my_pieces[rook_sq]
        del my_pieces[king_sq[0]]
        my_pieces[str("f%d" % (king_row))] = rook
        my_pieces[str("g%d" % (king_row))] = king

        return my_pieces

    def soft_execute_o_o_o_moves(self, my_pieces: dict) -> dict:
        king_sq = [x for x in my_pieces if my_pieces[x].name == PieceNames.KING]
        assert len(king_sq) == 1, str("Error: Unexpected number of kings = %d" % (len(king_sq)))
        assert king_sq[0][0] == "e", str("Error: Trying O-O-O, king not on e[x] square! = %s" % (king_sq))
        king_row = int(king_sq[0][1])
        rook_sq = str("a%d" % (king_row))
        assert rook_sq in my_pieces and my_pieces[rook_sq].name == PieceNames.ROOK, str(
            "Error: Trying O-O-O, rook missing at %s!" % (rook_sq)
        )
        rook = my_pieces[rook_sq]
        king = my_pieces[king_sq[0]]
        del my_pieces[rook_sq]
        del my_pieces[king_sq[0]]
        my_pieces[str("d%d" % (king_row))] = rook
        my_pieces[str("c%d" % (king_row))] = king

        return my_pieces

    def soft_execute_pawn_moves(self, move: str, my_pieces: dict, opp_pieces: dict) -> tuple[dict, dict]:
        color = PieceColors.BLACK if self.name == "black" else PieceColors.WHITE
        promotion_pieces = {
            "Q": Piece(color, PieceNames.QUEEN),
            "R": Piece(color, PieceNames.ROOK),
            "B": Piece(color, PieceNames.BISHOP),
            "N": Piece(color, PieceNames.KNIGHT),
        }

        sq_from = move[0:2]
        if move[2] == "x":
            sq_to = move[3:5]
            if sq_to not in opp_pieces:  # must be an en-passant capture
                pawn_to_capture = str("%s%s" % (sq_to[0], sq_from[1]))
                assert pawn_to_capture in opp_pieces, str(
                    "Error: en-passant capture detected, but pawn-to-capture not found at %s" % (pawn_to_capture)
                )
                del opp_pieces[pawn_to_capture]
            else:
                del opp_pieces[sq_to]
        else:
            sq_to = move[2:4]
        piece = my_pieces[sq_from]  # which must be a pawn
        if "=" in move:  # pawn promotion
            promoted_to = move.split("=")[1]
            piece = promotion_pieces[promoted_to]
        del my_pieces[sq_from]
        my_pieces[sq_to] = piece

        return my_pieces, opp_pieces

    def soft_execute_move(self, move: str, my_pieces: dict, opp_pieces: dict) -> tuple[dict, dict]:
        my_pieces_copy = copy.deepcopy(my_pieces)
        opp_pieces_copy = copy.deepcopy(opp_pieces)
        if move[0] in ["R", "B", "N", "Q", "K"]:  # non-pawn
            my_pieces_copy, opp_pieces_copy = self.soft_execute_non_pawn_moves(move, my_pieces_copy, opp_pieces_copy)
        elif move == "O-O":  # castling move
            my_pieces_copy = self.soft_execute_o_o_moves(my_pieces_copy)
        elif move == "O-O-O":
            my_pieces_copy = self.soft_execute_o_o_o_moves(my_pieces_copy)
        else:  # must be a pawn move
            my_pieces_copy, opp_pieces_copy = self.soft_execute_pawn_moves(move, my_pieces_copy, opp_pieces_copy)

        return my_pieces_copy, opp_pieces_copy

    def check_edge_cases_for_en_passant_offered(self, col: str, row_to: int, opp_pieces: dict):
        key = {"a": f"b{row_to}", "h": f"g{row_to}"}
        if key[col] in opp_pieces:
            if opp_pieces[key[col]].name == PieceNames.PAWN:
                return (col, True)

        return ("x", False)

    def check_non_edge_cases_for_en_passant_offered(self, col: str, row_to: int, opp_pieces: dict):
        idx = COLUMN_ALPHABETS.index(col)
        for c in [-1, 1]:
            key = f"{COLUMN_ALPHABETS[idx + c]}{row_to}"
            if key in opp_pieces:
                if opp_pieces[key].name == PieceNames.PAWN:
                    return (col, True)

        return ("x", False)

    def check_en_passant_offered(self, move: str, opp_pieces: dict) -> tuple[str, bool]:

        # Trivial cases
        if (
            (move in ["checkmate", "stalemate"]) or (move[0] in ["R", "B", "N", "Q", "K", "O"]) or ("x" in move)
        ):  # trivial case
            return ("x", False)

        to_return = ("x", False)
        row_from = int(move[1])
        row_to = int(move[3])
        if abs(row_to - row_from) == 2:  # two steps forward moved
            assert move[2] == move[0], f"Error: Illegal pawn move: {move}"
            col = move[0]
            if col in ["a", "h"]:  # edge-cases
                to_return = self.check_edge_cases_for_en_passant_offered(col, row_to, opp_pieces)
            else:
                to_return = self.check_non_edge_cases_for_en_passant_offered(col, row_to, opp_pieces)

        return to_return

    def get_all_non_king_moves(self, states: dict, my_pieces: dict, opp_pieces: dict) -> tuple[list, list]:

        moves = []
        squares_attacked = []

        # get all legal pawn moves
        pawns = [(key, my_pieces[key]) for key in my_pieces if my_pieces[key].name == PieceNames.PAWN]
        pawn_moves, sq_attacked = self.evaluate_pawn_moves(pawns, opp_pieces, my_pieces, states["en_passant"])
        moves.extend(pawn_moves)
        squares_attacked.extend(sq_attacked)

        # get all legal horsie moves
        knights = [(key, my_pieces[key]) for key in my_pieces if my_pieces[key].name == PieceNames.KNIGHT]
        knight_moves, sq_attacked = self.evaluate_knight_moves(knights, opp_pieces, my_pieces)
        moves.extend(knight_moves)
        squares_attacked.extend(sq_attacked)

        # get all legal bishop moves
        bishops = [(key, my_pieces[key]) for key in my_pieces if my_pieces[key].name == PieceNames.BISHOP]
        bishop_moves, sq_attacked = self.evaluate_bishop_moves(bishops, opp_pieces, my_pieces)
        moves.extend(bishop_moves)
        squares_attacked.extend(sq_attacked)

        # get all legal rook moves
        rooks = [(key, my_pieces[key]) for key in my_pieces if my_pieces[key].name == PieceNames.ROOK]
        rook_moves, sq_attacked = self.evaluate_rook_moves(rooks, opp_pieces, my_pieces)
        moves.extend(rook_moves)
        squares_attacked.extend(sq_attacked)

        # get all legal queen moves
        queens = [(key, my_pieces[key]) for key in my_pieces if my_pieces[key].name == PieceNames.QUEEN]
        queen_moves, sq_attacked = self.evaluate_queen_moves(queens, opp_pieces, my_pieces)
        moves.extend(queen_moves)
        squares_attacked.extend(sq_attacked)

        squares_attacked = list(set(squares_attacked))

        return moves, squares_attacked

    def get_squares_attacked_by_opp(self, my_pieces: dict, opp_pieces: dict) -> list:

        # default out-of-turn opponent states
        opp_states = {
            "en_passant": (
                "x",
                False,
            ),  # en-passant is not an 'attacking' move, no need to calculate out-of-turn
            "castling": [False, False, False],  # no need to compute castling moves
        }
        self.opponent_point_of_view = True  # temporarily enable this
        _, squares_attacked_by_opp = self.get_all_non_king_moves(opp_states, opp_pieces, my_pieces)
        self.opponent_point_of_view = False

        # calculate opponent king moves (while ignoring checks)
        opp_king = [(key, opp_pieces[key]) for key in opp_pieces if opp_pieces[key].name == PieceNames.KING]
        assert len(opp_king) == 1, str("Error: Unexpected number of opponent kings: %d" % (len(opp_king)))
        _, squares_attacked_by_opp_king = self.evaluate_king_moves(
            opp_states, opp_king[0], my_pieces, opp_pieces, [], ignore_checks=True
        )

        squares_attacked_by_opp.extend(squares_attacked_by_opp_king)
        squares_attacked_by_opp = list(set(squares_attacked_by_opp))

        return squares_attacked_by_opp

    def get_all_legal_moves(self, states: dict, my_pieces: dict, opp_pieces: dict) -> list[str]:

        moves, _ = self.get_all_non_king_moves(states, my_pieces, opp_pieces)

        # for calculating king moves, we need to know which squares are currently under attack by opponent
        squares_attacked_by_opp = self.get_squares_attacked_by_opp(my_pieces, opp_pieces)

        # calculate my king moves
        king = [(key, my_pieces[key]) for key in my_pieces if my_pieces[key].name == PieceNames.KING]
        assert len(king) == 1, str("Error: Unexpected number of my kings: %d" % (len(king)))
        king_moves, _ = self.evaluate_king_moves(
            states,
            king[0],
            opp_pieces,
            my_pieces,
            squares_attacked_by_opp,
            ignore_checks=False,
        )
        moves.extend(king_moves)

        return moves

    def evaluate_king_moves(
        self,
        states: dict,
        king: tuple,
        opp_pieces: dict,
        my_pieces: dict,
        protected_squares: list,
        ignore_checks: bool = False,
    ) -> tuple[list, list]:

        moves = []
        squares_attacked = []

        k, piece = king
        col, row = [x for x in k]
        row = int(row)

        possible_moves = [
            (0, 1),
            (0, -1),
            (1, 0),
            (1, 1),
            (1, -1),
            (-1, 0),
            (-1, 1),
            (-1, -1),
        ]
        for move in possible_moves:

            # get index of column alphabet
            col_idx = COLUMN_ALPHABETS.index(col)
            if -1 < (col_idx + move[0]) < 8 and 0 < (row + move[1]) < 9:
                new_loc = str("%s%d" % (COLUMN_ALPHABETS[col_idx + move[0]], row + move[1]))

                if ignore_checks:
                    if new_loc in opp_pieces:
                        moves.append(str("K%s%dx%s" % (col, row, new_loc)))
                    else:
                        moves.append(new_loc)
                    squares_attacked.append(new_loc)
                else:
                    if new_loc not in my_pieces:  # king is free to move there
                        if new_loc not in protected_squares:
                            if new_loc in opp_pieces:
                                moves.append(str("K%s%dx%s" % (col, row, new_loc)))
                            else:
                                moves.append(str("K%s%d%s" % (col, row, new_loc)))
                            squares_attacked.append(new_loc)

        # check castling
        castling_states = states["castling"]
        if not self.under_check:
            if castling_states[0] and castling_states[1]:  # test O-O
                # if these states are true, then king must be on row 1 or row 8
                # king can castle if rooks are under threat
                can_castle = True
                for sq in [str("f%d" % (row)), str("g%d" % (row))]:
                    if (sq in my_pieces) or (sq in opp_pieces) or (sq in protected_squares):
                        can_castle = False
                if can_castle:
                    moves.append("O-O")  # this move doesn't 'attack' squares

            if castling_states[2] and castling_states[1]:  # test O-O-O
                # if these states are true, then king must be on row 1 or row 8
                # king can castle if rooks are under threat
                can_castle = True
                for sq in [str("b%d" % (row)), str("c%d" % (row)), str("d%d" % (row))]:
                    if (sq in my_pieces) or (sq in opp_pieces) or (sq in protected_squares):
                        can_castle = False
                if can_castle:
                    moves.append("O-O-O")  # this move doesn't 'attack' squares

        return moves, squares_attacked

    def evaluate_queen_moves(
        self, queens: list[tuple[str, Piece]], opp_pieces: dict, my_pieces: dict
    ) -> tuple[list, list]:
        moves = []
        squares_attacked = []

        for queen in queens:
            q, _ = queen
            col, row_str = list(q)
            row = int(row_str)

            # get index of column alphabet
            col_idx = COLUMN_ALPHABETS.index(col)

            # test moves
            possible_directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            ]
            for p in possible_directions:
                mult = 1
                while -1 < (col_idx + mult * p[0]) < 8 and 0 < (row + mult * p[1]) < 9:
                    new_loc = str("%s%d" % (COLUMN_ALPHABETS[col_idx + mult * p[0]], row + mult * p[1]))
                    squares_attacked.append(new_loc)

                    # test capture
                    if new_loc in opp_pieces:
                        moves.append(str("Q%s%dx%s" % (col, row, new_loc)))
                        break
                    elif new_loc in my_pieces:
                        break
                    else:
                        moves.append(str("Q%s%d%s" % (col, row, new_loc)))
                        mult += 1

        return moves, squares_attacked

    def evaluate_rook_moves(
        self, rooks: list[tuple[str, Piece]], opp_pieces: dict, my_pieces: dict
    ) -> tuple[list, list]:
        moves = []
        squares_attacked = []

        for rook in rooks:
            r, _ = rook
            col, row_str = list(r)
            row = int(row_str)

            # get index of column alphabet
            col_idx = COLUMN_ALPHABETS.index(col)

            # test moves
            possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for p in possible_directions:
                mult = 1
                while -1 < (col_idx + mult * p[0]) < 8 and 0 < (row + mult * p[1]) < 9:
                    new_loc = str("%s%d" % (COLUMN_ALPHABETS[col_idx + mult * p[0]], row + mult * p[1]))
                    squares_attacked.append(new_loc)

                    # test capture
                    if new_loc in opp_pieces:
                        moves.append(str("R%s%dx%s" % (col, row, new_loc)))
                        break
                    elif new_loc in my_pieces:
                        break
                    else:
                        moves.append(str("R%s%d%s" % (col, row, new_loc)))
                        mult += 1

        return moves, squares_attacked

    def evaluate_bishop_moves(
        self, bishops: list[tuple[str, Piece]], opp_pieces: dict, my_pieces: dict
    ) -> tuple[list, list]:
        moves = []
        squares_attacked = []

        for bishop in bishops:
            b, _ = bishop
            col, row_str = list(b)
            row = int(row_str)

            # get index of column alphabet
            col_idx = COLUMN_ALPHABETS.index(col)

            # test moves
            possible_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for p in possible_directions:
                mult = 1
                while -1 < (col_idx + mult * p[0]) < 8 and 0 < (row + mult * p[1]) < 9:
                    new_loc = str("%s%d" % (COLUMN_ALPHABETS[col_idx + mult * p[0]], row + mult * p[1]))
                    squares_attacked.append(new_loc)  # piece is defending its own piece

                    # test capture
                    if new_loc in opp_pieces:
                        moves.append(str("B%s%dx%s" % (col, row, new_loc)))
                        break
                    elif new_loc in my_pieces:
                        break
                    else:
                        moves.append(str("B%s%d%s" % (col, row, new_loc)))
                        mult += 1

        return moves, squares_attacked

    def evaluate_knight_moves(
        self, knights: list[tuple[str, Piece]], opp_pieces: dict, my_pieces: dict
    ) -> tuple[list, list]:
        moves = []
        squares_attacked = []

        for knight in knights:
            k, _ = knight
            col, row_str = list(k)
            row = int(row_str)

            # get index of column alphabet
            col_idx = COLUMN_ALPHABETS.index(col)

            # test moves
            possible_moves = [
                (1, 2),
                (-1, 2),
                (-2, 1),
                (-2, -1),
                (-1, -2),
                (1, -2),
                (2, -1),
                (2, 1),
            ]
            for move in possible_moves:
                if -1 < (col_idx + move[0]) < 8 and 0 < (row + move[1]) < 9:
                    new_loc = str("%s%d" % (COLUMN_ALPHABETS[col_idx + move[0]], row + move[1]))
                    squares_attacked.append(new_loc)  # piece is defending its own piece

                    # test capture
                    if new_loc in opp_pieces:
                        moves.append(str("N%s%dx%s" % (col, row, new_loc)))
                    elif new_loc not in my_pieces:
                        moves.append(str("N%s%d%s" % (col, row, new_loc)))

        return moves, squares_attacked

    def evaluate_pawn_moves(
        self, pawns: list[tuple[str, Piece]], opp_pieces: dict, my_pieces: dict, en_passant: tuple
    ) -> tuple[list, list]:

        moves = []
        squares_attacked = []

        for pawn in pawns:
            p, _ = pawn
            col, row_str = list(p)
            row = int(row_str)

            assert row not in [1, 8], str("Error: Why is there a pawn on %s?" % (p))

            if self.name == "white":
                direction = 1
            elif self.name == "black":
                direction = -1
            else:
                pprint('Error: Please set player name to "white" or "black", currently: %s' % (self.name))
                sys.exit()

            # flip if looking from opponent's point-of-view
            if self.opponent_point_of_view:
                direction *= -1

            # look one row up
            row += direction

            # get index of column alphabet
            idx = COLUMN_ALPHABETS.index(col)

            # check if pawn can capture
            if idx == 0:  # edge-case: column 'a'
                squares_attacked.append(str("b%d" % (row)))
                if str("b%d" % (row)) in opp_pieces:  # enemy piece on capture square
                    if row in [1, 8]:  # pawn promotion
                        for promoted_piece in ["Q", "B", "N", "R"]:
                            moves.append(str("a%dxb%d=%s" % ((row - direction), row, promoted_piece)))
                    else:
                        moves.append(str("a%dxb%d" % ((row - direction), row)))
            elif idx == 7:  # edge-case: column 'h'
                squares_attacked.append(str("g%d" % (row)))
                if str("g%d" % (row)) in opp_pieces:  # enemy piece on capture square
                    if row in [1, 8]:  # pawn promotion
                        for promoted_piece in ["Q", "B", "N", "R"]:
                            moves.append(str("h%dxg%d=%s" % ((row - direction), row, promoted_piece)))
                    else:
                        moves.append(str("h%dxg%d" % ((row - direction), row)))
            else:
                if str("%s%d" % (COLUMN_ALPHABETS[idx - 1], row)) in opp_pieces:
                    if row in [1, 8]:  # pawn promotion
                        for promoted_piece in ["Q", "B", "N", "R"]:
                            moves.append(
                                str(
                                    "%s%dx%s%d=%s"
                                    % (
                                        col,
                                        (row - direction),
                                        COLUMN_ALPHABETS[idx - 1],
                                        row,
                                        promoted_piece,
                                    )
                                )
                            )
                    else:
                        moves.append(
                            str(
                                "%s%dx%s%d"
                                % (
                                    col,
                                    (row - direction),
                                    COLUMN_ALPHABETS[idx - 1],
                                    row,
                                )
                            )
                        )
                if str("%s%d" % (COLUMN_ALPHABETS[idx + 1], row)) in opp_pieces:
                    if row in [1, 8]:  # pawn promotion
                        for promoted_piece in ["Q", "B", "N", "R"]:
                            moves.append(
                                str(
                                    "%s%dx%s%d=%s"
                                    % (
                                        col,
                                        (row - direction),
                                        COLUMN_ALPHABETS[idx + 1],
                                        row,
                                        promoted_piece,
                                    )
                                )
                            )
                    else:
                        moves.append(
                            str(
                                "%s%dx%s%d"
                                % (
                                    col,
                                    (row - direction),
                                    COLUMN_ALPHABETS[idx + 1],
                                    row,
                                )
                            )
                        )

                squares_attacked.append(str("%s%d" % (COLUMN_ALPHABETS[idx - 1], row)))
                squares_attacked.append(str("%s%d" % (COLUMN_ALPHABETS[idx + 1], row)))

            # special en passant capture
            if en_passant[1]:
                idx_col = COLUMN_ALPHABETS.index(en_passant[0])
                if idx_col in [(idx + 1), (idx - 1)]:
                    if self.name == "white" and row == 6:
                        moves.append(str("%s%dx%s%d" % (col, (row - direction), en_passant[0], row)))
                    if self.name == "black" and row == 3:
                        moves.append(str("%s%dx%s%d" % (col, (row - direction), en_passant[0], row)))

                    # this is kind of irrelevant to calculate for king moves, but added in anyways
                    squares_attacked.append(str("%s%d" % (en_passant[0], row)))

            # check if pawn can move forward
            new_pos = str("%s%d" % (col, row))
            if (new_pos not in opp_pieces) and (new_pos not in my_pieces):  # no piece blocking

                # check promotion
                if row in [1, 8]:  # pawn promotion
                    for promoted_piece in ["Q", "B", "N", "R"]:
                        moves.append(str("%s%d%s%d=%s" % (col, (row - direction), col, row, promoted_piece)))
                else:
                    moves.append(str("%s%d%s%d" % (col, (row - direction), col, row)))

                # if pawn is in the opening rank, it can move forward by two as well
                if row in [3, 6]:
                    new_pos = str("%s%d" % (col, row + direction))
                    if (new_pos not in opp_pieces) and (new_pos not in my_pieces):  # no piece blocking
                        moves.append(str("%s%d%s%d" % (col, (row - direction), col, row + direction)))

        return moves, squares_attacked
