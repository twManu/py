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

"""
	"秦明": (79, 78, 90),     
	"宋江": (81, 100, 62),     
	"史進": (74, 69, 95),      
	"吳用": (86, 70, 58),      
	"晁蓋": (96, 68, 76),     
	"楊志": (97, 58, 79),   
	"武松": (68, 55, 98),    
	"清": (72, 66, 83),      
	"董平": (82, 51, 73),      
	"孫立": (54, 68, 72),      
	"索超": (62, 41, 89),      
	"朱同": (59, 72, 53),      
	"李云": (42, 73, 54),      
	"王煥": (77, 41, 50),      
	"朱武": (72, 50, 44),      
	"徐寧": (54, 53, 58),      
	"王英": (45, 31, 69),      
	"周通": (62, 31, 41),      
	"劉唐": (35, 27, 71),      
	"鄧飛": (32, 29, 59),      
	"黃安": (70, 35, 53),      
	"蘇定": (40, 32, 64),      
	"蔡京": (84, 29, 20),      
	"楊春": (32, 37, 61),      
	"陳達": (53, 25, 36),      
	"李吉": (29, 20, 23),      
	"王倫": (53, 36, 62),      
	"朱貴": (76, 42, 22),      
	"杜遷": (46, 27, 29),      
	"宋萬": (34, 25, 28),      
	"鄧龍": (24, 10, 26),      
	"李鬼": (17, 14, 28),      
	"薛永": (38, 52, 43),      
	"高濂": (67, 46, 82),      
	"雷橫": (83, 32, 55),      
	"黃信": (59, 43, 80),
	"裴宣": (45, 68, 49),      
	"楊雄": (41, 64, 56),      
	"龔旺": (40, 39, 48),      
	"鮑旭": (31, 28, 50),      
	"河濤": (44, 18, 38),      
	"劉高": (35, 12, 10),      
	"張保": (18, 16, 29),      
	"淩振": (40, 52, 29),      
	"楊林": (46, 29, 38),      
	"丘岳": (75, 39, 61),      
	"燕青": (90, 54, 65),      
	"杜微": (48, 34, 76),      
	"王進": (79, 91, 73),      
	"瓊英": (92, 73, 77),
	" ": (39, 42, 57),
	"燕 " : (46, 41, 60),
	"魯智深": (63, 74, 88),
	"盧俊義": (68, 63, 81),
	"時文彬": (44, 60, 27),
	"阮小七": (50, 42, 38),      
	"宿元景": (73, 94, 40),      
	"單廷珪": (71, 54, 50),
	"張蒙方": (24, 20, 42),
	"張叔夜": (60, 79, 42),     
	"魏定國": (52, 73, 51),      
	"牛邦喜": (50, 33, 36),      
	"張世開": (35, 26, 27),      
	"王定六": (20, 38, 23),      
	"張文遠": (16, 43, 20),      
	"西門慶": (14, 32, 25),      
	"郝思文": (45, 32, 36),
	"鈕文忠": (84, 29, 56),      
	"史文恭": (60, 33, 82),      
	"蕭嘉穗": (87, 70, 73),      
	"潘巧雲": (10, 22, 10),      
	"季三思": (42, 28, 51),      
	"崔道成": (25, 20, 57),      
	"丘小乙": (19, 12, 40),
	"許貫忠": (75, 88, 79)      
}


g_leader = ("林沖", "宋江", "史進", "晁蓋", "楊志", "魯智深", "武松")
"""

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
		super(bandit, self).__init__(f, self.FIELD_DESC, index, name)


# take care of file
class san5Parser(object):
	OFFSET_BANDIT = 0x1abe
	BANDIT_COUNT = 300
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


	def update(self):
		with open(self._fname, "r+b") as f:
			f.seek(self.OFFSET_BANDIT, 0)
			for hh in self._banditList:
				hh.write(f)


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
		print obj.index(), ', country=', obj.attr('country'), ', state=', obj.attr('state')
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
				obj.set('soldiar', 20000)
				obj.set('skill', 0xffffffff)
			elif obj.attr('strength') >= 90:
				obj.set('soldiar', 20000)
				obj.set('skill', 0xffffffff)
			elif obj.attr('strength') >= 80:
				obj.set('soldiar', 8000)
			else:
				obj.set('soldiar', 0)
			#set training only if soldiar
			if obj.attr('soldiar'):
				obj.set('training', 100)
				obj.set('moral', 100)
			else:
				obj.set('training', 0)
				obj.set('moral', 0)
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
	elif arg.showCountry:
		sP.showCountry(int(arg.showCountry), int(arg.level))
	elif arg.state:
		sP.showState(arg.state, int(arg.level))
	elif arg.index:
		sP.showPeople(arg.index, int(arg.level))
	else:
		sP.showPeople([], int(arg.level))
