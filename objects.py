import colorama
import numpy as np
from colorama import Fore, Back, Style
colorama.init()

# polymorphism


class coins:
    def __init__(self, height, width):
        self._height = height
        self._width = width

    def pos(self, x, y):
        self._pos_x = x
        self._pos_y = y
        self._color = Fore.YELLOW
        self._char = '$'

    def get_posx(self):
        return self._pos_x

    def get_posy(self):
        return self._pos_y

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width


class clouds:
    def __init__(self, x, y):
        self._pos_x = x
        self._pos_y = y
        self._color = Fore.WHITE
        self.clouds()

    def clouds(self):
        with open('clouds.txt', 'rb') as f:
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


class flame:
    def __init__(self):
        self._width = 1
        self._active = 1
        self._hitscore = 5
        # pos = 0 --> horizontal
        # pos = 1 --> vertical
        # pos = 2 --> at 45 angle

    def pos(self, x, y, h):
        self._pos_x = x
        self._pos_y = y
        self._height = h
        self._color_corners = Back.RED + Fore.RED + ' '
        self._color_fill = Back.YELLOW + Fore.YELLOW + ' '

    def angle(self, angle):
        self._angle = angle

    def get_active(self):
        return self._active

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_posx(self):
        return self._pos_x

    def get_posy(self):
        return self._pos_y

    def get_hitscore(self):
        return self._hitscore

    def get_angle(self):
        return self._angle

    def change_active(self, val):
        self._active = val


class shoot:
    def __init__(self, x, y, lim):
        # if this bullet is finished or not
        self._active = 1
        self._vel = 5
        self._height = 2
        self._width = 3
        self._limit = lim - self._width
        self._pos_x = x
        self._pos_y = y + self._height - 1
        self._color = Fore.CYAN
        self._char = ([['*' for col in range(self._width)]
                       for row in range(self._height)])

    def get_posx(self):
        return self._pos_x

    def get_posy(self):
        return self._pos_y

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_vel(self):
        return self._vel

    def get_limit(self):
        return self._limit

    def get_active(self):
        return self._active

    def change_active(self, val):
        self._active = val

    def change_posx(self, val):
        self._pos_x += val


class boss_shoot:
    def __init__(self, x, y, vely, lim, rows):
        # if this bullet is finished or not
        self._active = 1
        self._vel_x = 15
        self._vel_y = vely
        self._height = 3
        self._width = 3
        self._limit_x = lim
        self._limit_y = rows - 3
        self._pos_x = x
        self._pos_y = y
        self._color = Fore.WHITE
        self._char = [[' ', '*', ' '], ['*', '*', '*'], [' ', '*', ' ']]

    def get_active(self):
        return self._active

    def get_posx(self):
        return self._pos_x

    def get_posy(self):
        return self._pos_y

    def get_vely(self):
        return self._vel_y

    def get_velx(self):
        return self._vel_x

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_limitx(self):
        return self._limit_x

    def get_limity(self):
        return self._limit_y

    def change_active(self, val):
        self._active = val

    def change_posx(self, val):
        self._pos_x += val

    def change_posy(self, val):
        self._pos_y += val

    def change_vely(self, val):
        self._vel_y += val

    def change_velx(self, val):
        self._vel_x += val


class magnet:
    def __init__(self, x, y):
        self._pos_x = x
        self._pos_y = y
        self._height = 3
        self._width = 4
        self._color_left = Back.RED + Fore.BLACK
        self._color_right = Back.BLUE + Fore.BLACK
        self._transp = Back.BLACK + Fore.BLACK + ' '
        self._char = [[' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']]

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_posx(self):
        return self._pos_x

    def get_posy(self):
        return self._pos_y


class speedboost:
    def __init__(self, x, y, frm):
        self._pos_x = x
        self._pos_y = y
        self._height = 3
        self._width = 4
        self._active = 1
        self._speedboost_frame = frm
        self._color1 = Back.BLUE + Fore.BLACK
        self._color2 = Back.RED + Fore.BLACK
        self._transp = Back.BLACK + Fore.BLACK + ' '
        self._char = [[' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']]

    def change_active(self, val):
        self._active = val

    def get_active(self):
        return self._active

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_posx(self):
        return self._pos_x

    def get_posy(self):
        return self._pos_y


class dragon:
    def __init__(self, x, y, frm):
        self._pos_x = x
        self._pos_y = y
        self._height = 3
        self._width = 4
        self._active = 1
        self._dragon_frame = frm
        self._color1 = Back.YELLOW + Fore.BLACK
        self._color2 = Back.RED + Fore.BLACK
        self._transp = Back.BLACK + Fore.BLACK + ' '
        self._char = [[' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']]

    def change_active(self, val):
        self._active = val

    def get_active(self):
        return self._active

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_posx(self):
        return self._pos_x

    def get_posy(self):
        return self._pos_y
