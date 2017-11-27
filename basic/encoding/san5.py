#!/usr/bin/python
# coding=utf-8

import sys, struct, argparse
from struct import *
from field import *

g_savefile = "/home/manuchen/.dosbox/san5/SAVEDATA.S5P"

#name : (strength, charm)
g_bandit = {
	"關": (99, 96),      
	"張": (99, 44),
	"劉": (79, 99),
	"張文遠": (95, 85)
}

# each for a man
class bandit(field):
	BANDIT_SIZE = 31
	#bit 2 (4) is done
	FIELD_DESC = {
		'fields': ('n-4', 'n-3', 'n-2', 'n-1'
			, 'proies', 'experience'
			, 'soldiar', 'life-assume', 'done'
			, 'strength', 'wisdom', 'politic', 'charm'
			, 'training', 'moral', 'title', 'royalty'
			, 'state', 'country', 'n4', 'n5'
			, 'n6', 'n7', 'n8', 'skill'),
		'n-4': 'B',
		'n-3': 'B',
		'n-2': 'B',
		'n-1': 'B',
		'proies': 'H',
		'experience': 'H',
		'soldiar': 'H',
		'life-assume': 'B',
		'done': 'B',
		'strength': 'B',
		'wisdom': 'B',
		'politic': 'B',
		'charm': 'B',
		'training': 'B',
		'moral': 'B',
		'title': 'B',
		'royalty': 'B',
		'state': 'B',
		'country': 'B',
		'n4': 'B',
		'n5': 'B',
		'n6': 'B',
		'n7': 'B',
		'n8': 'B',
		'skill': 'I'
	}

	#opened file with cur pos for this man
	#exclusive 1-based index assigned and name for display
	def __init__(self, f, index, name=''):
		self._misc = None
		super(bandit, self).__init__(f, self.FIELD_DESC, index, name)


class misc(field):
	FIELD_DESC = {
		'fields': ('body', 'n1', 'n2', 'n3'
			, 'n4', 'n5', 'n6', 'n7'
			, 'n8', 'n9', 'n10', 'n11'
			, 'n12', 'n13', 'n14', 'n15'
			, 'n16', 'n17'),
		'body': 'B',
		'n1': 'B',
		'n2': 'B',
		'n3': 'B',
		'n4': 'B',
		'n5': 'B',
		'n6': 'B',
		'n7': 'B',
		'n8': 'B',
		'n9': 'B',
		'n10': 'B',
		'n11': 'B',
		'n12': 'B',
		'n13': 'B',
		'n14': 'B',
		'n15': 'B',
		'n16': 'B',
		'n17': 'B'
	}

	def __init__(self, f, index, name=''):
		super(misc, self).__init__(f, self.FIELD_DESC, index, name)


# take care of file
class san5Parser(object):
	OFFSET_BANDIT = 0x1abe
	OFFSET_MISC = 0x8690
	BANDIT_COUNT = 300
	MAX_SOLDIAR = 20000
	def __init__(self, fname, count=BANDIT_COUNT):
		#if leader specified, remember country
		self._fname = fname
		self.BANDIT_COUNT = count
		#data base
		self._banditList = []        #list of object
		self._banditByCountry = {}   #dict of object list by country
		self._banditByState = {}     #dict of object list by state
		self._stateList = []         #list of object
		with open(fname, "rb") as f:
			f.seek(self.OFFSET_BANDIT, 0)
			for i in range(self.BANDIT_COUNT):
				obj = bandit(f, i+1)
				if not self._insertPerson(obj):
					self.BANDIT_COUNT = i
					break
			f.seek(self.OFFSET_MISC, 0)
			for i in range(self.BANDIT_COUNT):
				obj = misc(f, i+1)
				self._banditList[i]._misc = obj


	def update(self):
		with open(self._fname, "r+b") as f:
			f.seek(self.OFFSET_BANDIT, 0)
			for hh in self._banditList:
				hh.write(f)
			f.seek(self.OFFSET_MISC, 0)
			for hh in self._banditList:
				hh._misc.write(f)


	# insert into database
	# Ret : obj - object inserted
	#       None - fail to insert owning to invalid value
	def _insertPerson(self, obj):
		# determine by valid 'strength'
		if not obj.attr('strength'):
			return None
		self._banditList.append(obj)
		country, state = obj.attr('country'), obj.attr('state')
		#create list if not present
		if not country in self._banditByCountry:
			self._banditByCountry[country] = []
		self._banditByCountry[country].append(obj)
		#create list if not present
		if not state in self._banditByState:
			self._banditByState[state] = []
		self._banditByState[state].append(obj)
		# check known characters
		for name in g_bandit:
			if g_bandit[name][0] == obj.attr('strength') and\
			   g_bandit[name][1] == obj.attr('charm'):
				obj.setName(name)
		return obj

	# In : broList - list of 1-based index (character) to add to country
	#
	def moveBrother2Country(self, broList, country):
		if not country in self._banditByCountry:
			print 'Invalid country'
			return
		toState = 0
		for man in self._banditByCountry[country]:
			toState = man.attr('state')
			break
		if not toState:
			print 'Fail to get the state of the first object'
			return
		for bro in broList:
			print 'modifying people['+bro+'] to state '+str(toState)
			indexInList = int(bro) - 1
			if indexInList >= len(self._banditList):
				print 'Invalid index '+bro+' ...skipped !!!'
				continue
			self._banditList[indexInList].set('country', country)
			self._banditList[indexInList].set('state', toState)
		self.update()


	# In : peopleList - 1-based list. if provided, show the man (str) in the list
	#               otherwise, show all
	def showPeople(self, peopleList, level=0):
		if not peopleList:
			peopleList = range(1, len(self._banditList)+1)
		for man in peopleList:
			indexInList = int(man) - 1
			if indexInList >= len(self._banditList):
				print 'Invalid index '+man+' ...skipped !!!'
				continue
			self._showPerson(self._banditList[indexInList], level)


	# show info by level
	# level 0 with minimal info
	def _showPerson(self, obj, level=0):
		name = obj.name()
		if name:
			print '*****'+name,
		else:
			print '******** no',
		print obj.index(), ', country=', obj.attr('country'), ', state=', obj.attr('state'),
		print ', body=', obj._misc.attr('body')
		print obj.attr('strength'),
		print obj.attr('wisdom'),
		print obj.attr('politic'),
		print obj.attr('charm'),
		if level >= 1:
			print 'skill=', format(obj.attr('skill'), '#010x')
			print 'soldiar= ', obj.attr('soldiar'), ', training= ', obj.attr('training'), ', moral= ', obj.attr('moral'),
			if 0x04 & obj.attr('done'): print 'done'
			else: print 'yet'
			print 'proies= ', obj.attr('proies'), ', experience= ', obj.attr('experience'), ', royalty= ', obj.attr('royalty')
		else:
			print


	#country is single int
	def showCountry(self, country, level=0):
		if country in self._banditByCountry:
			print 'There are', len(self._banditByCountry[country]), 'people in country', country
			for obj in self._banditByCountry[country]:
				self._showPerson(obj, level)

	#country is single int
	def modifyCountry(self, country):
		if country in self._banditByCountry:
			print 'There are', len(self._banditByCountry[country]), 'people in country', country
			#construct the list
			theList = []
			for obj in  self._banditByCountry[country]:
				theList.append(obj.index())
			self._refillPerson(theList)
			#todo save
			self.update()
			#self.showCountry(country, 1)

	# stateList is list in state in string
	def showState(self, stateList, level=0):
		for state in stateList:
			state = int(state)
			if state in self._banditByState:
				print 'There are', len(self._banditByState[state]), 'people in state', state
				for obj in self._banditByState[state]:
					self._showPerson(obj, level)
		

	# peopleList is a list of people in str
	def _refillPerson(self, peopleList):
		for man in peopleList:
			indexInList = int(man) - 1
			if indexInList >= len(self._banditList):
				print 'Invalid index '+man+' ...skipped !!!'
				continue
			obj = self._banditList[indexInList]
			#print "manutest", obj.index(), obj.attr('royalty')
			#skip man in the field
			if obj.attr('royalty') < 60:
				continue
			if obj.attr('wisdom') >= 90 and obj.attr('politic') >= 80:
				obj.set('soldiar', self.MAX_SOLDIAR)
			elif obj.attr('strength') >= 90:
				obj.set('soldiar', self.MAX_SOLDIAR)
			elif obj.attr('strength')+obj.attr('wisdom') >= 160:
				obj.set('soldiar', self.MAX_SOLDIAR)
			elif obj.attr('strength') >= 80:
				obj.set('soldiar', 8000)
			elif obj.attr('strength')+obj.attr('wisdom') >= 150:
				obj.set('soldiar', 8000)
			else:
				obj.set('soldiar', 0)
			#set training only if soldiar
			if obj.attr('soldiar'):
				if obj.attr('soldiar') == self.MAX_SOLDIAR:
					obj.set('skill', 0xffffffff)
				obj.set('training', 100)
				obj.set('moral', 100)
			else:
				obj.set('training', 0)
				obj.set('moral', 0)
			obj._misc.set('body', 100)
			obj.set('done', 0)
			obj.set('royalty', 100)


# Parse argument and make sure there is action to be taken
# Ret : arg - parsed result
def chk_param():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', action='store', dest='file', default=g_savefile,
		help='save file, default is '+g_savefile)
	parser.add_argument('-l', action='store', dest='leader', default=0,
		help='specify leader by 1-based index')
	parser.add_argument('-b', action='append', dest='brother', default=[],
		help='specify brother (multiple times) by 1-based index')
	parser.add_argument('-s', action='append', dest='state', default=[],
		help='specify state (multiple times) by 1-based index')
	parser.add_argument('-S', action='append', dest='stateRange', default=[],
		help='specify "stateA stateB" (multiple times) by 1-based index')
	parser.add_argument('-q', action='store', dest='query', default='shc',
		help='s (state), c (citizen), or h (hero), default sh (both)')
	parser.add_argument('-i', action='append', dest='index', default=[],
		help='index of object to query')
	parser.add_argument('-v', action='store', dest='level', default=0,
		help='verbose level, 0, 1 or 2')
	parser.add_argument('-m', action='store', dest='match', default='',
		help='match justice mercy courage 3 at a time, say -m 39 42 57')
	parser.add_argument('-r', action='store', dest='people', default=san5Parser.BANDIT_COUNT,
		help='number of people to load')
	parser.add_argument('-c', action='store', dest='showCountry', default=0,
		help='show people match given country')
	parser.add_argument('-C', action='store', dest='modifyCountry', default=0,
		help='modify people match given country')
	arg=parser.parse_args()
	return arg


#main
if __name__ == '__main__':
	arg = chk_param()
	sP = san5Parser(arg.file, int(arg.people))
	if arg.modifyCountry:
		sP.modifyCountry(int(arg.modifyCountry) )
	elif arg.brother and arg.leader:
		sP.moveBrother2Country(arg.brother, int(arg.leader))
	elif arg.showCountry:
		sP.showCountry(int(arg.showCountry), int(arg.level))
	elif arg.state:
		sP.showState(arg.state, int(arg.level))
	elif arg.index:
		sP.showPeople(arg.index, int(arg.level))
	else:
		sP.showPeople([], int(arg.level))
