import RPi.GPIO as GPIO
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
    def number_to_dac(self, number):
        GPIO.output(self.bits_gpio, [int(element) for element in bin(number)[2:].zfill(8)])
    def sequential_counting_adc(self):
        num = 0
        self.number_to_dac(num)
        time.sleep(self.compare_time)
        while(not GPIO.input(self.comp_gpio)):
            time.sleep(self.compare_time)
            num += 1
            if num > 255:
                break
            self.number_to_dac(num)
        self.number_to_dac(0)
        return num
    def successive_approximation_adc(self):
        self.number_to_dac(0)
        num = 0
        for bit in self.bits_gpio:
            num *= 2
            GPIO.output(bit, 1)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio):
                GPIO.output(bit, 0)
            else:
                num += 1
        self.number_to_dac(0)
        return num
    def successive_approximation_adc_indian(self):
        self.number_to_dac(0)
        num = 0
        GPIO.output(self.bits_gpio[0], 1)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio):
            GPIO.output(self.bits_gpio[0], 0)
        else:
            num += 1
        num *= 2
        GPIO.output(self.bits_gpio[1], 1)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio):
            GPIO.output(self.bits_gpio[1], 0)
        else:
            num += 1
        num *= 2
        GPIO.output(self.bits_gpio[2], 1)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio):
            GPIO.output(self.bits_gpio[2], 0)
        else:
            num += 1
        num *= 2
        GPIO.output(self.bits_gpio[3], 1)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio):
            GPIO.output(self.bits_gpio[3], 0)
        else:
            num += 1
        num *= 2
        GPIO.output(self.bits_gpio[4], 1)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio):
            GPIO.output(self.bits_gpio[4], 0)
        else:
            num += 1
        num *= 2
        GPIO.output(self.bits_gpio[5], 1)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio):
            GPIO.output(self.bits_gpio[5], 0)
        else:
            num += 1
        num *= 2
        GPIO.output(self.bits_gpio[6], 1)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio):
            GPIO.output(self.bits_gpio[6], 0)
        else:
            num += 1
        num *= 2
        GPIO.output(self.bits_gpio[7], 1)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio):
            GPIO.output(self.bits_gpio[7], 0)
        else:
            num += 1
        return num
    def get_sc_voltage(self):
        return self.sequential_counting_adc()/255*self.dynamic_range
    def get_sar_voltage(self):
        return self.successive_approximation_adc()/255*self.dynamic_range
    def get_sar_voltage_indian(self):
        return self.successive_approximation_adc_indian()/255*self.dynamic_range

if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.177)
        while True:
            print("Напряжение:", adc.get_sar_voltage(), "В")
            time.sleep(0.5)
    finally:
        adc.deinit()