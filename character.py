import colorama
from colorama import Fore, Back, Style
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
        # self.dy = 0.0013
        self.char = [[' ', '0', ' '], ['-', '|', '-'], ['/', '|', '\\']]
        self.color = Fore.BLUE
        self.lives = 3
        self.score = 0
        self.time = 100
        self.info = " "

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
