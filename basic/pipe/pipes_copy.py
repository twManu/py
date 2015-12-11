import pipes
import tempfile

p = pipes.Template()
p.debug(True)
p.append('grep -n tortor $IN', 'f-')

t = tempfile.NamedTemporaryFile('r')

p.copy('lorem.txt', t.name)

t.seek(0)
print t.read()
t.close()
