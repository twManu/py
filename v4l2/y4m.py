#!/usr/bin/python

import os, sys, struct, argparse, re

g_d4File="/tmp/save000.y4m"

class cY4M:
    def __init__(self, args):
        self._args = None
        self._inFile = None
        self._size = 0
        self._gotStartHeader = False
        self._gotFrame = False
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
            'I': r'I([^I]+)',
            'F': r'F([^F]+)',
            'C': r'C([^C]+)'
        }
        for key in matches:
            match = re.match(matches[key], inputStr)
            if match:
                return key, match
        return '', 0


    def levelPnt(self, level, msg):
        if level<=self._args.verbose:
            print msg
            return True
        return False

    
    #make sure YUV4MPEG2 got
    # return line w/o YUV4MPEG2
    #    "Error" - fail
    #    None - start header already got
    #    otherwise - reset of start header
    def parseStartHeader(self, fr):
        if self._gotStartHeader: return None
        #1st line
        while not self._gotStartHeader:
            line = fr.readline()
            self.levelPnt(2, line)
            words = line.split()
            #comment line
            if re.match(r'#(.+)', words[0]):
                continue
            print "format=", words[0]
            if words[0]!="YUV4MPEG2":
                print "error file format"
                return "Error"
            #valid start header
            self._gotStartHeader = True
            return re.sub(r'YUV4MPEG2', "", line)

    
    def parse(self):
        if not self._inFile:
            return
        with open(self._inFile, 'r') as fr:
            string = self.parseStartHeader(fr)
            if "Error" == string:
                return
            if string:
                print "... header found, processing", string
                string = self.parseFormat(fr, string)
                if string == "Error": return
                elif string == "Got":
                    print "... parsing done"
                    return
                elif string: return


    def parseFormat(self, fr, string):
        if self._gotFrame: return None
        while not self._gotFrame:
            #load a line of not provided
            if not string:
                string = fr.readline()
                self.levelPnt(2, string)
            string = string.strip()
            if re.match(r'FRAME', string):
                self.levelPnt(0, "frame got")
                self._gotFrame = True
                return "Got"
            words = string.split()
            #comment line
            if re.match(r'#(.+)', words[0]):
                continue
            for i in range(0, len(words)):
                key, value = self.pureNumInStr(words[i])
                if 'W'==key:
                    self.levelPnt(3, value.group(0))
                    self.levelPnt(1, "  width= "+value.group(1))
                    if not self._size:
                        self._size = int(value.group(1))
                    else: self._size *= int(value.group(1))
                elif 'H'==key:
                    self.levelPnt(3, value.group(0))
                    self.levelPnt(1, "  height= "+value.group(1))
                    if not self._size:
                        self._size = int(value.group(1))
                    else: self._size *= int(value.group(1))
                elif 'F'==key:
                    self.levelPnt(3, value.group(0))
                    values = value.group(1).split(":")
                    value = float(values[0])/float(values[1])
                    self.levelPnt(1, "  fps= "+str(value))
                elif 'A'==key:
                    self.levelPnt(3, value.group(0))
                    values = value.group(1).split(":")
                    value = float(values[0])/float(values[1])
                    self.levelPnt(1, "  aspect ratio= "+str(value))
                elif 'I'==key:
                    self.levelPnt(3, value.group(0))
                    if "p"==value.group(1): self.levelPnt(1, "  progressive")
                    else: self.levelPnt(1, "  interlaced")
                else:
                    self.levelPnt(1, value.group(0))
                    return "Error"
                string = None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', type=int, action='store', dest='verbose', default=0,
        choices=[0, 1, 2, 3])
    parser.add_argument('-f', action='store',
        dest='inFile', help='input file')
    parser.add_argument('-H', action='store_true',
        dest='hdrOnly', help='stop after header parsing, i.e 1st FRAME')
    args = parser.parse_args()
    obj = cY4M(args)
    obj.parse()

