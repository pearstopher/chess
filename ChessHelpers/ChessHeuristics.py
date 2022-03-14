# Chess Heuristics
#
# This file contains the chess heuristics which we have designed
# and which are used to score our chess positions in ChessEngineHelper.py


class Heuristics:
    def __init__(self):
        self.CHECKMATE = 1000
        self.STALEMATE = 0
        self.piece_score = {"k": 0, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}

    # heuristic #1: basic heuristic, scores boards based on piece value
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

    ############################################
    # additional heuristics (not yet integrated)
    ############################################

    # control_diagonals and control_center
    # - Mike K https://github.com/fieldsher
    def control_diagonals(self, board):
        # This procedure determines if diagonals are controlled by bishops or queen

        # Define figures capable of controlling the diagonals
        diagonal_figures = ["b", "q"]

        # set initial heuristic to zero
        diagonal_heuristics = 0

        # Convert board
        chess_board = MakeMatrix().convert_to_matrix(board)

        # Define diagonals
        black_diagonal = [chess_board[1][1], chess_board[2][2], chess_board[3][3], chess_board[4][4],
                          chess_board[5][5], chess_board[6][6], chess_board[7][7], chess_board[8][8]]

        white_diagonal = [chess_board[1][8], chess_board[2][7], chess_board[3][6], chess_board[4][5],
                          chess_board[5][4], chess_board[6][3], chess_board[7][2], chess_board[8][1]]

        for cell in black_diagonal:
            for figure in diagonal_figures:
                if figure == cell[1]:
                    diagonal_heuristics += 3
        for cell in white_diagonal:
            for figure in diagonal_figures:
                if figure == cell[1]:
                    diagonal_heuristics += 3

        return diagonal_heuristics

    def control_center(self, board, side):
        # This procedure will give heuristic points for control of central squares

        # Convert board
        chess_board = MakeMatrix().convert_to_matrix(board)

        # define central squares: e4, e5, d4, d5
        central_squares = [chess_board[4][4], chess_board[4][5], chess_board[5][4], chess_board[5][5]]

        # Define squares can be used to control central squares by pawns
        white_pawn_squares = [chess_board[3][3], chess_board[4][3], chess_board[5][3], chess_board[6][3],
                              chess_board[4][3], chess_board[4][4], chess_board[4][5], chess_board[4][6]]

        black_pawn_squares = [chess_board[3][6], chess_board[4][6], chess_board[5][6], chess_board[6][6],
                              chess_board[3][5], chess_board[4][5], chess_board[5][5], chess_board[5][6]]

        # Define squares can be used to control central squares by knights
        knight_squares = [chess_board[3][2], chess_board[4][2], chess_board[5][2], chess_board[6][2],
                          chess_board[2][3], chess_board[3][3], chess_board[6][3], chess_board[7][3],
                          chess_board[2][4], chess_board[7][4], chess_board[2][5], chess_board[7][5],
                          chess_board[2][6], chess_board[3][6], chess_board[6][6], chess_board[7][6],
                          chess_board[3][7], chess_board[4][7], chess_board[5][7], chess_board[6][7]]

        # Set control center heuristics to 0
        ccHeuristic = 0

        # Give points for each piece in central square (pawn or knight)

        for square in central_squares:
            if square[1] == "p":
                ccHeuristic += 1
            elif square[1] == "n":
                ccHeuristic += 2

        # Give points for white pawns in controlling positions
        if side == "white":
            for square in white_pawn_squares:
                if square == "p":
                    ccHeuristic += 1

        # Give points for black pawns in controlling positions
        if side == "white":
            for square in black_pawn_squares:
                if square == "p":
                    ccHeuristic += 1

        # Give points for knights controlling central squares

        for square in knight_squares:
            if square == "n":
                ccHeuristic += 2

        return ccHeuristic


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


