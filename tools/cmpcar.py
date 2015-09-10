#compare 2 carfiles
#by cobranail#gmail.com

import os
import sys

version = 0.3

def positions(target, source):
	'''Produce all positions of target in source'''
	pos = -1
	try:
		while True:
			pos = source.index(target, pos + 1)
			yield pos
	except ValueError:
		pass

def char4tovaluelitt(char4):
	return ord(char4[0]) + ord(char4[1])*256 + ord(char4[2])*65536 + ord(char4[3])*65536*256

def char4tovaluebig(char4):
	return ord(char4[3]) + ord(char4[2])*256 + ord(char4[1])*65536 + ord(char4[0])*65536*256


def getresindex3(datachunk):
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

def getpatchinfobyoffset(group, offset):
	for x in xrange(len(group)):
		line = group[x]
		if offset == line[0]:
			return x
	return -1

def inttochars(val):
	'''convert a int to 4chars , big endian'''
	a = format(val, 'X').zfill(8)
	c1 = chr(int(a[0:2],16))
	c2 = chr(int(a[2:4],16))
	c3 = chr(int(a[4:6],16))
	c4 = chr(int(a[6:8],16))
	return c1+c2+c3+c4

def locateinjection(dataslices,offset):
	'''locate the inject block index via offset'''
	for x in xrange(len(dataslices)):
		#idx, orig_offset , orig_length, bool , data
		if dataslices[x][1] == offset:
			return x
	return -1

def getistcname(istcdata):
	chkname = str(istcdata[40:40+128])
	sname = ''
	for x in chkname:
		if x>'\x00':
			sname = sname+x
	pass
	return sname


def buildslices(uidata):

	slice1_sp = 0
	slice2_sp = char4tovaluebig(uidata[16:20])  # datachunk1 length

	slice1_len = slice2_sp
	slice2_len = char4tovaluebig(uidata[20:24]) # datachunk2 length

	slice3sub_sp = char4tovaluebig(uidata[24:28]) 
	slice3sub_len = char4tovaluebig(uidata[28:32]) # sub datachunk len

	datachunk1 = uidata[slice1_sp : slice1_sp+slice1_len] #datachunk 1
	datachunk2 = uidata[slice2_sp : slice2_sp+slice2_len] #datachunk 2

	datachunk3sub = uidata[slice3sub_sp : slice3sub_sp+slice3sub_len] # sub datachunk

	tag_data_sp = 4 + 8 * char4tovaluebig(datachunk2[0:4])
	tag_data_count = char4tovaluebig(datachunk2[tag_data_sp: tag_data_sp+4])
	tag_data = datachunk2[tag_data_sp : tag_data_sp + 8*tag_data_count]

	return [[slice1_sp, slice1_len], [slice2_sp, slice2_len], [slice3sub_sp, slice3sub_len], [tag_data_sp, 4+tag_data_count*8]]

def buildslices_data(uidata):

	slice1_sp = 0
	slice2_sp = char4tovaluebig(uidata[16:20])  # datachunk1 length

	slice1_len = slice2_sp
	slice2_len = char4tovaluebig(uidata[20:24]) # datachunk2 length

	slice3sub_sp = char4tovaluebig(uidata[24:28]) 
	slice3sub_len = char4tovaluebig(uidata[28:32]) # sub datachunk len

	datachunk1 = uidata[slice1_sp : slice1_sp+slice1_len] #datachunk 1
	datachunk2 = uidata[slice2_sp : slice2_sp+slice2_len] #datachunk 2

	datachunk3sub = uidata[slice3sub_sp : slice3sub_sp+slice3sub_len] # sub datachunk

	tag_data_sp = 4 + 8 * char4tovaluebig(datachunk2[0:4])
	tag_data_count = char4tovaluebig(datachunk2[tag_data_sp: tag_data_sp+4])
	tag_data = datachunk2[tag_data_sp : tag_data_sp + 8*tag_data_count]

	return [[slice1_sp, slice1_len, datachunk1], [slice2_sp, slice2_len, datachunk2], [slice3sub_sp, slice3sub_len, datachunk3sub], [tag_data_sp, 4+tag_data_count*8, tag_data]]


def getdatablock(dataslicegrp):
	#slices
	print dataslicegrp[3][1]
	datachunk2 = dataslicegrp[1][2]
	datachunk1 = dataslicegrp[0][2]
	tag_data = dataslicegrp[3][2]
	print len(datachunk2)
	gp1 = getresindex3(datachunk2)
	#print len(gp1)
	#print 'gp2'
	#print 'tag_data_sp '+str(tag_data_sp)+', '+str(tag_data_count)
	#print len(tag_data)

	#non zero
	gp1nz = []
	for item in gp1:
		if item[2]>0:
			#length > 0
			gp1nz.append(item)


	#gpc = gp1nz+gp2nz+[[-2, slice3sub_sp, slice3sub_len]]

	idx = 0

	dataslices = []
	for idxgp in gp1nz:
		ioffset = idxgp[1]
		ilen = idxgp[2]
		dataslices.append([idx, ioffset, ilen , False ,datachunk1[ioffset:ioffset+ilen]])
		idx = idx+1
		pass

	pass
	return dataslices

#--------------load files--------------------

#read file resource refer
rsfile = sys.argv[1]
uifile = open(rsfile,'rb')
uidata = uifile.read()
uifile.close()

#read patch data
rsfile = sys.argv[2]
uifile = open(rsfile,'rb')
patchdata = uifile.read()
uifile.close()


#---------slice resource1---------

dataslicegrp1 = buildslices_data(uidata)
dataslices1 = getdatablock(dataslicegrp1)

dataslicegrp2 = buildslices_data(patchdata)
dataslices2 = getdatablock(dataslicegrp2)

#----------istc data---------------

istcgrp1 = []
istcgrp2 = []

for item in dataslices1:
	if len(item[4])>=4:
		char4 = item[4][0:4]
		if char4 == 'ISTC':
			name = getistcname(item[4])
			item.append(name+'~'+str(item[1]))
			istcgrp1.append(item)
			pass
		pass
	pass
for item in dataslices2:
	if len(item[4])>=4:
		char4 = item[4][0:4]
		if char4 == 'ISTC':
			name = getistcname(item[4])
			item.append(name+'~'+str(item[1]))
			istcgrp2.append(item)
			pass
		pass
	pass


print len(istcgrp1)
print len(istcgrp2)

#------------check differ-------------------
istcgrp1_sorted =  sorted(istcgrp1, key=lambda tup: tup[5])
istcgrp2_sorted =  sorted(istcgrp2, key=lambda tup: tup[5])

i = j =0 

while i<len(istcgrp1_sorted) and j<len(istcgrp2_sorted):

	name1 = getistcname(istcgrp1_sorted[i][4])
	name2 = getistcname(istcgrp2_sorted[j][4])
	if name1 == name2:
		if '@2x' not in name1:
			if len(istcgrp1_sorted[i][4]) != len(istcgrp2_sorted[j][4]):
				print 'len diff ->\t'+ istcgrp1_sorted[i][5] + '\t\t' + istcgrp2_sorted[j][5]
			else:
				if istcgrp1_sorted[i][4] != istcgrp2_sorted[j][4]:
					print 'data diff ->\t'+ istcgrp1_sorted[i][5] + '\t\t' + istcgrp2_sorted[j][5]
					pass
				pass
			pass
		pass
		i = i+1
		j = j+1
	elif name1 < name2:
		i = i+1
	elif name1 > name2:
		j = j+1
	pass

chkoffset = 0
'''
for x in range(0,len(dataslices_sorted)-1):
	chkoffset = dataslices_sorted[x][1]+dataslices_sorted[x][2]
	if dataslices_sorted[x+1][1] != chkoffset:
		print 'discontinue at index '+str(x)+', '+ str(dataslices_sorted[x][1])+'+'+str(dataslices_sorted[x][2]) + ' ~ '+str(dataslices_sorted[x+1][1])
		pass
	chkoffset = dataslices_sorted[x][1]+dataslices_sorted[x][2]
	pass
print '-----------------------'
for x in xrange(0,10):
	print str(dataslices1_sorted[x][1]) + '  ' + str(dataslices1_sorted[x][2])+ '   '+ dataslices1_sorted[x][5]
	pass
print '-----------------------'
for x in xrange(0,10):
	print str(dataslices2_sorted[x][1]) + '  ' + str(dataslices2_sorted[x][2])+ '   '+ dataslices2_sorted[x][5]
	pass
print '-----------------------'
'''
exit()
