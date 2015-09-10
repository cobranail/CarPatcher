#write hexcode for float number
#by cobranail#gmail.com

import struct
import sys

def toDoubleLE(num):
	t = struct.pack('<d',num)
	return t

def toDoubleBE(num):
	t = struct.pack('>d',num)
	return t

def toFloatLE(num):
	t = struct.pack('<f',num)
	return t

def toFloatBE(num):
	t = struct.pack('>f',num)
	return t



#num = float(sys.argv[1])


#s = struct.pack('<f',num)
#t = struct.pack('<d',num)

#print 'little-ed float: '+s.encode('hex_codec')
#print 'little-ed double: '+t.encode('hex_codec')

#s = struct.pack('>f',num)
#t = struct.pack('>d',num)

#print 'big-ed float: '+s.encode('hex_codec')
#print 'big-ed double: '+t.encode('hex_codec')

nlist = []

n = 0.0
while n <= 1.1:
	nlist.append([n,toFloatLE(n), toDoubleLE(n)])
	n=n+0.01

f = open(sys.argv[1], 'w')
f.write('----------------------------Little Ed-----------------------------\n')
for g in nlist:
	line = str(g[0]) + '  :  ' + g[1].encode('hex_codec') + ' , '+g[2].encode('hex_codec') + '\n'
	f.write(line)

f.close()
