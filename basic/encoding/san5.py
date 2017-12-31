#!/usr/bin/python
# coding=utf-8

import sys, struct, argparse, os
from struct import *
from field import *

g_savefile = [
	  "/home/manuchen/.dosbox/san5/SAVEDATA.S5P"
	, "C:\Users\User\Documents\san5\SAN5\SAVEDATA.S5P"
]

#name : (武力, 魅力, 政治)
g_bandit = {
	"呂布": (100, 67, 9),
	"關羽": (99, 96, 64),      
	"張飛": (99, 44, 17),
	"趙雲": (98, 95, 80),
	"許褚": (98, 82, 21),
	"馬超": (98, 82, 32),
	"典韋": (98, 57, 17),
	"黃忠": (97, 86, 68),
	"文醜": (97, 67, 12),
	"龐德": (97, 72, 41),
	"甘寧": (96, 71, 34),
	"太史慈": (96, 72, 39),
	"顏良": (95, 53, 21),
	"張遼": (95, 85, 68),
	"孫策": (95, 97, 62),
	"孫堅": (94, 93, 90),
	"魏延": (94, 56, 37),
	"夏侯惇": (94, 87, 81),
	"周泰": (94, 70, 51),
	"姜維": (93, 87, 81),	
	"徐晃": (93, 63, 57),
	"張郃": (93, 69, 54),
	"管亥": (93, 47, 23),
	"孟獲": (92, 67, 19),
	"沙摩柯": (92, 46, 13),
	"曹彰": (92, 79, 24),
	"夏侯淵": (91, 82, 43),
	"馬騰": (91, 88, 49),
	"華雄": (90, 41, 26),
	"曹操": (87, 98, 97),
	"呂蒙": (85, 84, 80),
	"孫權": (82, 96, 79),
	"陸遜": (79, 94, 87),
	"劉備": (79, 99, 77),
	"周瑜": (78, 96, 87),
	"徐庶": (68, 85, 86),
	"司馬懿": (67, 79, 91),
	"魯肅": (61, 90, 93),
	"諸葛亮": (60, 97, 96),
	"龐統": (56, 85, 86),
	"鄧艾": (87, 75, 88)
}

#0 based tuple
g_state = (
	'dummy',
	'襄平',
	'北平',
	'代縣',
	'晉陽',
	'南皮',
	'平原',
	'鄴',
	'北海',
	'濮陽',
	'陳留',
	'洛陽',
	'弘農',
	'長安',
	'安定',
	'天水',
	'西涼',
	'下邳',
	'徐州',
	'許昌',
	'譙',
	'汝南',
	'宛',
	'新野',
	'襄陽',
	'上庸',
	'江夏',
	'江陵',
	'武陵',
	'長沙',
	'桂陽',
	'零陵',
	'夀春',
	'建業',
	'吳',
	'會稽',
	'盧江',
	'豫章',
	'漢中',
	'下弁',
	'梓潼',
	'成都',
	'永安',
	'江州',
	'建寧',
	'雲南',
	'盧陵',
	'鄱陽'
)


class state(field):
	STATE_SIZE= 30
	FIELD_DESC = {
		'fields': (
			'預備兵', 'n-10'
			, 'n-9', 'n-8', 'n-7', 'n-6'
			, 'n-5', 'n-4', 'n-3', '人口'
			, '城防', '災害', 'n1', '開發', '商業'
			, 'n2', 'n3', '君主', '治水', '民忠'
			, '士氣', '訓練', 'n7'
		),
		'預備兵': 'I',
		'n-10': 'B',
		'n-9': 'B',
		'n-8': 'B',
		'n-7': 'B',
		'n-6': 'B',
		'n-5': 'B',
		'n-4': 'B',
		'n-3': 'B',
		'人口': 'H',
		'城防': 'H',
		'災害': 'B',
		'n1': 'B',
		'開發' : 'H',
		'商業': 'H',
		'n2': 'B',
		'n3': 'B',
		'君主': 'B',
		'治水': 'B',
		'民忠': 'B',
		'士氣': 'B',
		'訓練': 'B',
		'n7': 'B'
	}

	def __init__(self, f, index):
		if index >= len(g_state):
			super(state, self).__init__(f, self.FIELD_DESC, index, 'unknown')
		else:	
			super(state, self).__init__(f, self.FIELD_DESC, index, g_state[index])


	def show(self):
		print self.name(),
		print '君主', self.attr('君主'),
		print '城防', self.attr('城防'),
		print '開發', self.attr('開發'),
		print '商業', self.attr('商業'),
		print '治水', self.attr('治水'),
		print '民忠', self.attr('民忠')


# each for a man
class bandit(field):
	BANDIT_SIZE = 31
	#bit 2 (4) is done
	FIELD_DESC = {
		'fields': ('n-4', 'n-3', 'n-2', 'n-1'
			, '勇名', '經驗'
			, '兵數', '身份', '行動'
			, '武力', '智力', '政治', '魅力'
			, '訓練', '士氣', '將軍', '忠誠'
			, '所在', '君主', '性格', '寶物'
			, '技能'),
		'n-4': 'B',
		'n-3': 'B',
		'n-2': 'B',
		'n-1': 'B',
		'勇名': 'H',
		'經驗': 'H',
		'兵數': 'H',
		'身份': 'B',
		'行動': 'B',
		'武力': 'B',
		'智力': 'B',
		'政治': 'B',
		'魅力': 'B',
		'訓練': 'B',
		'士氣': 'B',
		'將軍': 'B',
		'忠誠': 'B',
		'所在': 'B',
		'君主': 'B',
		'性格': 'B',
		'寶物': 'I',
		'技能': 'I'
	}

	#opened file with cur pos for this man
	#exclusive 1-based index assigned and name for display
	def __init__(self, f, index, name=''):
		self._misc = None
		super(bandit, self).__init__(f, self.FIELD_DESC, index, name)


class misc(field):
	FIELD_DESC = {
		'fields': ('體力', 'n1', 'n2', 'n3'
			, 'n4', 'n5', 'n6', 'n7'
			, 'n8', 'n9', 'n10', 'n11'
			, 'n12', 'n13', 'n14', 'n15'
			, 'n16', 'n17'),
		'體力': 'B',
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
	OFFSET_STATE = 0x3f5
	STATE_COUNT = 47
	OFFSET_BANDIT = 0x1abe
	OFFSET_MISC = 0x8690
	BANDIT_COUNT = 300
	MAX_SOLDIAR = 20000
	def __init__(self, fname, count=BANDIT_COUNT):
		#if leader specified, remember country
		for i in reversed(range(len(fname))):
			if os.path.exists(fname[i]):
				self._fname = fname[i]
				break
		self.BANDIT_COUNT = count
		#data base
		self._banditList = []        #list of object
		self._banditByCountry = {}   #dict of object list by country
		self._stateByCountry = {}    #dict of state list by country
		self._banditByState = {}     #dict of object list by state
		self._stateList = []         #list of object
		with open(self._fname, "rb") as f:
			#read state data
			f.seek(self.OFFSET_STATE, 0)
			for i in range(self.STATE_COUNT):
				obj = state(f, i+1)
				self._stateList.append(obj)
				country = obj.attr('君主')
				if not country in self._stateByCountry:
					self._stateByCountry[country] = []
				self._stateByCountry[country].append(obj)
				#print 'added', country, 'w/'+obj.name()
			#read people data
			f.seek(self.OFFSET_BANDIT, 0)
			for i in range(self.BANDIT_COUNT):
				obj = bandit(f, i+1)
				if not self._insertPerson(obj):
					self.BANDIT_COUNT = i
					break
			#read people associated data
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
			f.seek(self.OFFSET_STATE, 0)
			for hh in self._stateList:
				hh.write(f)


	# insert into database
	# Ret : obj - object inserted
	#       None - fail to insert owning to invalid value
	def _insertPerson(self, obj):
		# determine by valid '武力'
		if not obj.attr('武力'):
			return None
		self._banditList.append(obj)
		country, state = obj.attr('君主'), obj.attr('所在')
		#create people list by country if not present
		if not country in self._banditByCountry:
			self._banditByCountry[country] = []
		self._banditByCountry[country].append(obj)
		#create list if not present
		if not state in self._banditByState:
			self._banditByState[state] = []
		self._banditByState[state].append(obj)
		# check known characters
		for name in g_bandit:
			if g_bandit[name][2] == obj.attr('政治') and\
			   g_bandit[name][1] == obj.attr('魅力'):
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
			toState = man.attr('所在')
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
			self._banditList[indexInList].set('君主', country)
			self._banditList[indexInList].set('所在', toState)
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
		for state in self._stateList:
			state.show()


	# show info by level
	# level 0 with minimal info
	def _showPerson(self, obj, level=0):
		name = obj.name()
		state = obj.attr('所在')
		if name:
			print name,
		else:
			print 'no',

		print obj.index(), ', 君主=', obj.attr('君主'), ', 所在=', state,
		#list is 0 based while index is 1 based
		if state >= len(g_state): print 'unknown',
		else: print '('+self._stateList[state-1].name()+')',
		print ', 體力=', obj._misc.attr('體力'), '    ',
		print obj.attr('武力'),
		print obj.attr('智力'),
		print obj.attr('政治'),
		print obj.attr('魅力'),
		if level >= 1:
			print '技能=', format(obj.attr('技能'), '#010x')
			print '寶物=', format(obj.attr('寶物'), '#010x')
			print '兵數= ', obj.attr('兵數'), ', 訓練= ', obj.attr('訓練'), ', 士氣= ', obj.attr('士氣'),
			if 0x04 & obj.attr('行動'): print '完成'
			else: print '未完'
			print '勇名= ', obj.attr('勇名'), ', 經驗= ', obj.attr('經驗'), ', 忠誠= ', obj.attr('忠誠'), ', 性格= ', obj.attr('性格')
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
			#self.showCountry(country, 1)
		for state in self._stateByCountry[country]:
			state.set('預備兵', 0)
			state.set('士氣', 0)
			state.set('訓練', 0)
			state.set('開發', 999)
			state.set('城防', 999)
			state.set('商業', 999)
			state.set('治水', 100)
			state.set('民忠', 100)
		#todo save
		self.update()


	# stateList is list in state in string
	def showState(self, stateList, level=0):
		for state in stateList:
			state = int(state)
			if state in self._banditByState:
				print 'There are', len(self._banditByState[state]), 'people in state', state
				for obj in self._banditByState[state]:
					self._showPerson(obj, level)
		

	# list of bro to modify
	def modifyBro(self, broList):
		nrBro = len(self._banditList)
		for index in broList:
			index = int(index)
			if index >= nrBro:
				print 'brother index', index, 'out of range'
			else:
				obj = self._banditList[index-1]
				print 'to modify', obj.name()
				obj.set('武力', obj.attr('武力') + 25)
		self.update()


	# peopleList is a list of people in str
	def _refillPerson(self, peopleList):
		for man in peopleList:
			indexInList = int(man) - 1
			if indexInList >= len(self._banditList):
				print 'Invalid index '+man+' ...skipped !!!'
				continue
			obj = self._banditList[indexInList]
			#print "manutest", obj.index(), obj.attr('忠誠')
			#skip man in the field
			if obj.attr('忠誠') < 60:
				continue
			if obj.attr('智力') >= 90 and obj.attr('政治') >= 80:
				obj.set('兵數', self.MAX_SOLDIAR)
			elif obj.attr('武力') >= 90:
				obj.set('兵數', self.MAX_SOLDIAR)
			elif obj.attr('武力')+obj.attr('智力') >= 160:
				obj.set('兵數', self.MAX_SOLDIAR)
			elif obj.attr('武力') >= 80:
				obj.set('兵數', 8000)
			elif obj.attr('武力')+obj.attr('智力') >= 150:
				obj.set('兵數', 8000)
			else:
				obj.set('兵數', 0)
			#set 訓練 only if soldiar
			if obj.attr('兵數'):
				if obj.attr('兵數') == self.MAX_SOLDIAR:
					obj.set('技能', 0xffffffff)
				obj.set('訓練', 100)
				obj.set('士氣', 100)
			else:
				obj.set('訓練', 0)
				obj.set('士氣', 0)
			obj._misc.set('體力', 100)
			obj.set('行動', 0)
			obj.set('忠誠', 100)


# Parse argument and make sure there is action to be taken
# Ret : arg - parsed result
def chk_param():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', action='append', dest='file', default=g_savefile,
		help='save file')
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
	parser.add_argument('-m', action='append', dest='modifyBro', default=[],
		help='modify brother by 1-based index')
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
	elif arg.modifyBro:
		sP.modifyBro(arg.modifyBro)
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
