try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(25,GPIO.IN,pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':
        while True:

            if GPIO.input(23) == False:
                print "PRESSED"

            time.sleep(0.2)

