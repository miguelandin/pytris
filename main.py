import pygame
import moderngl
import logics
import config as cf
from array import array
from pieces import Piece, PIECES


board = logics.new_board()


def draw_board(board: list[list], screen: pygame.Surface):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                continue
            color = cf.COLORS[board[row][col]]
            block = pygame.Rect(
                (col + cf.MARGIN_SIZE) * cf.BLOCK_SIZE, row *
                cf.BLOCK_SIZE, cf.BLOCK_SIZE, cf.BLOCK_SIZE)
            pygame.draw.rect(screen, color, block)


def draw_border(screen: pygame.Surface):
    left_border = pygame.Rect(
        (cf.MARGIN_SIZE*cf.BLOCK_SIZE), 0, 1, cf.SCREEN_HEIGHT)

    right_border = pygame.Rect(
        ((cf.MARGIN_SIZE+cf.BOARD_WIDTH)*cf.BLOCK_SIZE), 0, 1, cf.SCREEN_HEIGHT)

    pygame.draw.rect(screen, cf.WHITE, left_border)
    pygame.draw.rect(screen, cf.WHITE, right_border)


def draw_piece(blocks: tuple, color: tuple, screen: pygame.Surface, coords: tuple):
    for x, y in blocks:
        block = pygame.Rect((x + coords[0]) * cf.BLOCK_SIZE, (y + coords[1]) * cf.BLOCK_SIZE,
                            cf.BLOCK_SIZE, cf.BLOCK_SIZE)
        pygame.draw.rect(screen, color, block)


def draw_hold(hold_piece, screen: pygame.Surface):
    if hold_piece:
        draw_piece(
            hold_piece.INIT_COORDS, cf.COLORS[cf.TILES[hold_piece.COLOR]], screen, (1, 1))


def draw_next_pieces(pieces: list, screen: pygame.Surface):
    margin_top = 1
    for piece in pieces[:5]:
        draw_piece(piece.INIT_COORDS, cf.COLORS[cf.TILES[piece.COLOR]], screen,
                   (cf.MARGIN_SIZE + cf.BOARD_WIDTH + 1, margin_top))
        margin_top += 3


pygame.init()
screen = pygame.display.set_mode(
    (cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT),
    pygame.OPENGL | pygame.DOUBLEBUF,
)
pygame.display.set_caption("tetris-py")
clock = pygame.time.Clock()
running = True

time = 0
das_timer = 0
das_activate = False
current_direction = None
placed = False
can_swap = True
pieces: list = []
piece: Piece
restart: bool
piece, restart = logics.get_random_piece(pieces, PIECES, board)
hold_piece = None

display = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
ctx = moderngl.create_context()

# fmt: off
buffer = ctx.buffer(data=array("f", [
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,  # topright
    -1.0, -1.0, 0.0, 1.0,  # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
]))
# fmt: on

with open('shaders/background.vert', 'r', encoding='utf-8') as file:
    vertex_shader = file.read()

with open('shaders/background.frag', 'r', encoding='utf-8') as file:
    fragment_shader = file.read()

program = ctx.program(vertex_shader=vertex_shader,
                      fragment_shader=fragment_shader)
render_object = ctx.vertex_array(
    program, [(buffer, "2f 2f", "vertex", "screen_coords")]
)
display_texture = ctx.texture(display.get_size(), 4, display.get_view("1"))
display_texture.swizzle = "BGRA"
display_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE:
                piece.insta_down(board)
                logics.place_piece(piece, board)
                piece, restart = logics.get_random_piece(pieces, PIECES, board)
                time = 0
                placed = True
            elif event.key == pygame.K_UP:
                piece.rotate(board)
                time = 0
            elif event.key == pygame.K_c:
                if can_swap:
                    if hold_piece:
                        temp_piece = type(piece)
                        piece = hold_piece()
                        hold_piece = temp_piece
                    else:
                        hold_piece = type(piece)
                        piece, restart = logics.get_random_piece(
                            pieces, PIECES, board)
                    can_swap = False
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN):
                current_direction = event.key
                das_timer = pygame.time.get_ticks()
                das_activate = False
                if event.key == pygame.K_LEFT:
                    piece.move_left(board)
                elif event.key == pygame.K_RIGHT:
                    piece.move_right(board)
                elif event.key == pygame.K_DOWN:
                    if not piece.move_down(board):
                        time = 0

        if event.type == pygame.KEYUP:
            if event.key == current_direction:
                current_direction = None

    if current_direction:
        current_time = pygame.time.get_ticks()
        delay_needed = cf.DAS_REPEAT if das_activate or current_direction == pygame.K_DOWN else cf.DAS_DELAY

        if current_time - das_timer > delay_needed:
            if current_direction == pygame.K_LEFT:
                piece.move_left(board)
            elif current_direction == pygame.K_RIGHT:
                piece.move_right(board)
            elif current_direction == pygame.K_DOWN:
                if not piece.move_down(board):
                    time = 0

            das_timer = current_time
            das_activate = True

    if time > cf.FALL_TIMER:
        if piece.move_down(board):
            logics.place_piece(piece, board)
            piece, restart = logics.get_random_piece(pieces, PIECES, board)
            placed = True

        time = 0

    if placed:
        logics.clear_lines(board, logics.find_lines(board))
        placed = False
        can_swap = True

    if restart:
        board = logics.new_board()
        piece, restart = logics.get_random_piece(pieces, PIECES, board)

    display.fill((0, 0, 0, 0))
    draw_board(board, display)
    draw_piece(logics.calculate_end_coords(piece, board),
               cf.GREY, display, (5, 0))
    draw_piece(piece.piece_blocks,
               cf.COLORS[cf.TILES[piece.COLOR]], display, (5, 0))
    draw_border(display)
    draw_hold(hold_piece, display)
    draw_next_pieces(pieces, display)

    display_texture.write(display.get_view("1"))
    display_texture.use(0)
    program["iTime"] = pygame.time.get_ticks() / 1000.0
    program["iResolution"] = (
        cf.BOARD_WIDTH*cf.BLOCK_SIZE, cf.BOARD_HEIGHT*cf.BLOCK_SIZE)
    program["display"] = 0
    render_object.render(moderngl.TRIANGLE_STRIP)

    pygame.display.flip()
    clock.tick(60)
    time += 1
