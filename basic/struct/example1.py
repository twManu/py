from struct import *

myStruct = pack('hhl', 1, 2, 3)
arg1, arg2, arg3 = unpack('hhl', myStruct)
print str(arg1) + " " + str(arg2) + " " + str(arg3)
