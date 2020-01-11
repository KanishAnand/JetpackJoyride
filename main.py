import colorama
from colorama import Fore, Back, Style
from scenery import scenery
from input import input
from character import Person
import termios
import subprocess as sp
import time
import tty
import sys
import os

colorama.init()
rows, columns = 30, 90
# due to 0 based indexing of the grid
world_x = columns - 1
world_y = rows - 1

if __name__ == "__main__":
    # disabling buffering so don't have to press enter
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    player = Person(world_x, world_y)
    input = input()
    input.hide_cursor()

    while(1):
        if input.kbhit():
            val = input.getch()
            if(val == 'q'):
                break
            player.move(val)
        else:
            # use gravity when nothing is pressed
            player.gravity()

        player.check(world_x, world_y)
        player.info = "SCORE = " + str(player.score) + "        LIVES = " + str(player.lives) + "       TIME LEFT= " + str(player.time)
        game_map = scenery(player,rows, columns)
        game_map.object(player)
        output_str = ""
        for row in game_map.grid:
            for col in row:
                output_str += col
            output_str += '\n'
        # bring cursor to start instead of clearing the full screen
        print('\033[H' + output_str)
        sys.stdout.flush()
        time.sleep(0.1)

    input.show_cursor()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
