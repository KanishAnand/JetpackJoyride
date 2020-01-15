import colorama
from colorama import Fore, Back, Style
colorama.init()

# polymorphism


class coins:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.color = Fore.YELLOW + '$'


class flame:
    def __init__(self):
        self.width = 1
        self.active = 1
        self.hitscore = 5
        # pos = 0 --> horizontal
        # pos = 1 --> vertical
        # pos = 2 --> at 45 angle

    def pos(self, x, y, h):
        self.pos_x = x
        self.pos_y = y
        self.height = h
        self.color_corners = Back.RED + Fore.RED + ' '
        self.color_fill = Back.YELLOW + Fore.YELLOW + ' '

    def angle(self, angle):
        self.angle = angle


class shoot:
    def __init__(self, x, y, lim):
        # if this bullet is finished or not
        self.active = 1
        self.vel = 5
        self.height = 2
        self.width = 3
        self.limit = lim - self.width
        self.pos_x = x
        self.pos_y = y
        self.color = Fore.CYAN
        self.char = ([['*' for col in range(self.width)]
                      for row in range(self.height)])


class boss_shoot:
    def __init__(self, x, y, lim, rows):
        # if this bullet is finished or not
        self.active = 1
        self.vel_x = 3
        self.vel_y = 1
        self.height = 3
        self.width = 3
        self.limit_x = lim
        self.limit_y = rows - 4
        self.pos_x = x
        self.pos_y = y
        self.color = Fore.WHITE
        self.char = [[' ', '*', ' '], ['*', '*', '*'], [' ', '*', ' ']]


class magnet:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.height = 3
        self.width = 4
        self.color_left = Back.RED + Fore.BLACK
        self.color_right = Back.BLUE + Fore.BLACK
        self.transp = Back.BLACK + Fore.BLACK + ' '
        self.char = [['X', 'X', 'X', 'X'],
                     ['X', ' ', ' ', 'X'], ['X', ' ', ' ', 'X']]


class speedboost:
    def __init__(self, x, y, frm):
        self.pos_x = x
        self.pos_y = y
        self.height = 3
        self.width = 4
        self.speedboost_frame = frm
        self.color1 = Back.BLUE + Fore.BLACK
        self.color2 = Back.RED + Fore.BLACK
        self.transp = Back.BLACK + Fore.BLACK + ' '
        self.char = [[' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']]
