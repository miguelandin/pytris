import pygame
import moderngl
import logics
import config as cf
from array import array
from pieces import Piece, PIECES


board = logics.new_board()

pygame.init()
screen = pygame.display.set_mode(
    (cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT),
    pygame.OPENGL | pygame.DOUBLEBUF,
)
pygame.display.set_caption("tetris-py")
clock = pygame.time.Clock()
font = pygame.font.Font(None, cf.FONT_SIZE)
running = True

time = pygame.time.get_ticks()
das_timer = 0
das_activate: bool = False
current_direction = None
placed = False
can_swap = True
pieces: list = []
piece: Piece
restart: bool
piece, restart = logics.get_random_piece(pieces, PIECES, board)
hold_piece = None
level: int = cf.START_LEVEL
cleared_lines = 0
fall_time = logics.calculate_fall_time(level)
combo: int = 0
score: int = 0
combo_0_render: pygame.Surface = logics.render_outlined(
    font, str(0), cf.BLACK, cf.WHITE, cf.FONT_OUTLINE)
combo_render: pygame.Surface = combo_0_render
score_render: pygame.Surface = logics.render_outlined(
    font, str(score), cf.BLACK, cf.WHITE, cf.FONT_OUTLINE)


display = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
back_layer = pygame.Surface(
    (cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT), pygame.SRCALPHA)
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
                time = pygame.time.get_ticks()
                placed = True
            elif event.key == pygame.K_UP:
                piece.rotate(board)
                time = pygame.time.get_ticks()
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
                        time = pygame.time.get_ticks()

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
                    time = pygame.time.get_ticks()

            das_timer = current_time
            das_activate = True

    if pygame.time.get_ticks() - time > fall_time:
        if piece.move_down(board):
            logics.place_piece(piece, board)
            piece, restart = logics.get_random_piece(pieces, PIECES, board)
            placed = True

        time = pygame.time.get_ticks()

    if placed:
        lines_to_clear, lines_count = logics.find_lines(board)
        logics.clear_lines(board, lines_to_clear)
        cleared_lines += lines_count
        placed = False
        can_swap = True

        if lines_count > 0:
            score += logics.calculate_score(level, combo, lines_count)
            score_render = logics.render_outlined(
                font, str(score), cf.BLACK, cf.WHITE, cf.FONT_OUTLINE)
            combo += 1
            combo_render = logics.render_outlined(
                font, str(combo), cf.BLACK, cf.WHITE, cf.FONT_OUTLINE)
            if cleared_lines >= cf.LINES_PER_LEVEL * level:
                level += 1
                fall_time = logics.calculate_fall_time(level)
        else:
            combo = 0
            combo_render = combo_0_render

    if restart:
        board = logics.new_board()
        piece, restart = logics.get_random_piece(pieces, PIECES, board)
        cleared_lines = 0
        level = cf.START_LEVEL
        fall_time = logics.calculate_fall_time(level)

    display.fill((0, 0, 0, 0))
    back_layer.fill((0, 0, 0, 0))
    logics.draw_borders(display, back_layer)
    display.blit(back_layer, (0, 0))
    display.blit(score_render,  (logics.center_text(
        score_render), cf.BLOCK_SIZE*10))
    display.blit(combo_render, (logics.center_text(
        combo_render), cf.BLOCK_SIZE*15))
    logics.draw_board(board, display)
    logics.draw_shadow(logics.calculate_end_coords(piece, board),
                       (*cf.GREY, cf.OPACITY), display, cf.PIECE_POS)
    logics.draw_piece(piece.piece_blocks,
                      cf.COLORS[cf.TILES[piece.COLOR]], display, cf.PIECE_POS)
    logics.draw_hold(hold_piece, display)
    logics.draw_next_pieces(pieces, display)

    display_texture.write(display.get_view("1"))
    display_texture.use(0)
    program["iTime"] = pygame.time.get_ticks() / 1000.0
    program["iResolution"] = (
        cf.BOARD_WIDTH*cf.BLOCK_SIZE, cf.BOARD_HEIGHT*cf.BLOCK_SIZE)
    program["display"] = 0
    render_object.render(moderngl.TRIANGLE_STRIP)

    pygame.display.flip()
    clock.tick(90)
    print(f"combo: {combo}, cleared: {
          cleared_lines}, level: {level}, score: {score}")
