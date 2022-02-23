# Chess Program
#
# This chess program currently responds to the user by making random moves.
#
# Requirements:
# > pip install pygame
# > pip install python-chess
#
# todo: fix moves displaying incorrectly after checkmate
# todo: enable pawn promotion


import chess
import random
from gui import game_loop


# a move generator should accept a chess.Board
#   and return a chess.Move
def random_move_generator(board):
    moves = list(board.legal_moves)
    return random.choice(moves)


def main():
    # create a chess board object
    board = chess.Board()

    # run the game loop to display the board UI
    # parameters:
    #   a chess board
    #   a move generation function
    game_loop(board, random_move_generator)


if __name__ == '__main__':
    main()
