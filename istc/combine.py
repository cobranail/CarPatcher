# -*- coding: utf-8 -*- 
#!/bin/python

#by cobranail#gmail.com

#ver = 0.5
#add cut-out function. retina resource is not really 2x than non-retina resource, it may be slimed. 

import wx
import sys
import struct


def str2intle(s):
	n = struct.unpack('<i', s)[0]
	return n

def int2strle(i):
	s = struct.pack('<i', i)
	return s

def not_in_cutout(v,cutout):
	if cutout[0]<=v<cutout[0]+cutout[1]:
		return False
	else:
		return True

def loadimage2data(file, alpha, cutout):
	#load tiff imagefile, return a byte data
	img = wx.Bitmap(file, wx.BITMAP_TYPE_ANY).ConvertToImage()
	w = img.GetWidth()
	h = img.GetHeight()
	rgbdata = img.GetData()
	alphadata = None
	if img.HasAlpha():
		alphadata = img.GetAlphaData()
	else:
		#print file+' image no alphadata'
		#alpha = '\xFF'
		alphadata = alpha*(w*h)
	
	pbuf = ''
	outdata = ''
	for i in range(0,w*h):
		if not_in_cutout(i%w, cutout):
			pbuf = rgbdata[i*3 : i*3+3] + alphadata[i : i+1]
			outdata = outdata+pbuf
	print len(outdata)
	return [w-cutout[1],h,outdata]

def loadpattenheader(file):
	#load slice patten
	f = open(file, 'rb')
	patdata = f.read()
	f.close()
	ps1 = patdata[0:168] #header
	#w,h
	pw = str2intle(ps1[12:16])
	ph = str2intle(ps1[16:20])
	#
	ps2 = patdata[168:184] #data length
	len1 = str2intle(ps2[0:4])
	ps3 = patdata[168+16 : 168+16+len1] #slice, and other info
	
	return [pw,ph, ps1,ps2,ps3]

def newistc(g_header, g_image):
	print g_header[0],g_header[1],g_image[0], g_image[1]
	if g_header[0] == g_image[0] and g_header[1] == g_image[1]:
		#same w,h 
		ps1 = g_header[2]
		ps2 = g_header[3]
		ps3 = g_header[4]
		mlecdata = g_image[2]
		mlecheader = '\x4D\x4C\x45\x43\x00\x00\x00\x00\x00\x00\x00\x00' + int2strle(len(mlecdata))  #16 byte
		mlec = mlecheader + mlecdata
		newdata = ps1+ps2[0:12]+int2strle(len(mlec))+ps3+mlec
		return newdata
		pass
	else:
		print "error"
	pass

if __name__ == '__main__':
	patfile = sys.argv[1]
	imagerawfile = sys.argv[2]
	outfile = sys.argv[3]
	app = wx.App() 

	header = loadpattenheader(patfile)
	image = loadimage2data(imagerawfile)
	newdata = newistc(header, image, [0,0])

	f = open(outfile,'wb')
	f.write(newdata)
	f.close()

