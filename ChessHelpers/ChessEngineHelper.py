"""
Contains some utility methods that act as extensions to the chess library
"""

import chess
import random


class MakeMatrix:

    def __init__(self):
        self.board_mat = []

    def convert_to_matrix(self, board):
        board_str = board.epd()
        rows = board_str.split(" ", 1)[0].split("/")
        for row in rows:
            board_row = []
            for cell in row:
                if cell.isdigit():
                    for i in range(0, int(cell)):
                        board_row.append('--')
                else:
                    if cell.islower():  # black
                        board_row.append(("b", cell))
                    else:  # white
                        board_row.append(("w", cell.lower()))
            self.board_mat.append(board_row)
        return self.board_mat


class MoveGenerator:
    def __init__(self):
        self.CHECKMATE = 1000
        self.STALEMATE = 0
        self.piece_score = {"k": 0, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}

    '''
    Returns a random move from the list of all possible legal moves
    '''

    def random_move(self, board):
        moves = list(board.legal_moves)
        return random.choice(moves)

    '''
    Evaluate all moves from the list of all possible next, legal moves and decide which maximizes your score the most.
    We make the move in order to evaluate it and later undo it.
    '''

    def greedy_best_next_move(self, board):
        legal_moves = list(board.legal_moves)
        turn_multiplier = 1 if board.turn == chess.WHITE else -1
        max_score = -self.CHECKMATE
        best_move = None

        for player_move in legal_moves:
            board.push(player_move)  # make move
            if board.is_checkmate():
                score = self.CHECKMATE
            elif board.is_stalemate():
                score = self.STALEMATE
            else:
                score = turn_multiplier * self.score_material(board)
            if score > max_score:
                max_score = score
                best_move = player_move
            board.pop()  # undo the move

        if best_move is None:
            return self.random_move(board)

        return best_move

    '''
    To maximize your score and make the best move, you need to look into the opponent's future best move
    Only looks at the next opponent move
    '''

    def mini_max_easy(self, board):
        legal_moves = list(board.legal_moves)
        turn_multiplier = 1 if board.turn == chess.WHITE else -1
        opponent_min_max_score = self.CHECKMATE
        best_move = None

        for player_move in legal_moves:
            board.push(player_move)  # make move
            opponent_moves = list(board.legal_moves)
            opponent_max_score = -self.CHECKMATE
            for opponent_move in opponent_moves:
                board.push(opponent_move)  # make opponent's move
                if board.is_checkmate():
                    score = -turn_multiplier * self.CHECKMATE
                elif board.is_stalemate():
                    score = self.STALEMATE
                else:
                    score = -turn_multiplier * self.score_material(board)
                if score > opponent_max_score:
                    opponent_max_score = score
                board.pop()  # undo the opponent's move
            if opponent_max_score < opponent_min_max_score:
                opponent_min_max_score = opponent_max_score
                best_move = player_move
            board.pop()  # undo the player's move

        if best_move is None:
            return self.random_move(board)

        return best_move

    def score_material(self, board):
        chess_board = MakeMatrix().convert_to_matrix(board)
        score = 0
        count_black = 0
        count_white = 0
        for row in chess_board:
            for cell in row:
                color = cell[0]
                piece_type = cell[1]
                if color == "w":
                    count_white += 1
                    score += self.piece_score[piece_type]
                elif color == "b":
                    count_black += 1
                    score -= self.piece_score[piece_type]
        return score
