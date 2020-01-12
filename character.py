class Person:
    def __init__(self, world_x, world_y):
        # pos_x and pos_y represent coordinates of bottom left point of figure
        self.pos_x = 1
        self.pos_y = world_y - 3
        self.height = 3
        self.width = 3
        self.char = [[' ', '0', ' '], ['-', '|', '-'], ['/', '|', '\\']]
        self.lives = 3
        self.score = 0
        self.time = 100
        self.info = " "

    def check(self, world_x, world_y, offset):
        # check for limits out of screen
        if self.pos_x + self.width - 1 > world_x - 1 + offset:
            self.pos_x = world_x - self.width + offset
        if self.pos_x < offset + 1:
            self.pos_x = offset + 1
        if self.pos_y > world_y - 3:
            self.pos_y = world_y - 3
        if self.pos_y - self.height + 1 < 2:
            self.pos_y = self.height + 1

    def gravity(self):
        self.pos_y += 2

    def move(self, val):
        if(val == 'a' or val == 'A'):
            self.pos_x -= 1
        elif(val == 'd' or val == 'D'):
            self.pos_x += 1
        elif(val == 'w' or val == 'W'):
            self.pos_y -= 1
