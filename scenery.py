import numpy as np
import random
import colorama
from colorama import Fore, Back, Style
from objects import coins
colorama.init()


class scenery:
    def __init__(self, player, rows, cols, frames):
        self.rows = rows
        # 6 frames
        self.cols = cols*frames
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

        coin1 = coins(2, 12)
        # take care of random position so that it should not collide with upper border or lower border and other objects like player also
        a = random.randint(1, cols)
        b = random.randint(4, rows - 10)
        coin1.pos(a, b)
        for row in range(coin1.height):
            for col in range(coin1.width):
                self.grid[b - row][a + col] = coin1.color

        coin1 = coins(3, 8)
        # take care of random position so that it should not collide with upper border or lower border and other objects like player also
        a = random.randint(1, cols)
        b = random.randint(4, rows - 10)
        coin1.pos(a, b)
        for row in range(coin1.height):
            for col in range(coin1.width):
                self.grid[b - row][a + col] = coin1.color
                

    def object(self, player):
        for y in range(0, player.height):
            for x in range(0, player.width):
                self.grid[player.pos_y - y][player.pos_x +
                                            x] = Fore.BLUE + player.char[player.height - 1 - y][x]

    def clear(self, player):
        for y in range(0, player.height):
            for x in range(0, player.width):
                self.grid[player.pos_y - y][player.pos_x +
                                            x] = Back.BLACK + Fore.BLACK + ' '
