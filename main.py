from random import randint
import pyxel

x_head, y_head = 15, 12
x_body, y_body = [x_head - 1, x_head], [y_head, y_head]
move_y, move_x = 0, 0
apple_x, apple_y = x_head, y_head
up, down, left, rigth = -1, 1, -1, 1
fps = 60
score = -1
game_over = False


################
# Gaming Logic #
################
def update():
    global x_head, y_head,game_over, move_y, move_x, score

    #################
    # Gaming Motion #
    #################
    
    if pyxel.frame_count % 5 == 0:
        y_head = y_head + move_y
        x_head = x_head + move_x
        x_body.append(x_head)
        y_body.append(y_head)
        if x_head != apple_x:
            if y_head != apple_y:
                del x_body[0]
                del y_body[0]

    ##################
    # Game Over Mode #
    ##################
    if y_head >= 31 or y_head <= 0 or x_head >= 31 or x_head <= 0:
        game_over = True
    
    if game_over and pyxel.btnp(pyxel.KEY_R):
        x_head, y_head = 15, 12
        move_y, move_x= 0, 0
        score = 0
        game_over = False
    elif game_over:
        return
    


    ################
    # Motion Check #
    ################
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        if move_y != down:
            move_y = up
            move_x = 0
    elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        if move_y != up:
            move_y = down
            move_x = 0
    elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        if move_x != rigth:
            move_x = left
            move_y = 0
    elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        if move_x != left:
            move_x = rigth
            move_y = 0




def generate_snake():
    for x,y in zip(x_body,y_body):
        pyxel.pset(x,y, pyxel.COLOR_BROWN)

    #if pyxel.frame_count % 5 == 0:
    # x_body.append(x_head)
    # y_body.append(y_head)
    
    # del x_body[0] 
    # del y_body[0]


def generate_apple():
    global apple_y, apple_x, score

    if x_head == apple_x and y_head == apple_y:
        apple_x = randint(1, 30)
        apple_y = randint(1, 30)
        score += 1
    pyxel.pset(apple_x, apple_y, pyxel.COLOR_RED)
    


########################
# No Trespassing Walls #
########################
def generate_walls():
    pyxel.line(0,0, 0, 31, pyxel.COLOR_WHITE)
    pyxel.line(0, 31, 31, 31, pyxel.COLOR_WHITE)
    pyxel.line(31, 31, 31, 0, pyxel.COLOR_WHITE)
    pyxel.line(31, 0, 0, 0, pyxel.COLOR_WHITE)    




################
# Game Drawing #
################
def draw():
    pyxel.cls(pyxel.COLOR_BLACK)
    
    generate_snake()
    generate_apple()
    generate_walls()
    

    if game_over:
        pyxel.text(3, 3, f"SCORE:\n{score}", pyxel.COLOR_WHITE)
        #pyxel.text(3, 3, "(R)estart\n(Q)uit", pyxel.COLOR_WHITE)



pyxel.init(32, 32, caption="Snake Game", fps=fps, quit_key=pyxel.KEY_Q)
pyxel.load("nokia.pyxres")
pyxel.playm(0,loop=True)
pyxel.run(update, draw)