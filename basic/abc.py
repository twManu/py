#!/usr/bin/python

import argparse, sys

def param():
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', action='store', dest='acnt',
		help='array size')
	parser.add_argument('-l', action='store', dest='length',
		help='dma langth')
	arg = parser.parse_args()
	return arg

#
# main
#
arg=param()
found = 0
length = int(arg.length)
acnt = int(arg.acnt)
bc = length/acnt
for order in range(15):
	bcnt = (1<<(15-order))
	ccnt = bc/bcnt
	if (ccnt * bcnt)==bc:
		print str(ccnt)+' * '+str(bcnt)+' = '+str(bc)
		found = 1
		break
	else:
		print str(ccnt)+' * '+str(bcnt)+' != '+str(bc)

if found:
	if length!=acnt*bcnt*ccnt:
		print "something wrong"
		sys.exit(1)
	#acnt*bcnt by default
	#try to let ccnt smaller
	if bcnt<ccnt and acnt*ccnt<65536:
		#swap
		tmp = bcnt
		bcnt = ccnt
		ccnt = tmp
	#try optimize ccnt
	for i in range(3):
		ccnt1 = ccnt/5
		if ccnt==ccnt1*5:
			print 'try optimizing ccnt with 5',
			bcnt1 = bcnt*5
			if bcnt1*acnt<65536:
				print 'ok'
				bcnt = bcnt1
				ccnt = ccnt1
	print 'axbxc =',
	print acnt,
	print bcnt,
	print ccnt

