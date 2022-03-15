# Chess Program
#
# This chess program currently responds to the user by making random moves.
#
# Basic requirements:
# > pip install python-chess
# > pip install pygame
#

import chess
from ChessHelpers import ChessEngineHelper

CHECKMATE = 1000
STALEMATE = 0

GUI = True  # choose between graphical or terminal interface
if GUI:
    from interface.gui import play_chess
else:
    from interface.tui import play_chess


def main():
    # create a chess board object
    board = chess.Board()

    # run the game loop to display the board UI
    # parameters:
    #   a chess board
    #   a move generation function for white (optional, defaults to player)
    #   a move generation function for black (optional, defaults to player)
    #
    # return value:
    #   the outcome of the game (ignored)
    move_generator = ChessEngineHelper.MoveGenerator()
    #play_chess(board, black=move_generator.mini_max_move)
    play_chess(board, black=move_generator.mobility_advanced_best_next_move)


if __name__ == '__main__':
    main()
