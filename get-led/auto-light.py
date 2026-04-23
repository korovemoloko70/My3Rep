import RPi. GPIO as GPIO
GPIO. setmode(GPIO.BCM)

led = 26
sensor = 6
GPIO. setup(led, GPIO.OUT)
GPIO. setup(sensor, GPIO. IN)

while True:
     GPIO.output(led, not GPIO.input(sensor))
