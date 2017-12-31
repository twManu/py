#!/usr/bin/python
import os, sys, argparse, re

class cStruct():
	def __init__(self, path):
		if not os.path.exists(path):
			print 'Missing '+path
			return
		try:
			with open(path, 'r') as ff:
				self._parse(ff)
				#self._parse(ff, True)
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
	# Ret : indicator in type,
	#        I - int
	#        H - short
	#        B - char
	#        s - string
	def _getType(self, line):
		indicator = ''
		name = ''
		typeInPack = (
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
				for item in typeInPack:
					for tt in item[1]:
						if re.search(tt, type, re.I):
							indicator = item[0]
							if anArray:
								if indicator == 'B':
									#turn into string
									indicator = 's'
								indicator = str(anArray)+indicator
							break        #break for tt
					if indicator:      
						break                #break for item
		return indicator, name


	# do parsing
	def _parse(self, fd, verbose=False):
		inStruct = False
		pattern = ''
		index = 0
		varName = ''
		for line in fd:
			line = line.strip()
			if verbose:
				print line
			#remove comment in a line
			line = re.sub(r"//.*", '', line)
			line = re.sub(r"/\*[^\*]*\*/", '', line)
			if not line: continue
			# case in structure or not
			if inStruct:
				match = re.match(r"};$", line)
				if match:
					#out of struct
					inStruct = False
					if verbose:
						print 'out struct with '+line
					print pattern
					pattern = ''
					index = 0
				else:
					ii, nn = self._getType(line)
					if ii:
						pattern += ii
						print varName+str(index)+'_'+nn+' =', index
						index += 1
			else:
				#start of a struct
				#      struct name {
				# todo multi-line
				inStruct = re.search('struct ', line)
				if not inStruct:
					continue
				got, lastWord, resetLine = self._lastWord(line)
				if got:
					if lastWord == '{':
						got, lastWord, resetLine = self._lastWord(resetLine)
					varName = lastWord
					if verbose:
						print 'in struct with '+line
				else:
					inStruct = False
		if pattern:
			print pattern

#
# main
#
if len(sys.argv) < 2:
	print 'Please provide file name'
	sys.exit(-1)

obj = cStruct(sys.argv[1])
	