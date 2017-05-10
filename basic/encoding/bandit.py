#!/usr/bin/python
# coding=utf-8

import sys, struct, argparse
from struct import *
from field import *

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
	def __init__(self, f):
		super(state, self).__init__(f, self.FIELD_DESC)

		
	


# each for a man
class bandit(field):
	BANDIT_SIZE = 22
	FIELD_DESC = {
		'fields': ('年紀', '國家', '地區', '體力', '體力上限', '忠義', '仁愛', '勇氣', '力量', '技能', '智慧'\
			, '力量經驗', '技能經驗', '智慧經驗', '忠誠', '頭像', '名聲', '土兵', '角色', '未知19', '未知20', '未知21'),
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
		'名聲': 'B',
		'土兵': 'B',
		'角色': 'B',
		'未知19': 'B',
		'未知20': 'B',
		'未知21': 'B'
	}

	#opened file with cur pos for this man
	def __init__(self, f):
		super(bandit, self).__init__(f, self.FIELD_DESC)


# take care of file
class banditParser(object):
	OFFSET_BANDIT = 16
	OFFSET_STATE = 5964
	BANDIT_COUNT = 255
	STATE_COUNT = 49
	def __init__(self, fname):
		self._fname = fname
		#data base
		self._bandits = {}           #to access by name
		self._banditList = []        #list of object
		self._stateList = []         #list of object
		with open(fname, "r+b") as f:
			f.seek(self.OFFSET_BANDIT, 0)
			for i in range(self.BANDIT_COUNT):
				obj = bandit(f)
				self._bandits[self._lookup(i, obj)] = obj
				self._banditList.append(obj)
			f.seek(self.OFFSET_STATE, 0)
			#state is 0 based
			for i in range(self.STATE_COUNT):
				self._stateList.append(state(f))


	def _lookup(self, index, man):
		ability = pack('BBB', man.attr('忠義'), man.attr('仁愛'), man.attr('勇氣'))
		for mm, aa in g_bandit.iteritems():
			if ability == pack('BBB', aa[0], aa[1], aa[2]):
				return mm
		return "第"+str(index+1)+"位"

	#man is already a bandit object
	def show1Man(self, name, man):
		print name+" ("+str(man.attr("忠誠"))+")"
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


	#show a man or all
	def showMan(self, name):
		if name:
			if self._bandits.has_key(name):
				self.show1Man(name, self._bandits[name])
			else:
				print "unknown "+name
		else:
			for i in range(len(self._banditList)):
				man = self._banditList[i]
				for mm, obj in self._bandits.iteritems():
					if obj==man:
						#show 1 based
						print '#'+str(i+1),
						self.show1Man(mm, obj)
						break
	#show man by 1-based index
	def showManIndex(self, index):
		if index:
			if index<=len(self._banditList):
				man = self._banditList[index-1]
				for mm, obj in self._bandits.iteritems():
					if obj==man:
						#show 1 based
						self.show1Man(mm, obj)
						break
		else:
			for i in range(len(self._banditList)):
				man = self._banditList[i]
				for mm, obj in self._bandits.iteritems():
					if obj==man:
						#show 1 based
						print '#'+str(i+1),
						self.show1Man(mm, obj)
						break
				

	#i: 1 based 
	def show1State(self, stateObj, i):
		print str(i)+" 州"
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
		print '  支持 :',
		print stateObj.attr('支持'),
		print '  治水: ',
		print stateObj.attr('治水'),
		print '  地利 :',
		print stateObj.attr('地利'),
		print '  毛皮 :',
		print stateObj.attr('毛皮'),
		print '  財富 :',
		print stateObj.attr('財富')
		print '  武器 :',
		print stateObj.attr('武器'),
		print '  戰技: ',
		print stateObj.attr('戰技'),
		print ''


	#show a state or all(0)
	def showState(self, i):
		if i:
			self.show1State(self._stateList[i-1], i)
		else:
			for ss in self._stateList:
				i += 1
				self.show1State(ss, i)


# Parse argument and make sure there is action to be taken
# Ret : arg - parsed result
def chk_param():
	parser = argparse.ArgumentParser()
	parser.add_argument('-q', action='store', dest='query', default='sh',
		help='s (state) or h (hero), default both')
	parser.add_argument('-i', action='store', dest='index', default=0,
		help='index of object to query')
	arg=parser.parse_args()
	return arg


#main
if __name__ == '__main__':
	bP = banditParser("/home/manuchen/.dosbox/bandit/SAVEDATA")
	arg = chk_param()
	if 'h' in arg.query:
		bP.showManIndex(int(arg.index))
	if 's' in arg.query:
		bP.showState(int(arg.index))
	#bP.showMan("")
	#bP.showState(0)

