import glob
import os
import sys
import time
from subprocess import call

from PIL import Image
from neopixel import *

sys.path.append("/home/pi/pywork")
from piframe_systemfiles import basicTools

FPS = 24
WAIT_TIME = int(1000/FPS)
DEBOUNCE_TIME = 150
height = 8
counter = 0
oldCounter = -1
files = glob.glob('/home/pi/pywork/piframe_apps/animations/*bmp')
size = len(files)
startTime = time.time()
starTimeDebounce = startTime
pixePerFrame = basicTools.LED_COUNT

width = 0
frames = 0
rgb_im = None


def createAnimation():

    global oldCounter,counter
    global startTime,starTimeDebounce
    global width
    global frames
    global rgb_im

    if oldCounter != counter:

        file = files[counter]
        im = Image.open(file)
        #im = im.rotate(180)

        rgb_im = im.convert('RGB')
        width = im.size[0]
        frames = width/height
        oldCounter = counter

    frame = 0
    while frame < frames and oldCounter == counter:

        debounceTime = (starTimeDebounce * 1000) + DEBOUNCE_TIME - (time.time() * 1000)

        if debounceTime <= 0:
            slideButtons()
            starTimeDebounce = time.time()

        remainingTime = (startTime*1000) + WAIT_TIME - (time.time()*1000)

        if remainingTime <= 0:
            pixel = 0
            startTime = time.time()

            while pixel < pixePerFrame:
                value = pixel / height
                picY = int(round(value))
                picX = pixel - (picY * height) + (frame * height)
                r, g, b = rgb_im.getpixel((picX, picY))
                strip.setPixelColor(abs(pixel-63), Color(g, r, b))

                pixel += 1

            frame += 1
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

    counter = basicTools.checkPos(counter, size)

#TODO fix Bug, while switching between animations

def slideButtons():

    left = basicTools.getLeftButton()
    right = basicTools.getRightButton()
    ok = basicTools.getOkButton()

    changePos(right,left,ok)


if __name__ == '__main__':

    strip = basicTools.strip
    strip.begin()
    startTime = time.time()

    while True:
        createAnimation()
