class Person:
    def __init__(self, world_x, world_y):
        self.pos_x = 1
        self.pos_y = world_y - 1
        self.char = "+"

    def check(self, world_x, world_y):
        # check for limits out of screen
        if self.pos_x > world_x - 1:
            self.pos_x = world_x - 1
        if self.pos_x < 1:
            self.pos_x = 1
        if self.pos_y > world_y:
            self.pos_y = world_y
        if self.pos_y < 1:
            self.pos_y = 1

        # print(Back.BLUE)
        # print(colorama.ansi.clear_screen())

        # sp.call('clear', shell=True)
        # print(Fore.RED + "\033["+str(self.pos_y) +
        #       ";"+str(self.pos_x)+"H"+self.char)

    def gravity(self):
        self.pos_y += 2

    def move(self, val):
        if(val == 'a' or val == 'A'):
            self.pos_x -= 1
        elif(val == 'd' or val == 'D'):
            self.pos_x += 1
        elif(val == 'w' or val == 'W'):
            self.pos_y -= 1
