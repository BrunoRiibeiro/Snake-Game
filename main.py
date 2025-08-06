from random import randint
import pyxel


x_head, y_head = 15, 12
x_body, y_body = [x_head - 1, x_head], [y_head, y_head]
apple_x, apple_y = x_head, y_head
move_x, move_y = 0, 0
up, down, left, rigth = -1, 1, -1, 1
fps = 60
score = -1
game_over = False
changed = False
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
    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
        if not (move_y == down):
            move_y = up
            move_x = 0
    elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
        if not (move_y == up):
            move_y = down
            move_x = 0
    elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
        if not (move_x == rigth):
            move_x = left
            move_y = 0
    elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
        if not (move_x == left):
            move_x = rigth
            move_y = 0
    

#########################
# Random apple generate #
#########################
def update_apple():
    global apple_x, apple_y, score
    if x_head == apple_x and y_head == apple_y:
        apple_x = randint(1, 30)
        apple_y = randint(1, 30)
        score += 1 # for each apple eaten adds 1 point


def change_music_1(): # To change the song while game_over == True
    global changed
    pyxel.stop() 
    pyxel.playm(1, loop=True)
    changed = True

def change_music_2(): # To change the song while game_over == False
    global changed
    pyxel.stop()
    pyxel.playm(0, loop=True)
    changed = False


def update():
    global x_head, y_head, x_body, y_body, move_x, move_y, game_over, score, wrote
    
    update_snake()
    update_apple()
    motion()


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

    if game_over == True and changed == False: 
        change_music_1()
    if game_over == False and changed == True:                  
        change_music_2()           

    
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



################
# Game Drawing #
################
def draw_snake():
    for x, y in zip(x_body, y_body):
        if 11 <= score <= 20:
            pyxel.pset(x, y, pyxel.COLOR_BLACK)
        elif 21 <= score <= 50:
            pyxel.pset(x, y, pyxel.COLOR_WHITE)
        elif score >= 51:
            pyxel.pset(x, y, randint(0, 15))
        else:
            pyxel.pset(x, y, pyxel.COLOR_BROWN)


def draw_apple():
    if 10 <= score < 20:
        pyxel.pset(apple_x, apple_y, pyxel.COLOR_BLACK)
    elif 20 <= score < 50:
        pyxel.pset(apple_x, apple_y, pyxel.COLOR_WHITE)
    elif score >= 50:
        pyxel.pset(apple_x, apple_y, randint(0, 15))
    else:    
        pyxel.pset(apple_x, apple_y, pyxel.COLOR_RED)



def draw():
    pyxel.blt(0, 0, 0, 0, 0, 32, 32) # Draw the wallpaper

    draw_snake()
    draw_apple()

    if game_over:
        pyxel.text(3, 5, f"{name}\nSCORED:\n{score}", pyxel.COLOR_BLACK)
       



####################
# Imputs and Logic #
####################
pyxel.init(32, 32, "Snake Game", fps=fps, quit_key=pyxel.KEY_Q)
pyxel.load("arts_sets.pyxres") # load file "arts"
pyxel.image(0).set(32,32,["32","32"]) # set wallpaper
pyxel.playm(0,loop=True) # Play the pice in loop
pyxel.run(update, draw) # Run the update and draw functions
