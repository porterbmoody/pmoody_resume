#%%
# Remaining imports
import traceback
from flask import Flask, Response, request
import webbrowser
import chess
import chess.pgn
import chess.engine
import time
from ChessAI import ChessAI

board = chess.Board()
board
chess_ai = ChessAI()
chess_ai.get_best_move(board, depth = 3)

#%%

# move = chess_ai.get_best_move(board, depth = 5)
# move = chess_ai.get_best_move_poop(board, depth = 4, is_maximizing_player=True)
# board.push(move)

move = "e2e4"
board.push_san(move)
board


#%%
#################################################################################

# # Searching Ai's Move
# def get_ai_move(board):
#     move = chess_ai.get_best_move(board, depth = 3)
#     print("move:", move)
#     board.push(move)

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
    ret += '<form action="/human_and_ai_move/"><input type="submit" value="human and ai move:"><input name="human_and_ai_move" type="text"></input></form>'
    ret += '<form action="/dev/" method="post"><button name="ai move" type="submit">Make Ai Move</button></form>'
    # ret += '<form action="/engine/" method="post"><button name="Stockfish Move" type="submit">Make Stockfish Move</button></form>'
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
@app.route("/human_and_ai_move/")
def human_and_ai_move():
    try:
        move = request.args.get('human_and_ai_move', default="")
        board.push_san(move)
        if move != "":
            print("ai move")
            ai_move = chess_ai.get_best_move(board, depth = 3)
            board.push(ai_move)
    except Exception:
        traceback.print_exc()
    return main()
# Make Ai’s Move
@app.route("/dev/", methods=['POST'])
def dev():
    try:
        get_ai_move(board)
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



## take salesman out of the process

