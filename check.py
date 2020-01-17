import colorama
from colorama import Fore, Back, Style
colorama.init()


def check_coins(game_map, player):
    x = player.pos_x
    y = player.pos_y
    chr = Fore.YELLOW + '$'
    for row in range(player.height):
        for col in range(player.width):
            if game_map.grid[y - row][x + col] == chr:
                player.score += 1
                game_map.grid[y-row][x+col] = Back.BLACK + Fore.BLACK + ' '

    # l = len(game_map.coins_x)
    # for ind in range(l):
    #     a = game_map.coins_x[ind]
    #     b = game_map.coins_y[ind]
    #     if a >= player.pos_x and a < player.pos_x + player.width:
    #         if b >= player.pos_y and b < player.pos_y + player.height:
    #             player.score += 1
    #             game_map.coins_x[ind] = -1
    #             game_map.coins_y[ind] = -1
    #             game_map.grid[b][a] = Back.BLACK + Fore.BLACK + ' '


def check_flames(game_map, player):
    for val in game_map.flames:
        if val.active == 0:
            continue
        x = player.pos_x
        y = player.pos_y
        h = val.height
        fx = val.pos_x
        fy = val.pos_y
        ang = val.angle
        if ang == 0:
            # check condition
            if fy <= y and fy >= y - player.height + 1:
                if (fx >= x and fx <= x + player.width - 1) or (fx <= x and fx + h - 1 >= x + player.width - 1) or (x <= fx + h - 1 and fx + h - 1 <= x + player.width - 1):
                    if player.shield == 0:
                        player.dragon = 0
                        player.lives -= 1
                    val.active = 0
                    for ind in range(h):
                        game_map.grid[fy][fx+ind] = Back.BLACK + \
                            Fore.BLACK + ' '

        elif ang == 1:
            if fx >= x and fx <= x + player.width - 1:
                if (y >= fy and y - player.height + 1 <= fy) or (y <= fy and y - player.height + 1 >= fy - h + 1) or (y >= fy - h + 1 and y - player.height + 1 <= fy - h + 1):
                    if player.shield == 0:
                        player.dragon = 0
                        player.lives -= 1
                    val.active = 0
                    for ind in range(h):
                        game_map.grid[fy-ind][fx] = Back.BLACK + \
                            Fore.BLACK + ' '

        elif ang == 2:
            flag = 0
            oy = fy
            ox = fx
            for i in range(h):
                if (fx >= x and fx <= x + player.width - 1 and fy <= y and fy >= y - player.width + 1):
                    flag = 1
                    break
                fx += 1
                fy -= 1
            if flag == 1:
                if player.shield == 0:
                    player.dragon = 0
                    player.lives -= 1
                val.active = 0
                for ind in range(h):
                    game_map.grid[oy-ind][ox+ind] = Back.BLACK + \
                        Fore.BLACK + ' '


def check_flames_bullets(bullets, game_map, player):
    for blt in bullets:
        if blt.active == 0:
            continue
        left_x = blt.pos_x
        right_x = blt.pos_x + blt.width - 1
        bottom_y = blt.pos_y
        top_y = blt.pos_y - blt.height + 1

        for flm in game_map.flames:
            if flm.active == 0:
                continue

            fleft_x = flm.pos_x
            fright_x = flm.pos_x + flm.width - 1
            fbottom_y = flm.pos_y
            ftop_y = flm.pos_y - flm.height + 1
            ang = flm.angle

            if ang == 0:
                if fbottom_y <= bottom_y and fbottom_y >= top_y:
                    if (left_x <= fleft_x and right_x >= fleft_x) or (left_x >= fleft_x and right_x <= fright_x) or (left_x <= fright_x and right_x >= fright_x):
                        flm.active = 0
                        blt.active = 0
                        player.score += flm.hitscore
                        game_map.clear(blt)
                        for ind in range(flm.height):
                            game_map.grid[fbottom_y][fleft_x + ind] = Back.BLACK + \
                                Fore.BLACK + ' '

            elif ang == 1:
                if fleft_x >= left_x and fright_x <= right_x:
                    if (bottom_y >= fbottom_y and top_y <= fbottom_y) or (bottom_y <= fbottom_y and top_y >= ftop_y) or (bottom_y >= ftop_y and top_y <= ftop_y):
                        flm.active = 0
                        blt.active = 0
                        player.score += flm.hitscore
                        game_map.clear(blt)
                        for ind in range(flm.height):
                            game_map.grid[fbottom_y - ind][fleft_x] = Back.BLACK + \
                                Fore.BLACK + ' '

            elif ang == 2:
                flag = 0
                oy = fbottom_y
                ox = fleft_x
                for i in range(flm.height):
                    if (ox >= left_x and ox <= right_x and oy <= bottom_y and oy >= top_y):
                        flag = 1
                        break
                    ox += 1
                    oy -= 1

                if flag == 1:
                    flm.active = 0
                    blt.active = 0
                    player.score += flm.hitscore
                    game_map.clear(blt)
                    for ind in range(flm.height):
                        game_map.grid[fbottom_y-ind][fleft_x+ind] = Back.BLACK + \
                            Fore.BLACK + ' '


def check_player_bossenemy(player, bossenemy):
    if player.pos_x >= bossenemy.pos_x:
        if player.shield == 0:
            player.lives -= 1


def check_bossenemy_bullets(bullets, bossenemy, game_map):
    for blt in bullets:
        if blt.active == 0:
            continue

        if blt.pos_y <= bossenemy.pos_y and blt.pos_y >= bossenemy.pos_y - bossenemy.height + 1:
            if blt.pos_x >= bossenemy.pos_x:
                bossenemy.life -= 1
                if bossenemy.color == Fore.RED:
                    bossenemy.color = Fore.MAGENTA
                else:
                    bossenemy.color = Fore.RED
                blt.active = 0
                game_map.clear(blt)


def check_player_bossenemybullets(game_map, player, bossenemy):
    bottom_y = player.pos_y
    top_y = player.pos_y - player.height + 1
    left_x = player.pos_x
    right_x = player.pos_x + player.width - 1
    flag = 0
    for blt in bossenemy.bullets:
        if blt.active == 0:
            continue
        x = blt.pos_x
        y = blt.pos_y
        for i in range(blt.height):
            for j in range(blt.width):
                x = blt.pos_x + j
                y = blt.pos_y - i
                if(y >= top_y and y <= bottom_y and x <= right_x and x >= left_x):
                    flag = 1
                    game_map.clear(blt)
                    blt.active = 0
                    break
            if flag == 1:
                break
        if flag == 1:
            break
    if flag == 1:
        player.lives -= 1


def check_coll_matrix(mtrx1, mtrx2):
    lst = []
    flag = 0
    for i in range(mtrx1.height):
        for j in range(mtrx1.width):
            a = mtrx1.pos_y - i
            b = mtrx1.pos_x + j
            lst.append([a, b])

        for i in range(mtrx2.height):
            for j in range(mtrx2.width):
                a = mtrx2.pos_y - i
                b = mtrx2.pos_x + j
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
    for spd in game_map.speedboost:
        val = check_coll_matrix(spd, player)
        if val == 1:
            player.speedboost = 1
            game_map.speedboost_active = 1
            game_map.clear(spd)
            break


def check_player_dragon(game_map, player):
    val = 0
    for spd in game_map.dragon:
        val = check_coll_matrix(spd, player)
        if val == 1:
            player.dragon = 1
            game_map.clear(spd)
            break
