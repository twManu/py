#!/usr/bin/python
# coding=utf-8

import sys, struct, re

# each for an object
class field(object):
	#opened file with cur pos for this man
	#desc contains
	#   desc['f'] : tuple of each fieldName
	#   desc['t'] : tuple of type 'B', 'H', 'I', or signed version 'b', 'h', 'i'
	#               can be 5h
	#index and name are interpretted by parent
	def __init__(self, f, fieldDesc, index=0, name=''):
		self._field = {}
		self._desc = fieldDesc
		self._index = index
		self._name = name
		knownType = {
			  'b': 1
			, 'B': 1
			, 'h': 2
			, 'H': 2
			, 'i': 4
			, 'I': 4
		}
		if 'f' not in fieldDesc or 't' not in fieldDesc:
			print 'Missing descriptor'
			sys.exit(-1)
		#parsing type descriptor
		tList = []
		#single element gets char by literal
		if type(fieldDesc['t']) is str:
			n, t = self.checkType(fieldDesc['t'])
			for j in range(n):
				tList.append(t)
		else:
			for item in fieldDesc['t']:
				n, t = self.checkType(item)
				for j in range(n):
					tList.append(t)
		for i in range(len(tList)):
			tp = tList[i]
			fld = fieldDesc['f'][i]
			#print 'to read for', fld, knownType[tp], 'bytes'
			self._field[fld] = struct.unpack(tp, f.read(knownType[tp]))[0]
			#	raise NameError('unknown field type')


	# given 'B', return 1, 'B'
	# given '3B', return 3, 'B'
	def checkType(self, desc):
		match = re.match(r'(\d*)(\D+)', desc)
		if match.group(1):
			nr = int(match.group(1))
		else:
			nr = 1
		return nr, match.group(2)


	#given key, return value if valid
	#otherwise none returned
	def attr(self, key):
		if self._field.has_key(key):
			return self._field[key]
		return None


	#set value to key
	def set(self, key, value):
		if self._field.has_key(key):
			self._field[key] = value


	#reverse the unpack procedure
	def write(self, f):
		for ff in self._desc['fields']:
			f.write(struct.pack(self._desc[ff], self._field[ff]))


	def show(self):
		for key, value in self._field.iteritems():
			print key+': '+str(value)


	def setName(self, name):
		self._name = name


	def setIndex(self, index):
		self._index = index


	def name(self):
		return self._name


	def index(self):
		return self._index


#main
if __name__ == '__main__':
	import pipes, tempfile, struct
	fDesc = {
		'f': ('loyalty', 'mercy', 'courage'),
		't': ('B', '2B')
	}
	fDesc1 = {
		'f': ('loyalty', 'mercy', 'courage'),
		't': ('3B')
	}
	# Establish a very simple pipeline using stdio
	p = pipes.Template()
	#p.append('cat -', '--')
	#p.debug(True)

	# Establish an input file
	t = tempfile.NamedTemporaryFile(mode='w')
	t.write(struct.pack('3B', 1, 2, 3))
	t.write(struct.pack('3B', 3, 2, 1))
	t.flush()

	# Pass some text through the pipeline,
	# saving the output to a temporary file.
	f = p.open(t.name, 'r')
	obj = field(f, fDesc1)
	obj.show()

	obj = field(f, fDesc)
	obj.show()

