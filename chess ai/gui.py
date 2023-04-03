#%%
# Remaining imports
import traceback
from flask import Flask, Response, request
import webbrowser
import chess
import chess.pgn
import chess.engine
import time
#%%
#################################################################################

import chess
import chess.engine

def minimax_alpha_beta(board, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    if maximizing_player:
        max_score = float('-inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score, _ = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        return max_score, best_move
    else:
        min_score = float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score, _ = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, min_score)
            if alpha >= beta:
                break
        return min_score, best_move

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # we don't want to move the king, so it has no value
    }
    score = 0
    for square, piece in board.piece_map().items():
        if piece.color == board.turn:
            score += piece_values[piece.piece_type]
        else:
            score -= piece_values[piece.piece_type]
    return score

def get_best_move(board):
    if board.turn == chess.WHITE:
        score, move = minimax_alpha_beta(board, maximizing_player=True)
    else:
        score, move = minimax_alpha_beta(board, maximizing_player=False)
    return move

board = chess.Board()
#%%

# move = minimax_alpha_beta(board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
move = get_best_move(board)
board.push(move)
board

# while not board.is_game_over():
#     if board.turn == chess.WHITE:
#         _, move = minimax_alpha_beta(board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
#         board.push(move)
#     else:
#         _, move = minimax_alpha_beta(board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
#         board.push(move)



#%%
#################################################################################

# Searching Ai's Move
def get_ai_move():
    move = get_best_move(board)
    board.push(move)
# Searching Stockfish's Move
def stockfish():
    engine = chess.engine.SimpleEngine.popen_uci(
        "your_path/stockfish.exe")
    move = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(move.move)
app = Flask(__name__)
# Front Page of the Flask Web Page
@app.route("/")
def main():
    global count, board
    ret = '<html><head>'
    ret += '<style>input {font-size: 20px; } button { font-size: 20px; }</style>'
    ret += '</head><body>'
    ret += '<img width=510 height=510 src="/board.svg?%f"></img></br></br>' % time.time()
    ret += '<form action="/game/" method="post"><button name="New Game" type="submit">New Game</button></form>'
    ret += '<form action="/undo/" method="post"><button name="Undo" type="submit">Undo Last Move</button></form>'
    ret += '<form action="/move/"><input type="submit" value="Make Human Move:"><input name="move" type="text"></input></form>'
    ret += '<form action="/dev/" method="post"><button name="Comp Move" type="submit">Make Ai Move</button></form>'
    ret += '<form action="/engine/" method="post"><button name="Stockfish Move" type="submit">Make Stockfish Move</button></form>'
    return ret
# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')
# Human Move
@app.route("/move/")
def move():
    try:
        move = request.args.get('move', default="")
        board.push_san(move)
    except Exception:
        traceback.print_exc()
    return main()
# Make Ai’s Move
@app.route("/dev/", methods=['POST'])
def dev():
    try:
        get_ai_move()
    except Exception:
        traceback.print_exc()
    return main()
# Make UCI Compatible engine's move
@app.route("/engine/", methods=['POST'])
def engine():
    try:
        stockfish()
    except Exception:
        traceback.print_exc()
    return main()
# New Game
@app.route("/game/", methods=['POST'])
def game():
    board.reset()
    return main()
# Undo
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        board.pop()
    except Exception:
        traceback.print_exc()
    return main()



board = chess.Board()
webbrowser.open("http://127.0.0.1:5000/")
app.run()
