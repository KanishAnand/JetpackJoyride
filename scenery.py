import numpy as np
import random
import colorama
from colorama import Fore, Back, Style
from objects import coins, flame
colorama.init()


class scenery:
    def __init__(self, player, rows, cols, frames):
        self.rows = rows
        # 6 frames
        self.cols = cols*frames
        self.grid = ([[Back.BLACK + Fore.BLACK + ' ' for col in range(self.cols)]
                      for row in range(self.rows)])
        self.coins_x = []
        self.coins_y = []
        for val in range(self.cols):
            # sky
            if(len(player.info) > val):
                self.grid[0][val] = Fore.YELLOW + player.info[val]
            self.grid[1][val] = Fore.WHITE + 'X'
            # ground
            self.grid[self.rows - 1][val] = Fore.GREEN + 'X'
            self.grid[self.rows - 2][val] = Fore.GREEN + 'X'
            self.grid[self.rows - 3][val] = Fore.GREEN + 'X'

        for val in range(frames):
            # take care of random position so that it should not collide with upper border or lower border and other objects like player also
            left = 1 + (cols-2)*val
            right = (cols-2)*(val+1)
            
            no_of_coins = random.randint(3,14)

            for val in range(no_of_coins):
                coin1 = coins(1, 1)
                a = random.randint(left, right)
                b = random.randint(4, rows - 10)
                self.coins_x.append(a)
                self.coins_y.append(b)
                coin1.pos(a, b)
                for row in range(coin1.height):
                    for col in range(coin1.width):
                        self.grid[b - row][a + col] = coin1.color

            no_of_flames = random.randint(1,3)
            
            for val in range(no_of_flames):
                flame1 = flame()
                angle = random.randint(0,2)
                if angle == 0:
                    #horizontal
                    h = 15
                    flame1.angle(0)
                    a = random.randint(left, right-h-2)
                    b = random.randint(4 , rows-5)
                    flame1.pos(a, b,h)
                elif angle == 1:
                    #vertical
                    h = 6
                    flame1.angle(1)
                    a = random.randint(left, right)
                    b = random.randint(4 + h , rows - 5)
                    flame1.pos(a, b,h)
                else:
                    #45 degree
                    h = 7
                    flame1.angle(2)
                    a = random.randint(left, right - h - 2)
                    b = random.randint(4 +h, rows-5)
                    flame1.pos(a, b,h)


                for row in range(flame1.height):
                    if flame1.angle == 1:
                        if row == 0 or row == flame1.height - 1:
                            self.grid[b-row][a] = flame1.color_corners
                        else:
                            self.grid[b-row][a] = flame1.color_fill

                    elif flame1.angle == 0:
                        if row == 0 or row == flame1.height - 1:
                            self.grid[b][a+row] = flame1.color_corners
                        else:
                            self.grid[b][a+row] = flame1.color_fill
                    else:
                        if row == 0 or row == flame1.height - 1:
                            self.grid[b-row][a+row] = flame1.color_corners
                        else:
                            self.grid[b-row][a+row] = flame1.color_fill

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
