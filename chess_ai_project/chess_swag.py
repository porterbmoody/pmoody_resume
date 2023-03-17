#%%
import chess
import random
import time


def piece_value(piece_type):
    if piece_type == chess.PAWN:
        return 1
    elif piece_type == chess.KNIGHT:
        return 3
    elif piece_type == chess.BISHOP:
        return 3
    elif piece_type == chess.ROOK:
        return 5
    elif piece_type == chess.QUEEN:
        return 9
    elif piece_type == chess.KING:
        return 100
    else:
        return 0

def evaluate(board):
    if board.is_checkmate():
        return -10000 if board.turn else 10000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    material = 0
    for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        material += len(board.pieces(piece_type, chess.WHITE)) * (100 if piece_type != chess.PAWN else 10)
        material -= len(board.pieces(piece_type, chess.BLACK)) * (100 if piece_type != chess.PAWN else 10)
    return material

def minimax_ab_tt(board, depth, max_player, alpha=float('-inf'), beta=float('inf'), tt={}):
    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)
    tt_key = board.fen()
    
    if tt_key in tt:
        tt_entry = tt[tt_key]
        if tt_entry['depth'] >= depth:
            if tt_entry['flag'] == 'exact':
                return tt_entry['value'], tt_entry['move']
            elif tt_entry['flag'] == 'lowerbound':
                alpha = max(alpha, tt_entry['value'])
            elif tt_entry['flag'] == 'upperbound':
                beta = min(beta, tt_entry['value'])
            if alpha >= beta:
                return tt_entry['value'], tt_entry['move']
    
    if depth == 0 or board.is_game_over():
        return evaluate(board), None

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in legal_moves:
            board.push(move)
            eval, _ = minimax_ab_tt(board, depth - 1, False, alpha, beta, tt)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        tt[tt_key] = {'value': max_eval, 'move': best_move, 'depth': depth, 'flag': 'lowerbound' if max_eval <= alpha else 'exact'}
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in legal_moves:
            board.push(move)
            eval, _ = minimax_ab_tt(board, depth - 1, True, alpha, beta, tt)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        tt[tt_key] = {'value': min_eval, 'move': best_move, 'depth': depth, 'flag': 'upperbound' if min_eval >= beta else 'exact'}
        return min_eval, best_move

#%%
##################### gui
# Remaining imports
import traceback
from flask import Flask, Response, request
import webbrowser
import chess.svg

# Searching Ai's Move
def ai_move(board):
    tt = {}
    score, move = minimax_ab_tt(board, 4, board.turn, tt=tt)
    board.push(move)

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
    ret += '<form action="/human_move/"><input type="submit" value="human move:"><input name="human_move" type="text"></input></form>' 
    
    ret += '<form action="/human_and_ai_move/"><input type="submit" value="human and ai move:"><input name="human_and_ai_move" type="text"></input></form>' 

    print("just did human move html")
    ret += '<form action="/dev/" method="post"><button name="ai move" type="submit">make ai move</button></form>' 
    print("just did ai move html")
    return ret
# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')
# Human Move
@app.route("/human_move/")
def move():
    try:
        move = request.args.get('human_move', default="")
        board.push_san(move)
    except Exception:
        traceback.print_exc()
    return main()

# Human Move
@app.route("/human_and_ai_move/")
def human_and_ai_move():
    try:
        move = request.args.get('human_and_ai_move', default="")
        board.push_san(move)
        ai_move(board)
    except Exception:
        traceback.print_exc()
    return main()

# Make Ai’s Move
@app.route("/dev/", methods=['POST'])
def dev():
    try:
        ai_move(board)
    except Exception:
        traceback.print_exc()
    return main()
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
webbrowser.open("http://localhost:8888/")
app.run()
# %%
