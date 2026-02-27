from logics import find_space, is_colliding
from logics import calculate_end_coords
from config import SPAWN_CORDS

# pieces init coords
L_ORANGE_PIECE = ((1, 1), (0, 1), (2, 1), (2, 0))
L_CYAN_PIECE = ((1, 1), (0, 1), (2, 1), (0, 0))
SKEW_GREEN_PIECE = ((1, 1), (0, 1), (1, 0), (2, 0))
SKEW_RED_PIECE = ((1, 1), (0, 0), (1, 0), (2, 1))
T_PURPLE_PIECE = ((1, 1), (0, 1), (2, 1), (1, 0))
I_BLUE_PIECE = ((1, 0), (0, 0), (2, 0), (3, 0))
BLOCK_YELLOW_PIECE = ((0, 0), (1, 0), (0, 1), (1, 1))


class Piece:
    def __init__(self, piece_blocks: tuple, tile: str, init_pos: tuple[int, int]):
        i_x, i_y = init_pos
        self.piece_blocks = tuple([(x + i_x, y + i_y)
                                  for x, y in piece_blocks])
        self.color = tile

    def move_down(self, board: list[list]):
        new_piece_blocks = tuple([(x, y + 1) for x, y in self.piece_blocks])
        if not is_colliding(new_piece_blocks, board):
            self.piece_blocks = new_piece_blocks
            return False
        else:
            return True

    def move_left(self, board: list[list]):
        new_piece_blocks = tuple([(x - 1, y) for x, y in self.piece_blocks])
        if not is_colliding(new_piece_blocks, board):
            self.piece_blocks = new_piece_blocks

    def move_right(self, board: list[list]):
        new_piece_blocks = tuple([(x + 1, y) for x, y in self.piece_blocks])
        if not is_colliding(new_piece_blocks, board):
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

    def insta_down(self, board):
        self.piece_blocks = calculate_end_coords(self, board)


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


# Instances
PIECES = (
    LOrangePiece,
    LCyanPiece,
    SkewGreenPiece,
    SkewRedPiece,
    TPurplePiece,
    IBluePiece,
    BlockYellowPiece,
)
