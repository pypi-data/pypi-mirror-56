cdef extern from "iarduino_I2C_SHT.cpp":
    pass

cdef extern from "iarduino_I2C_SHT.h":
    cdef cppclass iarduino_I2C_SHT:
        iarduino_I2C_SHT() except +
        iarduino_I2C_SHT(unsigned char) except +
        bint begin()
        bint changeAddress(unsigned char)
        bint reset()
        unsigned char getAddress()
        unsigned char getVersion()
        float getTem()
        float getHum()
        bint getTemChanged()
        bint getHumChanged()
        bint setTemChange(float)
        bint setHumChange(float)
        bint setPeriod(float)
