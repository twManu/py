#!/usr/bin/python
import json

strJson='{"key1":"abc","key2":2}'

print 'string :', strJson
print 'Interpreted as json:' 
dictJson=json.loads(strJson)
print dictJson





