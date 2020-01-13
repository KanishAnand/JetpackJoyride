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
