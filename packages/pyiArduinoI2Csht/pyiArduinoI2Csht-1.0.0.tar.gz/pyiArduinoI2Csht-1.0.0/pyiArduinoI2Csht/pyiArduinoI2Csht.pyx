# distutils: language = c++
# cython: language_level = 3

from iarduino_I2C_SHT cimport iarduino_I2C_SHT
#from time import sleep

DEF_CHIP_ID_FLASH =  0x3C
DEF_CHIP_ID_METRO =  0xC3
DEF_MODEL_SHT   =   0x07

# Адреса регистров модуля:
REG_FLAGS_0          =  0x00
REG_BITS_0           =  0x01
REG_FLAGS_1          =  0x02
REG_BITS_1           =  0x03
REG_MODEL            =  0x04
REG_VERSION          =  0x05
REG_ADDRESS          =  0x06
REG_CHIP_ID          =  0x07
REG_SHT_PERIOD       =  0x08
REG_SHT_FLG          =  0x10
REG_SHT_TEM_L        =  0x11
REG_SHT_HUM_L        =  0x13
REG_SHT_TEM_CHANGE   =  0x15
REG_SHT_HUM_CHANGE   =  0x16
# Позиция битов и флагов:
SHT_TEM_NEGATIVE     =  0x80
SHT_FLG_CHANGED_HUM  =  0x04
SHT_FLG_CHANGED_TEM  =  0x02
SHT_FLG_CHANGED      =  0x01

NO_BEGIN = 1

cdef class pyiArduinoI2Csht:
    cdef iarduino_I2C_SHT c_sht

    def __cinit__(self, address=None, auto=None):

        if address is not None:

            self.c_sht = iarduino_I2C_SHT(address)

            if auto is None:
                #sleep(.5)
                if not self.c_sht.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля,"
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

        else:

            self.c_sht = iarduino_I2C_SHT()

            if auto is None:
                #sleep(.5)
                if not self.c_sht.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля, "
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

    def begin(self):
        return self.c_sht.begin()

    def changeAddress(self, unsigned char newAddr):
        return self.c_sht.changeAddress(newAddr)

    def reset(self):
        return self.c_sht.reset()

    def getAddress(self):
        return self.c_sht.getAddress()

    def getVersion(self):
        return self.c_sht.getVersion()

    def getTem(self):
        return self.c_sht.getTem()

    def getHum(self):
        return self.c_sht.getHum()

    def getTemChanged(self):
        return self.c_sht.getTemChanged()

    def getHumChanged(self):
        return self.c_sht.getHumChanged()

    def setTemChange(self, tem):
        return self.c_sht.setTemChange(tem)

    def setHumChange(self, hum):
        return self.c_sht.setHumChange(hum)

    def setPeriod(self, tim):
        return self.c_sht.setPeriod(tim)
