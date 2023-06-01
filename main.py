import pygame
import random

BLOCK_SIZE = 30
BOARD_MARGIN_X = 10
BOARD_MARGIN_Y = 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_OFFSET = 2

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
OCEAN = (0, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)


class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arr = [[None for i in range(4)] for j in range(4)]
        self._type = random.randint(0, 6)
        self._rotation = 0
        match self._type:
            case 0:
                self.arr[1][1] = Block(RED)  # 0000
                self.arr[2][1] = Block(RED)  # 0##0
                self.arr[2][2] = Block(RED)  # 00##
                self.arr[3][2] = Block(RED)  # 0000
            case 1:
                self.arr[2][1] = Block(GREEN)  # 0000
                self.arr[3][1] = Block(GREEN)  # 00##
                self.arr[1][2] = Block(GREEN)  # 0##0
                self.arr[2][2] = Block(GREEN)  # 0000
            case 2:
                self.arr[2][0] = Block(BLUE)  # 00#0
                self.arr[2][1] = Block(BLUE)  # 00#0
                self.arr[2][2] = Block(BLUE)  # 0##0
                self.arr[1][2] = Block(BLUE)  # 0000
            case 3:
                self.arr[1][1] = Block(YELLOW)  # 0000
                self.arr[1][2] = Block(YELLOW)  # 0##0
                self.arr[2][1] = Block(YELLOW)  # 0##0
                self.arr[2][2] = Block(YELLOW)  # 0000
            case 4:
                self.arr[1][0] = Block(WHITE)  # 0#00
                self.arr[1][1] = Block(WHITE)  # 0#00
                self.arr[1][2] = Block(WHITE)  # 0##0
                self.arr[2][2] = Block(WHITE)  # 0000
            case 5:
                self.arr[1][1] = Block(PURPLE)  # 0000
                self.arr[0][2] = Block(PURPLE)  # 0#00
                self.arr[1][2] = Block(PURPLE)  # ###0
                self.arr[2][2] = Block(PURPLE)  # 0000
            case 6:
                self.arr[0][1] = Block(OCEAN)  # 0000
                self.arr[1][1] = Block(OCEAN)  # ####
                self.arr[2][1] = Block(OCEAN)  # 0000
                self.arr[3][1] = Block(OCEAN)  # 0000

    def _get_rotated_array(self):
        _rotated = [[None for i in range(4)] for j in range(4)]
        if (self._type == 0 or self._type == 1 or self._type == 6) and self._rotation == 1:
            for x in range(4):
                for y in range(4):
                    _rotated[x][3 - y] = self.arr[y][x]
        else:
            for x in range(4):
                for y in range(4):
                    _rotated[3 - y][x] = self.arr[x][y]

        return _rotated

    def rotate(self):
        self.arr = self._get_rotated_array()

        if self._type == 5 or self._type == 4 or self._type == 2:
            self._rotation = (self._rotation + 1) % 4
        else:
            self._rotation = (self._rotation + 1) % 2

    def check_rotation(self, arr):
        if self._type == 3:
            return False

        _rotated = self._get_rotated_array()
        for i in reversed(range(4)):
            for j in range(4):
                if _rotated[j][i] is not None:
                    if self.y + i >= BOARD_HEIGHT or j + self.x < 0 or j + self.x >= BOARD_WIDTH:
                        return False
                    else:
                        if arr[j + self.x][i + self.y] is not None:
                            return False
        return True

    def move(self, x, y):
        self.x += x
        self.y += y

    # -1 bottom is reached, 0 can't move(cause of x), 1 is good
    def check_move(self, x, y, arr):
        for i in reversed(range(4)):
            for j in range(4):
                if self.arr[j][i] is not None:
                    if self.y + i + y >= BOARD_HEIGHT:
                        return -1
                    else:
                        if arr[j + self.x][i + self.y + y] is not None:
                            return -1

                    if j + x + self.x < 0 or j + x + self.x >= BOARD_WIDTH:
                        return 0
                    else:
                        if arr[j + self.x + x][i + self.y] is not None:
                            return 0
        return 1

    def render(self, display):
        for x in range(4):
            for y in range(4):
                if self.arr[x][y] is not None:
                    self.arr[x][y].x = self.x + x
                    self.arr[x][y].y = self.y + y
                    self.arr[x][y].render(display, BLOCK_SIZE)


class Board:
    def __init__(self):
        self.arr = [[None for i in range(BOARD_HEIGHT)] for j in range(BOARD_WIDTH)]
        self._current_piece = None
        self._next_piece = None
        self._points = 0
        self._font = pygame.font.SysFont(None, 36)
        self._point_text = self._font.render('Points', True, WHITE)
        self._tetris = False
        self.lost = False
        self._frame_block = Block()

    def render(self, display):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if self.arr[x][y] is not None:
                    self.arr[x][y].render(display, BLOCK_SIZE)
        self._next_piece.render(display,)
        self._current_piece.render(display)

        for i in range(BOARD_WIDTH):
            self._frame_block.y = -1
            self._frame_block.x = i
            self._frame_block.render(display, BLOCK_SIZE)
            self._frame_block.y = BOARD_HEIGHT
            self._frame_block.render(display, BLOCK_SIZE)

        for i in range(-1, BOARD_HEIGHT + 1):
            self._frame_block.x = -1
            self._frame_block.y = i
            self._frame_block.render(display, BLOCK_SIZE)
            self._frame_block.x = BOARD_WIDTH
            self._frame_block.render(display, BLOCK_SIZE)

        display.blit(self._point_text, (440, 300))
        points = self._font.render(str(self._points), True, WHITE)
        display.blit(points, (460, 350))

    def _move_blocks_down(self, y, arr):
        for i in reversed(range(y)):
            for x in range(BOARD_WIDTH):
                if arr[x][i] is not None:
                    self._move(0, 1, arr[x][i])

    def _move(self, x, y, block):
        self.arr[block.x + x][block.y + y] = block
        self.arr[block.x][block.y] = None
        block.x += x
        block.y += y

    def _delete_whole_lines(self):
        _deleted_lines = 0
        for y in range(BOARD_HEIGHT):
            _full_line = True
            for x in range(BOARD_WIDTH):
                if self.arr[x][y] is None:
                    _full_line = False
                    break
            if _full_line:
                _deleted_lines += 1
                for x in range(BOARD_WIDTH):
                    self.arr[x][y] = None
                self._move_blocks_down(y, self.arr)
        self._points += _deleted_lines * 100
        if _deleted_lines == 4:
            self._points += 400
            if self._tetris:
                self._points += 400
            else:
                self._tetris = True
        else:
            self._tetris = False

    def _insert(self, x, y, piece):
        self._current_piece = piece
        self._current_piece.y = y
        self._current_piece.x = x

    def start_game(self):
        self._next_piece = Tetromino(12, 2)
        self._create_new_piece()

    def _create_new_piece(self):
        self._next_piece.x = int(BOARD_WIDTH / 2)
        self._next_piece.y = 0
        if self._next_piece.check_move(0, 0, self.arr) == -1:
            self.lost = True
        else:
            self._delete_whole_lines()
            self._insert(int(BOARD_WIDTH / 2), 0, self._next_piece)
            self._next_piece = Tetromino(12, 2)

    def _write_down_current_piece(self, arr, y_diff=0):
        for x in range(4):
            for y in range(4):
                if self._current_piece.arr[x][y] is not None:
                    if self._current_piece.y + y + y_diff >= BOARD_HEIGHT:
                        print(3)
                    arr[self._current_piece.x + x][self._current_piece.y + y + y_diff] = self._current_piece.arr[x][y]
                    arr[self._current_piece.x + x][self._current_piece.y + y + y_diff].x = self._current_piece.x + x
                    arr[self._current_piece.x + x][self._current_piece.y + y + y_diff].y = self._current_piece.y + y

    def move_current_piece(self, x, y):
        match self._current_piece.check_move(x, y, self.arr):
            case 1:
                self._current_piece.move(x, y)
            case -1:
                self._write_down_current_piece(self.arr)
                self._create_new_piece()
            case 0:
                pass

    def rotate_current_piece(self):
        if self._current_piece.check_rotation(self.arr):
            self._current_piece.rotate()

    def restart(self):
        self.lost = False
        self.arr = [[None for i in range(BOARD_HEIGHT)] for j in range(BOARD_WIDTH)]
        self._points = 0
        self.start_game()


class Block:
    def __init__(self, color=GRAY):
        self.x = 0
        self.y = 0
        self.color = color

    def render(self, display, offset=0):
        pygame.draw.rect(display,
                         self.color,
                         pygame.Rect(
                             BOARD_MARGIN_X + self.x * (BLOCK_SIZE + BLOCK_OFFSET) + offset,
                             BOARD_MARGIN_Y + self.y * (BLOCK_SIZE + BLOCK_OFFSET) + offset,
                             BLOCK_SIZE,
                             BLOCK_SIZE))


class Button:
    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        self._font = pygame.font.SysFont(None, 48)
        self._text = self._font.render(text, 1, WHITE)
        self._size = self._text.get_size()
        self._surface = pygame.Surface(self._size)
        self._surface.fill(BLACK)
        self._surface.blit(self._text, (0, 0))
        self._rect = pygame.Rect(self.x, self.y, self._size[0], self._size[1])

    def render(self, display):
        display.blit(self._surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self._rect.collidepoint(x, y):
                return True
        return False


class App:
    def __init__(self):
        self._font = None
        self._menu_button = None
        self._board = None
        self._running = True
        self._display_surf = None
        self._size = self._width, self._height = 560, 720
        self._FPS = pygame.time.Clock()
        self._time = 0
        self._controls_up = False
        self._controls_down = False
        self._controls_left = False
        self._controls_right = False
        self._time_to_move_down = 10
        self._menu = True

    def _on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._board = Board()
        self._menu_button = Button("Play", self._width / 2 - 40, int(self._height / 3))
        self._board.start_game()
        self._font = pygame.font.SysFont(None, 48)

    def _on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self._menu_button.click(event) and self._menu:
                self._board.restart()
                self._menu = False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w | pygame.K_UP:
                    self._controls_up = True
                case pygame.K_a | pygame.K_LEFT:
                    self._controls_left = True
                case pygame.K_s | pygame.K_DOWN:
                    self._controls_down = True
                case pygame.K_d | pygame.K_RIGHT:
                    self._controls_right = True
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_w | pygame.K_UP:
                    self._controls_up = False
                case pygame.K_a | pygame.K_LEFT:
                    self._controls_left = False
                case pygame.K_s | pygame.K_DOWN:
                    self._controls_down = False
                case pygame.K_d | pygame.K_RIGHT:
                    self._controls_right = False

    def _on_loop(self):
        if self._board.lost:
            self._menu = True
        else:
            if self._time == self._time_to_move_down:
                self._board.move_current_piece(0, 1)
                self._time = 0
            else:
                self._time += 1

            if self._controls_right:
                self._board.move_current_piece(1, 0)
            elif self._controls_left:
                self._board.move_current_piece(-1, 0)
            elif self._controls_up:
                self._board.rotate_current_piece()
            elif self._controls_down:
                self._board.move_current_piece(0, 1)

    def _on_render(self):
        self._display_surf.fill((0, 0, 0))
        if self._menu:
            self._menu_button.render(self._display_surf)
        else:
            self._board.render(self._display_surf)
        pygame.display.flip()
        self._FPS.tick(20)

    def on_execute(self):
        self._on_init()

        while self._running:
            for event in pygame.event.get():
                self._on_event(event)
            self._on_loop()
            self._on_render()
        pygame.quit()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
