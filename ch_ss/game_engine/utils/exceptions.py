"""
Custom exceptions written here.
"""


class IllegalPieceException(Exception):
    """
    Exception to indicate that an illegal piece has been instantiated.

    e.g. <color = BLACK, name = EMPTY> should raise this exception.
    """

    pass
