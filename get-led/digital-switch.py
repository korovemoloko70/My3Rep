import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
state = False
GPIO.setup(led, GPIO.OUT)
button = 13
GPIO.setup(button, GPIO.IN)

while True:
    if GPIO.input(button):
        state = not state
        GPIO.output(led, state)
        time.sleep(0.2)