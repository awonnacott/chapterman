#!/usr/bin/env python

import wx
import wx.grid as grid

class Interface(wx.Frame):
	def __init__(self):
		self.app = wx.App()
		wx.Frame.__init__(self, None, title="ChapterMan Title", size=(640, 480), name="ChapterMan Name")
		
		self.icon = wx.Icon("icon.png")
		self.SetIcon(self.icon)
		
		self.statusBar = wx.StatusBar(self)
		self.SetStatusBar(self.statusBar)

		self.fileMenu = wx.Menu()
		self.fileNew = self.fileMenu.Append(wx.ID_NEW, "&New", "Start a file")
		self.fileOpen = self.fileMenu.Append(wx.ID_OPEN, "&Open", "Open a file")
		self.fileRevert = self.fileMenu.Append(wx.ID_REVERT_TO_SAVED, "Revert to Saved", "Destroy changes since the previous save")
		self.fileSave = self.fileMenu.Append(wx.ID_SAVE, "&Save", "Save this file")
		self.fileSaveAs = self.fileMenu.Append(wx.ID_SAVEAS, "Save &As...", "Save this file with a new name")
		self.fileExit = self.fileMenu.Append(wx.ID_EXIT, "&Exit", "Terminate the program")
		self.Bind(wx.EVT_MENU, self.onFileNew, self.fileNew)
		self.Bind(wx.EVT_MENU, self.onFileOpen, self.fileOpen)
		self.Bind(wx.EVT_MENU, self.onFileRevert, self.fileRevert)
		self.Bind(wx.EVT_MENU, self.onFileSave, self.fileSave)
		self.Bind(wx.EVT_MENU, self.onFileSaveAs, self.fileSaveAs)
		self.Bind(wx.EVT_MENU, self.onExit, self.fileExit)

		self.menuBar = wx.MenuBar()
		self.menuBar.Append(self.fileMenu, "&File")
		self.SetMenuBar(self.menuBar)

		self.toolBar = self.CreateToolBar()
		self.toolView = self.toolBar.AddLabelTool(-1, "View", wx.Bitmap("view.png"))
		self.Bind(wx.EVT_TOOL, self.onToolView)
		self.toolBar.Realize()
		self.SetToolBar(self.toolBar)

		self.grid = grid.Grid(self)
		self.grid.CreateGrid(20, 20)
		#self.grid.SetColLabelValue
		
		self.Show(True)
		self.app.MainLoop()

	def onFileNew(self, event):
		pass

	def onFileOpen(self, event):
		pass

	def onFileRevert(self, event):
		pass

	def onFileSave(self, event):
		pass

	def onFileSaveAs(self, event):
		pass

	def onExit(self, event):
		pass

	def onToolView(self, event):
		pass


if __name__ == "__main__":
	Interface()