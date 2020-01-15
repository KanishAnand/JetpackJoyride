import os
import tty
import sys
import termios
import colorama
from select import select


def kbhit():
    dr, dw, de = select([sys.stdin], [], [], 0)
    return dr != []


def getch():
    return sys.stdin.read(1)[0]


game_over = False
orig_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

while not game_over:
    if kbhit():
        x = getch()
        print("start")
        print(x)
        print("finish")
    else:
        pass
