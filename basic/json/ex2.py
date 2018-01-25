#!/usr/bin/python
# coding=Big5
import json

dictJson = {
	  'key1':"abc"
	, 'key2':2
}

print 'dictionary :', dictJson
print 'converted as:'
strJson=json.dumps(dictJson)
print strJson





