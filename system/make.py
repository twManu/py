#!/usr/bin/python

import re
from package import *


class v4l2(package):
	#relative to srcFullPath/usr/bin
	ubFile=('Debug/v4l2-tool', 'v4l2.py', 'miracast.png', 'webrtc.png')
	#file: path_relative_to_install_root
	copyDict={
		'atenDbus.conf' : '/etc/dbus-1/system.d'
	}
	# construct basic info especially path
	# In:
	#    srcPath - source path (dir), full or relative path to command path
	#              srcPath=command path if not provided 
	def __init__(self, srcPath='.'):
		super(v4l2, self).__init__(srcPath)
		if 'INSTALL_MOD_PATH' not in os.environ:
			print 'V4L2 environment might not be set correctly'
			sys.exit(-1)


	# do make
	# and whether to do installation or packing after that
	#
	def make(self, target=''):
		#clean then build
		if not super(v4l2, self).make(target, '', 'util', True):
			print 'Fail to build util'
			return False
		#clean then build
		if not super(v4l2, self).make(target, '', '.', True):
			print 'Fail to build v4l2'
			return False
		return True


	# do install with build result
	# In :
	#      path - full root path to install to
	#      default is environment INSTALL_MOD_PATH
	def install(self, rootPath=''):
		if not rootPath:	
			rootPath = os.environ['INSTALL_MOD_PATH']
		if not os.path.exists(rootPath):
			print 'Missing installation path'
			return False
		result = True
		for ff in self.ubFile:
			if not self.copy(self._srcFullPath+'/'+ff, rootPath+'/usr/bin'):
				result = False
		for ff in self.copyDict:
			if not self.copy(self._srcFullPath+'/'+ff, rootPath+self.copyDict[ff]):
				result = False
		return result
		

###
#main
#
if __name__ == '__main__':
	# Parse argument and make sure there is action to be taken
	# Ret : arg - parsed result
	def check_param():
		parser = argparse.ArgumentParser()
		parser.add_argument('-s', action='store', dest='srcPath', default='.',
			help='optional: source path (full or relative), current if not provided')
		parser.add_argument('-c', action='store_true', dest='doClean', default=False,
			help='make clean')
		parser.add_argument('-i', action='store_true', dest='doInstall', default=False,
			help='do install after make')
		parser.add_argument('-p', action='store_true', dest='doPacking', default=False,
			help='do packing after make')
		parser.add_argument('-q', action='store_true', dest='doQuery', default=False,
			help='do query or demo thing')
		arg=parser.parse_args()
		return arg

	arg = check_param()
	pkg = v4l2(arg.srcPath)
	if arg.doClean:
		if pkg.make('clean'):
			print 'Successfully making clean'
	elif arg.doQuery:
		pkg.info()
	else:
		if pkg.make(''):
			print 'Successfully making default target'
			if arg.doInstall:
				if pkg.install():
					print 'Successfully installed'

