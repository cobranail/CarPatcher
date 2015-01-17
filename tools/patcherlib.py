#osx carfile patcher function library
#by cobranail#gmail.com

import os
import sys
import struct

lib_version = 0.7

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
	return struct.unpack('<I', char4)[0]
	return ord(char4[0]) + ord(char4[1])*256 + ord(char4[2])*65536 + ord(char4[3])*65536*256

def char4tovaluebig(char4):
	return struct.unpack('>I', char4)[0]
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
	return struct.pack('>I',val)
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
	chkname = istcdata[40:40+127]
	sname = chkname.strip('\x00')
	return sname
def getistcsize(istcdata):
	w = char4tovaluelitt(istcdata[12:16])
	h = char4tovaluelitt(istcdata[16:20])
	return (w,h)
	pass

def cookpatchdata(origdata,patchdata):
	'''copy image slices info '''
	'''only modify name , now'''
	#origdata
	block0 = origdata[0:40]
	block1 = origdata[40:168] #name
	block2 = origdata[168:184] # info
	val1 = char4tovaluelitt(block2[0:4])
	block3 = origdata[184: 184+val1] #E903
	val1_1 = char4tovaluebig(block3[4:8])
	block3_1 = block3[0:8+val1_1] #E903~EB03
	block3_2 = block3[8+val1_1:val1] #EB03~MLEC
	val2 = char4tovaluelitt(block2[12:16])
	block4 = origdata[184+val1 : 184+val1+val2] #MLEC

	#patchdata
	pblock0 = patchdata[0:40]
	newname = getistcname(origdata)+'_mod'
	pblock1 = newname+patchdata[40+len(newname):168]
	#pblock1 = patchdata[40:168] #name
	pblock2 = patchdata[168:184] # info
	val1 = char4tovaluelitt(pblock2[0:4])
	pblock3 = patchdata[184: 184+val1] #E903
	val2 = char4tovaluelitt(pblock2[12:16])
	pblock4 = patchdata[184+val1 : 184+val1+val2] #MLEC

	#modify patch
	newpatch = pblock0 + pblock1 + block2[0:12]+pblock2[12:16] + block3 + pblock4
	newpatch = pblock0 + block1 + pblock2 + pblock3 + pblock4
	return newpatch
	pass


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

def compareistcdim(patch1, patch2):
	patch1w = char4tovaluebig(patch1[12:16])
	patch1h = char4tovaluebig(patch1[16:20])
	patch2w = char4tovaluebig(patch2[12:16])
	patch2h = char4tovaluebig(patch2[16:20])
	if patch1w != patch2w or patch1h != patch2h:
		return False
		pass
	pass
	return True


def sliceuidata(uidata):
	#---------slice resource---------

	#slices

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
	tag_data = datachunk2[tag_data_sp: tag_data_sp +4+ 8*tag_data_count]


	gp1 = getresindex3(datachunk2)
	print len(gp1)
	print 'gp2'
	print 'tag_data_sp '+str(tag_data_sp)+', '+str(tag_data_count)
	print len(tag_data)
	gp2 = getresindex3(tag_data)

	#non zero
	gp1nz = []
	for item in gp1:
		if item[2]>0:
			#length > 0
			gp1nz.append(item)
	gp2nz = []
	for item in gp2:
		if item[2]>0:
			#length > 0
			gp2nz.append(item)


	gpc = gp1nz+gp2nz+[[-2, slice3sub_sp, slice3sub_len]]  #non-zero index group
	
	idx = 0

	dataslices = []
	for idxgp in gpc:
		ioffset = idxgp[1]
		ilen = idxgp[2]
		dataslices.append([idx, ioffset, ilen , False ,uidata[ioffset:ioffset+ilen], ''])
		idx = idx+1
		pass

	#check if discontinue
	dataslices_sorted =  sorted(dataslices, key=lambda tup: tup[1])
	chkoffset = 0
	for x in range(0,len(dataslices_sorted)-1):
		chkoffset = dataslices_sorted[x][1]+dataslices_sorted[x][2]
		if dataslices_sorted[x+1][1] != chkoffset:
			print 'discontinue t1 at index '+str(x)+', '+ str(dataslices_sorted[x][1])+'+'+str(dataslices_sorted[x][2]) + ' ~ '+str(dataslices_sorted[x+1][1])
			pass
		chkoffset = dataslices_sorted[x][1]+dataslices_sorted[x][2]
		pass

	print '-----------------------'
	for x in xrange(0,10):
		print str(dataslices_sorted[x][1]) + '  ' + str(dataslices_sorted[x][2])
		pass
	print '-----------------------'
	pass
	return dataslices
	#-------------endof function-------------



def rebuilddata(uidata, dataslices, injectiondata):


	#slices

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
	tag_data = datachunk2[tag_data_sp: tag_data_sp +4+ 8*tag_data_count]


	gp1 = getresindex3(datachunk2)
	print len(gp1)
	print 'gp2'
	print 'tag_data_sp '+str(tag_data_sp)+', '+str(tag_data_count)
	print len(tag_data)
	gp2 = getresindex3(tag_data)

	#non zero
	gp1nz = []
	for item in gp1:
		if item[2]>0:
			#length > 0
			gp1nz.append(item)
	gp2nz = []
	for item in gp2:
		if item[2]>0:
			#length > 0
			gp2nz.append(item)


	gpc = gp1nz+gp2nz+[[-2, slice3sub_sp, slice3sub_len]]

	idx = 0

	dataslices = []
	for idxgp in gpc:
		ioffset = idxgp[1]
		ilen = idxgp[2]
		dataslices.append([idx, ioffset, ilen , False ,uidata[ioffset:ioffset+ilen]])
		idx = idx+1
		pass

	#check if discontinue
	dataslices_sorted =  sorted(dataslices, key=lambda tup: tup[1])
	chkoffset = 0
	for x in range(0,len(dataslices_sorted)-1):
		chkoffset = dataslices_sorted[x][1]+dataslices_sorted[x][2]
		if dataslices_sorted[x+1][1] != chkoffset:
			print 'discontinue t2 at index '+str(x)+', '+ str(dataslices_sorted[x][1])+'+'+str(dataslices_sorted[x][2]) + ' ~ '+str(dataslices_sorted[x+1][1])
			pass
		chkoffset = dataslices_sorted[x][1]+dataslices_sorted[x][2]
		pass

	print '-----------------------'
	for x in xrange(0,0):
		print str(dataslices_sorted[x][1]) + '  ' + str(dataslices_sorted[x][2])
		pass
	print '-----------------------'

	#-------------do patch -------------------------

	sum1 = 0
	sum2 = 0


	for item in injectiondata:
		#item : offset, data
		tidx = locateinjection(dataslices, item[0])
		sum1 = sum1 + dataslices[tidx][2]
		sum2 = sum2 + len(item[1])
		newpatch = item[1]
		newpatch = cookpatchdata(dataslices[tidx][4], item[1]) # only replace name
		if compareistcdim(dataslices[tidx][4], item[1]):	
			pass
		else:
			print '->warning, dim not same->, patch all'
		print 'patch data at : '+ str(dataslices[tidx][1]) + '  length : '+str(dataslices[tidx][2])+'->'+str(len(item[1])) + '  ,  '+getistcname(dataslices[tidx][4])
		dataslices[tidx] = [tidx, dataslices[tidx][1], dataslices[tidx][2], True , newpatch]
		pass

	print str(sum1)+', '+str(sum2)
	#---------------------rebuild uidata--------------------------

	#rebuild data
	dataslices_sorted =  sorted(dataslices, key=lambda tup: tup[1])
	#[idx,  ioffset,  ilen,  False,  uidata[ioffset:ioffset+ilen]]

	header512 = uidata[0:512]

	newdatachunk1 = uidata[0:512]
	offset_tls = [] #offset transfer
	differcount = 0
	vlen = 512
	for ditem in dataslices_sorted:
		ioffset = len(newdatachunk1)
		ilen = len(ditem[4])
		vlen = vlen + ilen
		if ditem[1]>=512:
			if ditem[1]!=ioffset:
				differcount = differcount+1
			offset_tls.append([[ditem[1],ditem[2]],[ioffset,ilen]]) # [[orig_offset, orig_len], [new_offset, new_len]]
			ditem[1] = ioffset
			ditem[2] = ilen
			newdatachunk1 = newdatachunk1+ditem[4]
		else:
			print 'before offset 512, ignore it '+str(ditem[1])
	 	pass 
	print 'differcount : '+str(differcount)
	print 'vlen : '+str(vlen)

	newdatachunk1_len = len(newdatachunk1)

	#rebuild index

	print len(gp1)

	for i in range(len(gp1)):
		pass
		kcount = 0
		rlist = []
		offsettlsemu = range(len(offset_tls))
		#offsettlsemu.reverse()
		for j in offsettlsemu:
			if gp1[i][1] == offset_tls[j][0][0]:
				#match
				gp1[i] = [gp1[i][0], offset_tls[j][1][0], offset_tls[j][1][1]]
				kcount=kcount+1
				rlist.append(offset_tls[j])
				#print 'info '+str(gp1[i][1])+', '+str(gp1[i][2])+' --> '+str(offset_tls[j][1][0]) + ', '+str(offset_tls[j][1][1])
				offset_tls.pop(j)
				break
				pass
		if kcount>1:
			print 'in gp1 kcount > 1 !!!!!!!!!! '
			print rlist
			pass
		pass

	for i in range(len(gp2)):
		kcount = 0;
		for j in range(len(offset_tls)):
			if gp2[i][1] == offset_tls[j][0][0]:
				#match
				gp2[i] = [gp2[i][0], offset_tls[j][1][0], offset_tls[j][1][1]]
				pass
			pass
		if kcount>1:
			print 'in gp2 kcount > 1 !!!!!!!!!!'
			pass
		pass
	for j in range(len(offset_tls)):
		if slice3sub_sp == offset_tls[j][0][0]:
			if slice3sub_sp != offset_tls[j][1][0]:
				print 'more !'
				pass
			pass
		pass




	section2header = datachunk2[0:4]
	section2index = section2header

	for idxitem in gp1:
		section2index = section2index + inttochars(idxitem[1]) + inttochars(idxitem[2])
		pass
	print len(section2index)
	section2index = section2index + tag_data[0:4]

	print len(gp2)
	for idxitem in gp2:
		section2index = section2index + inttochars(idxitem[1]) + inttochars(idxitem[2])
		pass

	section2index = section2index + '\x00'*16

	print len(section2index)

	newdatachunk1 = newdatachunk1[0:16]+inttochars(newdatachunk1_len)+newdatachunk1[20:newdatachunk1_len]

	newuidata = newdatachunk1+section2index

	print 'check new uidata continuious'
	slicedata(newuidata)

	f = open('new.car', 'wb')
	f.write(newuidata)
	f.close()

	print "patch Done!"
	pass




def loadcarfile(carfile):
	#read file resource refer
	uifile = open(carfile ,'rb')
	uidata = uifile.read()
	uifile.close()
	return uidata

def slicedata(uidata):
	dataslices = sliceuidata(uidata)
	return dataslices

def filteristc(dataslices):
	istclist = []
	for item in dataslices:
		if item[4][0:4] == 'ISTC':
			item[5] = getistcname(item[4])+'~'+str(item[1])
			istclist.append(item)
			pass
		pass
	return istclist

def loadpatch(patchfilelist):
	patchlist = []
	for pf in patchfilelist:
		f = open(pf, 'rb')
		data = f.read()
		patchlist.append([0 , data])
		f.close()
		pass
	return patchlist
