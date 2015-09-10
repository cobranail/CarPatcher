# -*- coding: utf-8 -*-
#osx yosemite carfile color decompressor
#by cobranail#gmail.com
#version 0.3
import os
import sys
import patcherlib

def char4tovaluelitt(char4):
	return ord(char4[0]) + ord(char4[1])*256 + ord(char4[2])*65536 + ord(char4[3])*65536*256

def char4tovaluebig(char4):
	return ord(char4[3]) + ord(char4[2])*256 + ord(char4[1])*65536 + ord(char4[0])*65536*256

def positions(target, source):
	'''Produce all positions of target in source'''
	pos = -1
	try:
		while True:
			pos = source.index(target, pos + 1)
			yield pos
	except ValueError:
		pass

def getresindex2(uidata):
	'''Get resource index, return a list'''
	datalen = len(uidata)

	#slice data
	t = uidata[16:20]
	sec1len = char4tovaluebig(t)
	datasec2 = uidata[sec1len:datalen]

	readit = True
	p = 20
	pz = -1
	group = []
	buffer = ''
	writebuffer = False
	while readit:
		char8 = datasec2[p:p+8]

		if char8[0:4] == '\x00\x00\x00\x00':
			print "zero"
			readit = False
			break
		else:
			s1 = [char8[i:i+4] for i in range(0, len(char8), 4)]
			group.append(s1)
		p=p+8
	return group

def getresindex4(datachunk):
	'''Get resource index, return a list'''
	chunklen = len(datachunk)
	count = char4tovaluebig(datachunk[0:4])
	group = []
	for i in range(count):
		#item in group : index,  offset,  length
		#s1 = [char8[i:i+4] for i in range(0, len(char8), 4)]
		z = i*8
		char8 = datachunk[4+z: 4+z+8]
		s1 = [i, char4tovaluebig(char8[0:4]), char4tovaluebig(char8[4:8])]
		group.append(s1)
		pass
	print 'resource count : '+str(len(group)) + ', value : '+str(count)
	return group



rsfile = sys.argv[1]

uifile = open(rsfile,'rb')

uidata = uifile.read()

uifile.close()

#slice data
datalen = len(uidata)
t = uidata[16:20]
sec1len = char4tovaluebig(t)
print 'total len:'+str(datalen)
print 'section 1 len:'+str(sec1len)

datasec1 = uidata[0:sec1len]
datasec2 = uidata[sec1len:datalen]

gp = getresindex4(datasec2)

rsfile = rsfile.replace('.', '_')
rsdir = rsfile+'_dir'

if not os.path.exists(rsdir):
   os.makedirs(rsdir)

print 'index group len:'+str(len(gp))
#print gp
for item in gp:
	offset = item[1]
	length = item[2]
	if length>0:
		char4 = uidata[offset:offset+4]
		datastr = uidata[offset:offset+length]
		if char4 == 'ISTC':
			outdata = uidata[offset:offset+length]
			chkname = str(outdata[40:40+128])
			sname = ''
			for x in chkname:
				if x>'\x00':
					sname = sname+x
			ofn = rsdir+'/'+str(offset)+'~'+sname
			ofile = open(ofn, 'wb')
			ofile.write(outdata)
			ofile.close()
		elif length == 132:
			sname = ''
			for x in datastr:
				if x>'\x00':
					sname = sname+x
			ofn = rsdir+'/'+str(offset)+'_'+sname
			ofile = open(ofn, 'wb')
			ofile.write(datastr)
			ofile.close()
		elif length == 12:
			ofn = rsdir+'/'+str(offset)+'_'+str(length)
			ofile = open(ofn, 'wb')
			ofile.write(datastr)
			ofile.close()
		else:
			ofn = rsdir+'/'+str(offset)+'_'+str(length)
			ofile = open(ofn, 'wb')
			ofile.write(datastr)
			ofile.close()
		pass
