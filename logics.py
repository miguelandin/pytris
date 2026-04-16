import random
from typing import TYPE_CHECKING
import config as cf
import pygame

if TYPE_CHECKING:
    from pieces import Piece


def new_board():
    return [[cf.TILES["SPACE"] for _ in range(cf.BOARD_WIDTH)] for _ in range(cf.BOARD_HEIGHT)]


def clear_lines(board: list[list], lines: tuple):
    for x in lines:
        board.pop(x)
        board.insert(0, [0] * cf.BOARD_WIDTH)


def find_lines(board: list[list]):
    lines: list[int] = []
    for row in range(len(board)):
        line = True
        col = 0
        while col in range(len(board[row])) and line:
            if board[row][col] == 0:
                line = False
            else:
                col += 1
        if line is True:
            lines.append(row)

    return tuple(lines), len(lines)


def get_random_piece(queue: list, pieces: tuple, board: list[list]):
    if len(queue) <= 5:
        new_pieces = list(pieces)
        random.shuffle(new_pieces)
        queue.extend(new_pieces)

    piece = queue.pop(0)()
    if is_colliding(piece.piece_blocks, board):
        return piece, True
    else:
        return piece, False


def is_colliding(piece_blocks, board: list[list]):
    for x, y in piece_blocks:
        if x < 0 or x >= cf.BOARD_WIDTH or y >= cf.BOARD_HEIGHT:
            return True
        if y >= 0 and not board[y][x] == cf.TILES["SPACE"]:
            return True
    return False


def calculate_end_coords(piece: "Piece", board: list[list]):
    actual_coords = piece.piece_blocks
    colision = False

    while not colision:
        next_coords = [[x, y + 1] for x, y in actual_coords]
        if not is_colliding(next_coords, board):
            actual_coords = next_coords
        else:
            colision = True

    return tuple(actual_coords)


def find_space(piece_blocks, board: list[list], iteration: int):
    if iteration == cf.MAX_UPWARDS:
        return None
    if not is_colliding(piece_blocks, board):
        return piece_blocks
    else:
        new_piece_blocks = [[x, y - 1] for x, y in piece_blocks]
        return find_space(new_piece_blocks, board, iteration + 1)


def place_piece(piece: "Piece", board: list[list]):
    for x, y in piece.piece_blocks:
        board[y][x] = cf.TILES[piece.COLOR]


def center_piece(blocks: tuple):
    return (cf.MARGIN_SIZE - (blocks[-1][0]+1))/2


def calculate_fall_time(level: int):
    return int(((0.8-((level-1)*0.007))**(level-1))*1000)


def calculate_score(level: int, combo: int, lines: int):
    combo_score = 50*combo*level
    line_score = cf.SCORES[lines] * level
    return combo_score + line_score


def draw_board(board: list[list], screen: pygame.Surface):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                continue
            color = cf.COLORS[board[row][col]]
            draw_piece([(col, row)], color, screen, (cf.MARGIN_SIZE, 0))


def draw_borders(screen: pygame.Surface, layer: pygame.Surface):
    left_border = pygame.Rect(
        (cf.MARGIN_SIZE*cf.BLOCK_SIZE)-cf.BORDER_WIDTH, 0, cf.BORDER_WIDTH, cf.SCREEN_HEIGHT)

    right_border = pygame.Rect(
        ((cf.MARGIN_SIZE+cf.BOARD_WIDTH)*cf.BLOCK_SIZE), 0, cf.BORDER_WIDTH,
        cf.SCREEN_HEIGHT)

    top_bar = pygame.Rect(
        cf.MARGIN_SIZE*cf.BLOCK_SIZE,
        cf.TOP_BUFFER*cf.BLOCK_SIZE,
        cf.BOARD_WIDTH*cf.BLOCK_SIZE,
        cf.BORDER_WIDTH)

    background = pygame.Rect(
        cf.MARGIN_SIZE*cf.BLOCK_SIZE+cf.BORDER_WIDTH, 0,
        cf.BOARD_WIDTH*cf.BLOCK_SIZE-cf.BORDER_WIDTH,
        cf.BOARD_HEIGHT*cf.BLOCK_SIZE)

    pygame.draw.rect(screen, cf.WHITE, left_border)
    pygame.draw.rect(screen, cf.WHITE, right_border)
    pygame.draw.rect(screen, (*cf.WHITE, cf.OPACITY), top_bar)
    pygame.draw.rect(layer, (*cf.BLACK, cf.OPACITY), background)


def draw_piece(blocks, color: tuple, screen: pygame.Surface, coords: tuple):
    darker_color = tuple((max(0, i-cf.DARKEN) for i in color[:3]))

    for x, y in blocks:
        block = pygame.Rect((x + coords[0]) * cf.BLOCK_SIZE,
                            (y + coords[1]) * cf.BLOCK_SIZE,
                            cf.BLOCK_SIZE,
                            cf.BLOCK_SIZE)
        pygame.draw.rect(screen, color, block)
        pygame.draw.rect(screen, darker_color, block, cf.BLOCK_BORDER)


def draw_shadow(blocks, color: tuple, screen: pygame.Surface, coords: tuple):
    for x, y in blocks:
        block = pygame.Rect((x + coords[0]) * cf.BLOCK_SIZE,
                            (y + coords[1]) * cf.BLOCK_SIZE,
                            cf.BLOCK_SIZE,
                            cf.BLOCK_SIZE)
        pygame.draw.rect(screen, color, block, cf.BLOCK_BORDER)


def draw_hold(hold_piece, screen: pygame.Surface):
    if hold_piece:
        blocks = hold_piece.INIT_COORDS
        draw_piece(
            blocks, cf.COLORS[cf.TILES[hold_piece.COLOR]], screen, (center_piece(blocks), cf.MARGIN_TOP))


def draw_next_pieces(pieces: list, screen: pygame.Surface):
    margin_top = cf.MARGIN_TOP
    for piece in pieces[:5]:
        blocks = piece.INIT_COORDS
        draw_piece(blocks, cf.COLORS[cf.TILES[piece.COLOR]], screen,
                   (cf.MARGIN_SIZE + cf.BOARD_WIDTH + center_piece(blocks), margin_top))
        margin_top += 3


def render_outlined(
    font: pygame.Font,
    text: str,
    text_color: pygame.typing.ColorLike,
    outline_color: pygame.typing.ColorLike,
    outline_width: int,
) -> pygame.Surface:
    old_outline = font.outline
    if old_outline != 0:
        font.outline = 0
    base_text_surf = font.render(text, True, text_color)
    font.outline = outline_width
    outlined_text_surf = font.render(text, True, outline_color)

    outlined_text_surf.blit(base_text_surf, (outline_width, outline_width))
    font.outline = old_outline
    return outlined_text_surf
