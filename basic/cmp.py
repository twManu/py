
item = (10, 3)
dict1 = {
	 (4, 12): "4/12"
	, (3, 5): "3/5"
	, (10, 3): "3/5"
}

for key in dict1:
	if item == key:
		print dict1[key]
	else:
		print "mismatch item: ",
		print key


