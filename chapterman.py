#!/usr/bin/env python

import wx
import wx.grid as grid
import os

# Select database library
# Must provide
#save(filename, db)
#load(filename) -> db
#same(filename, db) -> bool
import db_pickle as db
#import db_text as db
#import db_sql as db

class Mode:
    def __init__(self, cid, name, title, col, cols, new_vals, get_vals):
        self.cid      = cid
        self.name     = name
        self.title    = title
        self.col      = col
        self.cols     = cols
        self.new_vals = new_vals
        self.get_vals = get_vals

class Interface(wx.Frame):
    def __init__(self):
        self.filename = "default.p"
        self.dirname = os.path.dirname(os.path.realpath(__file__))
        self.db = db.load(self.get_filename())
        self.mdb = []

        # Create mode object for member type
        m_new_vals = {}
        m_get_vals = {}
        m_new_vals["Name"]       = lambda member : member
        m_get_vals["Name"]       = lambda member : member
        m_new_vals["Events"]     = lambda member : "0"
        m_get_vals["Events"]     = lambda member : str(len(self.get_events(member)))
        m_new_vals["Attendance"] = lambda member : "0"
        m_get_vals["Attendance"] = lambda member : self.get_attendance(member)
        member = Mode('m', "Members", "Membership List", False, ["Name", "Events", "Attendance"], m_new_vals, m_get_vals)
        self.mdb.append(member)

        # Create mode object for event type
        e_new_vals = {}
        e_get_vals = {}
        e_new_vals["Name"]       = lambda event : event
        e_get_vals["Name"]       = lambda event : event
        e_new_vals["Members"]    = lambda event : "0"
        e_get_vals["Members"]    = lambda event : str(len(self.get_members(event)))
        event = Mode('e', "Events", "Event List", True, ["Name", "Members"], e_new_vals, e_get_vals)
        self.mdb.append(event)

        # Create mode object for meeting type
        a_new_vals = {}
        a_get_vals = {}
        a_new_vals["Date"]       = lambda date : date
        a_get_vals["Date"]       = lambda date : date
        a_new_vals["Attendance"] = lambda date : "0"
        a_get_vals["Attendance"] = lambda date : self.get_date_attendance(date)
        meeting = Mode('a', "Meetings", "Meeting List", True, ["Date", "Attendance"], a_new_vals, a_get_vals)
        self.mdb.append(meeting)

        # Create mode object for form type
        f_new_vals = {}
        f_get_vals = {}
        f_new_vals["Form"]       = lambda form : form
        f_get_vals["Form"]       = lambda form : form
        form = Mode('f', "Forms", "Form List", True, ["Form"], f_new_vals, f_get_vals)
        self.mdb.append(form)

        self.mode = 'e'
        self.app = wx.App(False)
        wx.Frame.__init__(self, None, title="ChapterMan", size=(640, 480), name="ChapterMan")

        self.icon = wx.Icon("logo.png", wx.BITMAP_TYPE_ANY)
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
        self.edit = {}
        for mode in self.mdb:
            self.edit[mode.cid] = self.edit_menu.Append(-1, mode.name, "Edit " + mode.title)
            self.edit_menu.Bind(wx.EVT_MENU, self.on_edit(mode), self.edit[mode.cid])

        self.view_menu = wx.Menu()
        self.view = {}
        for mode in self.mdb:
            if mode.col:
                self.view[mode.cid] = self.view_menu.Append(-1, mode.name, mode.title)
                self.view_menu.Bind(wx.EVT_MENU, self.on_view(mode), self.view[mode.cid])

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

        self.SetBackgroundColour(wx.WHITE)

        self.Show(True)
        self.app.MainLoop()

    def get_filename(self):
        #return self.dirname + "/" + self.filename
        return os.path.join(self.dirname, self.filename)

    def fromgrid(self):
        rows = len(self.db['m'])
        cols = len(self.db[self.mode])
        for i in range(rows):
            for j in range(cols):
                self.db['m'+self.mode][i][j] = self.grid.GetCellValue(i, j).rstrip()

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
        self.mode = mode.cid
        self.update()

    def get_events(self, member):
        self.fromgrid()
        member_id = self.db['m'].index(member)
        return [event for event in self.db['me'][member_id] if event != ""]

    def get_attendance(self, member):
        self.fromgrid()
        member_id = self.db['m'].index(member)
        present = len([day for day in self.db['ma'][member_id] if day != ""])
        total = len(self.db['a'])
        if total == 0: return 0
        return str(10000*present/total/100.0)+"%" # Weird divisions to round result

    def get_date_attendance(self, date):
        self.fromgrid()
        date_id = self.db['a'].index(date)
        present = len([member for member in self.db['ma'] if member[date_id] != ""])
        total = len(self.db['a'])
        if total == 0: return 0
        return str(10000*present/total/100.0)+"%" # Weird divisions to round result

    def get_members(self, event):
        self.fromgrid()
        event_id = self.db['e'].index(event)
        member_id = 0
        members = []
        for member in self.db['m']:
            if self.db['me'][member_id][event_id] != "":
                members.append(member)
            member_id += 1
        return members

    def add_item(self, new_item, mode):
        if mode == 'm':
            self.fromgrid()
            self.db[mode].append(new_item)
            self.db[mode+'e'].append(len(self.db['e'])*[""])
            self.db[mode+'a'].append(len(self.db['a'])*[""])
            self.db[mode+'f'].append(len(self.db['f'])*[""])
            self.update()
        else:
            self.fromgrid()
            self.db[mode].append(new_item)
            for member in self.db['m'+mode]:
                member.append("")
            self.update()

    def delete_item(self, item, mode):
        if mode == 'm':
            self.fromgrid()
            item_id = self.db[mode].index(item)
            self.db[mode].pop(item_id)
            self.db[mode+'e'].pop(item_id)
            self.db[mode+'a'].pop(item_id)
            self.db[mode+'f'].pop(item_id)
            self.update()
        else:
            self.fromgrid()
            item_id = self.db[mode].index(item)
            self.db[mode].pop(item_id)
            for member in self.db['m'+mode]:
                member.pop(item_id)
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
            self.filename = "default.p"
            self.dirname = os.path.dirname(os.path.realpath(__file__))
            self.db = db.load(self.get_filename())
            self.update()
        return result

    def on_file_open(self, event):
        result = self.on_file_save_maybe(event)
        if (result == wx.ID_OK) or (result == wx.ID_NO):
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.p", wx.OPEN)
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
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "*.p", wx.SAVE)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.fromgrid()
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            db.save(self.get_filename(), self.db)
        dlg.Destroy()
        return result

    def on_edit(self, mode):
        def edit(event):
            edit_frame = wx.Frame(self, -1, title=mode.title, size=(640, 480))
            edit_frame.SetIcon(wx.Icon("edit.png", wx.BITMAP_TYPE_ANY))

            edit_sizer   = wx.BoxSizer(wx.VERTICAL)
            edit_sizers  = {}
            edit_buttons = {}
            edit_texts   = {}
            for col in mode.cols:
                edit_texts[col] = {}
            
            edit_top = wx.BoxSizer(wx.HORIZONTAL)
            for col in mode.cols:
                edit_top.Add(wx.StaticText(edit_frame, -1, col), 5)
            edit_sizer.Add(edit_top)

            def button(item):
                def on_button(event):
                    edit_buttons[item].Unbind(wx.EVT_BUTTON)
                    edit_buttons[item].Destroy()
                    for col in mode.cols:
                        edit_texts[col][item].Destroy()
                    edit_sizer.Remove(edit_sizers[item])
                    self.delete_item(item, mode.cid)
                    edit_sizer.Layout()
                    edit_frame.Update()
                return on_button

            def add_item_from_text(textctrl):
                def on_button(event):
                    new_item = textctrl.GetValue()
                    textctrl.Clear()
                    self.add_item(new_item, mode.cid)
                    edit_sizers[new_item] = wx.BoxSizer(wx.HORIZONTAL)
                    for col in mode.cols:
                        edit_texts[col][new_item] = wx.StaticText(edit_frame, -1, mode.new_vals[col](new_item))
                        edit_sizers[new_item].Add(edit_texts[col][new_item], 5, wx.ALIGN_CENTER)
                    edit_buttons[new_item] = wx.Button(edit_frame, -1, "-")
                    edit_sizers[new_item].Add(edit_buttons[new_item], 5, wx.ALIGN_CENTER)
                    edit_buttons[new_item].Bind(wx.EVT_BUTTON, button(new_item))
                    edit_sizer.Add(edit_sizers[new_item], 1)
                    edit_sizer.Layout()
                    edit_frame.Update()
                return on_button

            item_id = 0
            for item in self.db[mode.cid]:
                edit_sizers[item] = wx.BoxSizer(wx.HORIZONTAL)
                for col in mode.cols:
                    edit_texts[col][item] = wx.StaticText(edit_frame, -1, mode.get_vals[col](item))
                    edit_sizers[item].Add(edit_texts[col][item], 5, wx.ALIGN_CENTER)
                edit_buttons[item] = wx.Button(edit_frame, item_id, "-")
                edit_sizers[item].Add(edit_buttons[item], 5, wx.ALIGN_CENTER)
                edit_buttons[item].Bind(wx.EVT_BUTTON, button(item))
                edit_sizer.Add(edit_sizers[item], 1)
                item_id += 1

            edit_bottom = wx.BoxSizer(wx.HORIZONTAL)
            edit_display = wx.TextCtrl(edit_frame, -1, '',  style=wx.TE_RIGHT)
            edit_button_bottom = wx.Button(edit_frame, -1, "+")
            edit_button_bottom.Bind(wx.EVT_BUTTON, add_item_from_text(edit_display))
            edit_bottom.Add(edit_display, 0, wx.ALIGN_CENTER)
            edit_bottom.Add(edit_button_bottom, 0, wx.ALIGN_CENTER)
            edit_sizer.Add(edit_bottom, 1)
            edit_frame.SetSizer(edit_sizer)
            edit_frame.SetBackgroundColour(wx.WHITE)
            edit_frame.Show()
        return edit

    def on_view(self, mode):
        def view(event):
            self.set_mode(mode)
        return view

    def on_exit(self, event):
        result = self.on_file_save_maybe(event)
        if (result == wx.ID_OK) or (result == wx.ID_NO):
            self.Close(True)
        return result

    def on_tool_view(self, event):
        pass


if __name__ == "__main__":
    Interface()