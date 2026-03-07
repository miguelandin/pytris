from logics import find_space, is_colliding
from logics import calculate_end_coords
from config import SPAWN_COORDS


class Piece:
    INIT_COORDS: tuple = ()
    COLOR: str = ""

    def __init__(self):
        i_x, i_y = SPAWN_COORDS
        self.piece_blocks = tuple([(x + i_x, y + i_y)
                                  for x, y in self.INIT_COORDS])

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
    INIT_COORDS = ((1, 1), (0, 1), (2, 1), (2, 0))
    COLOR = "ORANGE"


class LCyanPiece(Piece):
    INIT_COORDS = ((1, 1), (0, 0), (0, 1), (2, 1))
    COLOR = "CYAN"


class SkewGreenPiece(Piece):
    INIT_COORDS = ((1, 1), (0, 1), (1, 0), (2, 0))
    COLOR = "GREEN"


class SkewRedPiece(Piece):
    INIT_COORDS = ((1, 1), (0, 0), (1, 0), (2, 1))
    COLOR = "RED"


class TPurplePiece(Piece):
    INIT_COORDS = ((1, 1), (0, 1), (1, 0), (2, 1))
    COLOR = "PURPLE"


class IBluePiece(Piece):
    INIT_COORDS = ((1, 0), (0, 0), (2, 0), (3, 0))
    COLOR = "BLUE"


class BlockYellowPiece(Piece):
    INIT_COORDS = ((0, 0), (1, 0), (0, 1), (1, 1))
    COLOR = "YELLOW"

    def rotate(self, board):
        pass


PIECES = (
    LOrangePiece,
    LCyanPiece,
    SkewGreenPiece,
    SkewRedPiece,
    TPurplePiece,
    IBluePiece,
    BlockYellowPiece,
)
