"""
Contains some utility methods that act as extensions to the chess library
"""

import chess
import random
import pygame  # need to process pygame events to prevent game freeze


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
        self.DEPTH = 6  # (in case it's counter-intuitive: these are individual moves, not pairs)
        self.piece_score = {"k": 0, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}
        self.QUIT = False

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
            opponent_max_score = self.CHECKMATE
            if board.is_checkmate():
                opponent_max_score = -self.CHECKMATE
            elif board.is_stalemate():
                opponent_max_score = self.STALEMATE
            else:
                opponent_max_score = -self.CHECKMATE
                for opponent_move in opponent_moves:
                    board.push(opponent_move)  # make opponent's move
                    if board.is_checkmate():
                        score = self.CHECKMATE
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

    '''
    Mini Max Recursive Algo
    '''

    def mini_max_move(self, board):
        legal_moves = list(board.legal_moves)
        global best_move
        best_move = None

        # changed 'white_to_move' to 'maximize'
        # it doesn't matter whose turn it is, as long as
        # we get the max of whichever colors turn it is
        #
        #   (made for some funny games when I was playing white,
        #    before I realized that the AI was trying to maximize
        #    my score instead of its own)
        maximize = True

        # alpha-beta pruning
        # (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode)
        # Initialize array to hold hold dummy highest and lowest values for pruning
        alpha_beta = [-10000, 10000]

        self.find_mini_max_move(board, legal_moves, self.DEPTH, maximize, alpha_beta)
        if self.QUIT is True:
            return False

        if best_move is None:
            best_move = self.random_move(board)
        return best_move

    def find_mini_max_move(self, board, legal_moves, depth, maximize, alpha_beta):
        # keep processing events while the mini max search is going
        # and allow the user to close the game if a move is in progress
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.QUIT = True
        if self.QUIT is True:
            return 0

        global best_move
        if depth == 0:
            return self.score_material(board)
        if maximize:
            max_score = -self.CHECKMATE
            for move in legal_moves:
                board.push(move)
                next_moves = list(board.legal_moves)
                score = self.find_mini_max_move(board, next_moves, depth - 1, False, alpha_beta)

                # pruning: quit if any move has a higher score than beta
                if score >= alpha_beta[1]:
                    board.pop()
                    break
                # pruning: update alpha value
                if score > alpha_beta[0]:
                    alpha_beta[0] = score

                if score > max_score:
                    max_score = score
                    if depth == self.DEPTH:
                        best_move = move
                board.pop()
            return max_score
        else:
            min_score = self.CHECKMATE
            for move in legal_moves:
                board.push(move)
                next_moves = list(board.legal_moves)
                score = self.find_mini_max_move(board, next_moves, depth - 1, True, alpha_beta)

                # pruning: quit if any move has a lower score than alpha
                if score <= alpha_beta[0]:
                    board.pop()
                    break
                # pruning: update beta value
                if score < alpha_beta[1]:
                    alpha_beta[1] = score

                if score < min_score:
                    min_score = score
                    if depth == self.DEPTH:
                        best_move = move
                board.pop()
            return min_score

    def score_material(self, board):
        if board.is_checkmate():
            return self.CHECKMATE
        if board.is_stalemate():
            return self.STALEMATE

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
    def control_diagonals(board):
    # This procedure determines if diagonals are controlled by bishops or queen
    
    # Define figures capable of controlling the diagonals
    diagonal_figures = [b, q]
    
    # set initial heuristic to zero
    diagonal_heuristics = 0
    
    # Convert board
    chess_board = MakeMatrix().convert_to_matrix(board)
    
    # Define diagonals
    black_diagonal = [chess_board[1,1], chess_board[2,2], chess_board[3,3], chess_board[4,4],
                      chess_board[5,5], chess_board[6,6], chess_board[7,7], chess_board[8,8]]
    
    white_diagonal = [chess_board[1,8], chess_board[2,7], chess_board[3,6], chess_board[4,5], 
                      chess_board[5,4], chess_board[6,3], chess_board[7,2], chess_board[8,1]]
    
        
    for cell in black_diagonal:   
        for figure in diagonal_figures:
            if figure == cell:
                diagonal_heuristics += 3
    for cell in white_diagonal:
        for figure in diagonal_figures:
            if figure == cell:
                diagonal_heuristics += 3
            
    
    return diagonal_heuristics

    def control_center(board, side):
    # This procedure will give heuristic points for control of central squares
    
    # Convert board
    chess_board = MakeMatrix().convert_to_matrix(board)
    
    # define central squares: e4, e5, d4, d5
    central_squares = [chess_board[4,4], chess_board[4,5], chess_board[5,4], chess_board[5,5]]
    
    # Define squares can be used to control central squares by pawns
    white_pawn_squares = [chess_board[3,3], chess_board[4,3], chess_board[5,3], chess_board[6,3],
                          chess_board[4,3], chess_board[4,4], chess_board[4,5], chess_board[4,6]]
    
    black_pawn_squares = [chess_board[3,6], chess_board[4,6], chess_board[5,6], chess_board[6,6], 
                          chess_board[3,5], chess_board[4,5], chess_board[5,5], chess_board[5,6]]
            
    # Define squares can be used to control central squares by knights
    knight_squares = [chess_board[3,2], chess_board[4,2], chess_board[5,2], chess_board[6,2],
                      chess_board[2,3], chess_board[3,3], chess_board[6,3], chess_board[7,3],
                      chess_board[2,4], chess_board[7,4], chess_board[2,5], chess_board[7,5],
                      chess_board[2,6], chess_board[3,6], chess_board[6,6], chess_board[7,6],
                      chess_board[3,7], chess_board[4,7], chess_board[5,7], chess_board[6,7]]
    
    # Set control center heuristics to 0
    ccHeuristic = 0
    
    # Give points for each piece in central square (pawn or knight)
    
    for square in central_squares:
        if square == p:
            ccHeuristic +=1
        elif square == n:
            ccHeuristic +=2  
    
    # Give points for white pawns in controlling positions
    if side == white:
        for square in white_pawn_squares:
            if square == p:
                ccHeuristic +=1
            
    # Give points for black pawns in controlling positions        
    if side == black:
        for square in black_pawn_squares:
            if square == p:
                ccHeuristic +=1
            
    
    # Give points for knights controlling central squares
    
    for square in knight_squares:
        if square == n:
            ccHeuristic += 2
            
    return ccHeuristic
