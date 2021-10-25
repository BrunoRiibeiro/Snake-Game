from random import randint
import pyxel


x_head, y_head = 15, 12
x_body, y_body = [x_head - 1, x_head], [y_head, y_head]
move_x, move_y = 0, 0
apple_x, apple_y = x_head, y_head
up, down, left, rigth = -1, 1, -1, 1
fps = 60
score = -1
game_over = False
name = input("Enter your name: ")
wrote = False
print(f"Your name is {name}")  


###############
# Leaderboard #
###############
def write():
    global wrote
    file = open("leaderboard.txt", "a")
    file.write(str(score) + "," + "\t" + name + "\n")
    file.close()
    wrote = True
    

##################################
# Gaming Motion and Snake Growth #
##################################
def update_snake():
    global x_head, y_head

    if move_x == 0 and move_y == 0:
        return

    if pyxel.frame_count % 5 == 0 and game_over == False:
        x_head += move_x
        y_head += move_y
        x_body.append(x_head)
        y_body.append(y_head)
        if not (x_head == apple_x and y_head == apple_y):
            del x_body[0] 
            del y_body[0]


################
# Motion Check #
################
def motion():
    global move_x, move_y
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
    

#########################
# Random apple generate #
#########################
def generate_apple():
    global apple_x, apple_y, score

    if x_head == apple_x and y_head == apple_y:
        apple_x = randint(1, 30)
        apple_y = randint(1, 30)
        score += 1 # for each apple eaten adds 1 point
    pyxel.pset(apple_x, apple_y, pyxel.COLOR_RED)




def update():
    global x_head, y_head, x_body, y_body, move_x, move_y, game_over, score, wrote

    ##################
    # Game Over Mode #
    ##################
    acc = set(zip(x_body,y_body))
   
    if len(acc) < len(y_body): # Check tail collision
        game_over = True
            
    if not (0 < x_head < 31) or not (0 < y_head < 31): # Check no trespassing wall collision
        game_over = True
    
    if game_over == True and wrote == False: # Write name and score in leaderboard
        write()

    ###########
    # Restart #
    ###########
    if game_over and pyxel.btnp(pyxel.KEY_R):
        x_head, y_head = 15, 12
        x_body, y_body = [x_head - 1, x_head], [y_head, y_head]
        move_x, move_y = 0, 0
        score = 0
        game_over = False
        wrote = False
    elif game_over:
        return

    update_snake()
    motion()



################
# Game Drawing #
################
def draw_snake():
    for x, y in zip(x_body, y_body):
        pyxel.pset(x, y, pyxel.COLOR_BROWN)

def draw():
    pyxel.blt(0, 0, 0, 0, 0, 32, 32) # Draw the wallpaper

    draw_snake()
    generate_apple()

    if game_over:
        pyxel.text(3, 5, f"{name}\nSCORED:\n{score}", pyxel.COLOR_BLACK)
       

####################
# Imputs and Logic #
####################
pyxel.init(32, 32, caption="Snake Game", fps=fps, quit_key=pyxel.KEY_Q)
pyxel.load("arts.pyxres") # load file "arts"
pyxel.image(0).set(32,32,["32","32"]) # set wallpaper
pyxel.playm(0,loop=True) # Play the pice in loop
pyxel.run(update, draw) # Run the update and draw functions
