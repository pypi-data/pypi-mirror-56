# ПРИМЕР ЧТЕНИЯ ВСЕХ ЗНАЧЕНИЙ ДАТЧИКА:

# Подключаем библиотеку для работы с датчиком температуры
# и влажности I2C-flash (Sensor Humidity and Temperature).
from pyiArduinoI2Csht import *

from time import sleep

# Объявляем объект sht для работы с функциями и методами библиотеки pyiArduinoI2Csht.
# Если при объявлении объекта указать адрес, например, sht(0xBB), то пример будет
# работать с тем модулем, адрес которого был указан.
sht = pyiArduinoI2Csht()

while True:
    # Выводим текущую температуру и влажность воздуха
    print("Температура = %.1f °C" % sht.getTem(), end='')
    print(", влажность = %.1f %%" % sht.getHum())
    sleep(.5)
