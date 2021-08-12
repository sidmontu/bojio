from bojio.game_engine.core.Piece import Piece, PieceColors, PieceNames

piece = Piece(PieceColors.BLACK, PieceNames.PAWN)
piece1 = Piece(PieceColors.BLACK, PieceNames.PAWN)
piece2 = Piece(PieceColors.WHITE, PieceNames.PAWN)
print(piece == piece1)
print(hash(piece))
print(hash(piece1))
print("%r" % (piece))
print(dir(piece))
