#!/usr/bin/python

import sys

if sys.version_info >= (3,0):
	name = input('What is your name?\n')
	print("Hi, %s." % (name))


#enter below is ok with windows python 3
#manu
#enter below instead with linux python 2.7, otherwise raw_input
#"manu:

raw_name = raw_input('What is your name?\n')
print("Hi, %s." % raw_name)
