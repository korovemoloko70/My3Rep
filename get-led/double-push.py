import RPi.GPIO as GPIO 
import time
GPIO.setmode(GPIO.BCM)

leds = [16, 12, 25, 17, 27, 23, 22, 24]
up = 9
down = 10

GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
GPIO.setup (up, GPIO.IN)
GPIO.setup(down, GPIO.IN)
num = 0
sleep_time = 0.2
def dec2bin(value) :
    return [int(element) for element in bin(value)[2:].zfill(8)]

while True:
   state_up = GPIO.input (up)
   state_down = GPIO. input (down)
   if state_down and state_up:
       num = 255
       print (num, dec2bin(num))
       time.sleep(sleep_time)
   elif state_up:
       num += 1
       if num > 255:
           num = 0
       print(num, dec2bin(num))
       time. sleep(sleep_time)
   elif state_down:
      num -= 1
      if num < 0:
            num = 0
      print (num,dec2bin(num))
      time. sleep(sleep_time)
   GPIO. output(leds, dec2bin(num))