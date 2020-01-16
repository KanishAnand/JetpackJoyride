import numpy as np
import random
import colorama
from colorama import Fore, Back, Style
from objects import *
from character import BossEnemy
colorama.init()


class scenery:
    def __init__(self, player, rows, cols, frames):
        self.rows = rows
        self.cols = cols*frames
        self.grid = ([[Back.BLACK + Fore.BLACK + ' ' for col in range(self.cols)]
                      for row in range(self.rows)])
        self.flames = []
        self.speedboost = []
        self.speedboost_active = 0
        self.magnet = []

        for val in range(self.cols):
            # sky
            if(len(player.info) > val):
                self.grid[0][val] = Fore.YELLOW + player.info[val]
            self.grid[1][val] = Fore.WHITE + 'X'
            # ground
            self.grid[self.rows - 1][val] = Fore.GREEN + 'X'
            self.grid[self.rows - 2][val] = Fore.GREEN + 'X'
            self.grid[self.rows - 3][val] = Fore.GREEN + 'X'

        magnet_frame = random.randint(4, frames-2)
        speedboost_frame = random.randint(2, 2)

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
                    if prevx_coins > right - w - 1:
                        no_of_coins -= 1
                        continue
                    a = random.randint(max(left, prevx_coins), right - w - 1)
                    b = random.randint(4, 11)
                    prevx_coins = a + w + 2
                    coin1.pos(a, b)
                    for row in range(coin1.height):
                        for col in range(coin1.width):
                            self.grid[b - row][a + col] = coin1.color
                    no_of_coins -= 1

                # FLAMES
                if no_of_flames != 0:
                    flame1 = flame()
                    angle = random.randint(0, 2)
                    if angle == 0:
                        # horizontal
                        h = 15
                        if(prevx_flames > right-h-2):
                            no_of_flames -= 1
                            continue
                        flame1.angle(0)
                        a = random.randint(max(left, prevx_flames), right-h-2)
                        b = random.randint(12, rows-5)
                        prevx_flames = a + h + 5
                        flame1.pos(a, b, h)
                    elif angle == 1:
                        # vertical
                        h = 6
                        if(prevx_flames > right):
                            no_of_flames -= 1
                            continue
                        flame1.angle(1)
                        a = random.randint(max(left, prevx_flames), right)
                        b = random.randint(10 + h, rows - 5)
                        prevx_flames = a + 5
                        flame1.pos(a, b, h)
                    else:
                        # 45 degree
                        h = 7
                        if(prevx_flames > right-h-2):
                            no_of_flames -= 1
                            continue
                        flame1.angle(2)
                        a = random.randint(
                            max(left, prevx_flames), right - h - 2)
                        b = random.randint(10 + h, rows-5)
                        prevx_flames = a + h + 5
                        flame1.pos(a, b, h)

                    self.flames.append(flame1)
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

                    no_of_flames -= 1

            # MAGNET
            if ind == magnet_frame:
                if(prevx_coins <= right):
                    a = random.randint(prevx_coins, right+4)
                else:
                    a = random.randint(prevx_coins, right)
                b = random.randint(4, 12)
                prevx_coins = a + 2
                self.mgnt_frame = magnet_frame
                self.mgnt_rangex = 40
                self.mgnt_pos_x = a
                self.mgnt_pos_y = b
                mgnt = magnet(a, b)
                self.magnet.append(mgnt)
                for i in range(mgnt.height):
                    for j in range(mgnt.width):
                        if j < mgnt.width/2:
                            self.grid[b-i][a+j] = mgnt.color_left + \
                                mgnt.char[mgnt.height - 1 - i][j]
                        else:
                            self.grid[b-i][a+j] = mgnt.color_right + \
                                mgnt.char[mgnt.height - 1 - i][j]

                self.grid[b][a+1] = mgnt.transp
                self.grid[b][a+2] = mgnt.transp
                self.grid[b-1][a+1] = mgnt.transp
                self.grid[b-1][a+2] = mgnt.transp

            # SPEEDBOOST
            if ind == speedboost_frame:
                if(prevx_coins <= right):
                    a = random.randint(prevx_coins, right+4)
                else:
                    a = random.randint(prevx_coins, right)
                b = random.randint(4, 12)
                prevx_coins = a + 2
                spd = speedboost(a, b, speedboost_frame)
                self.speedboost.append(spd)
                for i in range(spd.height):
                    for j in range(spd.width):
                        if (b - i + a + j) % 2 == 0:
                            self.grid[b-i][a+j] = spd.color1 + \
                                spd.char[spd.height - 1 - i][j]
                        else:
                            self.grid[b-i][a+j] = spd.color2 + \
                                spd.char[spd.height - 1 - i][j]
                self.grid[b-1][a+1] = spd.transp
                self.grid[b-1][a+2] = spd.transp

    def object(self, object):
        for y in range(0, object.height):
            for x in range(0, object.width):
                self.grid[object.pos_y - y][object.pos_x +
                                            x] = object.color + object.char[object.height - 1 - y][x]

    def objectp(self, object):
        for y in range(0, object.height):
            for x in range(0, object.width):
                if(object.shield == 0):
                    self.grid[object.pos_y - y][object.pos_x +
                                                x] = object.color + object.char[object.height - 1 - y][x]
                else:
                    self.grid[object.pos_y - y][object.pos_x +
                                                x] = object.shieldactive_color + object.char[object.height - 1 - y][x]

    def objectm(self, object):
        a = object.pos_x
        b = object.pos_y
        for i in range(object.height):
            for j in range(object.width):
                if j < object.width/2:
                    self.grid[b-i][a+j] = object.color_left + \
                        object.char[object.height - 1 - i][j]
                else:
                    self.grid[b-i][a+j] = object.color_right + \
                        object.char[object.height - 1 - i][j]

        self.grid[b][a+1] = object.transp
        self.grid[b][a+2] = object.transp
        self.grid[b-1][a+1] = object.transp
        self.grid[b-1][a+2] = object.transp

    def clear(self, object):
        for y in range(0, object.height):
            for x in range(0, object.width):
                self.grid[object.pos_y - y][object.pos_x +
                                            x] = Back.BLACK + Fore.BLACK + ' '
