#!/usr/bin/python
# coding=utf-8

import sys, struct

# each for a man
class bandit(object):
    BANDIT_SIZE = 22
    FIELD_DESC = ('年紀', '國家', '地區', '體力', '體力上限', '正義', '仁愛', '勇氣', '力量', '技能',\
    '智慧', '力量經驗', '技能經驗', '智慧經驗', '忠誠', '頭像', '名聲', '土兵', '角色', '未知19', '未知20', '未知21')
    #opened file with cur pos for this man
    def __init__(self, f):
        self._field = {}
        for i in range(self.BANDIT_SIZE):
            self._field[self.FIELD_DESC[i]], = struct.unpack('B', f.read(1))
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
