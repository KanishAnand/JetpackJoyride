from config import *
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

if __name__ == "__main__":
    # disabling buffering so don't have to press enter
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    player = Person(1, world_y)
    bossenemy = BossEnemy((world_x+1)*frames - 2, world_y)
    input = input()
    input.hide_cursor()
    info = "SCORE = " + str(player.get_score()) + "        LIVES = " + str(
        player.get_lives()) + "       TIME LEFT= " + str(player.get_time())
    player.change_info(info)
    game_map = scenery(player, rows, columns, frames)
    start_time = time.time()
    offset = 0
    bullets = []
    global_time = time.time()
    gtime = time.time()

    while(1):
        prev_life = player.get_lives()
        if bossenemy.get_lives() <= 0 and player.get_lives() != 0 and player.get_time() != 0:
            won(game_map, offset, rows, columns)
            info = "SCORE = " + str(player.get_score()) + "        LIVES = " + str(
                player.get_lives()) + "       TIME LEFT= " + str(player.get_time())
            player.change_info(info)
            for val in range(columns):
                if(len(player.get_info()) > val):
                    game_map.change_grid(0, offset +
                                         val, Fore.YELLOW + (player.get_info())[val])
                else:
                    game_map.change_grid(0, offset +
                                         val, Back.BLACK + Fore.BLACK + ' ')
            output_str = ""
            for row in range(rows):
                for col in range(columns):
                    output_str += game_map.get_grid(row, offset + col)
                output_str += '\n'
            print('\033[H' + output_str)
            break

        if player.get_lives() <= 0 or player.get_time() == 0:
            loose(game_map, offset, rows, columns)
            info = "SCORE = " + str(player.get_score()) + "        LIVES = " + str(
                player.get_lives()) + "       TIME LEFT= " + str(player.get_time())
            player.change_info(info)

            for val in range(columns):
                if(len(player.get_info()) > val):
                    game_map.change_grid(0, offset +
                                         val, Fore.YELLOW + (player.get_info())[val])
                else:
                    game_map.change_grid(0, offset +
                                         val, Back.BLACK + Fore.BLACK + ' ')
            output_str = ""
            for row in range(rows):
                for col in range(columns):
                    output_str += game_map.get_grid(row, offset + col)
                output_str += '\n'
            print('\033[H' + output_str)
            break
        if offset >= (frames-1)*(columns) - 2:
            offset_inc = 0
            fast_offset_inc = 0

        if time.time() - global_time >= 1:
            global_time += 1
            player.change_time(-1)

        if input.kbhit():
            val = input.getch()
            if(val == 'q' or val == 'Q'):
                break
            if val == 'b' or val == 'B':
                bullet = player.fire_laser(offset)
                bullets.append(bullet)
            elif val == ' ':
                if player.get_shield() == 0 and time.time() - player.get_prevshieldoccur() >= shield_renew_time:
                    player.change_shield(1)
                    player.change_shieldtime(time.time())
            else:
                player.change_vel(val)
        else:
            pass

        # if time.time() - gtime >= 0.2:
        # player.change_vely(player.get_gravity()*player._t)
        player._pos_y += round(player.get_gravity()*player._t)
        player._t += 0.2
        # gtime = time.time()

        if player.get_dragon() == 1:
            bullet = player.fire_laser(offset)
            bullets.append(bullet)

        if player.get_shield() == 1:
            if time.time() - player.get_shieldtime() >= shield_time:
                player.change_shield(0)
                player.change_shieldtime(0)
                player.change_prevshieldoccur(time.time())

        if player.get_speedboost() == 1 and time.time() - player.get_speedboosttime() >= 4:
            player.change_speedboost(0)
            game_map.change_speedboostactive(0)

        for val in bullets:
            if val.get_posx() > val.get_limit():
                val.change_active(0)
            if val.get_active() == 1:
                game_map.object(val)

        if player.get_shield() == 0:
            if game_map.get_mgntposx() >= offset and game_map.get_mgntposx() <= columns + offset:
                if abs(game_map.get_mgntposx() - player.get_posx()) <= game_map.get_mgntrangex():
                    if game_map.get_mgntposy() < player.get_posy():
                        player.change_vely(-0.61)
                    elif game_map.get_mgntposy() > player.get_posy():
                        player.change_vely(0.61)
                    if game_map.get_mgntposx() < player.get_posx():
                        player.change_velx(-1)
                    elif game_map.get_mgntposx() > player.get_posx():
                        player.change_velx(1)
            game_map.objectm((game_map.get_magnet())[0])

        if ((game_map.get_speedboost())[0]).get_active() == 1:
            game_map.objects((game_map.get_speedboost())[0])
        if ((game_map.get_dragon())[0]).get_active() == 1:
            game_map.objects((game_map.get_dragon())[0])

        player.change_pos()
        player.check(world_x, world_y, offset)
        # if game_map.get_mgntposx() >= offset and game_map.get_mgntposx() <= columns + offset:
        #     player.put_posy(max(
        #         player.get_posy(), game_map.get_mgntposy() + player._height))

        # check_coins should be before game_map.object as in check_coins we are checking if at positions there is some coin but in game_map we
        # are rewriting that position with player

        # to adjust position of boss enemy according to player's position
        if int(offset/((frames-2)*columns)) > 0:
            bossenemy.change_pos(offset+1, player.get_posy(), rows)
            game_map.object(bossenemy)
            for blt in bossenemy.get_bullets():
                if blt.get_active() == 1:
                    game_map.object(blt)

        check_player_speed_boost(game_map, player)
        check_player_dragon(game_map, player)
        if int(offset/((frames-2)*columns)) > 0:
            check_player_bossenemy(player, bossenemy)
            check_bossenemy_bullets(bullets, bossenemy, game_map)
            check_player_bossenemybullets(game_map, player, bossenemy)

        check_flames_bullets(bullets, game_map, player)
        check_flames(game_map, player)
        check_coins_bullets(game_map, bullets)
        check_coins(game_map, player)
        for cld in game_map.get_clouds():
            game_map.object(cld)

        if player.get_dragon() == 1:
            if player.get_cnt() <= 2:
                dragon(player, 'a.txt')
                player.change_cnt(1)
            elif player.get_cnt() <= 4:
                dragon(player, 'b.txt')
                player.change_cnt(1)
            elif player.get_cnt() <= 6:
                dragon(player, 'c.txt')
                player.change_cnt(1)
            elif player.get_cnt() <= 8:
                dragon(player, 'd.txt')
                player.change_cnt(1)
            elif player.get_cnt() <= 10:
                dragon(player, 'e.txt')
                player.change_cnt(1)
            else:
                dragon(player, 'f.txt')
                player.change_cnt(1)
                if player.get_cnt() == 12:
                    player.put_cnt(0)

        if player.get_dragon() == 0:
            player.change_height(3)
            player.change_width(3)
            player.change_char(
                [[' ', '0', ' '], ['-', '|', '-'], ['/', ' ', '\\']])
        game_map.objectp(player)

        # to update score lives and time everytime

        info = "SCORE = " + str(player.get_score()) + "        LIVES = " + str(
            player.get_lives()) + "       TIME LEFT= " + str(player.get_time())
        player.change_info(info)
        if player.get_shield() == 0 and time.time() - player.get_prevshieldoccur() >= shield_renew_time:
            player.change_info(info + "       Shield Available")
        elif player.get_shield() == 1:
            player.change_info(info + "        Shield In Use")
        else:
            player.change_info(info + "        Shield Not Available")
        for val in range(columns):
            if(len(player.get_info()) > val):
                game_map.change_grid(
                    0, val, Fore.YELLOW + (player.get_info())[val])
            else:
                game_map.change_grid(0, val, Back.BLACK + Fore.BLACK + ' ')

        game_map.object_sky(offset, columns)

        output_str = ""
        for row in range(rows):
            for col in range(columns):
                if(row == 0):
                    # to not move score lives and time line
                    output_str += game_map.get_grid(row, col)
                else:
                    output_str += game_map.get_grid(row, col+offset)
            output_str += '\n'

        # bring cursor to start instead of clearing the full screen
        print('\033[H' + output_str)

        for val in bullets:
            if val.get_active() == 1:
                game_map.clear(val)
                val.change_posx(2)

        game_map.clear(player)
        if int(offset/((frames-2)*columns)) > 0:
            game_map.clear(bossenemy)
            for blt in bossenemy.get_bullets():
                if blt.get_active() == 1:
                    game_map.clear(blt)
                    blt.change_posx(-blt.get_velx())
                    blt.change_posy(blt.get_vely())
                    # checkf for bullet colission person
                    if blt.get_posx() < blt.get_limitx() or blt.get_posy() > blt.get_limity() or blt.get_posy() < 2:
                        blt.change_active(0)

        tm = time.time()
        diff = tm - start_time
        if diff > 0.04 and offset < columns*(frames-1):
            if game_map.get_speedboostactive() == 1:
                offset += fast_offset_inc
            else:
                offset += offset_inc
            # done so that with screen moving back player's position should remain same
            if game_map.get_speedboostactive() == 1:
                player.change_velx(fast_offset_inc)
            else:
                player.change_velx(offset_inc)
            player.change_pos()
            for val in bullets:
                if val.get_active() == 1:
                    if game_map.get_speedboostactive() == 1:
                        val.change_posx(fast_offset_inc)
                    else:
                        val.change_posx(offset_inc)
            start_time = tm

        player.put_velx(0)
        sys.stdin.flush()
        sys.stdout.flush()
        time.sleep(0.02)
        final_life = player.get_lives()
        if final_life < prev_life:
            time.sleep(0.8)

    input.show_cursor()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
