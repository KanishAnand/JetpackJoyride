import numpy as np
import colorama
from colorama import Fore, Back, Style
colorama.init()


class scenery:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = ([[Back.BLUE + Fore.BLUE + ' ' for col in range(self.cols)]
                      for row in range(self.rows)])

        # for row in range(self.rows):
        #     for cols in range(self.cols):
        #         self.grid[row][cols] = Back.BLUE + Fore.BLUE + ' '

    def object(self, pos_x, pos_y):
        self.grid[pos_y][pos_x] = Fore.RED + '+'
