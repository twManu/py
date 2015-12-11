import pipes
import tempfile

p = pipes.Template()
p.append('cat $IN > $OUT', 'ff')
p.debug(True)

t = tempfile.NamedTemporaryFile('r')
f = p.open(t.name, 'w')
try:
    f.write('Some text')
finally:
    f.close()

t.seek(0)
print t.read()
t.close()
