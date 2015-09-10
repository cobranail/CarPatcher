# -*- coding: utf-8 -*-
#osx yosemite carfile decompressor
#by cobranail#gmail.com

#version 0.3
#publish

#version 0.2

import os
import sys


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





rsfile = sys.argv[1]

uifile = open(rsfile,'rb')

uidata = uifile.read()

uifile.close()

#slice data
datalen = len(uidata)
t = uidata[16:20]
sec1len = char4tovaluebig(t)
print datalen
print sec1len

datasec1 = uidata[0:sec1len]
datasec2 = uidata[sec1len:datalen]

gp = getresindex2(uidata)

rsdir = rsfile+'dir'

if not os.path.exists(rsdir):
    os.makedirs(rsdir)

for item in gp:
	offset = char4tovaluebig(item[0])
	length = char4tovaluebig(item[1])
	char4 = uidata[offset:offset+4]
	if char4 == 'ISTC':
		outdata = uidata[offset:offset+length]
		chkname = str(outdata[40:40+128])
		print chkname
		sname = ''
		for x in chkname:
			if x>'\x00':
				sname = sname+x
		ofn = rsdir+'/'+sname+'~'+str(offset)
		ofile = open(ofn, 'wb')
		ofile.write(outdata)
		ofile.close()
		pass
	pass
