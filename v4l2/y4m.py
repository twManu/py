#!/usr/bin/python

import os, sys, struct, argparse, re

file="/media/manu/230g/elephants_dream_1080p24.y4m"

def pureNumInStr(inputStr):
    return re.sub(r'[^0-9]', "", inputStr)

with open(file, 'r') as fr:
    line_nr=0
    for line in fr:
        line_nr += 1
        if 1==line_nr:
            words = line.split()
            print "format=", words[0]
            if words[0]!="YUV4MPEG2":
                print "error file format"
                break
            print "encoding=", words[1]
            #dimension
            _width=pureNumInStr(words[2])
            _height=pureNumInStr(words[3])
            print "dimension=", _width, _height
            #fps
            fpss=words[4].split(':')
            _fps1=pureNumInStr(fpss[0])
            _fps2=pureNumInStr(fpss[1])
            print "fps=", float(_fps1)/float(_fps2)
            print "ratio=", words[5]
        elif 2==line_nr:
            #FRAME
            print line
        else:
            frame=re.sub(r'FRAME$', "", line)
            print line_nr, len(line), len(frame)
            if line_nr>=5: break

