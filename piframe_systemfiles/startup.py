import glob
import os
import sys
import time
from subprocess import call

from PIL import Image
from neopixel import *

sys.path.append("/home/pi/pywork")
from piframe_systemfiles import basicTools

im = Image.open("/home/pi/pywork/piframe_systemfiles/PiFrame_Logo.bmp")
rgb_im = im.convert('RGB')
pixelPerFrame = 64
WAIT_TIME = 2000

def startScreen():

    pixel = 0

    while pixel < pixelPerFrame:
        value = pixel / 8
        picY = int(round(value))
        picX = pixel - (picY * 8)
        r, g, b = rgb_im.getpixel((picX, picY))
        strip.setPixelColor(abs(pixel - 63), Color(g, r, b))

        pixel += 1

    strip.show()

if __name__ == '__main__':

    strip = basicTools.strip
    strip.begin()
    startScreen()
    time.sleep(1)
    call(['python', '/home/pi/pywork/piframe_systemfiles/menu.py'])
    sys.exit()


