#%%
import chess
from copy import deepcopy
import random
import chess.polyglot


class ChessAI:

    def __init__(self) -> None:
        pass

    reader = chess.polyglot.open_reader('D:/Desktop/School/pmoody_resume/chess ai/data/baron30.bin')
    scoring= {'p': -1,
            'n': -3,
            'b': -3,
            'r': -5,
            'q': -9,
            'k': 0,
            'P': 1,
            'N': 3,
            'B': 3,
            'R': 5,
            'Q': 9,
            'K': 0,
            }

    #opening book
    @staticmethod
    def random_agent(board):
        return random.choice(list(board.legal_moves))

    @staticmethod
    def eval_board(board):
        score = 0
        pieces = board.piece_map()
        for key in pieces:
            score += ChessAI.scoring[str(pieces[key])]

        return score

    @staticmethod
    def eval_space(board):
        no_moves = len(list(board.legal_moves))

        # this function is always between 0 and 1 so we will never evaluate
        # this as being greater than a pawns value. The 20 value is arbitrary
        # but this number is chosen as it centers value around 0.5
        value = (no_moves/(20+no_moves))
        
        if board.turn == True:
            return value
        else:
            return -value

    @staticmethod
    def min_max(board, depth):

        opening_move = ChessAI.reader.get(board)
        if opening_move == None:
            pass
        else:
            return opening_move.move

        # generate list of possible moves
        moves = list(board.legal_moves)
        scores = []

        # score each move
        for move in moves:
            # temp allows us to leave the original game state unchanged
            temp = deepcopy(board)
            temp.push(move)

            # here we must check that the game is not over
            outcome = temp.outcome()
            
            # if checkmate
            if outcome == None:
                # if we have not got to the final depth
                # we search more moves ahead
                if depth > 1:
                    temp_best_move = ChessAI.min_max(temp, depth - 1)
                    temp.push(temp_best_move)

                scores.append(ChessAI.eval_board(temp))

            # if checkmate
            elif temp.is_checkmate():

                # we return this as best move as it is checkmate
                return move

            # if stalemate
            else:
                #value to disencourage a draw
                #the higher the less likely to draw
                #default value should be 0
                #we often pick 0.1 to get the bot out of loops in bot vs bot
                val = 1000
                if board.turn == True:
                    scores.append(-val)
                else:
                    scores.append(val)

            #this is the secondary eval function
            scores[-1] = scores[-1] + ChessAI.eval_space(temp)

        if board.turn == True:
            best_move = moves[scores.index(max(scores))]
        else:
            best_move = moves[scores.index(min(scores))]

        return best_move
    
    @staticmethod
    def get_best_move(board, depth):
        return ChessAI.min_max(board, depth)

board = chess.Board()
chess_ai = ChessAI()

#%%


move = chess_ai.min_max(board, depth = 3)
board.push(move)

board

#%%

# a simple wrapper function as the display only gives one imput , BOARD

# def min_max1(BOARD):
    # return min_max(BOARD,1)

# def min_max2(BOARD):
#     return min_max(BOARD,2)

# def min_max3(BOARD):
#     return min_max(BOARD,3)

# def min_max4(BOARD):
#     return min_max(BOARD,4)

    # @staticmethod
    # def evaluate_board(board):
    #     if board.is_checkmate():
    #         if board.turn:
    #             return -9999
    #         else:
    #             return 9999
    #     elif board.is_stalemate():
    #         return 0
    #     elif board.is_insufficient_material():
    #         return 0
    #     elif board.is_seventyfive_moves():
    #         return 0
    #     elif board.is_fivefold_repetition():
    #         return 0
    #     piece_values = {
    #         chess.PAWN: 1,
    #         chess.KNIGHT: 3,
    #         chess.BISHOP: 3,
    #         chess.ROOK: 5,
    #         chess.QUEEN: 9,
    #         chess.KING: 0  # we don't want to move the king, so it has no value
    #     }
    #     score = 0
    #     for square, piece in board.piece_map().items():
    #         if piece.color == board.turn:
    #             score += piece_values[piece.piece_type]
    #         else:
    #             score -= piece_values[piece.piece_type]
    #     return score

    # def minimax_alpha_beta(self, board, depth, alpha, beta
    #                        ):
    #     """Perform a minimax search with alpha-beta pruning on the given chess board."""
    #     if depth == 0 or board.is_game_over():
    #         return self.evaluate_board(board), None

    #     if board.turn == chess.WHITE:
    #         max_score = float('-inf')
    #         best_move = None
    #         for move in board.legal_moves:
    #             board.push(move)
    #             score, _ = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False)
    #             board.pop()
    #             if score > max_score:
    #                 max_score = score
    #                 best_move = move
    #             alpha = max(alpha, max_score)
    #             if alpha >= beta:
    #                 break
    #         return max_score, best_move
    #     else:
    #         min_score = float('inf')
    #         best_move = None
    #         for move in board.legal_moves:
    #             board.push(move)
    #             score, _ = self.minimax_alpha_beta(board, depth - 1, alpha, beta, True)
    #             board.pop()
    #             if score < min_score:
    #                 min_score = score
    #                 best_move = move
    #             beta = min(beta, min_score)
    #             if alpha >= beta:
    #                 break
    #         return min_score, best_move
            
        
    # def get_best_move(self, board, depth=4, alpha=float('-inf'), beta=float('inf')):
    #     return self.minimax_alpha_beta(board, depth, alpha, beta)[1]

