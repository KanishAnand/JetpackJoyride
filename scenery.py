import numpy as np
import colorama
from colorama import Fore, Back, Style
colorama.init()


class scenery:
    def __init__(self, player, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = ([[Back.BLACK + Fore.BLACK + ' ' for col in range(self.cols)]
                      for row in range(self.rows)])
        for val in range(self.cols):
            # sky
            if(len(player.info) > val):
                self.grid[0][val] = Fore.YELLOW + player.info[val]
            self.grid[1][val] = Fore.WHITE + 'X'
            # ground
            self.grid[self.rows - 1][val] = Fore.GREEN + 'X'
            self.grid[self.rows - 2][val] = Fore.GREEN + 'X'
            self.grid[self.rows - 3][val] = Fore.GREEN + 'X'

    def object(self, player):
        for y in range(0, player.height):
            for x in range(0, player.width):
                self.grid[player.pos_y - y][player.pos_x +
                                            x] = Fore.BLUE + player.char[player.height - 1 - y][x]
