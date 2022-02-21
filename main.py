# attribution:
# https://stackoverflow.com/questions/56984542/is-there-an-effiecient-way-of-making-a-function-to-drag-and-drop-multiple-pngs
#

import pygame


# constants and configuration
TILE_SIZE = 64
BORDER = 10
INFO_HEIGHT = 100  # informational window below board
BOARD_POS = (BORDER, BORDER)


# create the board surface by drawing the tiles
def create_board_surface():
    board_surface = pygame.Surface((TILE_SIZE*8, TILE_SIZE*8))
    dark = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(board_surface, pygame.Color((181, 136, 99) if dark else (240, 217, 181)), rect)
            dark = not dark
        dark = not dark
    return board_surface


def get_square_under_mouse(board):
    # mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(BOARD_POS)
    x, y = [int(v // TILE_SIZE) for v in mouse_pos]
    try:
        if x >= 0 and y >= 0:
            return board[y][x], x, y
    except IndexError:
        pass
    return None, None, None


def create_board():
    board = []
    for y in range(8):
        board.append([])
        for x in range(8):
            board[y].append(None)

    for x in range(0, 8):
        board[1][x] = ('black', 'pawn')
    for x in range(0, 8):
        board[6][x] = ('white', 'pawn')

    return board


def draw_pieces(screen, board, font, selected_piece):
    sx, sy = None, None
    if selected_piece:
        piece, sx, sy = selected_piece

    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece:
                selected = x == sx and y == sy
                color, piece_type = piece
                # s1 = font.render(piece_type[0], True, pygame.Color('red' if selected else color))
                # s2 = font.render(piece_type[0], True, pygame.Color('darkgrey'))
                s1 = pygame.image.load("images/" + color + "/" + piece_type + ".png").convert_alpha()
                s2 = pygame.image.load("images/" + color + "/" + piece_type + ".png").convert_alpha()
                s2.set_alpha(127)
                pos = pygame.Rect(BOARD_POS[0] + x*TILE_SIZE + 1, BOARD_POS[1] + y*TILE_SIZE + 1, TILE_SIZE, TILE_SIZE)
                # screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                # screen.blit(s1, s1.get_rect(center=pos.center))
                screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                screen.blit(s1, s1.get_rect(center=pos.center))



def draw_selector(screen, piece, x, y):
    if piece is not None:
        rect = (BOARD_POS[0] + x * TILE_SIZE, BOARD_POS[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)


def draw_drag(screen, board, selected_piece, font):
    if selected_piece:
        piece, x, y = get_square_under_mouse(board)
        if x is not None:
            rect = (BOARD_POS[0] + x * TILE_SIZE, BOARD_POS[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

        color, piece_type = selected_piece[0]
        s1 = font.render(piece_type[0], True, pygame.Color(color))
        s2 = font.render(piece_type[0], True, pygame.Color('darkgrey'))
        pos = pygame.Vector2(pygame.mouse.get_pos())
        # screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
        screen.blit(s2, s2.get_rect(center=pos + pygame.Vector2((1, 1))))
        screen.blit(s1, s1.get_rect(center=pos))
        selected_rect = pygame.Rect(BOARD_POS[0] + selected_piece[1] * TILE_SIZE, BOARD_POS[1] +
                                    selected_piece[2] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
        return x, y


def main():
    pygame.init()
    font = pygame.font.SysFont('', 32)
    pygame.display.set_caption("Chess Board")
    w = TILE_SIZE*8 + BORDER*2  # width of window
    h = w + INFO_HEIGHT
    screen = pygame.display.set_mode((w, h))
    board = create_board()
    board_surface = create_board_surface()
    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None
    while True:
        piece, x, y = get_square_under_mouse(board)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if piece is not None:
                    selected_piece = piece, x, y
            if e.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    piece, old_x, old_y = selected_piece
                    # board[old_y][old_x] = 0
                    board[int(old_y)][old_x] = 0
                    new_x, new_y = drop_pos
                    board[new_y][new_x] = piece
                selected_piece = None
                drop_pos = None

        screen.fill(pygame.Color(22, 21, 18))
        screen.blit(board_surface, BOARD_POS)
        draw_pieces(screen, board, font, selected_piece)
        draw_selector(screen, piece, x, y)
        drop_pos = draw_drag(screen, board, selected_piece, font)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
