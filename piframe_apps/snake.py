import math
import random
import sys
import time
from subprocess import call

from neopixel import *

sys.path.append("/home/pi/pywork/")
from piframe_systemfiles import basicTools

# 0 0 0 0 0 0
# 0 0 1 1 0 0
# 1 1 1 1 0 0
# 1 1 1 1 1 1
# 1 1 1 1 1 1

# 0 1 1 0 0 0
# 0 1 1 1 0 0
# 0 1 1 1 1 0
# 0 1 1 1 0 0
# 0 1 1 0 0 0


startspeed = 0.4

# Snake color Green, Red, Blue
head = Color(255,255,102)
tail = 100
tailEnd = Color(0,0,0)
tailColor = Color(255,153,51)
snakeHeadX = 7
snakeHeadY = 0
snakeLength = 3
#X and Y
directionCounter = 0
snake = [65] * basicTools.LED_COUNT * 2
#counting from 0
matrixLength = int(math.sqrt(basicTools.LED_COUNT)) - 1
matrix = [Color(0,0,0)] * basicTools.LED_COUNT

foodX = random.randint(0,matrixLength)
foodY = random.randint(0,matrixLength)
matrix[foodX + (foodY * 8)] = Color(255,100,200)
alive = True

#TODO Bug: Kopf aktualisiert sich schneller als Schwanz -> beisst sich in den Schwanz, obwohl sie es nicht kann

def updateMatrix(currentMatrix):
    for pixelPos in range(strip.numPixels()):
        strip.setPixelColor(pixelPos,currentMatrix[pixelPos])
    strip.show()

def moveLeft():
    global snakeHeadX
    if snakeHeadX == matrixLength:
        snakeHeadX = 0
    else:
        snakeHeadX += 1

def moveRight():
    global snakeHeadX
    if snakeHeadX == 0:
        snakeHeadX = matrixLength
    else:
        snakeHeadX -= 1

def moveUp():
    global snakeHeadY
    if snakeHeadY == matrixLength:
        snakeHeadY = 0
    else:
        snakeHeadY += 1

def moveDown():
    global snakeHeadY
    if snakeHeadY == 0:
        snakeHeadY = matrixLength
    else:
        snakeHeadY -= 1

def updateSnakePos():
    #old Pos
    snakeTail(snakeHeadX, snakeHeadY)
    viewTail(tailColor)

    #matrix[snakeHeadX+ (snakeHeadY*8)] = Color(0,0,0)
    global directionCounter

    if basicTools.getLeftButton():
        directionCounter -= 1

    elif basicTools.getRightButton():
        directionCounter += 1

    elif basicTools.getOkButton():
        basicTools.fadeOut()
        call(['python', '/home/pi/pywork/piframe_systemfiles/menu.py'])
        sys.exit

    checkCounter()
    moveDirection()

    #mew Pos
    matrix[snakeHeadX + (snakeHeadY*8)] = head

def checkCounter():

    global directionCounter

    if directionCounter < 0:
        directionCounter = 3
    elif directionCounter > 3:
        directionCounter = 0

def moveDirection():

    global directionCounter

    if directionCounter == 0:
        moveRight()
    elif directionCounter == 1:
        moveDown()
    elif directionCounter == 2:
        moveLeft()
    elif directionCounter == 3:
        moveUp()

def snakeTail(x,y):
    lastX = 0
    lastY = 0
    global snake

    for i in range(snakeLength):
        if i>0:
            x = snake[i]
            y = snake[i + basicTools.LED_COUNT]
            snake[i] = lastX
            snake[i + basicTools.LED_COUNT] = lastY
            lastX = x
            lastY = y
        else:
            lastX = snake[i]
            lastY = snake[i + basicTools.LED_COUNT]
            snake[i] = x
            snake[i + basicTools.LED_COUNT] = y

def viewTail(TailColor):

    for i in range(snakeLength):

        if snake[i] < 65:
            matrix[snake[i] + (snake[i + basicTools.LED_COUNT] * 8)] = TailColor

            if i >= snakeLength-1:
                matrix[snake[i] + (snake[i + basicTools.LED_COUNT] * 8)] = Color(0, 0, 0)

def spawnFood():
    global snakeLength
    global foodX
    global foodY
    global startspeed

    if snakeHeadX == foodX and snakeHeadY == foodY:
        snakeLength += 1
        startspeed *= 0.95
        matrix[foodX + (foodY * 8)] = Color(0,0,0)
        freeSpot = random.choice(checkMatrix())
        foodY = freeSpot/(matrixLength+1)
        foodX = freeSpot - (foodY*(matrixLength+1))
        #foodX = random.randint(0,matrixLength)
        #foodY = random.randint(0, matrixLength)
        matrix[foodX + (foodY * 8)] = Color(255,100,200)

def checkMatrix():
    freeSpots = []
    for i in range(basicTools.LED_COUNT):
        if matrix[i] == Color(0,0,0):
            freeSpots.append(i)

    return freeSpots

def death():

    global alive
    for i in range(snakeLength):
        if snakeHeadX == snake[i] and snakeHeadY == snake[i+ basicTools.LED_COUNT]:
            alive = False

def endSequence():

    global head

    for i in range(3):
        viewTail(Color(0, 0, 0))
        matrix[snakeHeadX + (snakeHeadY * 8)] = Color(0,0,0)
        updateMatrix(matrix)
        time.sleep(0.25)

        viewTail(tailColor)
        matrix[snakeHeadX + (snakeHeadY * 8)] = Color(255, 255, 102)
        updateMatrix(matrix)
        time.sleep(0.25)

    time.sleep(1)
    basicTools.fadeOut()
    call(['python', '/home/pi/pywork/piframe_systemfiles/menu.py'])
    sys.exit()


if __name__ == '__main__':

    strip = basicTools.strip
    strip.begin()
    currentTime = time.time()


    while alive:

        if currentTime+startspeed-time.time() <= 0:

            spawnFood()
            updateSnakePos()
            updateMatrix(matrix)
            currentTime = time.time()

        death()

    endSequence()

