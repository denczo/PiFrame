import time
from collections import deque
import threading
from neopixel import *

LED_COUNT = 64  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 60  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

thread_active = True

origin = 26
first = 240
second = int(first*0.5)
third = int(second*0.5)
fourth = int(third*0.5)

shade = deque([first,second,third,fourth])
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

def stopThread(active):
    global thread_active
    thread_active = active

def animation():

    global strip
    originPixel = origin

    for pixel in range(4):

        if pixel < 2:
            originPixel +=1
        elif pixel == 2:
            originPixel += 8
        elif pixel > 2:
            originPixel -=1

        strip.setPixelColor(originPixel, Color(0, shade[pixel], 0))
        #print originPixel

    shade.rotate(1)

def thread():
    global thread_active,strip
    #strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    startTime = time.time()
    waitTime = 0.1

    print 'Thread stare'
    while thread_active:

        if startTime+waitTime-time.time() <= 0:
            animation()
            strip.show()
            startTime = time.time()
            #time.sleep(0.1)

th=threading.Thread(target=thread)
#th.daemon = True
#if __name__ == '__main__':
 #   strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
  #  strip.begin()

    #while True:
    #    animation()
    #    strip.show()
    #    time.sleep(0.1)

