import pygame
import random

# pieces init coords
L_ORANGE_PIECE = ((1, 1), (0, 1), (2, 1), (2, 0))
L_CYAN_PIECE = ((1, 1), (0, 1), (2, 1), (0, 0))
SKEW_GREEN_PIECE = ((1, 1), (0, 1), (1, 0), (2, 0))
SKEW_RED_PIECE = ((1, 1), (0, 0), (1, 0), (2, 1))
T_PURPLE_PIECE = ((1, 1), (0, 1), (2, 1), (1, 0))
I_BLUE_PIECE = ((1, 0), (0, 0), (2, 0), (3, 0))
BLOCK_YELLOW_PIECE = ((0, 0), (1, 0), (0, 1), (1, 1))

# map
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# pygame
BLOCK_SIZE = 30
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

# game
SPAWN_CORDS = (3, 0)
MAX_UPWARDS = 3

# colors
WHITE = (0, 0, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

TILES = {"SPACE": 0, "ORANGE": 1, "CYAN": 2,
         "GREEN": 3, "RED": 4, "PURPLE": 5, "BLUE": 6, "YELLOW": 7}

COLORS = {0: WHITE, 1: ORANGE, 2: CYAN, 3: GREEN,
          4: RED, 5: PURPLE, 6: BLUE, 7: YELLOW}

board = [[TILES["SPACE"]
          for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def is_coliding(piece_blocks, board: list):
    for x, y in piece_blocks:
        if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
            return True
        if y >= 0 and not board[y][x] == TILES["SPACE"]:
            return True
    return False


def find_space(piece_blocks, board: list, iteration: int):
    if iteration == MAX_UPWARDS:
        return None
    if not is_coliding(piece_blocks, board):
        return piece_blocks
    else:
        new_piece_blocks = [[x, y-1] for x, y in piece_blocks]
        return find_space(new_piece_blocks, board, iteration + 1)


class Piece:
    def __init__(self, piece_blocks: tuple, tile: str, init_pos: tuple[int, int]):
        i_x, i_y = init_pos
        self.piece_blocks = tuple([(x + i_x, y + i_y)
                                   for x, y in piece_blocks])
        self.color = tile

    def move_down(self, board: list):
        new_piece_blocks = tuple([(x, y + 1) for x, y in self.piece_blocks])
        if not is_coliding(new_piece_blocks, board):
            self.piece_blocks = new_piece_blocks
            return False
        else:
            return True

    def move_left(self, board: list):
        new_piece_blocks = tuple([(x - 1, y) for x, y in self.piece_blocks])
        if not is_coliding(new_piece_blocks, board):
            self.piece_blocks = new_piece_blocks

    def move_right(self, board: list):
        new_piece_blocks = tuple([(x + 1, y) for x, y in self.piece_blocks])
        if not is_coliding(new_piece_blocks, board):
            self.piece_blocks = new_piece_blocks

    def rotate(self, board):
        pivot = self.piece_blocks[0]
        px, py = pivot
        new_cords = []
        for x, y in self.piece_blocks:
            new_cords.append((px - (y - py), py + (x - px)))
        final_piece_blocks = find_space(new_cords, board, 0)
        if final_piece_blocks:
            self.piece_blocks = tuple(final_piece_blocks)


class LOrangePiece(Piece):
    def __init__(self):
        super().__init__(L_ORANGE_PIECE, "ORANGE", SPAWN_CORDS)


class LCyanPiece(Piece):
    def __init__(self):
        super().__init__(L_CYAN_PIECE, "CYAN", SPAWN_CORDS)


class SkewGreenPiece(Piece):
    def __init__(self):
        super().__init__(SKEW_GREEN_PIECE, "GREEN", SPAWN_CORDS)


class SkewRedPiece(Piece):
    def __init__(self):
        super().__init__(SKEW_RED_PIECE, "RED", SPAWN_CORDS)


class TPurplePiece(Piece):
    def __init__(self):
        super().__init__(T_PURPLE_PIECE, "PURPLE", SPAWN_CORDS)


class IBluePiece(Piece):
    def __init__(self):
        super().__init__(I_BLUE_PIECE, "BLUE", SPAWN_CORDS)


class BlockYellowPiece(Piece):
    def __init__(self):
        super().__init__(BLOCK_YELLOW_PIECE, "YELLOW", SPAWN_CORDS)

    def rotate(self, board):
        return


def place_piece(piece: Piece, board: list):
    for x, y in piece.piece_blocks:
        board[y][x] = TILES[piece.color]


def calculate_end_coords(piece: Piece, board: list):
    actual_coords = piece.piece_blocks
    colision = False

    while not colision:
        next_coords = [[x, y+1] for x, y in actual_coords]
        if not is_coliding(next_coords, board):
            actual_coords = next_coords
        else:
            colision = True

    return actual_coords


def draw_board(board: list[list], screen: pygame.Surface):
    for row in range(len(board)):
        for col in range(len(board[row])):
            color = COLORS[board[row][col]]
            block = pygame.Rect(col * BLOCK_SIZE, row *
                                BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, color, block)


def draw_piece(piece: Piece, screen: pygame.Surface):
    coordinates = piece.piece_blocks
    color = COLORS[TILES[piece.color]]

    for x, y in coordinates:
        block = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, color, block)


# Instances
PIECES = (
    LOrangePiece,
    LCyanPiece,
    SkewGreenPiece,
    SkewRedPiece,
    TPurplePiece,
    IBluePiece,
    BlockYellowPiece
)

pygame.init()
screen = pygame.display.set_mode(
    (BOARD_WIDTH*BLOCK_SIZE, BOARD_HEIGHT*BLOCK_SIZE))
pygame.display.set_caption("tetris-py")
clock = pygame.time.Clock()
running = True

fall_speed = 1000
while running:
    piece = random.choice(PIECES)()
    placed = False
    time = 0
    while not placed:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_DOWN:
                            if piece.move_down(board):
                                place_piece(piece, board)
                                placed = True
                            time = 0
                        case pygame.K_LEFT:
                            piece.move_left(board)
                        case pygame.K_RIGHT:
                            piece.move_right(board)
                        case pygame.K_UP:
                            piece.rotate(board)

        time += 1
        if time > fall_speed:
            if piece.move_down(board):
                place_piece(piece, board)
                placed = True
            time = 0

        draw_board(board, screen)
        draw_piece(piece, screen)
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
