import colorama
from colorama import Fore, Back, Style
colorama.init()

def check_coins(game_map, player):
    l = len(game_map.coins_x)
    for ind in range(l):
        a = game_map.coins_x[ind]
        b = game_map.coins_y[ind]
        if a >= player.pos_x and a < player.pos_x + player.width:
            if b >= player.pos_y and b < player.pos_y + player.height:
                player.score += 1
                game_map.coins_x[ind] = -1
                game_map.coins_y[ind] = -1
                game_map.grid[b][a] = Back.BLACK + Fore.BLACK + ' '
