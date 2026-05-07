import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        """
        Конструктор класса R2R_ADC
        
        Args:
            dynamic_range: динамический диапазон ЦАП (опорное напряжение в вольтах)
            compare_time: время ожидания для установления напряжения (сек)
            verbose: флаг вывода отладочной информации
        """
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        # GPIO пины для 8-битного ЦАП (R-2R лестница)
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        # GPIO пин для входа компаратора
        self.comp_gpio = 21
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def __del__(self):
        """Деструктор: сбрасывает выходы и очищает настройки GPIO"""
        self.deinit()
    
    def deinit(self):
        """Выставляет 0 на выход ЦАП и очищает настройки GPIO"""
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
    
    def decimal2binary(self, value):
        """Преобразует десятичное число в список битов для GPIO
        
        Args:
            value: число от 0 до 255
            
        Returns:
            list: список битов длиной 8 (старший бит - первый)
        """
        return [int(bit) for bit in bin(value)[2:].zfill(8)]
    
    def number_to_dac(self, number):
        """Подаёт число на вход ЦАП
        
        Args:
            number: целое число от 0 до 255
        """
        if self.verbose:
            print(f"Подаю на ЦАП число: {number} (бинарно: {bin(number)[2:].zfill(8)})")
        GPIO.output(self.bits_gpio, self.decimal2binary(number))
    
    def sequential_counting_adc(self):
        """Последовательное приближение: ищет код, соответствующий входному напряжению
        
        Returns:
            int: цифровой код (0-255), соответствующий входному напряжению
        """
        for code in range(256):  # перебираем все возможные коды от 0 до 255
            self.number_to_dac(code)
            time.sleep(self.compare_time)  # даём время на установление и сравнение
            
            if self.verbose:
                comp_state = GPIO.input(self.comp_gpio)
                print(f"Код {code:3d} ({bin(code)[2:].zfill(8)}), компаратор: {comp_state}")
            
            # Если напряжение на ЦАП превысило входное, компаратор изменит состояние
            # Предполагаем: компаратор выдаёт 0, когда V_ЦАП <= V_вход, и 1, когда V_ЦАП > V_вход
            # Подстройте эту логику в зависимости от подключения вашего компаратора
            if GPIO.input(self.comp_gpio) == 1:  # компаратор переключился
                if self.verbose:
                    print(f"Найдено значение: {code}")
                return code
        
        # Если ничего не нашли (максимальное напряжение не достигнуто)
        if self.verbose:
            print("Внимание: напряжение не превышено, возвращаю максимальный код")
        return 255
    
    def get_sc_voltage(self):
        """Возвращает измеренное напряжение в вольтах
        
        Returns:
            float: измеренное напряжение
        """
        code = self.sequential_counting_adc()
        voltage = code * self.dynamic_range / 255.0
        if self.verbose:
            print(f"Код: {code}, Напряжение: {voltage:.4f} В")
        return voltage


# Основной охранник
if __name__ == "__main__":
    # Измерьте динамический диапазон вашего ЦАП (опорное напряжение) мультиметром
    # Например, если опорное напряжение 3.30 В, укажите 3.30
    DYNAMIC_RANGE = 3.30  # ВОЛЬТ - ИЗМЕРЬТЕ МУЛЬТИМЕТРОМ!
    
    # Создаём объект класса с отладочным выводом
    adc = None
    
    try:
        # Создаём объект АЦП
        adc = R2R_ADC(
            dynamic_range=DYNAMIC_RANGE,
            compare_time=0.01,
            verbose=True  # Для отладки можно включить подробный вывод
        )
        
        print("\n=== Начинаю измерение напряжения потенциометра ===")
        print("Крутите потенциометр для изменения напряжения\n")
        
        # Бесконечный цикл измерений
        while True:
            # Измеряем напряжение
            voltage = adc.get_sc_voltage()
            # Печатаем напряжение с точностью до 3 знаков
            print(f"Напряжение: {voltage:.3f} В")
            print("-" * 30)
            
            # Небольшая пауза между измерениями (опционально)
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\nПрограмма остановлена пользователем")
    
    finally:
        # Очищаем ресурсы GPIO через деструктор
        if adc is not None:
            adc.deinit()
        print("Ресурсы GPIO очищены. Завершение работы.")