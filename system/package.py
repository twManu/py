#!/usr/bin/python
#environment required

import os, sys, argparse, datetime


class package(object):
	# construct basic info especially path
	# In:
	#    srcPath - source path (dir), full or relative path to command path
	#              srcPath=command path if not provided 
	def __init__(self, srcPath='.'):
		if not os.path.exists(srcPath):
			print 'Path', srcPath, 'not exists'
			self._srcFullPath = None
		else:
			self._srcFullPath = os.path.abspath(srcPath)
			self._srcParentPath, self._srcBaseName =\
				self.getDirAndBase(self._srcFullPath)
			self._cmdFullPath = os.path.abspath('.')
			self._cmdParentPath, self._cmdBaseName =\
				self.getDirAndBase(self._cmdFullPath)
		self._fromJenkins = False
		if 'JOB_NAME' in os.environ:
			self._fromJenkins = True


	def info(self):
		print self.YYMMDD()
		print 'From Jenkins', self._fromJenkins
		print 'Full package path', self._srcFullPath
		print 'Package parent path', self._srcParentPath
		print 'Base package name', self._srcBaseName
		print 'Full command path', self._cmdFullPath
		print 'Package parent path', self._cmdParentPath
		print 'Base command name', self._cmdBaseName


	#return MMDD string
	def MMDD(self):
		return datetime.datetime.today().strftime('%m%d')


	#return YYMMDD string
	def YYMMDD(self):
		return datetime.datetime.today().strftime('%y%m%d')


	#
	# Return dirname and base of a path, no dir check
	# ex.
	#     d, b = getDirAndPath('../abc')
	# In : path - must not a null
	#
	def getDirAndBase(self, path):
		if not path:
			return None, None
		else:
			abs = os.path.abspath(path)
			dir = os.path.dirname(abs)
			base = os.path.basename(abs)
			return dir, base


	# do the following
	# if workDir
	#     cd workDir; rm link; ln -s src link
	# otherwise
	#     rm link; ln -s src link
	# In: workDir - if provided, must be existing
	#            otherwise, current directory is applied
	#     link - name under workDir to be created
	#     dst - anything to be linked from workDir
	# Ret: True - successful
	#      False - failure
	def link(self, link, dst, workDir):
		cmd = ''
		if workDir:
			if os.path.exists(workDir):
				cmd = 'cd ' + workDir + ';'
			else:
				print 'Target directory does not exist'
				return False
		if not link:
			print 'Missing link name'
		elif not dst:
			print 'Missing link target'
		else:
			#param ok
			cmd += 'rm -f ' + link + ';'
			cmd += 'ln -s ' + dst + ' ' + link
			return 0 == os.system(cmd)
		#case no execution 
		return False


	# just do cp -a src dst
	# Ret: True - successful
	#      False - failure
	def copy(self, src, dst):
		if not src:
			print 'Missing copy source'
		elif not dst:
			print 'Missing copy destination'
		else:
			return 0 == os.system('cp -a ' + src + ' ' + dst)
		#case no execution 
		return False


	# just do rm -f src
	# Ret: True - successful
	#      False - failure
	def remove(self, src):
		if not src:
			print 'Missing remove target'
		else:
			return 0 == os.system('rm -rf ' + src)
		#case no execution 
		return False


	# expect source is in _srcFullPath
	# optionally make clean and then make target against mkfile
	# In :
	#       target - target name to build, null ok
	#       mkfile - can be empty, then Makefile is checked before makefile
	#       subdir - cd path (under _srcFullPath) before make
	#       doClean - make clean first
	# Ret: True - successful
	#      False - failure
	def make(self, target='', mkfile='', subdir='.', doClean=True):
		#check makefile existence
		#path will be full dir path of makefile
		d4Mk = ('Makefile', 'makefile')
		dirMkfile = self._srcFullPath + '/'
		if subdir != '.':
			dirMkfile += subdir + '/'
		if not mkfile:
			# use default makefile
			for mkfile in d4Mk:
				if os.path.exists(dirMkfile + '/' + mkfile):
					break
			if not mkfile:
				print 'No default makefile found'
				return False
		if not os.path.exists(dirMkfile+mkfile):
			print 'Missing make file ' + mkfile + ' in ' + dirMkfile
			return False
		#compose command
		cmd = 'cd ' + dirMkfile
		if doClean:
			cmd += '; make clean'
		cmd += '; make -f ' + mkfile + ' ' + target
		return 0 == os.system(cmd)


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
		parser.add_argument('-l', action='store_true', dest='doLink', default=False,
			help='link test, need a and option b assigned')
		parser.add_argument('-r', action='store_true', dest='doRemove', default=False,
			help='remove file/dir, need a assigned')
		parser.add_argument('-c', action='store_true', dest='doCopy', default=False,
			help='copy test, need a and option b assigned')
		parser.add_argument('-m', action='store_true', dest='doMake', default=False,
			help='make target, need a (target) and b (makefile) assigned')
		parser.add_argument('-a', action='store', dest='src', default='',
			help='specify source to copy from or link name to be created')
		parser.add_argument('-b', action='store', dest='dst', default='',
			help='specify destination to copy to or link destination to be pointed')
		arg=parser.parse_args()
		return arg

	arg = check_param()
	pkg = package(arg.srcPath)
	if arg.doLink:
		dir, lnk = pkg.getDirAndBase(os.path.abspath(arg.src))
		if pkg.link(lnk, arg.dst, dir):
			print 'link successfully'
	elif arg.doCopy:
		if pkg.copy(arg.src, arg.dst):
			print 'copy successfully'
	elif arg.doRemove:
		if pkg.remove(arg.src):
			print 'remove successfully'
	elif arg.doMake:
		if not arg.dst:
			if pkg.make(arg.src):
				print 'make successfully'
		else:
			if pkg.make(arg.src, arg.dst):
				print 'make successfully'
	else:
		pkg.info()

