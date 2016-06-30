#!/usr/bin/python
# "9600,8,N,1" no timeout

import serial
ser=serial.Serial('/dev/ttyUSB0')
print(ser.name)
ser.write(b'hello')
ser.close()

