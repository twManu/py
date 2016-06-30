#!/usr/bin/python
# "38400,8,E,1" non blocking HW handshaking

import serial

with serial.Serial('/dev/ttyUSB0', 38400, timeout=0,
		parity=serial.PARITY_EVEN, rtscts=1) as ser:
	s = ser.read(100)              #read up to 100 bytes
	if s:
		print "got up to 100 bytes"
	else:
		print "got no data"
