# Chess
# Christopher Juncker

import chess
from gui import game_loop


def main():
    # create a chess board object
    board = chess.Board()

    # run the game loop to display the board UI
    game_loop(board)


if __name__ == '__main__':
    main()
