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
SPAWN_CORDS = (3, -3)
MAX_UPWARDS = 3

# colors
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

tile = {"SPACE": 0, "ORANGE": 1, "CYAN": 2,
        "GREEN": 3, "RED": 4, "PURPLE": 5, "BLUE": 6}

board = [[tile["SPACE"]
          for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def is_coliding(piece_blocks, board: list):
    for x, y in piece_blocks:
        if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
            return True
        if y >= 0 and not board[y][x] == tile["SPACE"]:
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
    def __init__(self, piece_blocks: tuple, color: tuple[int, int, int], init_pos: tuple[int, int]):
        i_x, i_y = init_pos
        self.piece_blocks = tuple([(x + i_x, y + i_y)
                                   for x, y in piece_blocks])
        self.color = color

    def move_down(self, board: list):
        new_piece_blocks = tuple([(x, y + 1) for x, y in self.piece_blocks])
        if not is_coliding(new_piece_blocks, board):
            self.piece_blocks = new_piece_blocks
            return True
        else:
            return False

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
        super().__init__(L_ORANGE_PIECE, ORANGE, SPAWN_CORDS)


class LCyanPiece(Piece):
    def __init__(self):
        super().__init__(L_CYAN_PIECE, CYAN, SPAWN_CORDS)


class SkewGreenPiece(Piece):
    def __init__(self):
        super().__init__(SKEW_GREEN_PIECE, GREEN, SPAWN_CORDS)


class SkewRedPiece(Piece):
    def __init__(self):
        super().__init__(SKEW_RED_PIECE, RED, SPAWN_CORDS)


class TPurplePiece(Piece):
    def __init__(self):
        super().__init__(T_PURPLE_PIECE, PURPLE, SPAWN_CORDS)


class IBluePiece(Piece):
    def __init__(self):
        super().__init__(I_BLUE_PIECE, BLUE, SPAWN_CORDS)


class BlockYellowPiece(Piece):
    def __init__(self):
        super().__init__(BLOCK_YELLOW_PIECE, YELLOW, SPAWN_CORDS)

    def rotate(self, board):
        return


# Instances
pieces = [
    LOrangePiece(),
    LCyanPiece(),
    SkewGreenPiece(),
    SkewRedPiece(),
    TPurplePiece(),
    IBluePiece(),
    BlockYellowPiece()
]

# 1. Configuración inicial
pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("tetris-py")
clock = pygame.time.Clock()
running = True

# 2. Bucle principal del juego
while running:
    # Manejo de eventos (Teclado, ratón, cerrar ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    # Lógica del juego (Aquí van los movimientos)

    # Renderizado (Dibujo)
    pantalla.fill((0, 0, 0))  # Color de fondo (RGB)

    # Actualizar la pantalla
    pygame.display.flip()

    # Control de FPS (60 cuadros por segundo)
    clock.tick(60)

pygame.quit()
