#!/usr/bin/python
import re

line = "Cats are smarter than dogs";

searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I)

if searchObj:
   print("searchObj.group() : ", "\"%s\"" % searchObj.group())
   print("searchObj.group(1) : ", "\"%s\"" % searchObj.group(1))
   print("searchObj.group(2) : ", "\"%s\"" % searchObj.group(2))
else:
   print("Nothing found!!")
