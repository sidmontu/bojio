# flake8: noqa

#!/usr/bin/env python3
"""
Main class and methods for exploring possible legal moves at varying depths.
"""

import pprint as pp

import attr

from ch_ss.game_engine.core.piece import Piece


@attr.s
class MoveNode:
    """
    Class and method that described a node in the MovesTree tree.

    Args:

    :prior (float) = The prior probability of selecting this state from its
    parent, i.e what was the probability with which this node was selected from
    the parent node above.

    :move_an (str) = Algebraic Notation (AN) of the move (e.g. g4)

    :color (str) = Color of player making the move ('black', or 'white')

    :children (list, default = []) = List of children to this node

    """

    _prior = attr.ib(factory=float)
    _move_an = attr.ib(factory=str)
    _color = attr.ib(factory=str)
    _children = attr.ib(factory=list)

    def __attrs_post_init__(self):
        """
        __post_init__ method to initialize local attributes needed to carry out
        Monte Carlo Tree Search (MCTS) with this node.
        """

        # number of times this state was visited during MCTS. "Good" states are
        # visited more often than "Bad" states
        self._visit_count = 0

        # the total value of this state from all visits
        self._value_sum = 0

        # board state at this node
        self._state = None

    def value(self):
        """
        Returns average value of the node.
        """
        return self._value_sum / self._visit_count

    def ucb_score(self, child):
        """
        Calculates the UCB (Upper Confidence Bound) score of the child.
        """
        prior_score = child._prior * math.sqrt(parent._visit_count) / (child._visit_count + 1)
        if child._visit_count > 0:
            # Value of the child from the perspective of the opponent, which is
            # why it is a negative of the child's value.
            value_score = -child._value()
        else:
            value_score = 0

        return value_score + prior_score


@attr.s
class MovesTree:
    """
    Class and methods to build trees of chess moves up to an input depth.

    Args:

    :color (str) = color of player from whose perspective the tree is built,
    'black' or 'white'

    :depth (int) = depth to which the tree is built to

    :max_delta (int) = maximum difference between combined pieces values of
    each player before search is stopped. Helps to prune the search tree from
    exploring lines that are damaging the player's position significantly. A
    larger value increases the compute time due to the larger search space,
    while too small a value may cause the explorer to miss out on corner-cases
    such as mating patterns that involve queen sacrifices.
    """

    _color = attr.ib(factory=str)
    _depth = attr.ib(default=1)
    _max_delta = attr.ib(default=14.0)

    def __attrs_post_init__(self):
        self._root = MoveNode(1.0, "root", self._color)

    def build_tree(self, all_pieces: list[tuple[str, Piece]]):
        """
        Builds the move tree to _depth whilte pruning the search space using
        the _max_delta heuristic.
        """

        player_pieces = [piece for piece in all_pieces if piece[1].color.name.lower() == self._color.lower()]
        opp_pieces = [piece for piece in all_pieces if piece[1].color.name.lower() != self._color.lower()]

        player_pieces_value = MovesExplorerStandardGame.calc_value(player_pieces)
        opp_pieces_value = MovesExplorerStandardGame.calc_value(opp_pieces)
        starting_difference = player_pieces_value - opp_pieces_value

        # build tree recursively
        def rec(p_pieces: list[tuple[str, Piece]], o_pieces: list[tuple[str, Piece]], depth: int):
            if depth == self._depth:
                return


@attr.s
class MovesExplorerStandardGame:
    """
    Class with static methods that follow the rules of standard chess games to
    evaluate positions and return legal moves.
    """

    @staticmethod
    def get_next_legal_moves(player_pieces: list[tuple[str, Piece]], opp_pieces: list[tuple[str, Piece]]) -> list:
        """
        Gets the next set of legal moves

        Args

        :player_pieces (list[tuple[str,Piece]]) = list of pieces of player
        running this search, where each piece is a tuple of its position
        (string), and the piece object.

        :opp_pieces (list[tuple[str,Piece]]) = list of opponent player's
        pieces, where each piece is a tuple of its position (string), and the
        piece object.
        """

        return []

    @staticmethod
    def calc_value(pieces: list[tuple[str, Piece]]) -> int:
        """
        Calculates sum of all piece values.

        Args:

        :pieces (list[tuple[str, Piece]]): list of pieces , where each piece is
        a tuple of its position (string), and the piece object.
        """
        values = [piece[1].value for piece in pieces]
        return sum(values)
