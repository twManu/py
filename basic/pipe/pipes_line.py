import subprocess

p=subprocess.Popen(['ps aux'], stdout=subprocess.PIPE, shell=True)
ite=iter(p.stdout.readline, b'')
for line in ite:
	line=line.strip()
	if line: print line

