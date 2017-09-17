#!/usr/bin/python

import sys, os
import numpy as np
from math import*

Fs=8000
f=500
sample=16
a=[0]*sample
for n in range(sample):
    a[n]=sin(2*pi*f*n/Fs)

print a
'''
if __name__ == '__main__':
	if len(sys.argv)<2:
		print '  Invalid argument.'
		print '  Usage:', sys.argv[0], 'FILENAME',
	sys.argv[1]
'''
