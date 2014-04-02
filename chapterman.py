#!/usr/bin/env python

import wx
import wx.grid as grid

class Interface(wx.Frame):
	def __init__(self):
		self.app = wx.App()
		wx.Frame.__init__(self, None, title="ChapterMan Title", size=(640, 480), name="ChapterMan Name")
		
		self.icon = wx.Icon("icon.png")
		self.SetIcon(self.icon)
		
		self.status_bar = wx.StatusBar(self)
		self.SetStatusBar(self.status_bar)

		self.file_menu = wx.Menu()
		self.file_new = self.fileMenu.Append(wx.ID_NEW, "&New", "Start a file")
		self.file_open = self.fileMenu.Append(wx.ID_OPEN, "&Open", "Open a file")
		self.file_revert = self.fileMenu.Append(wx.ID_REVERT_TO_SAVED, "Revert to Saved", "Destroy changes since the previous save")
		self.file_save = self.fileMenu.Append(wx.ID_SAVE, "&Save", "Save this file")
		self.file_saveas = self.fileMenu.Append(wx.ID_SAVEAS, "Save &As...", "Save this file with a new name")
		self.file_exit = self.fileMenu.Append(wx.ID_EXIT, "&Exit", "Terminate the program")
		self.Bind(wx.EVT_MENU, self.on_file_new, self.file_new)
		self.Bind(wx.EVT_MENU, self.on_file_open, self.file_open)
		self.Bind(wx.EVT_MENU, self.on_file_revert, self.file_revert)
		self.Bind(wx.EVT_MENU, self.onFileSave, self.file_save)
		self.Bind(wx.EVT_MENU, self.onFileSaveAs, self.file_saveas)
		self.Bind(wx.EVT_MENU, self.onExit, self.file_exit)

		self.menu_bar = wx.MenuBar()
		self.menu_bar.Append(self.fileMenu, "&File")
		self.SetMenuBar(self.menu_bar)

		self.tool_bar = self.CreateToolBar()
		self.tool_view = self.tool_bar.AddLabelTool(-1, "View", wx.Bitmap("view.png"))
		self.Bind(wx.EVT_TOOL, self.onToolView)
		self.tool_bar.Realize()
		self.SetToolBar(self.tool_bar)

		self.grid = grid.Grid(self)
		self.grid.CreateGrid(20, 20)
		#self.grid.SetColLabelValue
		
		self.Show(True)
		self.app.MainLoop()

	def on_file_new(self, event):
		pass

	def on_file_open(self, event):
		pass

	def on_file_revert(self, event):
		pass

	def on_file_save(self, event):
		pass

	def on_file_saveas(self, event):
		pass

	def on_exit(self, event):
		pass

	def on_tool_view(self, event):
		pass


if __name__ == "__main__":
	Interface()