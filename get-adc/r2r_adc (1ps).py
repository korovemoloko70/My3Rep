import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def decimal2binary(value):
        return [int(element) for element in bin(value)[2:].zfill(8)]

    def number_to_dac(self, number):
        GPIO.output(self.comp_gpio, self.decimal2binary(number))

    def sequential_counting_adc(self):
        k = 0
        while (k < self.dynamic_range):
            GPIO.output(self.bits_gpio, self.decimal2binary(k))
            time.sleep(0.01)
            k += 1
        