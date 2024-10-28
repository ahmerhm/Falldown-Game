import uvage
import random

#constants
screenWidth, screenHeight = 400, 600
gapWidth = 70
floorHeight = 30
floorSpeed = 9
floorColor = 'white'
floorInterval = 100
initialBallY = 50
gameOn = False
score = 0
scoreIncr = False
ballSpeed = 20

camera = uvage.Camera(screenWidth, screenHeight)
camera.draw(uvage.from_text(200, 300, 'Press Space to Start', 50, 'Green', bold = False))
camera.display()

#Creating Floors
floors = []

def resetGame():
    global gameOn, score, floorSpeed, scoreIncr, n
    gameOn = False
    score = 0
    floorSpeed = 9
    scoreIncr = False
    n = 1
    ball.center = [200, initialBallY]
    ball.yspeed = ballSpeed
    floors.clear()
    
def createFloors():
    gapX = random.randint(35, 365) #generates a random x coordinate for the gap which has a margin of half of the gapWidth on both sides
    gap = uvage.from_color(gapX, screenHeight, 'black', gapWidth, floorHeight) #creates a gap gamebox as a guide for the floors around it
    floor1 = uvage.from_color(gap.left/2, screenHeight, floorColor, gap.left, floorHeight)  #creates a floor gamebox based on the gap gamebox
    floor2 = uvage.from_color(((screenWidth - (floor1.width + gapWidth))/2) + floor1.width + gapWidth, screenHeight, floorColor, screenWidth - gap.right, floorHeight)
    floors.extend([floor1, floor2])

def moveFloors(): #method used to move floors up the screen
    global floors
    new_floors = []
    for floor in floors:
        floor.y -= floorSpeed
        if floor.y + floorHeight > 0:
            new_floors.append(floor)
    floors = new_floors

def drawObjects(): #draws all objects on the display
    camera.clear('black')
    camera.draw(ball)
    #floors
    for floor in floors:
        camera.draw(floor)
    #score
    camera.draw(uvage.from_text(30, screenHeight - 20, str(score), 40, 'red', bold = False))
    camera.display()

#BALL ATTRIBUTES
ball = uvage.from_circle(200, initialBallY, 'red', 20)
ball.xspeed = 0
ball.yspeed = ballSpeed

def tick():
    global gameOn
    global score
    global scoreIncr
    global ballSpeed
    global floorSpeed
    
    if uvage.is_pressing('space'):
        if not gameOn:
            resetGame()
        gameOn = True
    
    if gameOn:
        moveFloors()
        
        #checking to see if the game should create more floors
        if len(floors) == 0 or screenHeight - floors[-1].y >= floorInterval:
            createFloors()
            scoreIncr = False
        
        #moving the ball
        ball.move_speed()
        if uvage.is_pressing('left arrow'):
            ball.x -= 20
        elif uvage.is_pressing('right arrow'):
            ball.x += 20
        
        #ball boundaries
        if ball.bottom > screenHeight:
            ball.bottom = screenHeight
        if ball.left < 0:
            ball.left = 0
        elif ball.right > screenWidth:
            ball.right = screenWidth
        
        for floor in floors:
            if ball.bottom_touches(floor): #preventing the ball from going through the floors
                ball.move_to_stop_overlapping(floor)
                ball.speedy = floorSpeed
                ball.move_speed()
            if ball.y > floor.y and not scoreIncr:
                score += 1
                scoreIncr = True
        
        drawObjects()
        if ball.bottom < 0:
            gameOn = False
            camera.draw(uvage.from_text(200, 300, 'Game Over', 50, 'Red', bold = False))
            camera.display()

        
        ball.speedy += 0.0005

n = 1
if score > n*10:
    floorSpeed += 1
    n += 1

ticksPerSec = 30
uvage.timer_loop(ticksPerSec, tick)