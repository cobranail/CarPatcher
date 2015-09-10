# -*- coding: utf-8 -*- 
#!/bin/python
#istc batch mixer tool, create istc files from tiff files and a pattern
#by cobranail#gmail.com
#version 0.5
#add cut-out function

import wx
import sys
import struct

import combine

if __name__ == '__main__':
	patfile = sys.argv[1]
	listfile = sys.argv[2]
	ctout = [int(sys.argv[3]), int(sys.argv[4])]

	app = wx.App() 

	f = open(listfile, 'r')
	txt = f.readlines()
	f.close()

	for line in txt:
		header = combine.loadpattenheader(patfile)
		image = combine.loadimage2data(line.strip('\r\n'), alpha = '\x00', cutout = ctout) #default alpha
		newdata = combine.newistc(header, image)
		outfile = 'istc~'+line.strip('\r\n')
		f = open(outfile,'wb')
		f.write(newdata)
		f.close()
		pass
