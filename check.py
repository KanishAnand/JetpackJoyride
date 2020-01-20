import colorama
from colorama import Fore, Back, Style
from playsound import playsound
colorama.init()


def check_coins(game_map, player):
    x = player._pos_x
    y = player._pos_y
    chr = Fore.YELLOW + '$'
    for row in range(player._height):
        for col in range(player._width):
            if game_map._grid[y - row][x + col] == chr:
                # playsound('coin.mp3', False)
                player._score += 1
                game_map._grid[y-row][x+col] = Back.BLACK + Fore.BLACK + ' '

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
    for val in game_map._flames:
        if val._active == 0:
            continue
        x = player._pos_x
        y = player._pos_y
        h = val._height
        fx = val._pos_x
        fy = val._pos_y
        ang = val._angle
        if ang == 0:
            # check condition
            if fy <= y and fy >= y - player._height + 1:
                if (fx >= x and fx <= x + player._width - 1) or (fx <= x and fx + h - 1 >= x + player._width - 1) or (x <= fx + h - 1 and fx + h - 1 <= x + player._width - 1):
                    if player._shield == 0:
                        player._dragon = 0
                        player._lives -= 1
                    val._active = 0
                    for ind in range(h):
                        game_map._grid[fy][fx+ind] = Back.BLACK + \
                            Fore.BLACK + ' '

        elif ang == 1:
            if fx >= x and fx <= x + player._width - 1:
                if (y >= fy and y - player._height + 1 <= fy) or (y <= fy and y - player._height + 1 >= fy - h + 1) or (y >= fy - h + 1 and y - player._height + 1 <= fy - h + 1):
                    if player._shield == 0:
                        player._dragon = 0
                        player._lives -= 1
                    val._active = 0
                    for ind in range(h):
                        game_map._grid[fy-ind][fx] = Back.BLACK + \
                            Fore.BLACK + ' '

        elif ang == 2:
            flag = 0
            oy = fy
            ox = fx
            for i in range(h):
                if (fx >= x and fx <= x + player._width - 1 and fy <= y and fy >= y - player._width + 1):
                    flag = 1
                    break
                fx += 1
                fy -= 1
            if flag == 1:
                if player._shield == 0:
                    player._dragon = 0
                    player._lives -= 1
                val._active = 0
                for ind in range(h):
                    game_map._grid[oy-ind][ox+ind] = Back.BLACK + \
                        Fore.BLACK + ' '


def check_flames_bullets(bullets, game_map, player):
    for blt in bullets:
        if blt._active == 0:
            continue
        left_x = blt._pos_x
        right_x = blt._pos_x + blt._width - 1
        bottom_y = blt._pos_y
        top_y = blt._pos_y - blt._height + 1

        for flm in game_map._flames:
            if flm._active == 0:
                continue

            fleft_x = flm._pos_x
            fright_x = flm._pos_x + flm._width - 1
            fbottom_y = flm._pos_y
            ftop_y = flm._pos_y - flm._height + 1
            ang = flm._angle

            if ang == 0:
                if fbottom_y <= bottom_y and fbottom_y >= top_y:
                    if (left_x <= fleft_x and right_x >= fleft_x) or (left_x >= fleft_x and right_x <= fright_x) or (left_x <= fright_x and right_x >= fright_x):
                        flm._active = 0
                        blt._active = 0
                        player._score += flm._hitscore
                        game_map.clear(blt)
                        for ind in range(flm._height):
                            game_map._grid[fbottom_y][fleft_x + ind] = Back.BLACK + \
                                Fore.BLACK + ' '

            elif ang == 1:
                if fleft_x >= left_x and fright_x <= right_x:
                    if (bottom_y >= fbottom_y and top_y <= fbottom_y) or (bottom_y <= fbottom_y and top_y >= ftop_y) or (bottom_y >= ftop_y and top_y <= ftop_y):
                        flm._active = 0
                        blt._active = 0
                        player._score += flm._hitscore
                        game_map.clear(blt)
                        for ind in range(flm._height):
                            game_map._grid[fbottom_y - ind][fleft_x] = Back.BLACK + \
                                Fore.BLACK + ' '

            elif ang == 2:
                flag = 0
                oy = fbottom_y
                ox = fleft_x
                for i in range(flm._height):
                    if (ox >= left_x and ox <= right_x and oy <= bottom_y and oy >= top_y):
                        flag = 1
                        break
                    ox += 1
                    oy -= 1

                if flag == 1:
                    flm._active = 0
                    blt._active = 0
                    player._score += flm._hitscore
                    game_map.clear(blt)
                    for ind in range(flm._height):
                        game_map._grid[fbottom_y-ind][fleft_x+ind] = Back.BLACK + \
                            Fore.BLACK + ' '


def check_player_bossenemy(player, bossenemy):
    if player._pos_x >= bossenemy._pos_x:
        if player._shield == 0:
            player._lives -= 1


def check_bossenemy_bullets(bullets, bossenemy, game_map):
    for blt in bullets:
        if blt._active == 0:
            continue

        if blt._pos_y <= bossenemy._pos_y and blt._pos_y >= bossenemy._pos_y - bossenemy._height + 1:
            if blt._pos_x >= bossenemy._pos_x:
                bossenemy._life -= 1
                if bossenemy._color == Fore.RED:
                    bossenemy._color = Fore.MAGENTA
                else:
                    bossenemy._color = Fore.RED
                blt._active = 0
                game_map.clear(blt)


def check_player_bossenemybullets(game_map, player, bossenemy):
    bottom_y = player._pos_y
    top_y = player._pos_y - player._height + 1
    left_x = player._pos_x
    right_x = player._pos_x + player._width - 1
    flag = 0
    for blt in bossenemy._bullets:
        if blt._active == 0:
            continue
        x = blt._pos_x
        y = blt._pos_y
        for i in range(blt._height):
            for j in range(blt._width):
                x = blt._pos_x + j
                y = blt._pos_y - i
                if(y >= top_y and y <= bottom_y and x <= right_x and x >= left_x):
                    flag = 1
                    game_map.clear(blt)
                    blt._active = 0
                    break
            if flag == 1:
                break
        if flag == 1:
            break
    if flag == 1:
        player._lives -= 1


def check_coll_matrix(mtrx1, mtrx2):
    lst = []
    flag = 0
    for i in range(mtrx1._height):
        for j in range(mtrx1._width):
            a = mtrx1._pos_y - i
            b = mtrx1._pos_x + j
            lst.append([a, b])

        for i in range(mtrx2._height):
            for j in range(mtrx2._width):
                a = mtrx2._pos_y - i
                b = mtrx2._pos_x + j
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
    for spd in game_map._speedboost:
        val = check_coll_matrix(spd, player)
        if val == 1:
            player._speedboost = 1
            spd._active = 0
            game_map._speedboost_active = 1
            game_map.clear(spd)
            break


def check_player_dragon(game_map, player):
    val = 0
    for spd in game_map._dragon:
        val = check_coll_matrix(spd, player)
        if val == 1:
            spd._active = 0
            player._dragon = 1
            game_map.clear(spd)
            break
