# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 25 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class CPGuiFrame1
###########################################################################

class CPGuiFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"CarPatcherGui", pos = wx.DefaultPosition, size = wx.Size( 1024,768 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		BoxSizer0 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel3 = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.buttonLoadSA = wx.Button( self.m_panel3, wx.ID_ANY, u"Load SA", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.buttonLoadSA.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.buttonLoadSA.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.buttonLoadSA.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer8.Add( self.buttonLoadSA, 0, wx.ALL, 5 )
		
		self.buttonLoadPatch = wx.Button( self.m_panel3, wx.ID_ANY, u"Load Patch", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.buttonLoadPatch.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		bSizer8.Add( self.buttonLoadPatch, 0, wx.ALL, 5 )
		
		self.buttonCheck = wx.Button( self.m_panel3, wx.ID_ANY, u"Check", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.buttonCheck, 0, wx.ALL, 5 )
		
		self.buttonDo = wx.Button( self.m_panel3, wx.ID_ANY, u"Do patch", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.buttonDo, 0, wx.ALL, 5 )
		
		self.buttonSave = wx.Button( self.m_panel3, wx.ID_ANY, u"Save list", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.buttonSave, 0, wx.ALL, 5 )
		
		self.buttonLoad = wx.Button( self.m_panel3, wx.ID_ANY, u"Load List", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.buttonLoad, 0, wx.ALL, 5 )
		
		
		self.m_panel3.SetSizer( bSizer8 )
		self.m_panel3.Layout()
		bSizer8.Fit( self.m_panel3 )
		bSizer5.Add( self.m_panel3, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_panel2 = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_grid2 = wx.grid.Grid( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid2.CreateGrid( 5, 5 )
		self.m_grid2.EnableEditing( True )
		self.m_grid2.EnableGridLines( True )
		self.m_grid2.EnableDragGridSize( False )
		self.m_grid2.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid2.EnableDragColMove( False )
		self.m_grid2.EnableDragColSize( True )
		self.m_grid2.SetColLabelSize( 30 )
		self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid2.SetRowSize( 0, 18 )
		self.m_grid2.SetRowSize( 1, 18 )
		self.m_grid2.SetRowSize( 2, 18 )
		self.m_grid2.SetRowSize( 3, 18 )
		self.m_grid2.SetRowSize( 4, 18 )
		self.m_grid2.EnableDragRowSize( True )
		self.m_grid2.SetRowLabelSize( 80 )
		self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer7.Add( self.m_grid2, 1, wx.ALL|wx.EXPAND, 0 )
		
		
		self.m_panel2.SetSizer( bSizer7 )
		self.m_panel2.Layout()
		bSizer7.Fit( self.m_panel2 )
		bSizer5.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 1, wx.ALL|wx.EXPAND, 0 )
		
		
		self.m_panel1.SetSizer( bSizer4 )
		self.m_panel1.Layout()
		bSizer4.Fit( self.m_panel1 )
		BoxSizer0.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( BoxSizer0 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

