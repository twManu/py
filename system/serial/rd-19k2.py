#!/usr/bin/python
# "19200,8,N,1" 1s timeout

import serial

with serial.Serial('/dev/ttyUSB0', 19200, timeout=1) as ser:
	x = ser.read()                 #read one byte
	print "got a byte"
	s = ser.read(10)               #read up to 10 bytes
	print "got up to 10 bytes"
	line = ser.readline()          #read a '\n' terminated line
	print "got a line: \""+line+"\""
