import r2r_adc_ps as r2r_ps
import adc_plot_ps as adc_plot
import numpy as np
import time

adc = r2r_ps.R2R_ADC1ps(3.177, compare_time=0.0001)

voltage_vals = []
time_vals = []
duration = 3.0

try:
    begin_time = time.time_ns()
    ctime = begin_time
    while (ctime-begin_time)/1e9 < duration:
        ctime = time.time_ns()
        volt = adc.get_sar_voltage()
        print(volt)
        time_vals.append((ctime-begin_time)/1e9)
        voltage_vals.append(volt)
    adc_plot.plot_voltage_vs_time(time_vals, voltage_vals, np.max(voltage_vals))
    adc_plot.plot_sampling_period_hist(time_vals)
finally:
    adc.deinit()