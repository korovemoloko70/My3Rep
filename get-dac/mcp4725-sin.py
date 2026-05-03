import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 3.15
signal_frequency = 2
sampling_frequency = 1000

if __name__ == "__main__":
    try:
        amplitude = float(input("Введите амплитуду: "))
        signal_frequency = float(input("Введите частоту сигнала: "))
        sampling_frequency = float(input("Введите частоту дискретизации: "))
        dac = mcp.MCP4725(5.0, verbose = False)
        n = 0
        while True:
            voltage = amplitude*sg.get_sin_wave_amplitude(signal_frequency, 1/sampling_frequency*n)
            n += 1
            sg.wait_for_sampling_period(sampling_frequency)
            dac.set_voltage(voltage)
    except ValueError:
        print("Число введено неправильно!")

    finally:
        dac.deinit()