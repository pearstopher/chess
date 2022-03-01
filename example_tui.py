# Chess Program
#
# This chess program currently responds to the user by making random moves.
#
# Basic requirements:
# > pip install python-chess
# > pip install pygame
#

import chess
import random

GUI = False  # choose between graphical or terminal interface
if GUI:
    from interface.gui import play_chess
else:
    from interface.tui import play_chess


# a move generator should accept a chess.Board
#   and return a chess.Move
def random_move_generator(board):
    moves = list(board.legal_moves)
    return random.choice(moves)


def main():

    # Let's make the move generator play ten games against itself
    for _ in range(10):

        # create a chess board object
        board = chess.Board()

        # run the game loop to display the board UI
        # parameters:
        #   a chess board
        #   a move generation function for white (optional, defaults to player)
        #   a move generation function for black (optional, defaults to player)
        play_chess(board, white=random_move_generator, black=random_move_generator)


if __name__ == '__main__':
    main()
