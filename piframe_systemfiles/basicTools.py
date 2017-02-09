import glob
import os

import numpy
from PIL import Image
from neopixel import *
import sys
from subprocess import call
import RPi.GPIO as GPIO
import time

#DO NOT MODIFY ANYTHING!!! THOSE SETTINGS ARE ESSENTIAL!!!
#settings are for 8x8 Matrix

LED_COUNT = 64  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 60  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

bitmask = 0b00001
height = 5
step = 31

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(25,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#Example for letter A:
# 1 1 1 1
# 1 0 0 1
# 1 1 1 1
# 1 0 0 1
# 1 0 0 1

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
            [0b11111,0b00001,0b00001,0b11111],  #U
            [0b11110,0b00001,0b00001,0b11110],  #V
            [0b11111,0b01000,0b01000,0b11111],  #W
            [0b11011,0b00100,0b00100,0b11011],  #X
            [0b11000,0b00111,0b00111,0b11000],  #Y
            [0b11001,0b10101,0b10101,0b10011]]) #Z

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

def clearMatrix(strip):
    strip.begin()
    for pixelPos in range(LED_COUNT):
        strip.setPixelColor(pixelPos,Color(0,0,0))
    strip.show()

#====== FILES =======

def listFiles(directory):

    files = glob.glob(directory)
    size = len(files)
    for file in range(size):
        files[file] = os.path.basename(files[file])

    return files

def checkPos(counter, size):

    if counter >= size:
        counter = 0
    elif counter < 0:
        counter += size

    return counter

#====== GPIO BUTTONS ========

prevLeftButton = 0
prevRightButton = 0
prevOkButton = 0

def getLeftButton():
    global prevLeftButton
    currentButton = not(GPIO.input(23))

    if not(prevLeftButton) and currentButton:
        prevLeftButton = currentButton
        return prevLeftButton
    elif prevLeftButton and not(currentButton):
        prevLeftButton = 0
        return prevLeftButton
    else:
        return 0

def getRightButton():
    global prevRightButton
    currentButton = not(GPIO.input(25))

    if not (prevRightButton) and currentButton:
        prevRightButton = currentButton
        return prevRightButton
    elif prevRightButton and not(currentButton):
        prevRightButton = 0
        return prevRightButton
    else:
        return 0

def getOkButton():
    global prevOkButton
    currentButton = not (GPIO.input(24))

    if not (prevOkButton) and currentButton:
        prevOkButton = currentButton
        return prevOkButton
    elif prevOkButton and not (currentButton):
        prevOkButton = 0
        return prevOkButton
    else:
        return 0

#======= ANIMATION ========


def fadeOut():

    currentbrightness = LED_BRIGHTNESS

    while currentbrightness >= 0:
        strip.setBrightness(currentbrightness)
        currentbrightness -= 5;
        strip.show()
        time.sleep(0.05)

def fadeIn():

    startbrightness = 0

    while startbrightness <= LED_BRIGHTNESS:
        strip.setBrightness(startbrightness)
        startbrightness += 5;
        strip.show()
        time.sleep(0.05)


#======= DRAW GRAPHICS ======
"""
def drawGraphics(picArray,width):

    drawGraphics(picArray,width,63)


def drawGraphics(picArray,width,pos):

    shift = 8 - width
    color = 0

    for i in range(picArray):

        if picArray[i]:
            color = Color(123,50,50)
        else:
            color = Color(0,0,0)

        if picArray % width == 0:
            pos -= 1
        else:
            pos -= shift

        strip.setPixelColor(pos, color)
"""


