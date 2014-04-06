#!/usr/bin/env python

import wx
import wx.grid as grid

from os.path import join as path_join

# Select database library
# Must provide
    #db_save(filename, db)
    #db_load(filename) -> db
    #db_same(filename, db) -> bool
from db_pickle import *
#from db_text import *
#from db_sql import *

def empty_db():
    db = {}
    db['m']  = []   # members
    db['e']  = []   # events
    db['me'] = [[]] # members in events
    db['d']  = []   # meeting dates
    db['md'] = [[]] # attendance, members in dates
    db['f']  = []   # forms
    db['mf'] = [[]] # members' forms
    return db

class Interface(wx.Frame):
    def __init__(self):
        self.filename = ""
        self.dirname = ""
        self.db = empty_db()
        #self.db['m'] = ["Andrew", "Cynthia"]
        #self.db['e'] = ["Tech Bowl", "Chapter Team"]
        self.mode = 'e'
        self.app = wx.App(False)
        wx.Frame.__init__(self, None, title="ChapterMan Title", size=(640, 480), name="ChapterMan Name")
        
        self.icon = wx.Icon("icon.png")
        self.SetIcon(self.icon)
        
        self.status_bar = wx.StatusBar(self)
        self.SetStatusBar(self.status_bar)

        self.file_menu = wx.Menu()
        self.file_new    = self.file_menu.Append(wx.ID_NEW,             "&New",            "Start a file")
        self.file_open   = self.file_menu.Append(wx.ID_OPEN,            "&Open",           "Open a file")
        self.file_revert = self.file_menu.Append(wx.ID_REVERT_TO_SAVED, "Revert to Saved", "Destroy changes since the previous save")
        self.file_save   = self.file_menu.Append(wx.ID_SAVE,            "&Save",           "Save this file")
        self.file_saveas = self.file_menu.Append(wx.ID_SAVEAS,          "Save &As...",     "Save this file with a new name")
        self.file_exit   = self.file_menu.Append(wx.ID_EXIT,            "&Exit",           "Terminate the program")
        self.file_menu.Bind(wx.EVT_MENU, self.on_file_new,    self.file_new)
        self.file_menu.Bind(wx.EVT_MENU, self.on_file_open,   self.file_open)
        self.file_menu.Bind(wx.EVT_MENU, self.on_file_revert, self.file_revert)
        self.file_menu.Bind(wx.EVT_MENU, self.on_file_save,   self.file_save)
        self.file_menu.Bind(wx.EVT_MENU, self.on_file_saveas, self.file_saveas)
        self.file_menu.Bind(wx.EVT_MENU, self.on_exit,        self.file_exit)

        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.file_menu, "&File")
        self.SetMenuBar(self.menu_bar)
        # Add mode functions in menu

        self.tool_bar = self.CreateToolBar()
        self.tool_view = self.tool_bar.AddLabelTool(-1, "View", wx.Bitmap("view.png"))
        self.Bind(wx.EVT_TOOL, self.on_tool_view)
        self.tool_bar.Realize()
        self.SetToolBar(self.tool_bar)
        # Add mode function shortcuts on toolbar

        self.grid = grid.Grid(self)
        #self.grid.SetColLabelValue

        self.update()

        self.Show(True)
        self.app.MainLoop()

    def get_filename(self):
        return path_join(self.dirname, self.filename)

    def on_file_save_maybe(self, event):
    	print("fm")
        if db_same(self.get_filename(), self.db):
            result = wx.ID_OK
        else:
            dlg = wx.MessageDialog(self, "Save file?", "Keep the changes to the file?", wx.YES_NO)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                result = self.on_file_save(event)
            dlg.Destroy()
        return result

    def update(self):
    	print "u*"
        rows = len(self.db['m'])
        cols = len(self.db[self.mode])
        self.grid.Destroy()
        self.grid = grid.Grid(self)
        self.grid.CreateGrid(rows, cols)
        for i in range(rows):
        	self.grid.SetRowLabelValue(i, self.db['m'][i])
        for i in range(cols):
        	self.grid.SetColLabelValue(i, self.db[self.mode][i])

    def on_file_new(self, event):
    	print "fn"
        result = self.on_file_save_maybe(event)
        if (result == wx.ID_OK) or (result == wx.ID_NO):
            self.filename = ""
            self.dirname = ""
            self.db = empty_db()
            self.update()
        return result

    def on_file_open(self, event):
    	print "fo"
        result = self.on_file_save_maybe(event)
        if (result == wx.ID_OK) or (result == wx.ID_NO):
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*", wx.OPEN)
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                self.db = db_load(self.get_filename())
                self.update()
            dlg.Destroy()
        return result

    def on_file_revert(self, event):
    	print "fr"
        if (self.filename != "") and (self.dirname != ""):
            self.db = db_load(self.get_filename())
            self.update()
            result = wx.ID_OK
        else:
            result = wx.ID_NO
        return result

    def on_file_save(self, event):
    	print "fs"
        if (not self.get_filename()):
            result = self.on_file_saveas(event)
        elif db_same(self.get_filename(), self.db):
            result = wx.ID_OK
        else:
            db_save(self.get_filename(), self.db)
            result = wx.ID_OK
        return result

    def on_file_saveas(self, event):
    	print "fa"
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "*", wx.SAVE)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            db_save(self.get_filename(), self.db)
        dlg.Destroy(x)
        return result

    def on_exit(self, event):
    	print "e*"
        result = self.on_file_save_maybe(event)
        if (result == wx.ID_OK) or (result == wx.ID_NO):
            self.Close(True)
        return result

    def on_tool_view(self, event):
        pass


if __name__ == "__main__":
    Interface()