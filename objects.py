import colorama
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
        self._color = Fore.YELLOW + '$'


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


class boss_shoot:
    def __init__(self, x, y, lim, rows):
        # if this bullet is finished or not
        self._active = 1
        self._vel_x = 9
        self._vel_y = 1
        self._height = 3
        self._width = 3
        self._limit_x = lim
        self._limit_y = rows - 4
        self._pos_x = x
        self._pos_y = y
        self._color = Fore.WHITE
        self._char = [[' ', '*', ' '], ['*', '*', '*'], [' ', '*', ' ']]


class magnet:
    def __init__(self, x, y):
        self._pos_x = x
        self._pos_y = y
        self._height = 3
        self._width = 4
        self._color_left = Back.RED + Fore.BLACK
        self._color_right = Back.BLUE + Fore.BLACK
        self._transp = Back.BLACK + Fore.BLACK + ' '
        self._char = [['X', 'X', 'X', 'X'],
                      ['X', ' ', ' ', 'X'], ['X', ' ', ' ', 'X']]


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
