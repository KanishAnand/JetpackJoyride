import numpy as np
import random
import colorama
from colorama import Fore, Back, Style
from objects import *
from character import BossEnemy
colorama.init()


class scenery:
    def __init__(self, player, rows, cols, frames):
        self._rows = rows
        self._cols = cols*frames
        self._grid = ([[Back.BLACK + Fore.BLACK + ' ' for col in range(self._cols)]
                       for row in range(self._rows)])
        self._flames = []
        self._speedboost = []
        self._dragon = []
        self._speedboost_active = 0
        self._magnet = []
        self._coins_limit = 14

        for val in range(self._cols):
            # sky
            if(len(player._info) > val):
                self._grid[0][val] = Fore.YELLOW + player._info[val]
            self._grid[1][val] = Fore.WHITE + 'X'
            # ground
            self._grid[self._rows - 1][val] = Fore.GREEN + 'X'
            self._grid[self._rows - 2][val] = Fore.GREEN + 'X'
            self._grid[self._rows - 3][val] = Fore.GREEN + 'X'

        magnet_frame = random.randint(8, frames-2)
        speedboost_frame = random.randint(2, 4)
        dragon_frame = random.randint(5, 6)

        for ind in range(frames-1):
            # take care of random position so that it should not collide with upper border or lower border and other objects like player also
            left = 1 + (cols-2)*ind
            right = (cols-2)*(ind+1)

            no_of_flames = random.randint(1, 7)
            no_of_coins = random.randint(3, 30)
            prevx_coins = 1
            prevx_flames = 1

            while(no_of_coins != 0 and no_of_flames != 0):
                # COINS
                if no_of_coins != 0:
                    h = random.randint(1, 3)
                    w = random.randint(12, 25)
                    coin1 = coins(h, w)
                    if max(left, prevx_coins) > right - w - 1:
                        no_of_coins -= 1
                        continue
                    a = random.randint(max(left, prevx_coins), right - w - 1)
                    b = random.randint(4, self._coins_limit)
                    prevx_coins = a + w + 2
                    coin1.pos(a, b)
                    for row in range(coin1._height):
                        for col in range(coin1._width):
                            self._grid[b - row][a + col] = coin1._color
                    no_of_coins -= 1

                # FLAMES
                if no_of_flames != 0:
                    flame1 = flame()
                    angle = random.randint(0, 2)
                    if angle == 0:
                        # horizontal
                        h = 15
                        if(max(left, prevx_flames) > right-h-2):
                            no_of_flames -= 1
                            continue
                        flame1.angle(0)
                        a = random.randint(max(left, prevx_flames), right-h-2)
                        b = random.randint(self._coins_limit + 2, rows-5)
                        prevx_flames = a + h + 5
                        flame1.pos(a, b, h)
                    elif angle == 1:
                        # vertical
                        h = 6
                        if(max(left, prevx_flames) > right):
                            no_of_flames -= 1
                            continue
                        flame1.angle(1)
                        a = random.randint(max(left, prevx_flames), right)
                        b = random.randint(self._coins_limit + h + 2, rows - 5)
                        prevx_flames = a + 5
                        flame1.pos(a, b, h)
                    else:
                        # 45 degree
                        h = 7
                        if(max(left, prevx_flames) > right-h-2):
                            no_of_flames -= 1
                            continue
                        flame1.angle(2)
                        a = random.randint(
                            max(left, prevx_flames), right - h - 2)
                        b = random.randint(self._coins_limit + h + 2, rows-5)
                        prevx_flames = a + h + 5
                        flame1.pos(a, b, h)

                    self._flames.append(flame1)
                    for row in range(flame1._height):
                        if flame1._angle == 1:
                            if row == 0 or row == flame1._height - 1:
                                self._grid[b-row][a] = flame1._color_corners
                            else:
                                self._grid[b-row][a] = flame1._color_fill

                        elif flame1._angle == 0:
                            if row == 0 or row == flame1._height - 1:
                                self._grid[b][a+row] = flame1._color_corners
                            else:
                                self._grid[b][a+row] = flame1._color_fill
                        else:
                            if row == 0 or row == flame1._height - 1:
                                self._grid[b-row][a +
                                                  row] = flame1._color_corners
                            else:
                                self._grid[b-row][a+row] = flame1._color_fill

                    no_of_flames -= 1

            # MAGNET
            if ind == magnet_frame:
                if(prevx_coins > right):
                    a = random.randint(prevx_coins, right+5)
                else:
                    a = random.randint(prevx_coins, right)
                b = random.randint(4, self._coins_limit)
                prevx_coins = a + 2
                self._mgnt_frame = magnet_frame
                self._mgnt_rangex = 40
                self._mgnt_pos_x = a
                self._mgnt_pos_y = b
                mgnt = magnet(a, b)
                self._magnet.append(mgnt)
                for i in range(mgnt._height):
                    for j in range(mgnt._width):
                        if j < mgnt._width/2:
                            self._grid[b-i][a+j] = mgnt._color_left + \
                                mgnt._char[mgnt._height - 1 - i][j]
                        else:
                            self._grid[b-i][a+j] = mgnt._color_right + \
                                mgnt._char[mgnt._height - 1 - i][j]

                self._grid[b][a+1] = mgnt._transp
                self._grid[b][a+2] = mgnt._transp
                self._grid[b-1][a+1] = mgnt._transp
                self._grid[b-1][a+2] = mgnt._transp

            # SPEEDBOOST
            if ind == speedboost_frame:
                if(prevx_coins > right):
                    a = random.randint(prevx_coins, right+5)
                else:
                    a = random.randint(prevx_coins, right)
                b = random.randint(4, self._coins_limit)
                prevx_coins = a + 2
                spd = speedboost(a, b, speedboost_frame)
                self._speedboost.append(spd)
                for i in range(spd._height):
                    for j in range(spd._width):
                        if (b - i + a + j) % 2 == 0:
                            self._grid[b-i][a+j] = spd._color1 + \
                                spd._char[spd._height - 1 - i][j]
                        else:
                            self._grid[b-i][a+j] = spd._color2 + \
                                spd._char[spd._height - 1 - i][j]
                self._grid[b-1][a+1] = spd._transp
                self._grid[b-1][a+2] = spd._transp

            # DRAGON
            if ind == dragon_frame:
                if(prevx_coins > right):
                    a = random.randint(prevx_coins, right+5)
                else:
                    a = random.randint(prevx_coins, right)
                b = random.randint(4, self._coins_limit)
                prevx_coins = a + 2
                spd = dragon(a, b, speedboost_frame)
                self._dragon.append(spd)
                for i in range(spd._height):
                    for j in range(spd._width):
                        if (b - i + a + j) % 2 == 0:
                            self._grid[b-i][a+j] = spd._color1 + \
                                spd._char[spd._height - 1 - i][j]
                        else:
                            self._grid[b-i][a+j] = spd._color2 + \
                                spd._char[spd._height - 1 - i][j]
                self._grid[b-1][a+1] = spd._transp
                self._grid[b-1][a+2] = spd._transp

    def object(self, object):
        for y in range(0, object._height):
            for x in range(0, object._width):
                self._grid[object._pos_y - y][object._pos_x +
                                              x] = object._color + object._char[object._height - 1 - y][x]

    def objectp(self, object):
        for y in range(0, object._height):
            for x in range(0, object._width):
                if(object._shield == 0):
                    self._grid[object._pos_y - y][object._pos_x +
                                                  x] = object._color + object._char[object._height - 1 - y][x]
                else:
                    self._grid[object._pos_y - y][object._pos_x +
                                                  x] = object._shieldactive_color + object._char[object._height - 1 - y][x]

    def objectm(self, object):
        a = object._pos_x
        b = object._pos_y
        for i in range(object._height):
            for j in range(object._width):
                if j < object._width/2:
                    self._grid[b-i][a+j] = object._color_left + \
                        object._char[object._height - 1 - i][j]
                else:
                    self._grid[b-i][a+j] = object._color_right + \
                        object._char[object._height - 1 - i][j]

        self._grid[b][a+1] = object._transp
        self._grid[b][a+2] = object._transp
        self._grid[b-1][a+1] = object._transp
        self._grid[b-1][a+2] = object._transp

    def clear(self, object):
        for y in range(0, object._height):
            for x in range(0, object._width):
                self._grid[object._pos_y - y][object._pos_x +
                                              x] = Back.BLACK + Fore.BLACK + ' '
