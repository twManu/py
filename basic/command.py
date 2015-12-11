import commands
#import re

print("With 'mount -v':")
mount = commands.getoutput('mount -v')
lines = mount.splitlines()
#form mount-point and type in a tuple
points = map(lambda line: (line.split()[2], line.split()[4]), lines)
#print(points)

#output mount-point (type)
for mnt in points:
	item = " (".join(str(x) for x in mnt)
	print(item + ")")

print("")


print("With 'df':")
#get each line
line2 = commands.getoutput('df').splitlines()
#extract 6th word which stats with '/'
point2 = [line.split()[5] for line in line2 if line.split()[5].startswith('/')]
#print
for pnt in point2: print(pnt)

#point2 = [line.split()[5] for line in line2]
#for pnt in filter(lambda item: re.match('/.*', item), point2):
#	print(pnt)