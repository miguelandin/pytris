import pygame
import random
import moderngl
from array import array

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
BLOCK_SIZE = 50
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

# game
SPAWN_CORDS = (3, 0)
MAX_UPWARDS = 3
FALL_TIMER = 50
DAS_DELAY = 150
DAS_REPEAT = 50

# colors
WHITE = (0, 0, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (85, 85, 85)

TILES = {
    "SPACE": 0,
    "ORANGE": 1,
    "CYAN": 2,
    "GREEN": 3,
    "RED": 4,
    "PURPLE": 5,
    "BLUE": 6,
    "YELLOW": 7,
}

COLORS = {0: WHITE, 1: ORANGE, 2: CYAN, 3: GREEN,
          4: RED, 5: PURPLE, 6: BLUE, 7: YELLOW}

board = [[TILES["SPACE"]
          for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def is_coliding(piece_blocks, board: list[list]):
    for x, y in piece_blocks:
        if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
            return True
        if y >= 0 and not board[y][x] == TILES["SPACE"]:
            return True
    return False


def find_space(piece_blocks, board: list[list], iteration: int):
    if iteration == MAX_UPWARDS:
        return None
    if not is_coliding(piece_blocks, board):
        return piece_blocks
    else:
        new_piece_blocks = [[x, y - 1] for x, y in piece_blocks]
        return find_space(new_piece_blocks, board, iteration + 1)


class Piece:
    def __init__(self, piece_blocks: tuple, tile: str, init_pos: tuple[int, int]):
        i_x, i_y = init_pos
        self.piece_blocks = tuple([(x + i_x, y + i_y)
                                  for x, y in piece_blocks])
        self.color = tile

    def move_down(self, board: list[list]):
        new_piece_blocks = tuple([(x, y + 1) for x, y in self.piece_blocks])
        if not is_coliding(new_piece_blocks, board):
            self.piece_blocks = new_piece_blocks
            return False
        else:
            return True

    def move_left(self, board: list[list]):
        new_piece_blocks = tuple([(x - 1, y) for x, y in self.piece_blocks])
        if not is_coliding(new_piece_blocks, board):
            self.piece_blocks = new_piece_blocks

    def move_right(self, board: list[list]):
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


def place_piece(piece: Piece, board: list[list]):
    for x, y in piece.piece_blocks:
        board[y][x] = TILES[piece.color]


def calculate_end_coords(piece: Piece, board: list[list]):
    actual_coords = piece.piece_blocks
    colision = False

    while not colision:
        next_coords = [[x, y + 1] for x, y in actual_coords]
        if not is_coliding(next_coords, board):
            actual_coords = next_coords
        else:
            colision = True

    return tuple(actual_coords)


def draw_board(board: list[list], screen: pygame.Surface):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                continue
            color = COLORS[board[row][col]]
            block = pygame.Rect(
                col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
            )
            pygame.draw.rect(screen, color, block)


def draw_piece(coords: tuple, color: tuple, screen: pygame.Surface):
    for x, y in coords:
        block = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE,
                            BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, color, block)


def clear_lines(board: list[list], lines: tuple):
    for x in lines:
        board.pop(x)
        board.insert(0, [0] * BOARD_WIDTH)


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


def get_random_piece(queue: list, pieces: tuple):
    if len(queue) <= 5:
        new_pieces = list(pieces)
        random.shuffle(new_pieces)
        queue.extend(new_pieces)
    return queue.pop(0)()


pygame.init()
screen = pygame.display.set_mode(
    (BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE),
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
piece: Piece = get_random_piece(pieces, PIECES)
hold_piece = None

display = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
ctx = moderngl.create_context()
# fmt: off
buffer = ctx.buffer(data=array("f",[
    -1.0, 1.0, 0.0, 0.0,  # topleft
   1.0, 1.0, 1.0, 0.0,  # topright
    -1.0, -1.0, 0.0, 1.0,  # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
]))
# fmt: on

vertex_shader = """
#version 330 core
in vec2 vertex;
in vec2 screen_coords;
out vec2 uvs;

void main() {
    uvs = screen_coords;
    gl_Position = vec4(vertex, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330 core
in vec2 uvs;
out vec4 color;

uniform float iTime;
uniform vec2 iResolution;
uniform sampler2D display;

// --- CONFIGURACIÓN BALATRO ---
#define SPIN_ROTATION -2.0
#define SPIN_SPEED 7.0
#define OFFSET vec2(0.0)
#define COLOUR_1 vec4(0.871, 0.267, 0.231, 1.0)
#define COLOUR_2 vec4(0.0, 0.42, 0.706, 1.0)
#define COLOUR_3 vec4(0.086, 0.137, 0.145, 1.0)
#define CONTRAST 3.5
#define LIGTHING 0.4
#define SPIN_AMOUNT 0.25
#define PIXEL_FILTER 500.0
#define SPIN_EASE 1.0
#define IS_ROTATE false

vec4 effect(vec2 screenSize, vec2 screen_coords) {
    float pixel_size = length(screenSize.xy) / PIXEL_FILTER;
    vec2 uv = (floor(screen_coords.xy*(1./pixel_size))*pixel_size - 0.5*screenSize.xy)/length(screenSize.xy) - OFFSET;
    float uv_len = length(uv);
    
    float speed = (SPIN_ROTATION*SPIN_EASE*0.2);
    if(IS_ROTATE){
       speed = iTime * speed;
    }
    speed += 302.2;
    float new_pixel_angle = atan(uv.y, uv.x) + speed - SPIN_EASE*20.*(1.*SPIN_AMOUNT*uv_len + (1. - 1.*SPIN_AMOUNT));
    vec2 mid = (screenSize.xy/length(screenSize.xy))/2.;
    uv = (vec2((uv_len * cos(new_pixel_angle) + mid.x), (uv_len * sin(new_pixel_angle) + mid.y)) - mid);
    
    uv *= 30.;
    speed = iTime*(SPIN_SPEED);
    vec2 uv2 = vec2(uv.x+uv.y);
    
    for(int i=0; i < 5; i++) {
        uv2 += sin(max(uv.x, uv.y)) + uv;
        uv  += 0.5*vec2(cos(5.1123314 + 0.353*uv2.y + speed*0.131121),sin(uv2.x - 0.113*speed));
        uv  -= 1.0*cos(uv.x + uv.y) - 1.0*sin(uv.x*0.711 - uv.y);
    }
    
    float contrast_mod = (0.25*CONTRAST + 0.5*SPIN_AMOUNT + 1.2);
    float paint_res = min(2., max(0.,length(uv)*(0.035)*contrast_mod));
    float c1p = max(0.,1. - contrast_mod*abs(1.-paint_res));
    float c2p = max(0.,1. - contrast_mod*abs(paint_res));
    float c3p = 1. - min(1., c1p + c2p);
    float light = (LIGTHING - 0.2)*max(c1p*5. - 4., 0.) + LIGTHING*max(c2p*5. - 4., 0.);
    return (0.3/CONTRAST)*COLOUR_1 + (1. - 0.3/CONTRAST)*(COLOUR_1*c1p + COLOUR_2*c2p + vec4(c3p*COLOUR_3.rgb, c3p*COLOUR_1.a)) + light;
}

void main() {
    vec2 screen_coords = uvs * iResolution; 
    vec4 background = effect(iResolution, screen_coords);
    
    vec4 game_layer = texture(display, uvs);
    
    vec3 final_color = mix(background.rgb * 0.5, game_layer.rgb, game_layer.a);
    
    color = vec4(final_color, 1.0);
}
"""

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
                place_piece(piece, board)
                piece = get_random_piece(pieces, PIECES)
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
                        piece = get_random_piece(pieces, PIECES)
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
        delay_needed = DAS_REPEAT if das_activate or current_direction == pygame.K_DOWN else DAS_DELAY

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

    if time > FALL_TIMER:
        if piece.move_down(board):
            place_piece(piece, board)
            piece = get_random_piece(pieces, PIECES)
            placed = True

        time = 0

    if placed:
        clear_lines(board, find_lines(board))
        placed = False
        can_swap = True

    display.fill((0, 0, 0, 0))
    draw_board(board, display)
    draw_piece(calculate_end_coords(piece, board), GREY, display)
    draw_piece(piece.piece_blocks, COLORS[TILES[piece.color]], display)

    display_texture.write(display.get_view("1"))
    display_texture.use(0)
    program["iTime"] = pygame.time.get_ticks() / 1000.0
    program["iResolution"] = (BOARD_WIDTH*BLOCK_SIZE, BOARD_HEIGHT*BLOCK_SIZE)
    program["display"] = 0
    render_object.render(moderngl.TRIANGLE_STRIP)

    pygame.display.flip()
    clock.tick(60)
    time += 1
