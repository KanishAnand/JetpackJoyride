import numpy as np
import colorama
from colorama import Fore, Back, Style
from objects import boss_shoot
colorama.init()

# Inheritence : Person and BossEnemy are inherited from Character Class


class Character:
    def __init__(self, x, y):
        self._pos_x = x
        self._pos_y = y - 3
        self._gravity = 0.15
        self._velx = 0
        self._vely = 0
        self._cnt = 0


class Person(Character):
    def __init__(self, x, y):
        # pos_x and pos_y represent coordinates of bottom left point of figure

        self._height = 3
        self._width = 3
        self._dragon = 0
        self._char = [[' ', '0', ' '], ['-', '|', '-'], ['/', '|', '\\']]
        # self.char = [[' ', '0', ' '], ['/', '0', '\\'], ['/', ' ', '\\']]
        self._color = Fore.BLUE
        self._shieldactive_color = Fore.MAGENTA
        self._lives = 3
        self._score = 0
        self._time = 100
        self._info = " "
        self._speedboost = 0
        self._shield = 0
        self._shield_time = 0
        self._prev_shield_occur = -100
        Character.__init__(self, x, y)

    def check(self, world_x, world_y, offset):
        # check for limits out of screen
        if self._pos_x + self._width - 1 > world_x - 1 + offset:
            self._pos_x = world_x - self._width + offset
        if self._pos_x < offset + 1:
            self._pos_x = offset + 1
        if self._pos_y >= world_y - 3:
            self._pos_y = world_y - 3
            self._vely = 0
        if self._pos_y - self._height + 1 < 2:
            self._pos_y = self._height + 1
            # here self._pos_y is made 1 to give it downward force else it got stuck at top as always gravity rounds to 0 and here vely becomes 0
            self._vely = 0
            self._pos_y += 1

    def change_vel(self, val):
        if(val == 'a' or val == 'A'):
            self._velx -= 1
        elif(val == 'd' or val == 'D'):
            self._velx += 1
        elif(val == 'w' or val == 'W'):
            self._vely -= 1

    def change_pos(self):
        self._pos_x += round(self._velx)
        self._pos_y += round(self._vely)


def dragon(self, filename):
    with open(filename, 'rb') as f:
        arr = []
        cnt = 0
        mx = -1
        for line in f:
            arr.append(line)
            mx = max(mx, len(arr[cnt]))
            cnt += 1
    f.close()
    self._height = len(arr)
    self._width = mx
    self._char = np.array(([[' ' for col in range(self._width)]
                            for row in range(self._height)]))

    for i in range(self._height):
        # to remove last '\n' character in ascii art present already I have made loop till len(arr[i]) - 1
        for j in range(len(arr[i])-1):
            self._char[i][j] = chr(arr[i][j])


class BossEnemy(Character):
    def __init__(self, x, y):
        self._color = Fore.RED
        self._active = 1
        self._life = 10
        self._bullets = []
        Character.__init__(self, x, y)
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
        self._height = len(arr)
        self._width = mx
        self._pos_x = x - self._width
        self._pos_y = y - 3
        self._char = np.array(([[' ' for col in range(self._width)]
                                for row in range(self._height)]))

        for i in range(self._height):
            # to remove last '\n' character in ascii art present already I have made loop till len(arr[i]) - 1
            for j in range(len(arr[i])-1):
                self._char[i][j] = chr(arr[i][j])

    def change_pos(self, limit_x, player_pos_y, rows):
        self._pos_y = max(player_pos_y, self._height+2)
        self._cnt += 1
        if self._cnt % 30 == 0:
            self._pos_x += self._velx
            if(self._pos_x < limit_x):
                self._pos_x = limit_x
            blt = boss_shoot(self._pos_x, self._pos_y -
                             self._height + 10, limit_x, rows)
            self._bullets.append(blt)
