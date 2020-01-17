import numpy as np


class BossEnemy:
    def __init__(self):
        self.make_arr()

    def make_arr(self):
        with open('dragon1.txt', 'rb') as f:
            arr = []
            cnt = 0
            mx = -1
            for line in f:
                arr.append(line)
                l = len(arr[cnt])
                mx = max(mx, len(arr[cnt]))
                cnt += 1
        f.close()
        self.height = len(arr)
        self.width = mx
        self.char = np.array(([[' ' for col in range(self.width)]
                               for row in range(self.height)]))

        for i in range(self.height):
            for j in range(len(arr[i])-1):
                self.char[i][j] = chr(arr[i][j])


en = BossEnemy()
for i in range(en.char.shape[0]):
    for j in range(en.char.shape[1]):
        print(en.char[i][j], end=" ")
    print("\n")
