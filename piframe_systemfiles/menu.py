import glob
import os
import sys
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
letterCounter = 0
startTime = time.time()
waitTime = 0.1
leftBorder = 63
rightBorder = 56

origin = 63

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
width = 4
step = 32

def showLetter(origin, color, letter):

    #Spalte fuer Spalte
    for column in letter:
        #wenn innerhalb des vorgesehenen Abschnitts, dann zeige Buchstabe
        if checkOrigin(origin):
            #Jede Zeile in einer Spalte + Loeschspalte
            for i in range(height):

                if (column >> i) & bitmask:
                    strip.setPixelColor(origin, color)
                else:
                    strip.setPixelColor(origin,Color(0,0,0))

                #beim letzten Pixel zurueck zum Anfang springen
                if i < height-1:
                    origin -= 8
                elif i >= height-1:
                    origin += step

            #strip.show()

        origin -= 1

def checkOrigin(origin):
    if origin <= leftBorder and origin >= rightBorder:
        return True
    else:
        return False

def clearColumn(origin):

    if checkOrigin(origin):
        for i in range(height):
            strip.setPixelColor(origin, Color(0, 0, 0))
            origin -= 8

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
        files[file] = os.path.splitext(os.path.basename(files[file]))[0]


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
        call(['python', filename+'.py'])
        sys.exit()

    checkPos()

def slideButtons():

    left = basicTools.getLeftButton()
    right = basicTools.getRightButton()
    ok = basicTools.getOkButton()
    changePos(right,left,ok)

def showFile():

    print(files[counter])

def switchColor(switch):

    if switch:
        return Color(100,160,40)
    else:
        return Color(100,160,30)

def writeWord(letterLeft,origin,switch):

    countLetters = len(letterLeft)
    posInAlphabet = ord(letterLeft[0])%32 - 1

    color = switchColor(switch)

    showLetter(origin, color, basicTools.alphabet[posInAlphabet])
    origin -= 4

    if countLetters > 1:
        countLetters -= 1
        letterLeft = letterLeft[-countLetters:]
        writeWord(letterLeft,origin,not(switch))
    elif countLetters <= 1:
        clearColumn(origin)

def slideWord():

    global startTime
    global origin
    global waitTime

    word = files[counter]
    wordLength = len(word)
    writeWord(word, origin, True)
    remainingTime = startTime + waitTime - time.time()

    if remainingTime <= 0:
        startTime = time.time()
        waitTime = 0.1

        if origin < leftBorder+(wordLength*width):
            origin += 1

            if origin == basicTools.LED_COUNT - 1:
                waitTime = 3
        else:
            origin = rightBorder

if __name__ == '__main__':

    strip = basicTools.strip
    strip.begin()

    listFiles()
    barBackground()

    startbrightness = 0
    strip.setBrightness(startbrightness)
    waitTime = 5

    while True:

        slideWord()
        barBackground()
        calculateBar()
        slideButtons()
        strip.show()

        #animation
        while startbrightness <= basicTools.LED_BRIGHTNESS:
            strip.setBrightness(startbrightness)
            startbrightness += 5;
            strip.show()
            time.sleep(0.05)







