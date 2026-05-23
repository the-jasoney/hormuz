import turtle
from time import time
from random import randint

# screen parameters
screen = turtle.Screen()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
GRID_SIZE = 50

PLAYER_SPEED = 1

# 0 for splash
# 1 for 
game_state = 0

oil_side_left = True # false 

screen.setup(500, 500)
screen.bgpic("")  # TODO: add bgpic
screen.tracer(0)

screen.addshape("missile.gif")
# for dt calculation
last_time = time()

# game parameters
obstacles: list['Missile'] = []
spawners: list['Spawner'] = []

# whether game is running
running: bool = True
level = 0
resetting = False

wasdplayer: turtle.Turtle = turtle.Turtle()
wasdplayer.pu()
wasdplayer.shape("turtle")
wasdplayer.lt(0)
wasdplayeralive = True
# true when player first collides, next frame is drawn before reset, gets set to number of seconds cooldown lasts, then reset is called and it gets set to 0 again
wasdplayerdeadflag = False
wasdplayerdeadtimer = 0
wasdpx = -100
wasdpy = -250 + GRID_SIZE
wasdlastpx = wasdpx
wasdlastpy = wasdpy
wasdscore = 0

arrowplayer: turtle.Turtle = turtle.Turtle()
arrowplayer.pu()
arrowplayer.shape("turtle")
arrowplayer.lt(90)
arrowplayeralive = True
arrowplayerdeadflag = 0
arrowplayerdeadtimer = 0
arrowpx = 100
arrowpy = -250 + GRID_SIZE
arrowlastpx = arrowpx
arrowlastpy = arrowpy
arrowscore = 0

oilpx = randint(1, 4) * GRID_SIZE * (-1 if oil_side_left else 1)
oilplayer = turtle.Turtle()
oilplayer.pu()
screen.addshape("oil.gif")
oilplayer.shape("oil.gif")
oilplayer.color("black")
oilplayer.setx(oilpx)
oilplayer.sety(250 - GRID_SIZE)

text = turtle.Turtle()
text.pu()
text.ht()

# reusable obstacle class
class Missile: 
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.object = turtle.Turtle()
        self.object.pu()
        self.object.speed(0)
        self.object.lt(90)
        self.object.color("red")
        
        self.object.shape("missile.gif")
        self.object.setx(x)
        self.object.sety(y)

    # runs every gameloop, returns whether the object is off the screen
    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.object.setx(self.x)
        self.object.sety(self.y)
        
        if (
            self.x > SCREEN_WIDTH / 2
            or self.x < -SCREEN_WIDTH / 2
            or self.y > SCREEN_HEIGHT / 2
            or self.y < -SCREEN_HEIGHT / 2
        ):
            return False
        else:
            return True

class Spawner:
    timer = randint(0, 10)
    
    def __init__(self, y, difficulty: float):
        self.y = y
        self.difficulty = difficulty

        for i in range(5):
            x = 250 - (i * 150) - randint(50, 100)  # evenly spread, slight randomness
            obstacles.append(Missile(x, self.y, -0.25 * self.difficulty, 0))

    def update(self, dt):
        global obstacles
        
        self.timer -= dt * 0.5
        if self.timer <= 0:
            self.timer = randint(int(200 / self.difficulty), int(500 / self.difficulty))
            obstacles.append(Missile(250, self.y, -0.25 * self.difficulty, 0))

# global levels list
LEVELS = [
    [
        (2 * GRID_SIZE, 5),
        (0, 5),
        (-2 * GRID_SIZE, 5),
    ],
    [
        (2 * GRID_SIZE, 7),
        (GRID_SIZE, 7),
        (0, 8),
        (-GRID_SIZE, 7),
        (-2 * GRID_SIZE, 7),
    ],
    [
        (2 * GRID_SIZE, 10),
        (GRID_SIZE, 11),
        (0, 10),
        (-GRID_SIZE, 11),
        (-2 * GRID_SIZE, 10),
    ],
    [
        (3 * GRID_SIZE, 8),
        (GRID_SIZE, 8),
        (0, 10),
        (-GRID_SIZE, 9),
        (-2 * GRID_SIZE, 10),
        (-3 * GRID_SIZE, 15),
    ]
]

spawners = [Spawner(y, difficulty) for y, difficulty in LEVELS[level]]

def reset():
    global wasdpx, wasdpy, wasdplayeralive, wasdplayerdeadflag, wasdplayerdeadtimer, \
           arrowpx, arrowpy, arrowplayeralive, arrowplayerdeadflag, arrowplayerdeadtimer, \
           wasdlastpx, wasdlastpy, arrowlastpx, arrowlastpy, \
           obstacles, spawners, oilpx, screen, running, resetting
    from time import sleep

    resetting = True

    if level >= len(LEVELS):
        running = False
        for obs in obstacles:
            obs.object.ht()
            obs.object.clear()
        wasdplayer.ht()
        arrowplayer.ht()
        oilplayer.ht()
        screen.update()
        return
    
    sleep(0.5)
    wasdplayerdeadflag = False
    wasdplayerdeadtimer = 0
    arrowplayerdeadflag = False  
    arrowplayerdeadtimer = 0
    wasdlastpx = -100
    wasdlastpy = -250 + GRID_SIZE
    arrowlastpx = 100
    arrowlastpy = -250 + GRID_SIZE
    
    wasdpx = -100
    wasdpy = -250 + GRID_SIZE
    wasdplayeralive = True

    arrowpx = 100
    arrowpy = -250 + GRID_SIZE
    arrowplayeralive = True

    wasdplayer.setx(-100)
    wasdplayer.sety(-250 + GRID_SIZE)
    wasdplayer.setheading(90)
    wasdplayer.st()
    
    arrowplayer.setx(100)
    arrowplayer.sety(-250 + GRID_SIZE)
    arrowplayer.setheading(90)
    arrowplayer.st()
    
    oilplayer.setx(oilpx)
    oilplayer.sety(250 - GRID_SIZE)
    oilplayer.st()

    for obs in obstacles:
        obs.object.ht()
        obs.object.clear()
     
    obstacles = []

    spawners = [Spawner(y, difficulty) for y, difficulty in LEVELS[level]]

    oilpx = (randint(1, 4) if oil_side_left else randint(5, 9)) * GRID_SIZE
    
    screen.tracer(0)

    wasdplayer.st()
    arrowplayer.st()
    
    screen.update()
    resetting = False

def up_d():
    global wasdpy, wasdplayeralive, wasdlastpy, resetting
    if not wasdplayeralive:
        return
    if resetting:
        return

    wasdlastpy = wasdpy
    
    if wasdpy < SCREEN_HEIGHT/2 - GRID_SIZE:
        wasdpy += GRID_SIZE

    wasdplayer.setheading(90)
    

def dn_d():
    global wasdpy, wasdplayeralive, wasdlastpy
    if not wasdplayeralive:
        return
    if resetting:
        return

    wasdlastpy = wasdpy
    
    if wasdpy > -SCREEN_HEIGHT/2 + GRID_SIZE:
        wasdpy -= GRID_SIZE

    wasdplayer.setheading(270)

def lt_d():
    global wasdpx, wasdplayeralive, wasdlastpx
    if not wasdplayeralive:
        return
    if resetting:
        return
    wasdlastpx = wasdpx
    if wasdpx > -SCREEN_WIDTH/2 + GRID_SIZE:
        wasdpx -= GRID_SIZE
    wasdplayer.setheading(180)

def rt_d():
    global wasdpx, wasdplayeralive, wasdlastpx
    if not wasdplayeralive:
        return
    if resetting:
        return
    wasdlastpx = wasdpx
    if wasdpx < SCREEN_WIDTH/2 - GRID_SIZE:
        wasdpx += GRID_SIZE
    wasdplayer.setheading(0)

def up_a():
    global arrowpy, arrowplayeralive, arrowlastpy
    if not arrowplayeralive:
        return

    if resetting:
        return
        
    arrowlastpy = arrowpy
    if arrowpy < SCREEN_HEIGHT/2 - GRID_SIZE:
        arrowpy += GRID_SIZE
    arrowplayer.setheading(90)

def dn_a():
    global arrowpy, arrowplayeralive, arrowlastpy
    if not arrowplayeralive:
        return
    arrowlastpy = arrowpy
    if resetting:
        return
    if arrowpy > -SCREEN_HEIGHT/2 + GRID_SIZE:
        arrowpy -= GRID_SIZE
    arrowplayer.setheading(270)

def lt_a():
    global arrowpx, arrowplayeralive, arrowlastpx
    if not arrowplayeralive:
        return

    if resetting:
        return
    
    arrowlastpx = arrowpx
    if arrowpx > -SCREEN_WIDTH/2 + GRID_SIZE:
        arrowpx -= GRID_SIZE
    arrowplayer.setheading(180)

def rt_a():
    global arrowpx, arrowplayeralive, arrowlastpx
    if not arrowplayeralive:
        return

    if resetting:
        return
    arrowlastpx = arrowpx
    if arrowpx < SCREEN_WIDTH/2 - GRID_SIZE:
        arrowpx += GRID_SIZE
    arrowplayer.setheading(0)

def escape():
    global running, game_state
    running = False
    game_state = 3
    raise InterruptedError()

def deltatime():
    global last_time

    new_time = time()
    dt = new_time - last_time
    last_time = new_time

    return dt * 100


def gameloop():
    global wasdpx, wasdpy, wasdplayer, screen, arrowpx, arrowpy, arrowplayer, obstacles, spawners, wasdplayeralive, arrowplayeralive, wasdscore, arrowscore, oilpx, oilplayer, level, wasdplayerdeadflag, arrowplayerdeadflag, wasdplayerdeadtimer, arrowplayerdeadtimer, wasdlastpx, wasdlastpy, arrowlastpx, arrowlastpy
    dt = deltatime()

    for i in spawners:
        i.update(dt)
        
    for i in obstacles:
        i.update(dt)
        if i.x > 250 or i.x < -250:
            i.object.ht()
            obstacles.remove(i)
        if (abs(i.x - wasdpx) < GRID_SIZE/2 and abs(i.y - wasdpy) < GRID_SIZE/2 and wasdplayeralive) or (abs(i.x - wasdlastpx) < GRID_SIZE/2 and abs(i.y - wasdlastpy) < GRID_SIZE/2 and wasdplayeralive):
            i.object.ht()
            obstacles.remove(i)
            wasdplayer.setx(wasdpx)
            wasdplayer.sety(wasdpy)
            wasdplayerdeadtimer = 0.5
            wasdplayerdeadflag = True
        if (abs(i.x - arrowpx) < GRID_SIZE/2 and abs(i.y - arrowpy) < GRID_SIZE/2 and arrowplayeralive) or (abs(i.x - arrowlastpx) < GRID_SIZE/2 and abs(i.y - arrowlastpy) < GRID_SIZE/2 and arrowplayeralive):
            i.object.ht()
            obstacles.remove(i)
            arrowplayer.setx(arrowpx)
            arrowplayer.sety(arrowpy)
            arrowplayerdeadtimer = 0.5
            arrowplayerdeadflag = True
        

    if wasdpx == arrowpx and wasdpy == arrowpy and wasdplayeralive and arrowplayeralive:
        wasdplayerdeadtimer = 0.5
        wasdplayerdeadflag = True
        arrowplayerdeadtimer = 0.5
        arrowplayerdeadflag = True
        wasdplayer.setx(wasdpx)
        wasdplayer.sety(wasdpy)
        arrowplayer.setx(arrowpx)
        arrowplayer.sety(arrowpy)

    if arrowplayerdeadflag:
        arrowplayerdeadtimer -= dt
        if arrowplayerdeadtimer <= 0:
            arrowplayeralive = False
            arrowplayer.ht()
            arrowplayerdeadflag = False
            
    if wasdplayerdeadflag:
        wasdplayerdeadtimer -= dt
        if wasdplayerdeadtimer <= 0:
            wasdplayeralive = False
            wasdplayer.ht()
            wasdplayerdeadflag = False
        

    if oilpx == wasdpx and 250-GRID_SIZE == wasdpy and wasdplayeralive:
        wasdscore += 1
        level += 1
        oilplayer.setx(oilpx)
        oilplayer.sety(250 - GRID_SIZE)
        oilplayer.st()
    
        wasdplayer.setx(wasdpx)
        wasdplayer.sety(wasdpy)
        wasdplayer.st()
        reset()
        
    if oilpx == arrowpx and 250-GRID_SIZE == arrowpy and arrowplayeralive:
        arrowscore += 1
        level += 1
        oilplayer.setx(oilpx)
        oilplayer.sety(250 - GRID_SIZE)
        oilplayer.st()
    
        wasdplayer.setx(wasdpx)
        wasdplayer.sety(wasdpy)
        wasdplayer.st()
        reset()
    
    oilplayer.setx(oilpx)
    oilplayer.sety(250 - GRID_SIZE)
    oilplayer.st()

    wasdplayer.setx(wasdpx)
    wasdplayer.sety(wasdpy)
    wasdplayer.st()
    
    if not wasdplayeralive:
        wasdplayer.ht()

    arrowplayer.setx(arrowpx)
    arrowplayer.sety(arrowpy)
    arrowplayer.st()
    
    if not arrowplayeralive:
        arrowplayer.ht()

    if not (wasdplayeralive or arrowplayeralive):
        reset()

    wasdlastpx = wasdpx
    wasdlastpy = wasdpy
    arrowlastpx = arrowpx
    arrowlastpy = arrowpy
    
    text.clear()
    text.setx(0)
    text.sety(SCREEN_HEIGHT/2 - 50)
    text.write(f"Level {level + 1}/4 China: {arrowscore} US: {wasdscore}", align="center", font=("Arial", 24, "normal"))   
    
    screen.update()

def space():
    global game_state, wasdscore, arrowscore, level, running
    if game_state == 0:
        game_state = 1
    if game_state == 2:
        game_state = 1
        wasdscore = 0
        arrowscore = 0
        level = 0
        running = True
        reset()

def splash():
    global wasdplayer, arrowplayer, obstacles, oilplayer
    screen.bgpic("splash.png")  # TODO: add splash screen
    for obstacle in obstacles:
        obstacle.object.ht()
    wasdplayer.ht()
    arrowplayer.ht()
    oilplayer.ht()
    while game_state == 0:
        screen.update()

def setup():
    global obstacles, spawners
    global screen

    # set up screen

    # load sprites
    # screen.addshape("abc.xyz")
    screen.addshape("america.gif")
    screen.addshape("china.gif")

    wasdplayer.shape("america.gif")
    arrowplayer.shape("china.gif")

    # set up controls
    screen.onkey(up_d, "w")
    screen.onkey(dn_d, "s")
    screen.onkey(lt_d, "a")
    screen.onkey(rt_d, "d")
    screen.onkey(up_a, "Up")
    screen.onkey(dn_a, "Down")
    screen.onkey(lt_a, "Left")
    screen.onkey(rt_a, "Right")
    screen.onkey(escape, "Escape")
    screen.onkey(space, "space")
    screen.listen()

def run_gameloop():
    global running, game_state, screen
    screen.bgpic("bg.gif")
    while running and game_state == 1:
        gameloop()
    game_state = 2
    return

def end():
    global screen
    for obstacle in obstacles:
        obstacle.object.ht()
    wasdplayer.ht()
    arrowplayer.ht()
    oilplayer.ht()
    screen.bgpic("gameover.png")
    text.clear()
    text.setx(-100)
    text.sety(-150)
    text.write(f"Game Over, US: {wasdscore} China: {arrowscore}", align="center", font=("Arial", 16, "normal"))
    text.sety(-200)
    text.write("US Won" if wasdscore > arrowscore else "China Won" if arrowscore > wasdscore else "Tie", align="center", font=("Arial", 12, "normal"))
    screen.onkey(space, 'space')
    while game_state == 2:
        screen.update()
    return

def main():
    global oilplayer, wasdplayer, arrowplayer
    setup()
    while True:
        match game_state:
            case 0:
                splash()
            case 1:
                for obstacle in obstacles:
                    obstacle.object.st()
                oilplayer.st()
                wasdplayer.st()
                arrowplayer.st()
                screen.bgpic("")
                screen.bgcolor(1,1,1)
                run_gameloop()
            case 2:
                end()
            case 3:
                break

    screen.bye()


if __name__ == "__main__":
    try: 
        main()
    except:
        screen.bye()
