import termios
import sys
import tty

clrscr = chr(27) + "[2J"
pos_x = 20
pos_y = 80

if __name__ == "__main__":
    clear()
    # disabling buffering so you don't have to press enter
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

    while(1):
        print_char(pos_x,pos_y,"+")
        val = sys.stdin.read(1)[0]
        move(val)

    #enabling previous settings
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)  
        
def print_char(x, y, char):
    print("\033["+str(y)+";"+str(x)+"H"+char)

def clear():
    print(clrscr)

def move(val):
    global pos_x,pos_y
    if(val == 'a' or val == 'A'):
        pos_x += 1
    elif(val == 'd' or val == 'D'):
        pos_x -= 1  
