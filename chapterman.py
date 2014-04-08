#!/usr/bin/env python

import wx
import wx.grid as grid

from os.path import join as path_join

# Select database library
# Must provide
#save(filename, db)
#load(filename) -> db
#same(filename, db) -> bool
import db_pickle as db
#import db_text as db
#import db_sql as db


def empty_db():
    db = {}
    db['m']  = []    # members
    db['e']  = []    # events
    db['me'] = [[]]  # members in events
    db['a']  = []    # meeting dates
    db['ma'] = [[]]  # attendance, members in dates
    db['f']  = []    # forms
    db['mf'] = [[]]  # members' forms
    return db


class Interface(wx.Frame):
    def __init__(self):
        self.filename = ""
        self.dirname = ""
        self.db = empty_db()
        self.db['m'] = ["Andrew", "Cynthia", "Kyle"]
        self.db['e'] = ["Tech Bowl", "Chapter Team"]
        self.db['me'] = [["yes", "apples"], ["foobar", "cenicolia"], ["peru", "mango"]]
        self.db['a'] = ["4/4", "4/5"]
        self.db['ma'] = [["yes", "apples"], ["foobar", "cenicolia"], ["peru", "mango"]]
        self.db['f'] = ["States Permission", "States Meds"]
        self.db['mf'] = [["yes", "apples"], ["foobar", "cenicolia"], ["peru", "mango"]]
        self.mode = 'e'
        self.app = wx.App(False)
        wx.Frame.__init__(self, None, title="ChapterMan", size=(640, 480), name="ChapterMan")

        self.icon = wx.Icon("icon.png", wx.BITMAP_TYPE_ANY)
        self.SetIcon(self.icon)

        self.status_bar = wx.StatusBar(self)
        self.SetStatusBar(self.status_bar)

        self.file_menu   = wx.Menu()
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

        self.edit_menu = wx.Menu()
        self.edit_m    = self.edit_menu.Append(-1, "Members",  "Edit Membership List")
        self.edit_e    = self.edit_menu.Append(-1, "Events",   "Edit List of Events")
        self.edit_a    = self.edit_menu.Append(-1, "Meetings", "Edit Meeting Days")
        self.edit_f    = self.edit_menu.Append(-1, "Forms",    "Edit List of Forms")
        self.edit_menu.Bind(wx.EVT_MENU, self.on_edit_m, self.edit_m)
        self.edit_menu.Bind(wx.EVT_MENU, self.on_edit_e, self.edit_e)
        self.edit_menu.Bind(wx.EVT_MENU, self.on_edit_a, self.edit_a)
        self.edit_menu.Bind(wx.EVT_MENU, self.on_edit_f, self.edit_f)

        self.view_menu = wx.Menu()
        self.view_e    = self.view_menu.Append(-1, "Events",     "Event View")
        self.view_a    = self.view_menu.Append(-1, "Attendance", "Meeting View")
        self.view_f    = self.view_menu.Append(-1, "Forms",      "Form View")
        self.view_menu.Bind(wx.EVT_MENU, self.on_view_e, self.view_e)
        self.view_menu.Bind(wx.EVT_MENU, self.on_view_a, self.view_a)
        self.view_menu.Bind(wx.EVT_MENU, self.on_view_f, self.view_f)

        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.file_menu, "&File")
        self.menu_bar.Append(self.edit_menu, "&Edit")
        self.menu_bar.Append(self.view_menu, "&View")
        self.SetMenuBar(self.menu_bar)

        self.tool_bar = self.CreateToolBar()
        self.tool_view = self.tool_bar.AddLabelTool(-1, "View", wx.Bitmap("view.png"))
        self.Bind(wx.EVT_TOOL, self.on_tool_view)
        self.tool_bar.Realize()
        self.SetToolBar(self.tool_bar)

        self.grid = grid.Grid(self)

        self.update()

        self.Show(True)
        self.app.MainLoop()

    def get_filename(self):
        return path_join(self.dirname, self.filename)

    def fromgrid(self):
        rows = len(self.db['m'])
        cols = len(self.db[self.mode])
        for i in range(rows):
            for j in range(cols):
                self.db['m'+self.mode][i][j] = self.grid.GetCellValue(i, j)

    def update(self):
        rows = len(self.db['m'])
        cols = len(self.db[self.mode])
        self.grid.Destroy()
        self.grid = grid.Grid(self)
        self.grid.CreateGrid(rows, cols)
        for i in range(rows):
            self.grid.SetRowLabelValue(i, self.db['m'][i])
        for i in range(cols):
            self.grid.SetColLabelValue(i, self.db[self.mode][i])
        for i in range(rows):
            for j in range(cols):
                self.grid.SetCellValue(i, j, self.db['m'+self.mode][i][j])
        self.grid.AutoSize()

    def set_mode(self, mode):
        self.fromgrid()
        if mode == 'e':
            self.mode = 'e'
        elif mode == 'a':
            self.mode = 'a'
        elif mode == 'f':
            self.mode = 'f'
        self.update()

    def delete_member(self, member):
        self.fromgrid()
        member_id = self.db['m'].index(member)
        self.db['m'].pop(member_id)
        self.db['me'].pop(member_id)
        self.db['a'].pop(member_id)
        self.db['ma'].pop(member_id)
        self.db['f'].pop(member_id)
        self.db['mf'].pop(member_id)
        self.update()

    def get_events(self, mebmer):
        self.fromgrid()
        member_id = self.db['m'].index(member)
        return [event for event in self.db['e'][member_id] if event != ""]

    def get_attendance(self, member):
        self.fromgrid()
        member_id = self.db['m'].index(member)
        present = len([day for day in self.db['a'][member_id] if day != ""])
        total = len(self.db['a'][member_id])
        return present/total

    def add_member(self, new_member):
        self.fromgrid()
        self.db['m'].append(new_member)
        self.db['me'].append(len(self.db['e'])*[""])
        self.db['ma'].append(len(self.db['a'])*[""])
        self.db['mf'].append(len(self.db['f'])*[""])
        self.update()

    def on_file_save_maybe(self, event):
        if db.same(self.get_filename(), self.db):
            result = wx.ID_OK
        else:
            dlg = wx.MessageDialog(self, "Save file?", "Keep the changes to the file?", wx.YES_NO)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                result = self.on_file_save(event)
            dlg.Destroy()
        return result

    def on_file_new(self, event):
        result = self.on_file_save_maybe(event)
        if (result == wx.ID_OK) or (result == wx.ID_NO):
            self.filename = ""
            self.dirname = ""
            self.db = empty_db()
            self.update()
        return result

    def on_file_open(self, event):
        result = self.on_file_save_maybe(event)
        if (result == wx.ID_OK) or (result == wx.ID_NO):
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*", wx.OPEN)
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                self.db = db.load(self.get_filename())
                self.update()
            dlg.Destroy()
        return result

    def on_file_revert(self, event):
        if (self.filename != "") and (self.dirname != ""):
            self.db = db.load(self.get_filename())
            self.update()
            result = wx.ID_OK
        else:
            result = wx.ID_NO
        return result

    def on_file_save(self, event):
        if not self.get_filename():
            result = self.on_file_saveas(event)
        elif db.same(self.get_filename(), self.db):
            result = wx.ID_OK
        else:
            self.fromgrid()
            db.save(self.get_filename(), self.db)
            result = wx.ID_OK
        return result

    def on_file_saveas(self, event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "*", wx.SAVE)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.fromgrid()
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            db.save(self.get_filename(), self.db)
        dlg.Destroy()
        return result

    def on_edit_m(self, event):
        edit_m_frame = wx.Frame(self, -1, title="Member List", size=(640, 480), name="Member List")

        edit_m_sizer = wx.BoxSizer(wx.VERTICAL)
        edit_m_sizers = len(self.db['m'])*[None]
        edit_m_buttons = len(self.db['m'])*[None]
        
        edit_m_top = wx.BoxSizer(wx.HORIZONTAL)
        edit_m_top.Add(wx.StaticText(edit_m_frame, -1, "Name"), 5)
        edit_m_top.Add(wx.StaticText(edit_m_frame, -1, "Events"), 5)
        edit_m_top.Add(wx.StaticText(edit_m_frame, -1, "Attendance"), 5)
        edit_m_sizer.Add(edit_m_top)

        def button(member):
            def on_button(event):
                edit_m_sizer.Remove(edit_m_sizers[member])
                self.delete_member(member)
            return on_button

        def add_member_from_text(textctrl):
            def on_button(event):
                new_member = textctrl.GetValue()
                textctrl.Clear()
                self.add_member(new_member)
                edit_m_sizers[new_member] = wx.BoxSizer(wx.HORIZONTAL)
                edit_m_sizers[new_member].Add(wx.StaticText(edit_m_frame, -1, new_member), 5)
                edit_m_sizers[new_member].Add(wx.StaticText(edit_m_frame, -1, 0, 5)
                edit_m_sizers[new_member].Add(wx.StaticText(edit_m_frame, -1, 0, 5)
                edit_m_buttons[new_member] = wx.Button(edit_m_frame, -1, "-")
                edit_m_sizers[new_member].Add(edit_m_buttons[new_member])
                edit_m_buttons[new_member].Bind(wx.EVT_BUTTON, button(new_member))
                edit_m_sizer.Insert(-1, edit_m_sizers[new_member], 1)
            return on_button

        member_id = 0
        for member in self.db['m']:
            edit_m_sizers[member] = wx.BoxSizer(wx.HORIZONTAL)
            edit_m_sizers[member].Add(wx.StaticText(edit_m_frame, -1, member), 5)
            edit_m_sizers[member].Add(wx.StaticText(edit_m_frame, -1, 0, 5)
            edit_m_sizers[member].Add(wx.StaticText(edit_m_frame, -1, 0, 5)
            edit_m_buttons[member] = wx.Button(edit_m_frame, member_id, "-")
            edit_m_sizers[member].Add(edit_m_buttons[member])
            edit_m_buttons[member].Bind(wx.EVT_BUTTON, button(member))
            edit_m_sizer.Add(edit_m_sizers[member], 1)
            member_id += 1

        edit_m_bottom = wx.BoxSizer(wx.HORIZONTAL)
        edit_m_display = wx.TextCtrl(edit_m_frame, -1, '',  style=wx.TE_RIGHT)
        edit_m_button_bottom = wx.Button(edit_m_frame, -1, "+")
        edit_m_button_bottom.Bind(wx.EVT_BUTTON, self.add_member_from_text(edit_m_display))
        edit_m_bottom.Add(edit_m_display, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 4)
        edit_m_sizer.Add(edit_m_bottom)
        edit_m_frame.SetSizer(edit_m_sizer)
        edit_m_frame.Show()

    def on_edit_e(self, event):
        self.set_mode("e")

    def on_edit_a(self, event):
        self.set_mode("a")

    def on_edit_f(self, event):
        self.set_mode("f")

    def on_view_e(self, event):
        self.set_mode("e")

    def on_view_a(self, event):
        self.set_mode("a")

    def on_view_f(self, event):
        self.set_mode("f")

    def on_exit(self, event):
        result = self.on_file_save_maybe(event)
        if (result == wx.ID_OK) or (result == wx.ID_NO):
            self.Close(True)
        return result

    def on_tool_view(self, event):
        pass


if __name__ == "__main__":
    Interface()