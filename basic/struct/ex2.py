#!/usr/bin/python
import os, sys, argparse, re, struct

val = bytearray(12)
struct.pack_into('BB', val, 2, 2, 3)
struct.pack_into('BB', val, 0, 0, 1)
for i in range(4):
	print struct.unpack_from('B', val, i)


	
