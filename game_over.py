import colorama
from colorama import Fore, Back, Style
import numpy as np
colorama.init()


class game_over:
    def __init__(self, x, y, filename):
        self._color = Fore.RED
        self.make_arr(x, y, filename)

    def make_arr(self, x, y, filename):
        with open(filename, 'rb') as f:
            arr = []
            cnt = 0
            mx = -1
            for line in f:
                arr.append(line)
                mx = max(mx, len(arr[cnt]))
                cnt += 1
        f.close()
        self._height = len(arr)
        self._width = mx
        self._pos_x = x - self._width//2
        self._pos_y = y + self._height//2
        self._char = np.array(([[' ' for col in range(self._width)]
                                for row in range(self._height)]))

        for i in range(self._height):
            # to remove last '\n' character in ascii art present already I have made loop till len(arr[i]) - 1
            for j in range(len(arr[i])-1):
                self._char[i][j] = chr(arr[i][j])


def won(game_map, offset, rows, columns):
    for rw in range(rows):
        for val in range(columns):
            game_map.change_grid(rw, val+offset, Back.BLACK + Fore.BLACK + ' ')
            game_map.change_grid(0, val+offset, Fore.WHITE + 'X')
            game_map.change_grid(1, val+offset, Fore.WHITE + 'X')
            # ground
            game_map.change_grid(rows-1, val+offset, Fore.GREEN + 'X')
            game_map.change_grid(rows-2, val+offset, Fore.GREEN + 'X')
            game_map.change_grid(rows-3, val+offset, Fore.GREEN + 'X')

    win = game_over(offset + columns//2, rows//2, 'win.txt')
    game_map.object(win)


def loose(game_map, offset, rows, columns):
    for rw in range(rows):
        for val in range(columns):
            game_map.change_grid(rw, val+offset, Back.BLACK + Fore.BLACK + ' ')
            game_map.change_grid(0, val+offset, Fore.WHITE + 'X')
            game_map.change_grid(1, val+offset, Fore.WHITE + 'X')
            # ground
            game_map.change_grid(rows-1, val+offset, Fore.GREEN + 'X')
            game_map.change_grid(rows-2, val+offset, Fore.GREEN + 'X')
            game_map.change_grid(rows-3, val+offset, Fore.GREEN + 'X')

    loose = game_over(offset + columns//2, rows//2, 'loose.txt')
    game_map.object(loose)
