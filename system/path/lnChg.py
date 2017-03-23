#!/usr/bin/python

import os, sys, subprocess, re, argparse, glob


# Parse argument and make sure there is action to be taken
# Ret : arg - parsed result
def check_param():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', action='store', dest='linkName', default='',
		help='name of link to create/modify, the directory is provided as well')
	parser.add_argument('-s', action='store', dest='srcName', default='',
		help='name of source to link to')
	parser.add_argument('-f', action='store_true', dest='force', default=False,
		help='force action')

	arg=parser.parse_args()
	if not arg.srcName:
		print 'Missing source name !!!'	
		parser.print_help()
		sys.exit()

	#get full name of link
	if not arg.linkName:
		print 'Missing link name !!!'	
		parser.print_help()
		sys.exit(1)
	else:
		arg.linkName=os.path.abspath(arg.linkName)

	return arg

#
# main
#
arg=check_param()
dirName=os.path.dirname(arg.linkName)
linkName=os.path.basename(arg.linkName)
if not os.path.exists(arg.srcName):
	if not os.path.exists(dirName+'/'+arg.srcName):
		print 'Source file '+arg.srcName+' does not exist !!!'
		sys.exit()
if os.path.islink(arg.linkName):
	print 'to modify '+linkName+' under '+dirName+' as '+arg.srcName
	os.system('cd '+dirName+';rm '+linkName+';ln -s '+arg.srcName+' '+linkName)
elif os.path.isfile(arg.linkName):
	print 'to delete '+linkName+' under '+dirName+' and link it as '+arg.srcName
	if not arg.force:
		print 'to ask...todo'
		sys.exit(0)
elif os.path.isdir(arg.linkName):
	print 'to remove directory '+linkName+' under '+dirName+' and link file as '+arg.srcName
	if not arg.force:
		print 'to ask...todo'
		sys.exit(0)
else:
	print 'to create link '+linkName+' under '+dirName+' to '+arg.srcName
