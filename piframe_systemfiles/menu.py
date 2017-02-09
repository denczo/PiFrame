import glob
import os
import sys
import threading
import time
from subprocess import call
import numpy
from neopixel import *
sys.path.append("/home/pi/pywork")
from piframe_systemfiles import basicTools

os.system('clear')
files = 0
size = 0
counter = 0
lCounter = 0
startTime = 0
waitTime = 0.2
startPosF = 63
startPosS = 59
currentPos = 0

alphabet = numpy.array([
            [0b11111,0b00101,0b00101,0b11111],  #A
            [0b11111,0b10101,0b10101,0b01010],  #B
            [0b01110,0b10001,0b10001,0b01010],  #C
            [0b11111,0b10001,0b10001,0b01110],  #D
            [0b11111,0b10101,0b10101,0b10101],  #E
            [0b11111,0b10100,0b10100,0b10100],  #F
            [0b01110,0b10001,0b10101,0b10110],  #G
            [0b11111,0b00100,0b00100,0b11111],  #H
            [0b00000,0b11111,0b11111,0b00000],  #I
            [0b10010,0b10001,0b10001,0b11110],  #J
            [0b11111,0b00100,0b01110,0b10001],  #K
            [0b11111,0b10000,0b10000,0b10000],  #L
            [0b11111,0b00010,0b00010,0b11111],  #M
            [0b11111,0b00110,0b01100,0b11111],  #N
            [0b01110,0b10001,0b10001,0b01110],  #O
            [0b11111,0b10100,0b10100,0b01000],  #P
            [0b01110,0b10001,0b10011,0b01111],  #Q
            [0b11111,0b00101,0b01101,0b10010],  #R
            [0b10010,0b10101,0b10101,0b01001],  #S
            [0b10000,0b11111,0b11111,0b10000],  #T
            [0b11111,0b10000,0b10000,0b11111],  #U
            [0b11110,0b00001,0b00001,0b11110],  #V
            [0b11111,0b01000,0b01000,0b11111],  #W
            [0b11011,0b00100,0b00100,0b11011],  #X
            [0b11000,0b00111,0b00111,0b11000],  #Y
            [0b11001,0b10101,0b10101,0b10011]]) #Z
bitmask = 0b00001
height = 5
step = 31

def showLetter(origin, color, letter):

    counter = 1

    for column in letter:

        for i in range(height):
            if (column >> i) & bitmask:
                strip.setPixelColor(origin, color)
            else:
                strip.setPixelColor(origin,Color(0,0,0))

            if counter < height:
                origin -= 8
            elif counter >= height:
                origin += step
                counter = 0

            counter+=1
            strip.show()

def calculateBar():

    sizeSlider = 0
    origin = 15
    if size > 0:
        sizeSlider = 8/size

    else:
        sizeSlider = 1

    part = size/8.0
    sliderPos = int(round(counter/part))

    for i in range(sizeSlider):
        #R,G,B
        strip.setPixelColor(origin-sliderPos, Color(100,160,50))
        sliderPos+=1

def listFiles():

    global files,size,dir

    files = glob.glob('/home/pi/pywork/piframe_apps/*py')
    size = len(files)
    for file in range(size):
        files[file] = os.path.basename(files[file])


    showFile()

def checkPos():

    global counter, size

    if counter >= size:
        counter = 0
    elif counter < 0:
        counter += size

def barBackground():

    pos = 15;

    for i in range(8):
        strip.setPixelColor(pos, Color(20,60,10))
        pos -= 1

def changePos(right, left, ok):

    global counter

    if right:
        counter += 1
    elif left:
        counter -= 1
    elif ok:
        basicTools.fadeOut()
        filename = os.path.join('/home/pi/pywork/piframe_apps', files[counter])
        print filename
        call(['python', filename])
        sys.exit()

    checkPos()

def slideButtons():

    left = basicTools.getLeftButton()
    right = basicTools.getRightButton()
    ok = basicTools.getOkButton()
    changePos(right,left,ok)

def showFile():

    print(files[counter])

def getfirst2Letter():

    first2Letter = files[counter][:2]
    first = ord(first2Letter[0])%32 - 1
    second = ord(first2Letter[1])%32 - 1

    #G,R,B
    showLetter(63,Color(100,160,30),alphabet[first])
    showLetter(59,Color(100,160,40),alphabet[second])


def slideLetters():

    letters = files[counter]
    countLetters = len(letters)
    global lCounter
    global startTime
    global waitTime
    global currentPos


    leftBorder = startPosF - 8
    rightBorder = startPosF
    sub = 4

    startTime = time.time()

    remainingTime = startTime+waitTime-time.time()

    if currentPos < startPosS:
        sub -= 8

    if remainingTime <= 0:
        lCounter += 1
        startTime = time.time()
        waitTime = 0.2

    first = ord(letters[lCounter]) % 32 - 1
    showLetter(currentPos, Color(100, 160, 30), alphabet[first])

    if lCounter < countLetters:
        second = ord(letters[lCounter + 1]) % 32 - 1
        # G,R,B
        showLetter(currentPos-4, Color(100, 160, 40), alphabet[second])
    else:
        lCounter = 0
        waitTime = 2

if __name__ == '__main__':

    strip = basicTools.strip
    strip.begin()

    listFiles()
    barBackground()

    startbrightness = 0
    strip.setBrightness(startbrightness)

    while True:

        calculateBar()
        showFile()
        getfirst2Letter()
        barBackground()
        slideButtons()

        #animation
        while startbrightness <= basicTools.LED_BRIGHTNESS:
            strip.setBrightness(startbrightness)
            startbrightness += 5;
            strip.show()
            time.sleep(0.05)







