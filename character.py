import numpy as np
from config import *
import colorama
from colorama import Fore, Back, Style
from objects import boss_shoot, shoot
colorama.init()


# Inheritence : Person and BossEnemy are inherited from Character Class

class Character:
    def __init__(self, x, y):
        self._pos_x = x
        self._pos_y = y - 3
        self._gravity = 0.5
        self._t = 1
        self._velx = 0
        self._vely = 0
        self._cnt = 0


class Person(Character):
    def __init__(self, x, y):
        # pos_x and pos_y represent coordinates of bottom left point of figure
        self._height = 3
        self._width = 3
        self._dragon = 0
        self._char = [[' ', '0', ' '], ['-', '|', '-'], ['/', ' ', '\\']]
        # self.char = [[' ', '0', ' '], ['/', '0', '\\'], ['/', ' ', '\\']]
        self._color = Fore.BLUE
        self._shieldactive_color = Fore.MAGENTA
        self._lives = 3
        self._score = 0
        self._time = 100
        self._info = " "
        self._speedboost = 0
        self._speedboosttime = 0
        self._shield = 0
        self._shield_time = 0
        self._prev_shield_occur = -100
        super().__init__(x, y)

    def check(self, world_x, world_y, offset):
        # check for limits out of screen
        if self._pos_x + self._width - 1 > world_x - 1 + offset:
            self._pos_x = world_x - self._width + offset
        if self._pos_x < offset + 1:
            self._pos_x = offset + 1
        if self._pos_y >= world_y - 3:
            self._pos_y = world_y - 3
            self._vely = 0
            self._t = 1
        if self._pos_y - self._height + 1 <= 2:
            self._pos_y = self._height + 1
            # here self._pos_y is made 1 to give it downward force else it got stuck at top as always gravity rounds to 0 and here vely becomes 0
            self._vely = 0
            self._pos_y += 1
            self._t = 1

    def change_vel(self, val):
        if(val == 'a' or val == 'A'):
            self._velx -= 1
        elif(val == 'd' or val == 'D'):
            self._velx += 1
        elif(val == 'w' or val == 'W'):
            self._vely -= 1

    def fire_laser(self, offset):
        return shoot(self.get_posx() + self.get_width(),
                     self.get_posy() - self.get_height() + 1, world_x + offset - 1)

    def change_pos(self):
        self._pos_x += round(self._velx)
        self._pos_y += round(self._vely)

    def change_vely(self, val):
        self._vely += val

    def change_velx(self, val):
        self._velx += val

    def change_posx(self, val):
        self._pos_x += val

    def change_posy(self, val):
        self._pos_y += val

    def put_velx(self, val):
        self._velx = val

    def put_posx(self, val):
        self._pos_x = val

    def put_posy(self, val):
        self._pos_y = val

    def put_cnt(self, val):
        self._cnt = val

    def change_info(self, info):
        self._info = info

    def change_shield(self, val):
        self._shield = val

    def change_prevshieldoccur(self, val):
        self._prev_shield_occur = val

    def change_time(self, time):
        self._time += time

    def change_shield(self, val):
        self._shield = val

    def change_shieldtime(self, val):
        self._shield_time = val

    def change_cnt(self, val):
        self._cnt += val

    def change_height(self, val):
        self._height = val

    def change_width(self, val):
        self._width = val

    def change_char(self, val):
        self._char = val

    def change_life(self, val):
        self._lives += val

    def change_dragon(self, val):
        self._dragon = val

    def change_score(self, val):
        self._score += val

    def change_speedboost(self, val):
        self._speedboost = val

    def change_speedboosttime(self, val):
        self._speedboosttime = val

    def get_speedboost(self):
        return self._speedboost

    def get_lives(self):
        return self._lives

    def get_time(self):
        return self._time

    def get_score(self):
        return self._score

    def get_cnt(self):
        return self._cnt

    def get_speedboosttime(self):
        return self._speedboosttime

    def get_info(self):
        return self._info

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_posx(self):
        return self._pos_x

    def get_posy(self):
        return self._pos_y

    def get_shield(self):
        return self._shield

    def get_gravity(self):
        return self._gravity

    def get_dragon(self):
        return self._dragon

    def get_shieldtime(self):
        return self._shield_time

    def get_prevshieldoccur(self):
        return self._prev_shield_occur


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
        super().__init__(x, y)
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
        val = self._pos_y - self._height + 10
        if val < player_pos_y:
            vely = 1
        elif val > player_pos_y:
            vely = -1
        else:
            vely = 0
        self._cnt += 1
        if self._cnt % 24 == 0:
            self._pos_x += self._velx
            if(self._pos_x < limit_x):
                self._pos_x = limit_x
            blt = self.fire_laser(vely, limit_x, rows)
            self._bullets.append(blt)

    def fire_laser(self,  vely, limit_x, rows):
        return boss_shoot(self._pos_x, self._pos_y -
                          self._height + 10, vely, limit_x, rows)

    def get_lives(self):
        return self._life

    def get_bullets(self):
        return self._bullets

    def get_posx(self):
        return self._pos_x

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_posy(self):
        return self._pos_y

    def get_color(self):
        return self._color

    def change_life(self, val):
        self._life += val

    def change_color(self, val):
        self._color = val
