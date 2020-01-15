import numpy as np
import colorama
from colorama import Fore, Back, Style
from objects import boss_shoot
colorama.init()


class Person:
    def __init__(self, world_x, world_y):
        # pos_x and pos_y represent coordinates of bottom left point of figure
        self.pos_x = 1
        self.pos_y = world_y - 3
        self.height = 3
        self.width = 3
        self.velx = 0
        self.vely = 0
        self.gravity = 0.1
        self.char = [[' ', '0', ' '], ['-', '|', '-'], ['/', '|', '\\']]
        # self.char = [[' ', '0', ' '], ['/', '0', '\\'], ['/', ' ', '\\']]
        self.color = Fore.BLUE
        self.shieldactive_color = Fore.MAGENTA
        self.lives = 3
        self.score = 0
        self.time = 100
        self.info = " "
        self.speedboost = 0
        self.shield = 0
        self.shield_time = 0
        self.prev_shield_occur = -100

    def check(self, world_x, world_y, offset):
        # check for limits out of screen
        if self.pos_x + self.width - 1 > world_x - 1 + offset:
            self.pos_x = world_x - self.width + offset
        if self.pos_x < offset + 1:
            self.pos_x = offset + 1
        if self.pos_y >= world_y - 3:
            self.pos_y = world_y - 3
            self.vely = 0
        if self.pos_y - self.height + 1 <= 2:
            self.pos_y = self.height + 1
            # here self.pos_y is made 1 to give it downward force else it got stuck at top as always gravity rounds to 0 and here vely becomes 0
            self.vely = 0
            self.pos_y += 1

    # def gravity(self):
    #     self.pos_y += 2

    def change_vel(self, val):
        if(val == 'a' or val == 'A'):
            self.velx -= 1
        elif(val == 'd' or val == 'D'):
            self.velx += 1
        elif(val == 'w' or val == 'W'):
            self.vely -= 1

    def change_pos(self):
        self.pos_x += round(self.velx)
        self.pos_y += round(self.vely)


class BossEnemy:
    def __init__(self, x, y):
        self.color = Fore.RED
        self.active = 1
        self.vel_x = -5
        self.cnt = 0
        self.life = 10
        self.bullets = []
        self.make_arr(x, y)

    def make_arr(self, x, y):
        with open('BossEnemy.txt', 'rb') as f:
            arr = []
            cnt = 0
            mx = -1
            for line in f:
                arr.append(line)
                mx = max(mx, len(arr[cnt]))
                cnt += 1
        f.close()
        self.height = len(arr)
        self.width = mx
        self.pos_x = x - self.width
        self.pos_y = y - 3
        self.char = np.array(([[' ' for col in range(self.width)]
                               for row in range(self.height)]))

        for i in range(self.height):
            # to remove last '\n' character in ascii art present already I have made loop till len(arr[i]) - 1
            for j in range(len(arr[i])-1):
                self.char[i][j] = chr(arr[i][j])

    def change_pos(self, limit_x, player_pos_y, rows):
        self.pos_y = max(player_pos_y, self.height+2)
        self.cnt += 1
        if self.cnt % 30 == 0:
            self.pos_x += self.vel_x
            if(self.pos_x < limit_x):
                self.pos_x = limit_x
            blt = boss_shoot(self.pos_x, self.pos_y -
                             self.height + 10, limit_x, rows)
            self.bullets.append(blt)
