#!/usr/bin/python
import os, sys, argparse, re

class cStruct():
	def __init__(self, path, verbose=0):
		self._inStruct = False
		self._inDefine = False
		self._index = 0                  #both struct and define use it
		self._varName = ''               #var of struct and also define prefix
		self._formatString = ''          #format string of struct
		self._verbose = verbose
		if not os.path.exists(path):
			print 'Missing '+path
			return
		try:
			with open(path, 'r') as ff:
				self._parse(ff)
		except:
			print "fail to open "+path


	# given a line, analyze last word and anything before
	# Ret : False, xx, xx - failure
	#       True, last, before - success
	def _lastWord(self, line):
		#print line
		line = line.strip()
		# remove ' '+anything in tail
		match = re.search(r'[ \t]([^ \t]+)$', line)
		if not match:
			return False, '', ''
		lw = match.group(1)
		line = re.sub(match.group(), '', line).strip()
		return True, lw, line


	# given a line in field statement
	# analysize it as var part and type part
	# say 'unsigned int a[32];' -> a[32] and unsigned int
	# Ret : (formatString, fieldName)
	#        I - int, fieldName
	#        H - short, fieldName
	#        B - char, fieldName
	#        s - string, fieldName
	#        fail - '', not defined
	def _getType(self, line):
		formatChar = ''
		name = ''
		formatCharByType = (
			  ('I', ('enum', 'int', 'u32', 's32'))
			, ('B', ('char', 'u8', 's8'))
			, ('H', ('short', 'u16', 's16'))
			
		)
		line = line.strip().strip(';')
		if line:
			#print line
			#two parts in variable and varType
			got, lastWord, resetLine = self._lastWord(line)
			if got:
				# remove variable part got type part
				type = resetLine.split()[0]
				var = lastWord
				#print type+' :'+var
				anArray = re.search(r'\[(\d+)\]', var)
				if anArray:
					var = var.split('[')[0]
					anArray = int(anArray.group(1))
				else:
					anArray = 0
				name = var
				#print var+'in type '+varType
				for fcItem in formatCharByType:
					for tt in fcItem[1]:
						if re.search(tt, type, re.I):
							formatChar = fcItem[0]
							if anArray:
								if formatChar == 'B':
									#turn into string
									formatChar = 's'
								formatChar = str(anArray)+formatChar
							return formatChar, name
			else:
				print line+' fails to be parsed as a variable'
		else:
			print line+' is empty and skipped'
		return formatChar, name


	# Check if a line starts with '#define'
	# In : line - stripped and comments none
	# Ret : '' - if not a start
	#       otherwise - the name global variable
	def _defStart(self, line):
		symbol = ''
		if not self._inDefine and re.match(r'#define', line, re.I):
			if self._verbose>=1:
				print 'defStart with '+line
			got, lastWord, resetLine = self._lastWord(line)
			if got:
				symbol = 'g_'+lastWord
				print symbol+' = {'
				self._structEnd('};')
				self._varName = lastWord
				self._inDefine = True
				self._index = 0
			else:
				print 'fail to parse define start '+line
		return symbol


	# Check if in define body whi
	# In : line - stripped and comments none
	# Ret: True - '=' found and is a define body
	#      NOTE: empty is True to in order to be ignored
	#      False - otherwise
	def _defBody(self, line):
		if self._inDefine:
			# case in define
			line = line.strip()
			if not line:             #skip empty
				return True
			# it must be 'a = b'
			if re.match(self._varName, line, re.I) and re.search('=', line):
				if self._verbose>=1:
					print 'defBody with '+line
				word0 = line.split('=')[0].strip()
				if self._index:
					print '\t, \''+word0+'\''+': '+word0
				else:
					print '\t  \''+word0+'\''+': '+word0
				return True
			self._defEnd()
		return False


	# Ends a definition
	def _defEnd(self):
		if self._inDefine:
			if self._verbose>=1:
				print 'defEnd'
			self._inDefine = False
			print '}'
			print


	# Check if a line contains 'struct '
	# In : line - stripped and comments none
	# Ret : True - if variable is parsed
	#       False - not a struct
	def _structStart(self, line):
		if not self._inStruct and re.search('struct ', line):
			got, lastWord, resetLine = self._lastWord(line)
			if got:
				if self._verbose>=1:
					print 'structStart with '+line
				if lastWord == '{':
					#drop trailing '{'
					got, lastWord, resetLine = self._lastWord(resetLine)
				self._defEnd()
				self._varName = lastWord
				self._inStruct = True
				self._index = 0
				self._formatString = ''
				return True
		return False


	# Check if ends a struct
	# In : line - stripped and comments none
	# Ret: True - yes
	#      otherwise - not
	# todo }; must be together
	def _structEnd(self, line):
		if self._inStruct and re.match(r"};$", line):
			if self._verbose>=1:
				print 'structEnd with '+line
			self._inStruct = False
			print self._varName+'_formatString =\''+self._formatString+'\''
			print
			return True
		return False


	# Check if a line 'type var'
	# In : line - stripped and comments none
	# Ret : True - if variable is parsed
	#       False - not a struct
	def _structBody(self, line):
		if self._inStruct:
			if self._verbose>=1:
				print 'structBody with '+line
			ii, nn = self._getType(line)
			if ii:
				self._formatString += ii
				print self._varName+str(self._index)+'_'+nn+' =', self._index
				self._index += 1
				return True
		return False


	# do parsing of
	# 1. struct
	# 2. #define XXX
	#
	def _parse(self, fd):
		for line in fd:
			if self._verbose>=2:
				print 'echo '+line
			line = line.strip()
			if not line:
				continue
			#remove comment in a line
			line = re.sub(r"//.*", '', line)
			line = re.sub(r"/\*[^\*]*\*/", '', line)
			line = line.strip()
			if not line:
				continue
			elif self._defStart(line):
				continue
			elif self._defBody(line):
				continue
			else:
				self._defEnd()
				if self._structStart(line):
					continue
				elif self._structEnd(line):
					continue
				else:
					self._structBody(line)
		self._defEnd()
		self._structEnd('};')


#
# main
#
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Please provide file name'
		sys.exit(-1)
	elif len(sys.argv) == 2:
		level = 0
	else:
		level = int(sys.argv[2])
	obj = cStruct(sys.argv[1], level)
	