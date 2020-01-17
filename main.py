import colorama
from colorama import Fore, Back, Style
from scenery import scenery
from input import input
from character import *
from objects import shoot
from game_over import *
import termios
from check import *
import subprocess as sp
import time
import tty
import sys
import os

colorama.init()
rows, columns = 30, 90
frames = 12
offset_inc = 1
global_time = 0
fast_offset_inc = 2
shield_renew_time = 30
shield_time = 10
# due to 0 based indexing of the grid
world_x = columns - 1
world_y = rows - 1

if __name__ == "__main__":
    # disabling buffering so don't have to press enter
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    player = Person(world_x, world_y)
    bossenemy = BossEnemy(world_x*frames, world_y)
    input = input()
    input.hide_cursor()
    offset = 0
    player.info = "SCORE = " + str(player.score) + "        LIVES = " + str(
        player.lives) + "       TIME LEFT= " + str(player.time)
    game_map = scenery(player, rows, columns, frames)
    start_time = time.time()
    bullets = []
    global_time = time.time()
    gtime = time.time()

    while(1):
        if bossenemy.life <= 0 and player.lives != 0 and player.time != 0:
            won(game_map, offset, rows, columns)
            player.info = "SCORE = " + str(player.score) + "        LIVES = " + str(
                player.lives) + "       TIME LEFT= " + str(player.time)
            for val in range(columns):
                if(len(player.info) > val):
                    game_map.grid[0][offset +
                                     val] = Fore.YELLOW + player.info[val]
                else:
                    game_map.grid[0][offset +
                                     val] = Back.BLACK + Fore.BLACK + ' '
            output_str = ""
            for row in range(rows):
                for col in range(columns):
                    output_str += game_map.grid[row][offset + col]
                output_str += '\n'
            print('\033[H' + output_str)
            break

        if player.lives <= 0 or player.time == 0:
            loose(game_map, offset, rows, columns)
            player.info = "SCORE = " + str(player.score) + "        LIVES = " + str(
                player.lives) + "       TIME LEFT= " + str(player.time)
            for val in range(columns):
                if(len(player.info) > val):
                    game_map.grid[0][offset +
                                     val] = Fore.YELLOW + player.info[val]
                else:
                    game_map.grid[0][offset +
                                     val] = Back.BLACK + Fore.BLACK + ' '
            output_str = ""
            for row in range(rows):
                for col in range(columns):
                    output_str += game_map.grid[row][offset + col]
                output_str += '\n'
            print('\033[H' + output_str)
            break
        if offset >= (frames-1)*(columns) - 2:
            offset_inc = 0
            fast_offset_inc = 0

        if time.time() - global_time >= 1:
            global_time += 1
            player.time -= 1

        if input.kbhit():
            val = input.getch()
            if(val == 'q' or val == 'Q'):
                break
            if val == ' ':
                bullet = shoot(player.pos_x + player.width,
                               player.pos_y - player.height + 1, world_x + offset - 1)
                bullets.append(bullet)
            elif val == 's':
                if player.shield == 0 and time.time() - player.prev_shield_occur >= shield_renew_time:
                    player.shield = 1
                    player.shield_time = time.time()
            else:
                player.change_vel(val)
        else:
            # pass
            if time.time() - gtime >= 0.022:
                player.vely += player.gravity
                gtime = time.time()

        if player.dragon == 1:
            bullet = shoot(player.pos_x + player.width,
                           player.pos_y - player.height + 1, world_x + offset - 1)
            bullets.append(bullet)

        if player.shield == 1:
            if time.time() - player.shield_time >= shield_time:
                player.shield = 0
                player.shield_time = 0
                player.prev_shield_occur = time.time()

        for val in bullets:
            if val.pos_x > val.limit:
                val.active = 0
            if val.active == 1:
                game_map.object(val)

        if player.shield == 0:
            if game_map.mgnt_pos_x >= offset and game_map.mgnt_pos_x <= columns + offset:
                if abs(game_map.mgnt_pos_x - player.pos_x) <= game_map.mgnt_rangex:
                    if game_map.mgnt_pos_y < player.pos_y:
                        player.vely -= 0.61
                    elif game_map.mgnt_pos_y > player.pos_y:
                        player.vely += 0.61
                    if game_map.mgnt_pos_x < player.pos_x:
                        player.velx -= 1
                    elif game_map.mgnt_pos_x > player.pos_x:
                        player.velx += 1
            game_map.objectm(game_map.magnet[0])

        # if time.time() - gtime >= 0.022:
        #     player.vely += player.gravity
        #     gtime = time.time()

        player.change_pos()
        player.check(world_x, world_y, offset)
        if game_map.mgnt_pos_x >= offset and game_map.mgnt_pos_x <= columns + offset:
            player.pos_y = max(player.pos_y, game_map.mgnt_pos_y + 3)
        # check_coins should be before game_map.object as in check_coins we are checking if at positions there is some coin but in game_map we
        # are rewriting that position with player

        # to adjust position of boss enemy according to player's position
        if int(offset/((frames-2)*columns)) > 0:
            bossenemy.change_pos(offset+1, player.pos_y, rows)
            game_map.object(bossenemy)
            for blt in bossenemy.bullets:
                if blt.active == 1:
                    game_map.object(blt)

        check_player_speed_boost(game_map, player)
        check_player_dragon(game_map, player)
        if int(offset/((frames-2)*columns)) > 0:
            check_player_bossenemy(player, bossenemy)
            check_bossenemy_bullets(bullets, bossenemy, game_map)
            check_player_bossenemybullets(game_map, player, bossenemy)
        check_flames_bullets(bullets, game_map, player)
        check_flames(game_map, player)
        check_coins(game_map, player)
        if player.dragon == 1:
            if player.cnt <= 10:
                dragon(player, 'dragon1.txt')
                player.cnt += 1
            else:
                dragon(player, 'dragon2.txt')
                player.cnt += 1
                if player.cnt == 20:
                    player.cnt = 0

        if player.dragon == 0:
            player.height = 3
            player.width = 3
            player.char = [[' ', '0', ' '], ['-', '|', '-'], ['/', '|', '\\']]
        game_map.objectp(player)

        # to update score lives and time everytime

        player.info = "SCORE = " + str(player.score) + "        LIVES = " + str(
            player.lives) + "       TIME LEFT= " + str(player.time)
        if player.shield == 0 and time.time() - player.prev_shield_occur >= shield_renew_time:
            player.info += "       Shield Available"
        elif player.shield == 1:
            player.info += "        Shield In Use"
        else:
            player.info += "        Shield Not Available"
        for val in range(columns):
            if(len(player.info) > val):
                game_map.grid[0][val] = Fore.YELLOW + player.info[val]
            else:
                game_map.grid[0][val] = Back.BLACK + Fore.BLACK + ' '
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
        if int(offset/((frames-2)*columns)) > 0:
            game_map.clear(bossenemy)
            for blt in bossenemy.bullets:
                if blt.active == 1:
                    game_map.clear(blt)
                    blt.pos_x -= blt.vel_x
                    blt.pos_y += blt.vel_y
                    # checkf for bullet colission person
                    if blt.pos_x < blt.limit_x or blt.pos_y > blt.limit_y:
                        blt.active = 0

        tm = time.time()
        diff = tm - start_time
        if diff > 0.04 and offset < columns*(frames-1):
            if game_map.speedboost_active == 1:
                offset += fast_offset_inc
            else:
                offset += offset_inc
            # done so that with screen moving back player's position should remain same
            if game_map.speedboost_active == 1:
                player.velx += fast_offset_inc
            else:
                player.velx += offset_inc
            player.change_pos()
            for val in bullets:
                if val.active == 1:
                    if game_map.speedboost_active == 1:
                        val.pos_x += fast_offset_inc
                    else:
                        val.pos_x += offset_inc
            start_time = tm

        player.velx = 0
        sys.stdin.flush()
        sys.stdout.flush()
        time.sleep(0.02)

    input.show_cursor()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
