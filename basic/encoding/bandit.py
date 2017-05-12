#!/usr/bin/python
# coding=utf-8

import sys, struct, argparse
from struct import *
from field import *


g_savefile = "/home/manuchen/.dosbox/bandit/SAVEDATA"

#name : (justice, mercy, courage)
g_bandit = {
	"花榮": (91, 75, 84),      
	"林沖": (100, 61, 80),     
	"秦明": (79, 78, 90),     
	"宋江": (81, 100, 62),     
	"關勝": (75, 90, 83),      
	"史進": (74, 69, 95),      
	"吳用": (86, 70, 58),      
	"晁蓋": (96, 68, 76),     
	"楊志": (97, 58, 79),   
	"武松": (68, 55, 98),    
	"張清": (72, 66, 83),      
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

# each for a state
class state(field):
	STATE_SIZE = 24
	FIELD_DESC = {
	'fields': ('黃金', '糧草', '金屬', '毛皮', '物價', '治水', '地利', '財富', '支持', '武器', '戰技'\
		, '未知11', '未知12', '未知13', '未知14', '未知15', '未知16', '未知17', '未知18', '未知19'),
		'黃金': 'H',
		'糧草': 'H',
		'金屬': 'H',
		'毛皮': 'H',
		'物價': 'B',
		'治水': 'B',
		'地利': 'B',
		'財富': 'B',
		'支持': 'B',
		'武器': 'B',
		'戰技': 'B',
		'未知11': 'B',
		'未知12': 'B',
		'未知13': 'B',
		'未知14': 'B',
		'未知15': 'B',
		'未知16': 'B',
		'未知17': 'B',
		'未知18': 'B',
		'未知19': 'B'
	}

	#opened file with cur pos for this man
	#1-based index
	#name to display
	def __init__(self, f, index):
		super(state, self).__init__(f, self.FIELD_DESC, index, '第'+str(index)+'州')

		
	#1-based index
	def update(self):
		self.set('黃金', 20000)
		self.set('糧草', 20000)
		self.set('金屬', 20000)
		self.set('毛皮', 20000)
		self.set('治水', 100)
		self.set('地利', 100)
		self.set('財富', 100)
		self.set('支持', 100)
		self.set('武器', 100)
		self.set('戰技', 100)


# each for a man
class bandit(field):
	BANDIT_SIZE = 22
	FIELD_DESC = {
		'fields': ('年紀', '國家', '地區', '體力', '體力上限', '忠義', '仁愛', '勇氣', '力量', '技能', '智慧'\
			, '力量經驗', '技能經驗', '智慧經驗', '忠誠', '頭像', '名聲', '土兵', '角色', '未知20', '未知21'),
		'年紀': 'B',
		'國家': 'B',
		'地區': 'B',
		'體力': 'B',
		'體力上限': 'B',
		'忠義': 'B',
		'仁愛': 'B',
		'勇氣': 'B',
		'力量': 'B',
		'技能': 'B',
		'智慧': 'B',
		'力量經驗': 'B',
		'技能經驗': 'B',
		'智慧經驗': 'B',
		'忠誠': 'B',
		'頭像': 'B',
		'名聲': 'H',
		'土兵': 'B',
		'角色': 'B',
		'未知20': 'B',
		'未知21': 'B'
	}

	#opened file with cur pos for this man
	#exclusive 1-based index assigned and name for display
	def __init__(self, f, index, name=''):
		super(bandit, self).__init__(f, self.FIELD_DESC, index, name)


	#1-based index
	def brother(self, leader=None):
		self.set('體力', 255)
		self.set('體力上限', 255)
		self.set('力量', 100)
		self.set('技能', 127)
		self.set('智慧', 127)
		self.set('忠誠', 100)
		self.set('土兵', 100)
		if not leader:
			role = self.attr('角色')
			role |= 2
			self.set('角色', role)


	def leader(self):
		#leader won't set role brother
		self.brother(1)
		self.set('忠義', 99)
		self.set('仁愛', 99)
		self.set('勇氣', 99)
		self.set('名聲', 999)


# take care of file
class banditParser(object):
	OFFSET_BANDIT = 16
	OFFSET_STATE = 5964
	BANDIT_COUNT = 255
	STATE_COUNT = 49
	def __init__(self, fname):
		self._fname = fname
		#data base
		self._banditList = []        #list of object
		self._stateList = []         #list of object
		with open(fname, "rb") as f:
			f.seek(self.OFFSET_BANDIT, 0)
			for i in range(self.BANDIT_COUNT):
				obj = bandit(f, i+1)
				obj.setName(self._match(i+1, obj))
				self._banditList.append(obj)
			f.seek(self.OFFSET_STATE, 0)
			#state is 0 based
			for i in range(self.STATE_COUNT):
				self._stateList.append(state(f, i+1))


	def update(self):
		with open(self._fname, "r+b") as f:
			f.seek(self.OFFSET_BANDIT, 0)
			for hh in self._banditList:
				hh.write(f)
			f.seek(self.OFFSET_STATE, 0)
			for ss in self._stateList:
				ss.write(f)

	#1 based index	
	def _match(self, index, man):
		ability = pack('BBB', man.attr('忠義'), man.attr('仁愛'), man.attr('勇氣'))
		for mm, aa in g_bandit.iteritems():
			if ability == pack('BBB', aa[0], aa[1], aa[2]):
				return mm
		return "第"+str(index)+"位"


	#man is already a bandit object
	def _show1Man(self, man, level):
		print '#'+str(man.index())+' '+man.name()+" ("+str(man.attr("忠誠"))+")"
		if level>=1:
			print '    忠義 仁愛 勇氣 =',
			print man.attr("忠義"),
			print man.attr("仁愛"),
			print man.attr("勇氣"),
			print "("+pack('BBB', man.attr("忠義"), man.attr("仁愛"), man.attr("勇氣")).encode('hex')+")"
			print '    力量 技能 智慧 =',
			print man.attr("力量"),
			print man.attr("技能"),
			print man.attr("智慧"),
			print "("+pack('BBB', man.attr("力量"), man.attr("技能"), man.attr("智慧")).encode('hex')+")"


	#show single man by 1-based index
	#level: int 0, 1 or 2
	def showManIndex(self, index, level):
		if index:
			if index<=len(self._banditList):
				self._show1Man(self._banditList[index-1], level)
		else:
			for i in range(len(self._banditList)):
				self._show1Man(self._banditList[i], level)


	#set as brother with 1 based index
	#Ret : 0 - fail to update
	#      1 - successful
	def brother(self, index):
		if index and index<=len(self._banditList):
			self._banditList[index-1].brother()
			return 1
		return 0


	#set as leader with 1 based index
	#Ret : 0 - fail to update
	#      1 - successful
	def leader(self, index):
		if index and index<=len(self._banditList):
			self._banditList[index-1].leader()
			return 1
		return 0
	

	#set state parameters with 1 based index
	#Ret : 0 - fail to update
	#      1 - successful
	def state(self, index):
		if index and index<=len(self._stateList):
			self._stateList[index-1].update()
			return 1
		return 0


	#i: 1 based 
	def show1State(self, stateObj, level):
		print stateObj.name(),
		print '  黃金 :',
		print stateObj.attr('黃金'),
		print '  糧草: ',
		print stateObj.attr('糧草'),
		print '  金屬 :',
		print stateObj.attr('金屬'),
		print '  毛皮 :',
		print stateObj.attr('毛皮'),
		print '  物價 :',
		print stateObj.attr('物價')
		if not level:
			return
		print '        支持 :',
		print stateObj.attr('支持'),
		print '  治水: ',
		print stateObj.attr('治水'),
		print '  地利 :',
		print stateObj.attr('地利'),
		print '  毛皮 :',
		print stateObj.attr('毛皮'),
		print '  財富 :',
		print stateObj.attr('財富')
		if level<2:
			return
		print '        武器 :',
		print stateObj.attr('武器'),
		print '  戰技: ',
		print stateObj.attr('戰技'),
		print ''


	#show a state or all(0)
	def showState(self, i, level):
		if i:
			self.show1State(self._stateList[i-1], level)
		else:
			#now i=0
			for ss in self._stateList:
				i += 1
				self.show1State(ss, level)


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
	parser.add_argument('-q', action='store', dest='query', default='sh',
		help='s (state) or h (hero), default sh (both)')
	parser.add_argument('-i', action='append', dest='index', default=[],
		help='index of object to query')
	parser.add_argument('-v', action='store', dest='level', default=0,
		help='verbose level, 0, 1 or 2')
	arg=parser.parse_args()
	return arg


#main
if __name__ == '__main__':
	arg = chk_param()
	modify = 0
	bP = banditParser(arg.file)
	if arg.leader:
		modify += bP.leader(int(arg.leader))
	for bb in arg.brother:
		modify += bP.brother(int(bb))
	for ss in arg.state:
		modify += bP.state(int(ss))
	if modify:
		print 'writing file'
		bP.update()
	#still response to query
	if 'h' in arg.query:
		for ii in arg.index:
			bP.showManIndex(int(ii), arg.level)
	if 's' in arg.query:
		for ii in arg.index:
			bP.showState(int(ii), arg.level)

