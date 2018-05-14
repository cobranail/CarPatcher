#!/bin/python
#carfile patcher wxpython gui
#by cobranail#gmail.com
#ver 0.8
import wx
import sys
import os

import noname
import patcherlib

main_frm = None

carslicedata = []
global patchdatalist
global uidata
global dataslices
global istcslicedata
global patchfiles
patchdatalist = []
uidata = ''
dataslices = []
istcslicedata = []
patchfiles = []

def funcLoadSA(self):

	global patchdatalist
	global uidata
	global dataslices
	global istcslicedata
	dlg = wx.FileDialog(
		main_frm,
		message="Choose a file",
		defaultDir=os.getcwd(),
		defaultFile="",
		style=wx.FD_OPEN | wx.FD_CHANGE_DIR
		)

	# Show the dialog and retrieve the user response. If it is the OK response,
	# process the data.
	if dlg.ShowModal() == wx.ID_OK:
		# This returns a Python list of files that were selected.
		paths = dlg.GetPaths()
		carfile = paths[0]
		uidata = patcherlib.loadcarfile(carfile)
		dataslices = patcherlib.slicedata(uidata)
		istcslicedata = patcherlib.filteristc(dataslices)
		istcslicedata_sorted =  sorted(istcslicedata, key=lambda tup: tup[5])
		ext = len(istcslicedata_sorted)
		print 'istc count: ' + str(ext)
		#clear old rows
		r = main_frm.m_grid2.GetNumberRows()
		if r>0:
			main_frm.m_grid2.DeleteRows(numRows = r)
		#add new rows
		main_frm.m_grid2.AppendRows(numRows = ext)
		for i in range(ext):
			fn = patcherlib.getistcname(istcslicedata_sorted[i][4])
			if len(istcslicedata_sorted[i][4])<=132:
				fn = istcslicedata_sorted[i][5].split('~')[0]
			#print istcslicedata_sorted[i][1]
			main_frm.m_grid2.SetCellValue(i, 0, fn)
			main_frm.m_grid2.SetCellValue(i, 1, str(istcslicedata_sorted[i][1]))
			size = patcherlib.getistcsize(istcslicedata_sorted[i][4])
			main_frm.m_grid2.SetCellValue(i, 2, str(size[0])+'x'+str(size[1]))
			pass
	pass


	r = main_frm.m_grid2.GetNumberRows()
	c = main_frm.m_grid2.GetNumberCols()
	#main_frm.m_grid2.AppendRows(numRows = 10)
	r = main_frm.m_grid2.GetNumberRows()
	c = main_frm.m_grid2.GetNumberCols()

	#cell = main_frm.m_grid2.GetCellEditor(1,2)
	#main_frm.m_grid2.SetCellValue(1,2,'asdfg1223')
	for i in range(r):
		#main_frm.m_grid2.SetCellValue(i, 0, 'asdf1234.range')
		#main_frm.m_grid2.SetCellValue(i, 1,  str(i*5+1))
		pass
	pass



def funcLoadPatch(self):
	global patchdatalist
	global uidata
	global dataslices
	global istcslicedata
	global patchfiles
	dlg = wx.FileDialog(
		main_frm,
		message="Choose a file",
		defaultDir=os.getcwd(),
		defaultFile="",
		style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
		)

	# Show the dialog and retrieve the user response. If it is the OK response,
	# process the data.
	if dlg.ShowModal() == wx.ID_OK:
		# This returns a Python list of files that were selected.
		paths = dlg.GetPaths()
		selrow = main_frm.m_grid2.GetGridCursorRow()
		selcol = main_frm.m_grid2.GetGridCursorCol()
		print selrow
		for fn in paths:
			f = open(fn, 'rb')
			data = f.read()
			f.close()
			#soff = main_frm.m_grid2.GetCellValue(selrow, 1)
			#ioff = int(soff)
			#patchdatalist.append([ioff, data])
			main_frm.m_grid2.SetCellValue(selrow, 3, fn)
			main_frm.m_grid2.SetCellValue(selrow, 4, str(len(data)))
			selrow = selrow+1
	pass


def checklist(self):
	global patchdatalist
	global uidata
	global dataslices
	global istcslicedata
	global patchfiles

	print len(uidata)
	print len(dataslices)
	print len(istcslicedata)
	print len(patchdatalist)

	patchdatalist = []
	r = main_frm.m_grid2.GetNumberRows()
	for i in range(r):
		slicename = main_frm.m_grid2.GetCellValue(i, 0)
		patchname = main_frm.m_grid2.GetCellValue(i, 3)
		if slicename != '' and patchname != '':
			#not a empty cell
			f = open(patchname, 'rb')
			data = f.read()
			f.close()
			soff = main_frm.m_grid2.GetCellValue(i, 1)
			ioff = int(soff)
			patchdatalist.append([ioff, data])
			pass
		pass
	pass
	print 'checked patches : '+str(len(patchdatalist))

def dopatch(self):
	global patchdatalist
	global uidata
	global dataslices
	global istcslicedata
	print "start"
	patcherlib.rebuilddata(uidata, dataslices, patchdatalist)

	pass

def savelist(self):
	listsave = []
	r = main_frm.m_grid2.GetNumberRows()
	for i in range(r):
		slicename = main_frm.m_grid2.GetCellValue(i, 0)
		patchname = main_frm.m_grid2.GetCellValue(i, 3)
		if patchname != '':
			listsave.append(str(i)+'\t\t'+patchname+'\n')
			pass
		pass
	pass
	dlg = wx.FileDialog(
		main_frm,
		message="Choose a list file",
		defaultDir=os.getcwd(),
		defaultFile="listsv.txt",
		style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		)

	# Show the dialog and retrieve the user response. If it is the OK response,
	# process the data.
	if dlg.ShowModal() == wx.ID_OK:
		# This returns a Python list of files that were selected.
		paths = dlg.GetPath()
		print paths
		listfile = paths
		f = open(listfile, 'w')
		for line in listsave:
			f.write(line)
			pass
		f.close()
		print str(len(listsave)) + ' lines saved'
	pass

def loadlist(self):
	listload = []
	r = main_frm.m_grid2.GetNumberRows()

	dlg = wx.FileDialog(
		main_frm,
		message="Choose a list file",
		defaultDir=os.getcwd(),
		defaultFile="listsv.txt",
		style=wx.FD_OPEN | wx.FD_CHANGE_DIR
		)

	# Show the dialog and retrieve the user response. If it is the OK response,
	# process the data.
	if dlg.ShowModal() == wx.ID_OK:
		# This returns a Python list of files that were selected.
		paths = dlg.GetPaths()
		listfile = paths[0]
		f = open(listfile, 'r')
		text = f.readlines()
		f.close()
		for line in text:
			ss = line.strip().split('\t\t')
			idx = int(ss[0])
			if idx<r:
				main_frm.m_grid2.SetCellValue(idx, 3 , ss[1])
				pass
			pass
		pass
		print str(len(text)) + ' lines loaded'

	pass


app = wx.App()
main_frm = noname.CPGuiFrame1(None)

main_frm.m_grid2.SetColSize(0, 500)
main_frm.m_grid2.SetColSize(3, 500)
#clear old rows
r = main_frm.m_grid2.GetNumberRows()
main_frm.m_grid2.DeleteRows(numRows = r)
#set col labels
main_frm.m_grid2.SetColLabelValue(0, 'carfile istc')
main_frm.m_grid2.SetColLabelValue(1, 'offset addr')
main_frm.m_grid2.SetColLabelValue(2, 'w h')
main_frm.m_grid2.SetColLabelValue(3, 'patch')
main_frm.m_grid2.SetColLabelValue(4, 'patch wh')

main_frm.buttonLoadSA.Bind( wx.EVT_BUTTON, funcLoadSA )
main_frm.buttonLoadPatch.Bind( wx.EVT_BUTTON, funcLoadPatch )
main_frm.buttonCheck.Bind( wx.EVT_BUTTON, checklist )
main_frm.buttonDo.Bind( wx.EVT_BUTTON, dopatch )
main_frm.buttonSave.Bind( wx.EVT_BUTTON, savelist )
main_frm.buttonLoad.Bind( wx.EVT_BUTTON, loadlist )

main_frm.Show()
app.MainLoop()
