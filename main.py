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
frames = 6
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
    offset = 0
    player.info = "SCORE = " + str(player.score) + "        LIVES = " + str(
        player.lives) + "       TIME LEFT= " + str(player.time)
    game_map = scenery(player, rows, columns, frames)
    start_time = time.time()
    while(1):
        if input.kbhit():
            val = input.getch()
            if(val == 'q'):
                break
            player.move(val)
        else:
            # use gravity when nothing is pressed
            player.gravity()

        player.check(world_x, world_y, offset)
        game_map.object(player)
        output_str = ""
        for row in range(rows):
            for col in range(columns):
                output_str += game_map.grid[row][offset + col]
            output_str += '\n'

        print('\033[H' + output_str)
        game_map.clear(player)
        tm = time.time()
        diff = tm - start_time
        diff = int(diff)
        if diff == 1:
            offset += 1
            # done so that with screen moving back player's position should remain same
            player.move('d')
            start_time = tm

        # bring cursor to start instead of clearing the full screen
        sys.stdin.flush()
        sys.stdout.flush()
        # time.sleep(0.03)

    input.show_cursor()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
