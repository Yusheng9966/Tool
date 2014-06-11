import os
import sys
print os.getcwd()
argv = sys.argv
print argv
if len(argv)<3:
	print "---usage: pyinputfile <inputfile> <shellcommand>"
	print 'example: pyinputfile input.txt "git rm --cached"'
	exit()

f = open(argv[1], "r")
l = f.readlines()
f.close()
a = [ n.replace('\n','') for n in l ]
for n in a:
	os.system( argv[2]+"  "+n)

exit()




