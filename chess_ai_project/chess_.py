#%%

import chess 

board = chess.Board()

legal_moves = list(board.legal_moves)
legal_moves
board


# %%
# board.push_san("e4")

# board.push_san("e5")
# board.push_san("Qh5")
# board.push_san("Nc6")
# board.push_san("Bc4")
# board.push_san("Nf6")
# board.push_san("Qxf7")

board.is_checkmate()
# board

#%%

# Nf3 = chess.Move.from_uci("g1f3")

# board
board.outcome()



