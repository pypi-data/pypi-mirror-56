import pygame
import sys
import random
from datetime import datetime
import time


class LifeGame:
    def __init__(self, screen_width=840, screen_height=670, cell_size=10, dead_color=(0, 0, 0),
                 alive_color=(50, 230, 200), max_fps=10):
        """
        Initialize grid, set default game state, initialize screen
        :param screen_width: Game window width
        :param screen_height: Game window height
        :param cell_size: Diameter of circles.
        :param dead_color: RGB tuple
        :param alive_color: RGB tuple
        :param max_fps: Framerate cap to limit game speed
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.dead_color = dead_color
        self.alive_color = alive_color
        self.max_fps = max_fps

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clear_screen()
        pygame.display.flip()

        self.last_frame_completed = 0
        self.desire_millisecond_between_updates = (1.0 / self.max_fps) * 1000.0

        self.num_col = int(self.screen_width / self.cell_size)
        self.num_row = int(self.screen_height / self.cell_size)
        self.active_state = 0
        self.grids = []
        self.init_grids()

        self.paused = False
        self.game_over = False

    def init_grids(self):
        """
        Creat and stores the default active and inactive grid
        :return: None
        """
        def creat_grid():
            """
            Genarate an empty 2 grid
            :return:
            """
            rows = []
            for i in range(self.num_row):
                columns = [0] * self.num_col
                rows.append(columns)
            return rows

        self.grids.append(creat_grid())
        self.grids.append(creat_grid())
        self.set_grid()

    def set_grid(self, value=None, grid=0):
        """
        Set an entire grid an once. Set to a single value or random 0/1

        Examples:
            set_grid(0) # all dead
            set_grid(1) # all alive
            set_grid() # random
            set_grid(None) # random

        :param value: Value to set the cells to 0 or 1
        :param grid: Index of grid for active or inactive (0/1)
        :return:
        """

        for r in range(self.num_row):
            for c in range(self.num_col):
                if value is None:
                    cell_value = random.choice([0, 1])
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value

    def draw_grid(self):
        """
        Given the grid and cell state. draw the cell on the screen
        :return:
        """
        self.clear_screen()
        for r in range(self.num_row):
            for c in range(self.num_col):
                if self.grids[self.active_state][r][c] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color
                circle_rect = pygame.draw.circle(self.screen,
                                                 color,
                                                 (int((c * self.cell_size) + (self.cell_size/2)),
                                                  int((r * self.cell_size) + (self.cell_size/2))),
                                                 int(self.cell_size/2),
                                                 0)

        pygame.display.flip()
        pass

    def clear_screen(self):
        """
        fill whole screen with the dead color
        :return:
        """
        self.screen.fill(self.dead_color)

    def get_cell(self, row_num, col_num):
        """
        Get the alive/dead (0/1) state of a specific  cell in active grid
        :param row_num:
        :param col_num:
        :return: 0 or 1 depending on state of cell. Defaults to 0 (dead)
        """
        try:
            cell_value = self.grids[self.active_state][row_num][col_num]
        except:
            cell_value = 0
        return cell_value

    def check_cell_neighbors(self, row_index, col_index):
        """
        Get the number of alive neighbor cells, and determine the state  of the cell
        for the next generation. Determine whether is lives, dead, survives, or is born
        :param row_index: Row number of the cell to check
        :param col_index: Column number of the cell to check
        :return: 0 or 1 depending on next generation state of cell
        """
        # Get the number of alive cells surrounding current cell
        num_alive_neighbors = 0

        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        # implement 4 rules of game
        if self.grids[self.active_state][row_index][col_index] == 1:
            if num_alive_neighbors > 3:  # Overpopulation
                return 0
            if num_alive_neighbors < 2:  # Underpopulation
                return 0
            if num_alive_neighbors == 3 or num_alive_neighbors == 2:
                return 1
        elif self.grids[self.active_state][row_index][col_index] == 0:
            if num_alive_neighbors == 3:
                return 1
        return self.grids[self.active_state][row_index][col_index]

    def update_generation(self):
        """
        Inspect the current generation state, prepare next generation
        Update the inactive grid to store next generation
        :return:
        """
        self.set_grid(0, self.inactive_grid())
        for r in range(self.num_row):
            for c in range(self.num_col):
                next_gen_state = self.check_cell_neighbors(r, c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state

        self.active_state = self.inactive_grid()

    def inactive_grid(self):
        """
        Simple helper function to get the index of the inactive grid. If active grid is 0 will return 1 and vice_versa
        :return:
        """
        return (self.active_state + 1) % 2

    def handle_events(self):
        """
        Handle any key presses:
        s : start/stop (pause) the game
        r: randomize the grid
        q: quit the game
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == 's':
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                elif event.unicode == 'r':
                    self.active_state = 0
                    self.set_grid(None, self.active_state)
                    self.set_grid(0, self.inactive_grid())
                elif event.unicode == 'q':
                    self.game_over = True
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        """
        Kick of the game and loop for ever until quit state
        :return:
        """
        while True:
            if self.game_over:
                return
            self.handle_events()
            if self.paused:
                continue

            self.update_generation()
            self.draw_grid()
            self.cap_frame_rate()

    def cap_frame_rate(self):
        """
        If game is running too fast and updating frames too frequently, just wait too maintain stable framerate

        :return:
        """
        now = pygame.time.get_ticks()
        time_after_last_update = now - self.last_frame_completed
        sleep_time = self.desire_millisecond_between_updates - time_after_last_update
        if sleep_time > 0:
            pygame.time.delay(int(sleep_time))
        self.last_frame_completed = now
