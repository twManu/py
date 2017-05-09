#!/usr/bin/python
# coding=utf-8

import sys, struct

# each for an object
class field(object):
    #opened file with cur pos for this man
    #desc contains
    #   desc['fields'] : tuple of each fieldName
    #   desc[<fieldName>] : unpack parameter 'B', 'H', 'I', or signed version 'b', 'h', 'i'
    def __init__(self, f, fieldDesc):
        self._field = {}
        for ff in fieldDesc['fields']:
            if fieldDesc[ff] == 'b' or fieldDesc[ff] == 'B':
                self._field[ff], = struct.unpack(fieldDesc[ff], f.read(1))
            elif fieldDesc[ff] == 'h' or fieldDesc[ff] == 'H':
                self._field[ff], = struct.unpack(fieldDesc[ff], f.read(2))
            elif fieldDesc[ff] == 'i' or fieldDesc[ff] == 'I':
                self._field[ff], = struct.unpack(fieldDesc[ff], f.read(4))
            else:
                raise NameError('unknown field type')

    #given key, return value if valid
    #otherwise none returned
    def attr(self, key):
        if self._field.has_key(key):
            return self._field[key]
        return None

    def show(self):
        for key, value in self._field.iteritems():
            print key+': '+str(value)


#main
if __name__ == '__main__':
    fDesc = {
        'fields': ('忠義', '仁愛', '勇氣'),
        '忠義': 'B',
        '仁愛': 'B',
        '勇氣': 'B'
    } 
    with open('test', "rb") as f:
        #pop offset 16 and '年紀', '國家', '地區', '體力', '體力上限'
        f.read(16+5)
        obj = field(f, fDesc)
        obj.show()