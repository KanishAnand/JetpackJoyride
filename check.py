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
        x = player.pos_x
        y = player.pos_y
        h = val['height']
        fx = val['x']
        fy = val['y']
        ang = val['angle']
        if ang == 0:
            # check condition
            if fy <= y and fy >= y - player.height + 1:
                if (fx >= x and fx <= x + player.width - 1) or (fx <= x and fx + h - 1 >= x + player.width - 1) or (x <= fx + h - 1 and fx + h - 1 <= x + player.width - 1):
                    player.lives -= 1
                    val['x'] = -1
                    val['y'] = -1
                    val['angle'] = 10
                    for ind in range(h):
                        game_map.grid[fy][fx+ind] = Back.BLACK + \
                            Fore.BLACK + ' '

        elif ang == 1:
            if fx >= x and fx <= x + player.width - 1:
                if (y >= fy and y - player.height + 1 <= fy) or (y <= fy and y - player.height + 1 >= fy - h + 1) or (y >= fy - h + 1 and y - player.height + 1 <= fy - h + 1):
                    player.lives -= 1
                    val['x'] = -1
                    val['y'] = -1
                    val['angle'] = 10
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
                player.lives -= 1
                val['x'] = -1
                val['y'] = -1
                val['angle'] = 10
                for ind in range(h):
                    game_map.grid[oy-ind][ox+ind] = Back.BLACK + \
                        Fore.BLACK + ' '
