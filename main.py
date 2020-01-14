import colorama
from colorama import Fore, Back, Style
from scenery import scenery
from input import input
from character import Person
from objects import shoot
import termios
from check import *
import subprocess as sp
import time
import tty
import sys
import os

colorama.init()
rows, columns = 30, 90
frames = 6
flag = 0
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
    bullets = []

    while(1):
        if input.kbhit():
            val = input.getch()
            if(val == 'q' or val == 'Q'):
                break
            if val == ' ':
                bullet = shoot(player.pos_x + player.width,
                               player.pos_y - player.height + 1, world_x + offset - 1)
                bullets.append(bullet)
            else:
                player.change_vel(val)
        else:
            pass

        for val in bullets:
            if val.pos_x > val.limit:
                val.active = 0
            if val.active == 1:
                game_map.object(val)

        player.vely += player.gravity
        player.change_pos()
        player.check(world_x, world_y, offset)
        # check_coins should be before game_map.object as in check_coins we are checking if at positions there is some coin but in game_map we
        # are rewriting that position with player

        check_flames_bullets(bullets, game_map)
        check_flames(game_map, player)
        check_coins(game_map, player)
        game_map.object(player)
        # to update score lives and time everytime
        player.info = "SCORE = " + str(player.score) + "        LIVES = " + str(
            player.lives) + "       TIME LEFT= " + str(player.time)
        for val in range(columns):
            if(len(player.info) > val):
                game_map.grid[0][val] = Fore.YELLOW + player.info[val]
        output_str = ""
        for row in range(rows):
            for col in range(columns):
                if(row == 0):
                    # to not move score lives and time line
                    output_str += game_map.grid[row][col]
                else:
                    output_str += game_map.grid[row][offset + col]
            output_str += '\n'

        # bring cursor to start instead of clearing the full screen
        print('\033[H' + output_str)

        for val in bullets:
            if val.active == 1:
                game_map.clear(val)
                val.pos_x += 2
        game_map.clear(player)
        tm = time.time()
        diff = tm - start_time
        if diff > 0.04:
            offset += 1
            # done so that with screen moving back player's position should remain same
            player.velx += 1
            player.change_pos()
            for val in bullets:
                if val.active == 1:
                    val.pos_x += 1
            start_time = tm

        player.velx = 0
        sys.stdin.flush()
        sys.stdout.flush()
        time.sleep(0.02)

    input.show_cursor()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
