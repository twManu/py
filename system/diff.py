#!/usr/bin/python
#

import os, sys, re, argparse, glob
#sys.path.append("path")
sys.path.append("./path")
sys.path.append("../basic")
from libPath import cPath


class cDiff(cPath):
	# myPath is source that other might link to
	def __init__(self, myPath, otherPath, debug=False):
		super(cDiff, self).__init__(myPath, False)
		self._otherPathObj=None
		self._linkAppend=""
		self._debug=debug
		if self._pathName:
			#self._subFiles=self.getSubFiles()
			self._otherPathObj=cPath(otherPath)
			if self._otherPathObj:
				self._otherPathName=self._otherPathObj.getPath()
				if not self._otherPathName:
					self._otherPathObj=None
				else:
					self._findLinkAppend()

	def _debug(self, msg=""):
		if self._debug: print msg
			
	# call after both path are valid
	# Out : _linkAppend updated
	def _findLinkAppend(self):
		if self._linkAppend:
			return
		tmp1=self._pathName
		tmp2=self._otherPathObj.getPath()
		print "Checking "+tmp1+" against "+tmp2
		while not re.match(tmp2, tmp1):
			tmp2=os.path.dirname(tmp2)
			if tmp2 == "/":
				print "  Match at root"
				break
			self._linkAppend += "../"
		self._linkAppend += os.path.basename(self._pathName)
		self._DBG("append set as: "+self._linkAppend)
			
	def getLinkAppend(self):
		return self._linkAppend


	def _findSo1(self):
		totalSize=0
		oPath=self._otherPathObj.getPath()
		for ff in self.getSubFiles():
			self._DBG("")
			fname1=self._pathName+ff
			self._DBG(fname1, False)
			if not os.path.isfile(fname1): continue
			self._DBG(' a file', False)
			fsize=os.path.getsize(fname1)
			if fsize < 4000: continue
			self._DBG(' large size', False)
			fname2=oPath+ff
			if os.path.isfile(fname2):
				self._DBG(' other', False)
				if os.path.getsize(fname2) >=4000:
					totalSize += fsize
					self._DBG(fsize)
					#print "ln -s "+self._linkAppend+ff+
		self._DBG("")
		self._DBG(totalSize)

	#find both presenst, both size>4000, then link to src
	def _findSo3(self):
		totalSize=0
		oPath=self._otherPathObj.getPath()
		#find from src dir
		for dirPath, dirNames, fileNames in os.walk(self._pathName):
			subPath=re.sub(self._pathName, "", dirPath)
			#/var/lib -> var/lib
			nSubPath=re.sub(r'^/', "", subPath)
			#add prepend owning to subpath
			words=subPath.split('/')
			prepend=""
			for section in subPath.split('/'):
				if section.strip(): prepend += "../"
			prepend += self._linkAppend+subPath
			#so in src subdir
			for soFile in glob.glob(self._pathName+subPath+'/*.so*'):
				if os.path.islink(soFile): continue
				if os.path.isdir(soFile): continue
				srcSize = os.path.getsize(soFile)
				base=os.path.basename(soFile)
				tgtPath=oPath+subPath+'/'+os.path.basename(soFile)       #other file
				if os.path.isfile(tgtPath):
					tgtSize = os.path.getsize(tgtPath)
					if tgtSize != srcSize:
						self._DBG("Size mismatch")
					else:
						os.system("rm -f "+tgtPath)
						cmd = "cd "+oPath+subPath+"; ln -s "+prepend+"/"+base+" "+base
						os.system(cmd)
						self._DBG("pushd "+oPath+subPath)
						self._DBG("ln -s "+prepend+"/"+base+" "+base)
						totalSize += tgtSize
				else:
					self._DBG("Missing target "+tgtPath)
		self._DBG(str(totalSize))


	#find both presenst, both size>4000, then link to src
	def _findSo2(self):
		totalSize=0
		oPath=self._otherPathObj.getPath()
		#find from src dir
		for dirPath, dirNames, fileNames in os.walk(self._pathName):
			subPath=re.sub(self._pathName, "", dirPath)
			#/var/lib -> var/lib
			nSubPath=re.sub(r'^/', "", subPath)
			#add prepend owning to subpath
			words=subPath.split('/')
			prepend=""
			for section in subPath.split('/'):
				if section.strip(): prepend += "../"
			prepend += self._linkAppend+subPath
			for ff in fileNames:
				fpath=oPath+subPath+'/'+ff                 #other file
				if os.path.islink(fpath): continue
				if os.path.isfile(fpath):
					fsize = os.path.getsize(fpath)
					if fsize < 4000: continue
					os.system("rm -f "+fpath)
					cmd = "cd "+oPath+subPath+"; ln -s "+prepend+"/"+ff+" "+ff
					os.system(cmd)
					self._DBG("pushd "+oPath+subPath)
					self._DBG("ln -s "+prepend+"/"+ff+" "+ff)
					totalSize += fsize
		self._DBG(str(totalSize))

	def _findSo(self, subPath):
		oPath=self._otherPathObj.getPath()
		nSubPath=re.sub(r'^/', "", subPath)
		totalSize=0
		for ff in glob.glob(self._pathName+subPath+'/*.so*'):
			if os.path.islink(ff): continue
			if os.path.isdir(ff): continue
			fsize=os.path.getsize(ff)
			if fsize < 4000: continue
			base=os.path.basename(ff)
			if os.path.exists(oPath+subPath+'/'+base):
				totalSize += fsize
				print 'ln -s '+self._linkAppend+nSubPath+'/'+base,
				print '      size= '+str(fsize)
		print 'Total size = '+str(totalSize)

	#Return path object of the other path
	def getOtherObj(self):
		return self._otherPathObj

# main
#
if __name__ == '__main__':
	dir1=cPath("~/work/aphsdk/targetNFS")
	dir2=cPath("~/work/aphsdk/linux-devkit/sysroots/cortexa15hf-neon-linux-gnueabi")
	chkPath=("/usr/lib", "/lib")
	if not dir1.getPath() or not dir2.getPath():
		print "Invalid path ... program exits"
		system.exit(1)
	obj=cDiff(dir1.getPath(), dir2.getPath())
	obj._findSo3()
