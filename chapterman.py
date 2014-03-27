#!/usr/bin/env python

import wx
import wx.grid as grid

class Interface(wx.Frame):
	def __init__(self):
		self.app = wx.App()
		wx.Frame.__init__(self, None, title="ChapterMan Title", size=(640, 480), name="ChapterMan Name")
		
		# self.field
		
		# self.icon = wx.Icon("icon.png", wx.BITMAP_TYPE_ANY, 32, 32)
		# self.SetIcon(self.icon)
		
		self.statusBar = wx.StatusBar(self)
		self.SetStatusBar(self.statusBar)

		self.fileMenu = wx.Menu()
		self.fileNew = self.fileMenu.Append (wx.ID_NEW, "&New", "Start a file")
		self.fileOpen = self.fileMenu.Append (wx.ID_OPEN, "&Open", "Open a file")
		self.fileRevert = self.fileMenu.Append (wx.ID_REVERT_TO_SAVED, "Revert to Saved", "Destroy changes since the previous save")
		self.filePrint = self.fileMenu.Append (wx.ID_PRINT, "&Print", "Print the file")
		self.fileSave = self.fileMenu.Append (wx.ID_SAVE, "&Save", "Save this file")
		self.fileSaveAs = self.fileMenu.Append (wx.ID_SAVEAS, "Save &As...", "Save this file with a new name")
		self.fileExit = self.fileMenu.Append (wx.ID_EXIT, "&Exit", "Terminate the program")
		self.Bind (wx.EVT_MENU, self.OnFileNew, self.fileNew)
		self.Bind (wx.EVT_MENU, self.OnFileOpen, self.fileOpen)
		self.Bind (wx.EVT_MENU, self.OnFileRevert, self.fileRevert)
		self.Bind (wx.EVT_MENU, self.OnFileSave, self.fileSave)
		self.Bind (wx.EVT_MENU, self.OnFileSaveAs, self.fileSaveAs)
		self.Bind (wx.EVT_MENU, self.OnExit, self.fileExit)

		self.menuBar = wx.MenuBar()
		self.menuBar.Append(self.fileMenu, "&File")
		self.SetMenuBar(self.menuBar)

		self.toolBar = wx.ToolBar(self)
		#self.toolBar.AddTool
		self.toolBar.Realize()
		self.SetToolBar(self.toolBar)

		self.grid = grid.Grid(self)
		self.grid.CreateGrid(20, 20)
		#self.grid.SetColLabelValue
		
		self.Show(True)
		self.app.MainLoop()

	def OnFileNew(self, event):
		pass

	def OnFileOpen(self, event):
		pass

	def OnFileRevert(self, event):
		pass

	def OnFileSave(self, event):
		pass

	def OnFileSaveAs(self, event):
		pass

	def OnExit(self, event):
		pass


if __name__ == "__main__":
	Interface()