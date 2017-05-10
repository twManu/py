#!/usr/bin/python

import sys, os

FNAME='modify.py'

if not os.path.exists:
	print "Missing "+FNAME
	sys.exit(1)

fname = '/tmp/'+FNAME
os.system("cp "+FNAME+' '+fname)
with open(fname, "r+b") as f:
	f.seek(2, 0)
	f.write('A')

print 'diff of two:'
os.system('diff '+FNAME+' '+fname)
	
