import time
import colorama
from colorama import Fore, Back, Style
from playsound import playsound
colorama.init()


def check_coins(game_map, player):
    x = player.get_posx()
    y = player.get_posy()
    chr = Fore.YELLOW + '$'
    for row in range(player.get_height()):
        for col in range(player.get_width()):
            if game_map.get_grid(y-row, x+col) == chr:
                # playsound('coin.mp3', False)
                player.change_score(1)
                game_map.change_grid(
                    y-row, x+col, Back.BLACK + Fore.BLACK + ' ')

    # l = len(game_map._coins_x)
    # for ind in range(l):
    #     a = game_map._coins_x[ind]
    #     b = game_map._coins_y[ind]
    #     if a >= player._pos_x and a < player._pos_x + player._width:
    #         if b >= player._pos_y and b < player._pos_y + player._height:
    #             player._score += 1
    #             game_map._coins_x[ind] = -1
    #             game_map._coins_y[ind] = -1
    #             game_map._grid[b][a] = Back.BLACK + Fore.BLACK + ' '


def check_flames(game_map, player):
    for val in game_map.get_flames():
        if val.get_active() == 0:
            continue
        x = player.get_posx()
        y = player.get_posy()
        h = val.get_height()
        fx = val.get_posx()
        fy = val.get_posy()
        ang = val.get_angle()
        if ang == 0:
            # check condition
            if fy <= y and fy >= y - player.get_height() + 1:
                if (fx >= x and fx <= x + player.get_width() - 1) or (fx <= x and fx + h - 1 >= x + player.get_width() - 1) or (x <= fx + h - 1 and fx + h - 1 <= x + player.get_width() - 1):
                    if player.get_shield() == 0:
                        player.change_dragon(0)
                        player.change_life(-1)
                    val.change_active(0)
                    for ind in range(h):
                        game_map.change_grid(
                            fy, fx+ind, Back.BLACK + Fore.BLACK + ' ')

        elif ang == 1:
            if fx >= x and fx <= x + player.get_width() - 1:
                if (y >= fy and y - player.get_height() + 1 <= fy) or (y <= fy and y - player.get_height() + 1 >= fy - h + 1) or (y >= fy - h + 1 and y - player.get_height() + 1 <= fy - h + 1):
                    if player.get_shield() == 0:
                        player.change_dragon(0)
                        player.change_life(-1)
                    val.change_active(0)
                    for ind in range(h):
                        game_map.change_grid(
                            fy-ind, fx, Back.BLACK + Fore.BLACK + ' ')

        elif ang == 2:
            flag = 0
            oy = fy
            ox = fx
            for i in range(h):
                if (fx >= x and fx <= x + player.get_width() - 1 and fy <= y and fy >= y - player.get_width() + 1):
                    flag = 1
                    break
                fx += 1
                fy -= 1
            if flag == 1:
                if player.get_shield() == 0:
                    player.change_dragon(0)
                    player.change_life(-1)
                val.change_active(0)
                for ind in range(h):
                    game_map.change_grid(
                        oy-ind, ox+ind, Back.BLACK + Fore.BLACK + ' ')


def check_flames_bullets(bullets, game_map, player):
    for blt in bullets:
        if blt.get_active() == 0:
            continue
        left_x = blt.get_posx()
        right_x = blt.get_posx() + blt.get_width() - 1
        bottom_y = blt.get_posy()
        top_y = blt.get_posy() - blt.get_height() + 1

        for flm in game_map.get_flames():
            if flm.get_active() == 0:
                continue

            fleft_x = flm.get_posx()
            fright_x = flm.get_posx() + flm.get_width() - 1
            fbottom_y = flm.get_posy()
            ftop_y = flm.get_posy() - flm.get_height() + 1
            ang = flm.get_angle()

            if ang == 0:
                if fbottom_y <= bottom_y and fbottom_y >= top_y:
                    if (left_x <= fleft_x and right_x >= fleft_x) or (left_x >= fleft_x and right_x <= fright_x) or (left_x <= fright_x and right_x >= fright_x):
                        flm.change_active(0)
                        blt.change_active(0)
                        player._score += flm.get_hitscore()
                        game_map.clear(blt)
                        for ind in range(flm.get_height()):
                            game_map.change_grid(
                                fbottom_y, fleft_x + ind, Back.BLACK + Fore.BLACK + ' ')

            elif ang == 1:
                if fleft_x >= left_x and fright_x <= right_x:
                    if (bottom_y >= fbottom_y and top_y <= fbottom_y) or (bottom_y <= fbottom_y and top_y >= ftop_y) or (bottom_y >= ftop_y and top_y <= ftop_y):
                        flm.change_active(0)
                        blt.change_active(0)
                        player._score += flm.get_hitscore()
                        game_map.clear(blt)
                        for ind in range(flm._height):
                            game_map.change_grid(
                                fbottom_y - ind, fleft_x, Back.BLACK + Fore.BLACK + ' ')

            elif ang == 2:
                flag = 0
                oy = fbottom_y
                ox = fleft_x
                for i in range(flm.get_height()):
                    if (ox >= left_x and ox <= right_x and oy <= bottom_y and oy >= top_y):
                        flag = 1
                        break
                    ox += 1
                    oy -= 1

                if flag == 1:
                    flm.change_active(0)
                    blt.change_active(0)
                    player._score += flm.get_hitscore()
                    game_map.clear(blt)
                    for ind in range(flm.get_height()):
                        game_map.change_grid(
                            fbottom_y-ind, fleft_x+ind, Back.BLACK + Fore.BLACK + ' ')


def check_player_bossenemy(player, bossenemy):
    if player.get_posx() >= bossenemy.get_posx():
        if player.get_shield() == 0:
            player.change_life(-1)


def check_bossenemy_bullets(bullets, bossenemy, game_map):
    for blt in bullets:
        if blt.get_active() == 0:
            continue

        if blt.get_posy() <= bossenemy.get_posy() and blt.get_posy() >= bossenemy.get_posy() - bossenemy.get_height() + 1:
            if blt.get_posx() >= bossenemy.get_posx():
                bossenemy.change_life(-1)
                if bossenemy.get_color() == Fore.RED:
                    bossenemy.change_color(Fore.MAGENTA)
                else:
                    bossenemy.change_color(Fore.RED)
                blt.change_active(0)
                game_map.clear(blt)


def check_player_bossenemybullets(game_map, player, bossenemy):
    bottom_y = player.get_posy()
    top_y = player.get_posy() - player.get_height() + 1
    left_x = player.get_posx()
    right_x = player.get_posx() + player.get_width() - 1
    flag = 0
    for blt in bossenemy.get_bullets():
        if blt.get_active() == 0:
            continue
        x = blt.get_posx()
        y = blt.get_posy()
        for i in range(blt.get_height()):
            for j in range(blt.get_width()):
                x = blt.get_posx() + j
                y = blt.get_posy() - i
                if(y >= top_y and y <= bottom_y and x <= right_x and x >= left_x):
                    flag = 1
                    game_map.clear(blt)
                    blt.change_active(0)
                    break
            if flag == 1:
                break
        if flag == 1:
            break
    if flag == 1:
        player.change_life(-1)


def check_coll_matrix(mtrx1, mtrx2):
    lst = []
    flag = 0
    for i in range(mtrx1.get_height()):
        for j in range(mtrx1.get_width()):
            a = mtrx1.get_posy() - i
            b = mtrx1.get_posx() + j
            lst.append([a, b])

        for i in range(mtrx2.get_height()):
            for j in range(mtrx2.get_height()):
                a = mtrx2.get_posy() - i
                b = mtrx2.get_posx() + j
                if [a, b] in lst:
                    flag = 1
                    break
            if flag == 1:
                break
        if flag == 1:
            break
    if flag == 1:
        return True


def check_player_speed_boost(game_map, player):
    val = 0
    for spd in game_map.get_speedboost():
        val = check_coll_matrix(spd, player)
        if val == 1:
            player.change_speedboost(1)
            tm = time.time()
            player.change_speedboosttime(tm)
            spd.change_active(0)
            game_map.change_speedboostactive(1)
            game_map.clear(spd)
            break


def check_player_dragon(game_map, player):
    val = 0
    for spd in game_map.get_dragon():
        val = check_coll_matrix(spd, player)
        if val == 1:
            spd.change_active(0)
            player.change_dragon(1)
            game_map.clear(spd)
            break


def check_coins_bullets(game_map, bullets):
    for blt in bullets:
        if blt._active == 1:
            for coin in game_map._coins:
                if check_coll_matrix(blt, coin):
                    game_map.clear(blt)
                    game_map.objectc(coin)
                    blt._active = 0
