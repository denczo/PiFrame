import os
import sys
import time
from subprocess import call

from PIL import Image
from neopixel import *

sys.path.append("/home/pi/pywork")
from piframe_systemfiles import basicTools

fps = 2
counter = 0
files = basicTools.listFiles('/home/pi/pywork/piframe_apps/animations/*bmp')
size = len(files)

def getPixelData():

    file = os.path.join('/home/pi/pywork/piframe_apps/animations', files[counter])

    im = Image.open(file)
    im = im.rotate(180)
    im.save
    rgb_im = im.convert('RGB')

    startTime = time.time()
    waitTime = 0.2

    # only quadratic pictures! height = width of a single picture
    width,height = im.size

    frames = width/height
    pixelPerFrame = height*height
    picX = 0
    picY = 0

    frame = 0
    while frame < frames:
        slideButtons()
        pixel = 0

        remainingTime = startTime+waitTime-time.time()

        if remainingTime <= 0:

            startTime = time.time()
            while pixel < pixelPerFrame:

                value = pixel/height
                picY = int(round(value))
                shift = 0
                picX = pixel - (value*height) + (frame*height)

                r,g,b = rgb_im.getpixel((picX,picY))

                strip.setPixelColor(pixel, Color(g,r,b))
                pixel += 1

            #time.sleep(0.1)
            strip.show()
            frame += 1

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

def slideButtons():

    left = basicTools.getLeftButton()
    right = basicTools.getRightButton()
    ok = basicTools.getOkButton()
    changePos(right,left,ok)


if __name__ == '__main__':

    strip = basicTools.strip
    strip.begin()

    while True:
        getPixelData()

