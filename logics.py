import random
from typing import TYPE_CHECKING
import config as cf

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

    return tuple(lines)


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
        board[y][x] = cf.TILES[piece.color]
