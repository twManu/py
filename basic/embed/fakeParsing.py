'''fakeParsing.py - Python source designed to demonstrate the use of python dict object'''

class Parsing: 
	def __init__(self):
		self.dict = {}
		self.dict["itemInt"] = 5
		self.dict["itemBool"] = False
		self.dict["itemList"] = ['a', 'b', 'c']
		self.dict["itemString"] = "this string"
    
	def getDict(self):
		return self.dict
