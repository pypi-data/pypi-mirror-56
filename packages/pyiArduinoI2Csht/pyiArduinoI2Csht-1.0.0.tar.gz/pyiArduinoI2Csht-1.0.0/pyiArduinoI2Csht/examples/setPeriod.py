# ЗАДАНИЕ ПЕРИОДА ОБНОВЛЕНИЯ ПОКАЗАНИЙ ДАТЧИКОВ:

# Подключаем библиотеку для работы с датчиком температуры и влажности I2C-flash (Sensor Humidity and Temperature).
from pyiArduinoI2Csht import *
from time import sleep

# Объявляем объект sht для работы с функциями и методами библиотеки pyiArduinoI2Csht.
# Если при объявлении объекта указать адрес, например, sht(0xBB),
# то пример будет работать с тем модулем, адрес которого был указан.
sht = pyiArduinoI2Csht()

# Указываем модулю обновлять показания датчиков каждые две секунды.
sht.setPeriod(2.0)

while True:
    # Выводим текущую температуру и влажность
    print("t="+str(sht.getTem())+"°C, ")
    print("RH="+str(sht.getHum())+"%%")
    sleep(.1)
