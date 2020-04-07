import sys
from typing import List, Tuple

from button_class import *
from settings import *


class App:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.grid_check = []
        self.grid = []
        self.mousePos = (0, 0)
        self._selected = (-1, -1)
        self.playing_buttons = []
        self.end_buttons = []
        self.menu_buttons = []
        self.load_buttons()
        self.font = pygame.font.SysFont("arial", cell_size // 2)
        self.invalid = []
        self.solved = False
        self.load()

    """ Initializing Functions """
    @staticmethod
    def set_title_and_icon():
        """ Set The Title And The Icon Of The Main Window """
        pygame.display.set_caption("Sukodu")
        icon = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(icon)

    def load(self):
        """ Load Game Resources """
        self.set_title_and_icon()
        self.load_buttons()
        self.update_grid(test_board_1)

    def load_buttons(self):
        """ Load All The Buttons """
        self.playing_buttons.append(Button(20, 40, 100, 40, "Hello"))

    """ Main Game Functions """

    def run(self):
        """ Play Function """
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()
            pygame.display.update()
        pygame.quit()
        sys.exit()

    def events(self):
        """ Look For Game Events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.set_selected(self.mouse_on_grid())
            if self.get_selected() is not None and event.type == pygame.KEYDOWN:
                selected = self.get_selected()
                if event.key == pygame.K_UP:
                    self.find_next_unlocked(selected[0], selected[1], 0, -1)
                if event.key == pygame.K_DOWN:
                    self.find_next_unlocked(selected[0], selected[1], 0, 1)
                if event.key == pygame.K_LEFT:
                    self.find_next_unlocked(selected[0], selected[1], -1, 0)
                if event.key == pygame.K_RIGHT:
                    self.find_next_unlocked(selected[0], selected[1], 1, 0)
                if event.unicode != '' and event.unicode in '123456789':
                    self.grid[selected[0]][selected[1]] = int(event.unicode)
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.grid[selected[0]][selected[1]] = 0

    def update(self):
        """ This Will Call All The Update Functions """
        self.mousePos = pygame.mouse.get_pos()
        self.update_button_hover_status()
        self.update_invalid()
        self.update_status()

    def draw(self):
        """ This Will Call All The Draw Functions """
        self.screen.fill(WHITE)
        self.color_invalid()
        self.draw_selected()
        self.shade_locked_cells()
        self.draw_grid()
        self.draw_buttons()
        self.draw_numbers()

    """ Draw Functions """

    def draw_grid(self):
        """ It Draws The Main Grid """
        pygame.draw.rect(self.screen, BLACK,
                         (*grid_pos, WIDTH - 150, HEIGHT-150), 2)
        for x in range(9):
            pygame.draw.line(
                self.screen,
                BLACK,
                (grid_pos[0] + (x * cell_size), grid_pos[1]),
                (grid_pos[0] + (x * cell_size), grid_pos[1] + 450),
                2 if x % 3 == 0 else 1
            )
            pygame.draw.line(
                self.screen,
                BLACK,
                (grid_pos[0], grid_pos[1] + (x * cell_size)),
                (grid_pos[0] + 450, grid_pos[1] + (x * cell_size)),
                2 if x % 3 == 0 else 1
            )

    def draw_selected(self):
        """ It Colors The Selected Cell """
        if self.get_selected() is not None and not self.check_if_locked(self.get_selected()):
            self.color_cell(pos=self.get_selected(
            ), color=SELECTED_INVALID if self.get_selected() in self.invalid else SELECTED)

    def draw_numbers(self):
        """ It Will Draw The Numbers On The Board """
        for i in range(9):
            for j in range(9):
                pos = self.get_pos_in_grid(i, j)
                text = self.grid[i][j]
                text = '' if text == 0 else str(text)
                self.text_to_screen(text, pos)

    def draw_buttons(self):
        """ This Will Draw All The Buttons Onto The Screen """
        for button in self.playing_buttons:
            button.draw(self.screen)

    def shade_locked_cells(self):
        """ It Will Shade All The Locked Cells """
        for i in range(9):
            for j in range(9):
                if self.grid_check[i][j] != 0:
                    self.color_cell(pos=(i, j), color=LOCKED_CELL)

    def color_invalid(self):
        """ It Will Color The Invalid Entry """
        for i in self.invalid:
            self.color_cell(i, INVALID)

    """ Update Functions """

    def update_invalid(self):
        """ Check For All The InValid Entries And Add Them To The InValid List """
        self.invalid = []
        for i in range(9):
            for j in range(9):
                if not self.check_if_locked((i, j)) and not self.check_entered((i, j)) and self.grid[i][j] != 0:
                    self.invalid.append((i, j))

    def update_status(self):
        """ Check Weather The Game Is Solved Or Not """
        if len(self.invalid) != 0:
            return False
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return False
        self.solved = True
        print("solved")
        return True

    def update_button_hover_status(self):
        """ This Will Update The Button Hover Status """
        for button in self.playing_buttons:
            button.update(self.mousePos)

    """ Helper Functions """

    def find_next_unlocked(self, x: int, y: int, i: int, j: int):
        """ Find The Next Cell Which Is Unlocked From The Given Position """
        if i == -1:
            for a in range(x - 1, -1, -1):
                if not self.check_if_locked((a, y)):
                    self.set_selected((a, y))
                    return
        if i == 1:
            for a in range(x + 1, 9):
                if not self.check_if_locked((a, y)):
                    self.set_selected((a, y))
                    return
        if j == -1:
            for a in range(y - 1, -1, -1):
                if not self.check_if_locked((x, a)):
                    self.set_selected((x, a))
                    return
        if j == 1:
            for a in range(y + 1, 9):
                if not self.check_if_locked((x, a)):
                    self.set_selected((x, a))
                    return

    def mouse_on_grid(self):
        """ Finds The Mouse Position Relative To The Grid """
        if self.mousePos[0] < grid_pos[0] or self.mousePos[1] < grid_pos[1]:
            return None
        if self.mousePos[0] > grid_pos[0] + grid_size or self.mousePos[1] > grid_pos[1] + grid_size:
            return None
        temp = (self.mousePos[0] - grid_pos[0]
                ) // cell_size, (self.mousePos[1] - grid_pos[1]) // cell_size
        if not self.check_if_locked(temp):
            return temp

    def check_if_locked(self, pos: Tuple[int, int]) -> bool:
        return self.grid_check[pos[0]][pos[1]] != 0

    def text_to_screen(self, text: str, pos: Tuple[int, int]):
        font = self.font.render(text, False, BLACK)
        pos = pos[0] + cell_size // 3, pos[1] + cell_size // 4
        self.screen.blit(font, pos)

    @staticmethod
    def get_pos_in_grid(i: int, j: int):
        return grid_pos[0] + i * cell_size, grid_pos[1] + j * cell_size

    def color_cell(self, pos: Tuple[int, int], color: Tuple[int, int, int]):
        position = self.get_pos_in_grid(pos[0], pos[1])
        pygame.draw.rect(self.screen, color, (*position, cell_size, cell_size))

    def check_entered(self, pos: Tuple[int, int]) -> bool:
        value = self.grid[pos[0]][pos[1]]
        for i in range(9):
            if value == self.grid[pos[0]][i] and pos[1] != i:
                return False
            if value == self.grid[i][pos[1]] and pos[0] != i:
                return False
        for i in range(pos[0] - pos[0] % 3, pos[0] + 3 - pos[0] % 3):
            for j in range(pos[1] - pos[1] % 3, pos[1] + 3 - pos[1] % 3):
                if value == self.grid[i][j] and pos != (i, j):
                    return False
        return True

    def update_grid(self, grid: List[List[int]]):
        self.grid_check = [[grid[j][i]
                            for j in range(len(grid))] for i in range(len(grid[0]))]
        self.grid = [[j for j in i] for i in self.grid_check]

    """ Getters And Setters """

    def get_selected(self) -> Tuple[int, int]:
        return self._selected if self._selected != (-1, -1) else None

    def set_selected(self, value: Tuple[int, int]):
        if value:
            self._selected = value
        else:
            self._selected = (-1, -1)
