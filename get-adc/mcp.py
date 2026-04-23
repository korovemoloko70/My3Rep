import mcp3021_driver as mcp
import adc_plot
import numpy as np
import time

adc = mcp.MCP3021(5.0)

voltage_vals = []
time_vals = []
duration = 10.0

try:
    begin_time = time.time_ns()
    ctime = begin_time
    while (ctime-begin_time)/1e9 < duration:
        ctime = time.time_ns()
        volt = adc.get_voltage()
        time_vals.append((ctime-begin_time)/1e9)
        voltage_vals.append(volt)
    adc_plot.plot_voltage_vs_time(time_vals, voltage_vals, np.max(voltage_vals))
    adc_plot.plot_sampling_period_hist(time_vals)
finally:
    adc.deinit()