# Chess TUI
#
# This file contains a terminal user interface for displaying python-chess boards.
# Entering moves like this is very tedious, I definitely recommend using the GUI!
#
# Note: By default, my terminal in Pycharm did not display the board correctly with Jetbrains default font.
#   Courier New, Consolas, Lucida Sans Typewriter, everything else works fine.
#   (File -> Settings -> Editor -> Colors Scheme -> Console Font)
#

import chess

ENABLE_ILLEGAL_MOVES = False


def game_loop(board, move_generator):
    while True:
        if board.turn == chess.WHITE:

            # print chess board to the terminal
            print()
            print(board.unicode(invert_color=True))

            # prompt the player for a move
            legal_moves = list(board.legal_moves)
            print("\nAvailable moves:")
            for m in legal_moves:
                print(m.uci(), end=", ")
            uci = input("\n\nWhite's move: ")
            move = chess.Move.from_uci(uci)

            # attempt to make the move
            if move in board.legal_moves or ENABLE_ILLEGAL_MOVES:
                board.push(move)

        else:
            # find out if the game is over
            outcome = board.outcome()
            if outcome is None:
                # generate and push a move to the board
                move = move_generator(board)
                board.push(move)
                print("Black's move:", move.uci())
            else:
                print("Game over!")
                print(outcome)
                print()
                return
