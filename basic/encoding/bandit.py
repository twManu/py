#!/usr/bin/python
# coding=utf-8

import sys, struct
from field import *

# each for a man
class bandit(field):
    BANDIT_SIZE = 22
    FIELD_DESC = {
        'fields': ('年紀', '國家', '地區', '體力', '體力上限', '正義', '仁愛', '勇氣', '力量', '技能', '智慧'\
            , '力量經驗', '技能經驗', '智慧經驗', '忠誠', '頭像', '名聲', '土兵', '角色', '未知19', '未知20', '未知21'),
        '年紀': 'B',
        '國家': 'B',
        '地區': 'B',
        '體力': 'B',
        '體力上限': 'B',
        '正義': 'B',
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
        print self._field['正義'], self._field['仁愛'], self._field['勇氣']


# take care of file
class banditParser(object):
    OFFSET_BANDIT = 16
    BANDIT_COUNT = 255
    def __init__(self, fname):
        self._fname = fname
        with open(fname, "rb") as f:
            skip = f.read(self.OFFSET_BANDIT)
            for i in range(self.BANDIT_COUNT):
                self._bandit = bandit(f)
                #val=f.read(22), print val.encode(hex) 


#main
if __name__ == '__main__':
    bP = banditParser("/home/manu/Downloads/SAN5/bandit/SAVEDATA")
