import time
def db(n): return [int(i) for i in bin(n)[2:].zfill(8)]
class R2R_ADC:
    def __init__(self, dr, ctime = 0.01, verb = False):
        self.dr = dr
        self.verb = verb
        self.ctime = ctime

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
    def setn(self, n):
        if (0<=n<=255):GPIO.output(self.bits_gpio, db(n))
        else:
            print("out of range")
            return
    def sec_count_adc(self):
        for n in range(256):
            self.setn(n)
            time.sleep(self.ctime)
            if GPIO.input(self.comp_gpio) == 0:return n
        return 255
    def get_sc_v(self):return self.sec_count_adc()*(self.dr/255.0)

if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.297)
        while True:
            print(adc.get_sc_v())
    finally:
        adc.deinit()