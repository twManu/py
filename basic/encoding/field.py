#!/usr/bin/python
# coding=utf-8

import sys, struct

# each for an object
class field(object):
	#opened file with cur pos for this man
	#desc contains
	#   desc['fields'] : tuple of each fieldName
	#   desc[<fieldName>] : unpack parameter 'B', 'H', 'I', or signed version 'b', 'h', 'i'
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
		for ff in fieldDesc['fields']:
			if fieldDesc[ff] in knownType:
				print 'to read for', ff, knownType[fieldDesc[ff]], 'bytes'
				self._field[ff] = struct.unpack(fieldDesc[ff],\
					f.read(knownType[fieldDesc[ff]]))[0]
			else:
				raise NameError('unknown field type')


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
'''
	doesn't work w/ Windows
		'fields': ('忠義', '仁愛', '勇氣'),
		'忠義': 'B',
		'仁愛': 'B',
		'勇氣': 'B'
'''
	fDesc = {
		'fields': ('loyalty', 'mercy', 'courage'),
		'loyalty': 'B',
		'mercy': 'B',
		'courage': 'B'
	} 
	with open('test', "rb") as f:
		#pop offset 16 and '年紀', '國家', '地區', '體力', '體力上限'
		f.read(16+5)
		obj = field(f, fDesc)
		obj.show()

