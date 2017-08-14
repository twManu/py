#!/usr/bin/python

import os, sys, re, argparse, glob, commands, struct


#main
if __name__ == '__main__':
	# supported sum size
	validSum = ('1', '2', '4')
	# type char for supported sum size
	sumDict = {
		  '1': 'B'
		, '2': 'H'
		, '4': 'I'
	}
	def check_param():
		defaultSumIndex = 0               #default check sume size (index into validSum)
		#
		# build message
		msg = ""
		for i in range(len(validSum)):
			if i != len(validSum)-1:
				# not the last, need ',' trailing
				msg += validSum[i] + ' '
				if i == defaultSumIndex:
					msg += '(default)'
				msg += ', '
			else:
				msg += 'or '
				msg += validSum[i] + ' byte sum'

        	parser = argparse.ArgumentParser()
	        parser.add_argument('-f', action='store', dest='input_file_name', default=None,
        	        help='full path file name')
		parser.add_argument('-s', action='store', dest='size_of_sum', default=validSum[defaultSumIndex],
        	        help=msg)
	        arg=parser.parse_args()
		# look up type char
		arg.typeChar = None
		if not arg.size_of_sum in validSum:
			print 'Size of check sum '+arg.size_of_sum+' not supported'
			sys.exit(1)
		else:
			arg.typeChar = sumDict[arg.size_of_sum]
			arg.size_of_sum = int(arg.size_of_sum)
		# check file name
		if not arg.input_file_name:
			print 'Missing input file '
			sys.exit(1)
		elif not os.path.exists(arg.input_file_name):
			print 'Invalid input file '+arg.input_file_name+' not supported'
			sys.exit(1)
        	return arg

	arg=check_param()
	if not arg.typeChar:
		sys.exit(1)
	sum = 0
	with open(arg.input_file_name, "rb") as f:
		#check size
		f.seek(0, os.SEEK_END)
		fsize = f.tell()
		f.seek(0, os.SEEK_SET)
		print ' size of '+arg.input_file_name+' is '+str(fsize)
		while fsize:
			if fsize >= arg.size_of_sum:
				sum += struct.unpack(arg.typeChar, f.read(arg.size_of_sum))[0]
				fsize -= arg.size_of_sum
			else:
				if fsize >= 2:
					sum += struct.unpack('H', f.read(2))[0]
					fsize -= 2
				if fsize:
					sum += struct.unpack('B', f.read(1))[0]
					fsize = 0
	if 1 == arg.size_of_sum:
		sum &= 0xff
		print('sum = 0x%2X'% (sum))
	elif 2 == arg.size_of_sum:
		sum &= 0xffff
		print('sum = 0x%4X'% (sum))
	else:
		sum &= 0xffffffff
		print('sum = 0x%8X'% (sum))
