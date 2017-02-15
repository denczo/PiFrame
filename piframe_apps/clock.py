import sys
import time
from subprocess import call

from neopixel import *

sys.path.append("/home/pi/pywork/")
from piframe_systemfiles import basicTools

ZERO    = [1,1,0,
           1,1,0,
           1,1,0,
           1,1,0]

ONE     = [0,1,0,
           0,1,0,
           0,1,0,
           0,1,0]

TWO     = [1,1,0,
           0,1,0,
           1,0,0,
           1,1,0]

THREE   = [1,1,0,
           0,1,0,
           0,1,0,
           1,1,0]

FOUR    = [1,0,0,
           1,1,0,
           0,1,0,
           0,1,0]

FIVE    = [1,1,0,
           1,0,0,
           0,1,0,
           1,1,0]

SIX     = [1,1,0,
           1,0,0,
           1,1,0,
           1,1,0]

SEVEN   = [1,1,0,
           0,1,0,
           0,1,0,
           0,1,0]

EIGHT   = [ 0,1,0,
            0,1,0,
            1,0,1,
            1,1,1 ]

NINE    = [1,1,0,
           1,1,0,
           0,1,0,
           1,1,0]

counter = 0
numbers = [ZERO,ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE]

digitColors = [Color(255, 123, 123),Color(255,255,255),Color(153,255,51),Color(115, 255, 64),Color(0,128,255),Color(51,255,255)]
size = len(digitColors)/2

#DO NOT CHANGE ANYTHING IN THIS METHOD!
def showDigit(digit, origin, color):

    counter = 1
    length = len(numbers[digit])
    width = 0
    step = 0

    if length > 8:

        width = 3
        step = 6
    elif length <= 8:
        width = 2
        step = 7

    for number in numbers[digit]:
        if number:
            strip.setPixelColor(origin, color)
        else:
            strip.setPixelColor(origin,Color(0,0,0))

        if counter < width:
            origin -= 1
        elif counter >= width:
            origin -= step
            counter = 0

        counter+=1
        strip.show()

def changePos(right, left, ok):

    global counter

    if right:
        counter += 1
    elif left:
        counter -= 1
    elif ok:
        basicTools.fadeOut()
        call(['python', '/home/pi/pywork/piframe_systemfiles/menu.py'])
        sys.exit

    checkPos()

def checkPos():

    global counter, size

    if counter >= size:
        counter = 0
    elif counter < 0:
        counter = size-1

def slideButtons():

    changePos(basicTools.getRightButton(), basicTools.getLeftButton(), basicTools.getOkButton())

def hours():

    global counter

    hour = time.strftime("%H")
    origin = 63
    for digit in hour:
        showDigit(int(digit),origin, digitColors[counter-1])
        origin-= 3

def minutes():

    global counter

    minute = time.strftime("%M")
    origin = 29
    for digit in minute:
        showDigit(int(digit),origin,digitColors[counter+size-1])
        origin-=3

if __name__ == '__main__':

    strip = basicTools.strip
    strip.begin()

    while True:
        print counter
        hours()
        minutes()
        slideButtons()

