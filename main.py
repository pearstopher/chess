# Chess
# Christopher Juncker

import chess
import random
from gui import game_loop


def random_move(board):
    moves = list(board.legal_moves)
    return random.choice(moves)


def main():
    # create a chess board object
    board = chess.Board()

    # run the game loop to display the board UI
    # parameters:
    #   a chess board
    #   a move generation function
    game_loop(board, random_move)


if __name__ == '__main__':
    main()
