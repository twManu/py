#!/usr/bin/python

import os, sys, struct, argparse, re

g_d4File="/tmp/save000.y4m"

class cY4M:
    def __init__(self, args):
        self._args = None
        self._inFile = None
        self._size = 0
        if args:
            self._args = args
            self._inFile = args.inFile
        if not self._inFile:
            self._inFile = g_d4File
        if not os.path.isfile(self._inFile):
            print "invalid input file", self._inFile
            self._inFile = ""


    #get identification and value
    def pureNumInStr(self, inputStr):
        matches = {
            'W': r'W([0-9]+)',
            'H': r'H([0-9]+)',
            'A': r'A([^A]+)',
            'I': r'I[^I]',
            'F': r'F([^F]+)'
        }
        for key in matches:
            match = re.match(matches[key], inputStr)
            if match:
                return key, match
        return '', 0


    def levelPnt(self, level, msg):
        if level>=self._args.verbose:
            print msg
            return True
        return False

    
    def parse(self):
        if not self._inFile:
            return
        with open(self._inFile, 'r') as fr:
            #1st line
            line = fr.readline()
            self.levelPnt(2, line)
            words = line.split()
            print "format=", words[0]
            if words[0]!="YUV4MPEG2":
                print "error file format"
                return
            for i in range(1, len(words)):
                key, value = self.pureNumInStr(words[i])
                if not key: break
                elif 'W'==key:
                    if not self.levelPnt(3, value.group(0)):
                        self.levelPnt(2, value.group(1))
                    if not self._size:
                        self._size = int(value.group(1))
                    else: self._size *= int(value.group(1))
                elif 'H'==key:
                    if not self.levelPnt(3, value.group(0)):
                        self.levelPnt(2, value.group(1))
                    if not self._size:
                        self._size = int(value.group(1))
                    else: self._size *= int(value.group(1))
                elif 'F'==key:
                    if not self.levelPnt(3, value.group(0)):
                        self.levelPnt(2, value.group(1))
                elif 'A'==key:
                    if not self.levelPnt(3, value.group(0)):
                        self.levelPnt(2, value.group(1))
                elif 'I'==key:
                    if not self.levelPnt(3, value.group(0)):
                        self.levelPnt(2, value.group(1))
                else: self.levelPnt(1, value.group(0))
            print "420 size=", self._size+self._size/2
            print "422 size=", self._size*2
            self._size += self._size/2
            frames = 0
            while True:
                line = fr.readline()
                frame=re.match(r'FRAME', line)
                if frame:
                    frames += 1
                    self.levelPnt(2, frame.group(0)+' '+str(frames))
                    fr.read(self._size)
                else: break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', type=int, action='store', dest='verbose', default=0,
        choices=[0, 1, 2, 3])
    parser.add_argument('-f', action='store',
        dest='inFile', help='input file')
    args = parser.parse_args()
    obj = cY4M(args)
    obj.parse()

