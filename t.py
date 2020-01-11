import colorama
from colorama import Fore, Back, Style
from select import select
import termios
import subprocess as sp
# import atexit
import tty
import sys
import os

colorama.init()
rows, columns = os.popen('stty size', 'r').read().split()
world_x = int(columns)
world_y = int(rows) - 1

class Person:
    def __init__(self):
        self.pos_x = 50
        self.pos_y = 30
        self.char = "+"

    def update(self):
        # check for limits out of screen
        if self.pos_x > world_x:
            self.pos_x = world_x
        if self.pos_x < 1:
            self.pos_x = 1
        if self.pos_y > world_y:
            self.pos_y = world_y
        if self.pos_y < 1:
            self.pos_y = 1

        print(Fore.RED + "\033["+str(self.pos_y) +
              ";"+str(self.pos_x)+"H"+self.char)

    def gravity(self):
        self.pos_y += 3

    def move(self, val):
        if(val == 'a' or val == 'A'):
            self.pos_x -= 1
        elif(val == 'd' or val == 'D'):
            self.pos_x += 1
        elif(val == 'w' or val == 'W'):
            self.pos_y -= 1

if __name__ == "__main__":
    clear()
    # disabling buffering so you don't have to press enter
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

    while(1):
        print(Back.BLUE)
        print(colorama.ansi.clear_screen())
        print_char(pos_x, pos_y, "+")
        val = sys.stdin.read(1)[0]
        move(val)

    # enabling previous settings
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)



if __name__ == "__main__":
    # disabling buffering so you don't have to press enter
    # atexit.register(set_orig_settings)
    orig_settings = termios.tcgetattr(sys.stdin)
    set_new_settings()
    player = Person()
    hide_cursor()

    while(1):
        if kbhit():
            val = getch()
            if(val == 'q'):
                break
            player.move(val)
        else:
            # use gravity when nothing is pressed
            player.gravity()
        player.update()

    show_cursor()
    set_orig_settings()

    # enabling previous settings
    # termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, orig_settings)
