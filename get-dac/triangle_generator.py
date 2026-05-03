import numpy as np
import time

def get_trig_wave_amplitude(freq, time):
    period = 0.5/freq
    offset = time%period
    if(offset < period/2): return 2*offset/period;
    else: return 2-2*offset/period

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1.0/sampling_frequency)