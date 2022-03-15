# Chess Heuristics
#
# This file contains the chess heuristics which we have designed
# and which are used to score our chess positions in ChessEngineHelper.py


class Heuristics:
    def __init__(self):
        self.CHECKMATE = 1000
        self.STALEMATE = 0
        self.piece_score = {"k": 0, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}
        self.mobility_piece_score = {"k": 4, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}

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

    # mobility - number of legal moves available to a player after the current move
    # - Rajashree P https://github.com/fieldsher
    def mobility(self, board):
        return board.legal_moves.count()

    # mobility - number of pieces attacked + number pieces defended

    def get_rook_score_for_mobility_advanced(self, chess_board, row, col):
        score = 0

        row_index = row + 1
        col_index = col

        while row_index <= 7:
            piece_type = chess_board[row_index][col_index][1]
            if piece_type != "-":
                score += self.mobility_piece_score[piece_type]
                break
            row_index += 1

        row_index = row - 1

        while row_index >= 0:
            piece_type = chess_board[row_index][col_index][1]
            if piece_type != "-":
                score += self.mobility_piece_score[piece_type]
                break
            row_index -= 1

        row_index = row
        col_index = col + 1

        while col_index <= 7:
            piece_type = chess_board[row_index][col_index][1]
            if piece_type != "-":
                score += self.mobility_piece_score[piece_type]
                break
            col_index += 1

        col_index = col - 1

        while col_index >= 0:
            piece_type = chess_board[row_index][col_index][1]
            if piece_type != "-":
                score += self.mobility_piece_score[piece_type]
                break
            col_index -= 1

        return score

    def get_bishop_score_for_mobility_advanced(self, chess_board, row, col):
        score = 0

        row_index = row + 1
        col_index = col + 1

        while row_index <= 7 and col_index <= 7:
            piece_type = chess_board[row_index][col_index][1]
            if piece_type != "-":
                score += self.mobility_piece_score[piece_type]
                break
            row_index += 1
            col_index += 1

        row_index = row - 1
        col_index = col - 1

        while row_index >= 0 and col_index >= 0:
            piece_type = chess_board[row_index][col_index][1]
            if piece_type != "-":
                score += self.mobility_piece_score[piece_type]
                break
            row_index -= 1
            col_index -= 1

        row_index = row + 1
        col_index = col - 1

        while row_index <= 7 and col_index >= 0:
            piece_type = chess_board[row_index][col_index][1]
            if piece_type != "-":
                score += self.mobility_piece_score[piece_type]
                break
            row_index += 1
            col_index -= 1

        row_index = row - 1
        col_index = col + 1

        while row_index >= 0 and col_index <= 7:
            piece_type = chess_board[row_index][col_index][1]
            if piece_type != "-":
                score += self.mobility_piece_score[piece_type]
                break
            row_index -= 1
            col_index += 1

        return score

    def get_score_for_mobility_advanced(self, chess_board, row_index, col_index):
        score = 0

        if 0 <= row_index <= 7 and 0 <= col_index <= 7:
            piece_type = chess_board[row_index][col_index][1]
            if piece_type != "-":
                score += self.mobility_piece_score[piece_type]

        return score

    def mobility_advanced(self, board, player_move):
        # Convert board
        chess_board = MakeMatrix().convert_to_matrix(board)

        score = 0

        to_square = player_move.to_square
        row = 7 - int(to_square / 8)
        col = to_square % 8
        cur_color = chess_board[row][col][0]
        cur_piece_type = chess_board[row][col][1]

        board.pop()
        temp_chess_board = MakeMatrix().convert_to_matrix(board)
        temp_color = temp_chess_board[row][col][0]
        temp_piece_type = temp_chess_board[row][col][1]
        if temp_color == "w" and temp_piece_type != "-":
            score += self.mobility_piece_score[temp_piece_type]
        board.push(player_move)
        chess_board = MakeMatrix().convert_to_matrix(board)

        # knight
        if cur_piece_type == "n":
            offset = [-2, -1, 1, 2]
            for row_offset in offset:
                for col_offset in offset:
                    if abs(row_offset) + abs(col_offset) == 3:
                        new_row_pos = row + row_offset
                        new_col_pos = col + col_offset
                        if 0 <= new_row_pos <= 7 and 0 <= new_col_pos <= 7:
                            piece_type = chess_board[new_row_pos][new_col_pos][1]
                            if piece_type != "-":
                                score += self.mobility_piece_score[piece_type]

        # queen
        if cur_piece_type == "q":
            score += self.get_rook_score_for_mobility_advanced(chess_board, row, col)
            score += self.get_bishop_score_for_mobility_advanced(chess_board, row, col)

        # rook
        if cur_piece_type == "r":
            score += self.get_rook_score_for_mobility_advanced(chess_board, row, col)

        # bishop
        if cur_piece_type == "b":
            score += self.get_bishop_score_for_mobility_advanced(chess_board, row, col)

        # pawn
        if cur_piece_type == "p":
            row_index = row + 1
            col_index = col + 1

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

            col_index = col - 1

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

        # king
        if cur_piece_type == "k":
            row_index = row + 1
            col_index = col + 1

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

            col_index = col - 1

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

            row_index = row - 1
            col_index = col - 1

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

            col_index = col + 1

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

            row_index = row + 1
            col_index = col

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

            row_index = row - 1

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

            row_index = row
            col_index = col + 1

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

            col_index = col - 1

            score += self.get_score_for_mobility_advanced(chess_board, row_index, col_index)

        return score


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


