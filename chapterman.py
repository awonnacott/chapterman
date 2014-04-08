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
        self.edit_m    = self.edit_menu.Append(-1, "Members",  "Edit Memberhip List")
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
        return present/total

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

    def add_member(self, new_member):
        self.fromgrid()
        self.db['m'].append(new_member)
        self.db['me'].append(len(self.db['e'])*[""])
        self.db['ma'].append(len(self.db['a'])*[""])
        self.db['mf'].append(len(self.db['f'])*[""])
        self.update()

    def delete_member(self, member):
        self.fromgrid()
        member_id = self.db['m'].index(member)
        self.db['m'].pop(member_id)
        self.db['me'].pop(member_id)
        self.db['ma'].pop(member_id)
        self.db['mf'].pop(member_id)
        self.update()

    def add_event(self, new_event):
        self.fromgrid()
        self.db['e'].append(new_event)
        for member_e in self.db['me']:
            member_e.append("")
        self.update()

    def delete_event(self, event):
        self.fromgrid()
        event_id = self.db['e'].index(event)
        self.db['e'].pop(event_id)
        for member_e in self.db['me']:
            member_e.pop(event_id)
        self.update()

    def add_date(self, new_date):
        self.fromgrid()
        self.db['a'].append(new_date)
        for member_a in self.db['ma']:
            member_a.append("")
        self.update()

    def delete_date(self, date):
        self.fromgrid()
        date_id = self.db['a'].index(date)
        self.db['a'].pop(date_id)
        for member_a in self.db['ma']:
            member_a.pop(date_id)
        self.update()

    def add_form(self, new_form):
        self.fromgrid()
        self.db['f'].append(new_form)
        for member_f in self.db['mf']:
            member_f.append("")
        self.update()

    def delete_form(self, form):
        self.fromgrid()
        form_id = self.db['f'].index(form)
        self.db['f'].pop(form_id)
        for member_f in self.db['mf']:
            member_f.pop(form_id)
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
        edit_m_frame = wx.Frame(self, -1, title="Event List", size=(640, 480), name="Event List")

        edit_m_sizer = wx.BoxSizer(wx.VERTICAL)
        edit_m_sizers = {}
        edit_m_buttons = {}
        edit_m_texts1 = {}
        edit_m_texts2 = {}
        edit_m_texts3 = {}
        
        edit_m_top = wx.BoxSizer(wx.HORIZONTAL)
        edit_m_top.Add(wx.StaticText(edit_m_frame, -1, "Name"), 5)
        edit_m_top.Add(wx.StaticText(edit_m_frame, -1, "Events"), 5)
        edit_m_top.Add(wx.StaticText(edit_m_frame, -1, "Attendance"), 5)
        edit_m_sizer.Add(edit_m_top)

        def button(member):
            def on_button(e):
                print "removing member " + member
                print "sizer" + str(edit_m_sizers[member])
                edit_m_buttons[member].Unbind(wx.EVT_BUTTON)
                edit_m_buttons[member].Destroy()
                edit_m_texts1[member].Destroy()
                edit_m_texts2[member].Destroy()
                edit_m_texts3[member].Destroy()
                edit_m_sizer.Remove(edit_m_sizers[member])
                self.delete_member(member)
                edit_m_sizer.Layout()
                edit_m_frame.Update()
            return on_button

        def add_member_from_text(textctrl):
            def on_button(e):
                new_member = textctrl.GetValue()
                textctrl.Clear()
                self.add_member(new_member)
                edit_m_sizers[new_member] = wx.BoxSizer(wx.HORIZONTAL)
                edit_m_texts1[new_member] = wx.StaticText(edit_m_frame, -1, new_member)
                edit_m_sizers[new_member].Add(edit_m_texts1[new_member], 5)
                edit_m_texts2[new_member] = wx.StaticText(edit_m_frame, -1, "0")
                edit_m_sizers[new_member].Add(edit_m_texts2[new_member], 5)
                edit_m_texts3[new_member] = wx.StaticText(edit_m_frame, -1, "0")
                edit_m_sizers[new_member].Add(edit_m_texts3[new_member], 5)
                edit_m_buttons[new_member] = wx.Button(edit_m_frame, -1, "-")
                edit_m_sizers[new_member].Add(edit_m_buttons[new_member])
                edit_m_buttons[new_member].Bind(wx.EVT_BUTTON, button(new_member))
                edit_m_sizer.Add(edit_m_sizers[new_member], 1)
                edit_m_sizer.Layout()
                edit_m_frame.Update()
            return on_button

        member_id = 0
        for member in self.db['m']:
            edit_m_sizers[member] = wx.BoxSizer(wx.HORIZONTAL)
            edit_m_texts1[member] = wx.StaticText(edit_m_frame, -1, member)
            edit_m_sizers[member].Add(edit_m_texts1[member], 5)
            edit_m_texts2[member] = wx.StaticText(edit_m_frame, -1, str(len(self.get_events(member))))
            edit_m_sizers[member].Add(edit_m_texts2[member], 5)
            edit_m_texts3[member] = wx.StaticText(edit_m_frame, -1, str(self.get_attendance(member)))
            edit_m_sizers[member].Add(edit_m_texts3[member], 5)
            edit_m_buttons[member] = wx.Button(edit_m_frame, member_id, "-")
            edit_m_sizers[member].Add(edit_m_buttons[member])
            edit_m_buttons[member].Bind(wx.EVT_BUTTON, button(member))
            edit_m_sizer.Add(edit_m_sizers[member], 1)
            member_id += 1

        edit_m_bottom = wx.BoxSizer(wx.HORIZONTAL)
        edit_m_display = wx.TextCtrl(edit_m_frame, -1, '',  style=wx.TE_RIGHT)
        edit_m_button_bottom = wx.Button(edit_m_frame, -1, "+")
        edit_m_button_bottom.Bind(wx.EVT_BUTTON, add_member_from_text(edit_m_display))
        edit_m_bottom.Add(edit_m_display)
        edit_m_bottom.Add(edit_m_button_bottom)
        edit_m_sizer.Add(edit_m_bottom, 1)
        edit_m_frame.SetSizer(edit_m_sizer)
        edit_m_frame.Show()

    def on_edit_e(self, event):
        edit_e_frame = wx.Frame(self, -1, title="Event List", size=(640, 480), name="Event List")

        edit_e_sizer = wx.BoxSizer(wx.VERTICAL)
        edit_e_sizers = {}
        edit_e_buttons = {}
        edit_e_texts1 = {}
        edit_e_texts2 = {}
        
        edit_e_top = wx.BoxSizer(wx.HORIZONTAL)
        edit_e_top.Add(wx.StaticText(edit_e_frame, -1, "Name"), 5)
        edit_e_top.Add(wx.StaticText(edit_e_frame, -1, "Members"), 5)
        edit_e_sizer.Add(edit_e_top)

        def button(event):
            def on_button(e):
                edit_e_buttons[event].Unbind(wx.EVT_BUTTON)
                edit_e_buttons[event].Destroy()
                edit_e_texts1[event].Destroy()
                edit_e_texts2[event].Destroy()
                edit_e_sizer.Remove(edit_e_sizers[event])
                self.delete_event(event)
                edit_e_sizer.Layout()
                edit_e_frame.Update()
            return on_button

        def add_event_from_text(textctrl):
            def on_button(e):
                new_event = textctrl.GetValue()
                textctrl.Clear()
                self.add_event(new_event)
                edit_e_sizers[new_event] = wx.BoxSizer(wx.HORIZONTAL)
                edit_e_texts1[new_event] = wx.StaticText(edit_e_frame, -1, new_event)
                edit_e_sizers[new_event].Add(edit_e_texts1[new_event], 5)
                edit_e_texts2[new_event] = wx.StaticText(edit_e_frame, -1, "0")
                edit_e_sizers[new_event].Add(edit_e_texts2[new_event], 5)
                edit_e_buttons[new_event] = wx.Button(edit_e_frame, -1, "-")
                edit_e_sizers[new_event].Add(edit_e_buttons[new_event])
                edit_e_buttons[new_event].Bind(wx.EVT_BUTTON, button(new_event))
                edit_e_sizer.Add(edit_e_sizers[new_event], 1)
                edit_e_sizer.Layout()
                edit_e_frame.Update()
            return on_button

        event_id = 0
        for event in self.db['e']:
            edit_e_sizers[event] = wx.BoxSizer(wx.HORIZONTAL)
            edit_e_texts1[event] = wx.StaticText(edit_e_frame, -1, event)
            edit_e_sizers[event].Add(edit_e_texts1[event], 5)
            edit_e_texts2[event] = wx.StaticText(edit_e_frame, -1, str(len(self.get_members(event))))
            edit_e_sizers[event].Add(edit_e_texts2[event], 5)
            edit_e_buttons[event] = wx.Button(edit_e_frame, event_id, "-")
            edit_e_sizers[event].Add(edit_e_buttons[event])
            edit_e_buttons[event].Bind(wx.EVT_BUTTON, button(event))
            edit_e_sizer.Add(edit_e_sizers[event], 1)
            event_id += 1

        edit_e_bottom = wx.BoxSizer(wx.HORIZONTAL)
        edit_e_display = wx.TextCtrl(edit_e_frame, -1, '',  style=wx.TE_RIGHT)
        edit_e_button_bottom = wx.Button(edit_e_frame, -1, "+")
        edit_e_button_bottom.Bind(wx.EVT_BUTTON, add_event_from_text(edit_e_display))
        edit_e_bottom.Add(edit_e_display)
        edit_e_bottom.Add(edit_e_button_bottom)
        edit_e_sizer.Add(edit_e_bottom, 1)
        edit_e_frame.SetSizer(edit_e_sizer)
        edit_e_frame.Show()

    def on_edit_a(self, event):
        edit_a_frame = wx.Frame(self, -1, title="Date List", size=(640, 480), name="Date List")

        edit_a_sizer = wx.BoxSizer(wx.VERTICAL)
        edit_a_sizers = {}
        edit_a_buttons = {}
        edit_a_texts1 = {}
        
        edit_a_top = wx.BoxSizer(wx.HORIZONTAL)
        edit_a_top.Add(wx.StaticText(edit_a_frame, -1, "Date"), 5)
        edit_a_sizer.Add(edit_a_top)

        def button(date):
            def on_button(event):
                edit_a_buttons[date].Unbind(wx.EVT_BUTTON)
                edit_a_buttons[date].Destroy()
                edit_a_texts1[date].Destroy()
                edit_a_sizer.Remove(edit_a_sizers[date])
                self.delete_date(date)
                edit_a_sizer.Layout()
                edit_a_frame.Update()
            return on_button

        def add_date_from_text(textctrl):
            def on_button(event):
                new_date = textctrl.GetValue()
                textctrl.Clear()
                self.add_date(new_date)
                edit_a_sizers[new_date] = wx.BoxSizer(wx.HORIZONTAL)
                edit_a_texts1[new_date] = wx.StaticText(edit_a_frame, -1, new_date)
                edit_a_sizers[new_date].Add(edit_a_texts1[new_date], 5)
                edit_a_buttons[new_date] = wx.Button(edit_a_frame, -1, "-")
                edit_a_sizers[new_date].Add(edit_a_buttons[new_date])
                edit_a_buttons[new_date].Bind(wx.EVT_BUTTON, button(new_date))
                edit_a_sizer.Add(edit_a_sizers[new_date], 1)
                edit_a_sizer.Layout()
                edit_a_frame.Update()
            return on_button

        date_id = 0
        for date in self.db['a']:
            edit_a_sizers[date] = wx.BoxSizer(wx.HORIZONTAL)
            edit_a_texts1[date] = wx.StaticText(edit_a_frame, -1, date)
            edit_a_sizers[date].Add(edit_a_texts1[date], 5)
            edit_a_buttons[date] = wx.Button(edit_a_frame, date_id, "-")
            edit_a_sizers[date].Add(edit_a_buttons[date])
            edit_a_buttons[date].Bind(wx.EVT_BUTTON, button(date))
            edit_a_sizer.Add(edit_a_sizers[date], 1)
            date_id += 1

        edit_a_bottom = wx.BoxSizer(wx.HORIZONTAL)
        edit_a_display = wx.TextCtrl(edit_a_frame, -1, '',  style=wx.TE_RIGHT)
        edit_a_button_bottom = wx.Button(edit_a_frame, -1, "+")
        edit_a_button_bottom.Bind(wx.EVT_BUTTON, add_date_from_text(edit_a_display))
        edit_a_bottom.Add(edit_a_display)
        edit_a_bottom.Add(edit_a_button_bottom)
        edit_a_sizer.Add(edit_a_bottom, 1)
        edit_a_frame.SetSizer(edit_a_sizer)
        edit_a_frame.Show()

    def on_edit_f(self, event):
        edit_f_frame = wx.Frame(self, -1, title="Form List", size=(640, 480), name="Form List")

        edit_f_sizer = wx.BoxSizer(wx.VERTICAL)
        edit_f_sizers = {}
        edit_f_buttons = {}
        edit_f_texts1 = {}
        
        edit_f_top = wx.BoxSizer(wx.HORIZONTAL)
        edit_f_top.Add(wx.StaticText(edit_f_frame, -1, "Form"), 5)
        edit_f_sizer.Add(edit_f_top)

        def button(form):
            def on_button(event):
                edit_f_buttons[form].Unbind(wx.EVT_BUTTON)
                edit_f_buttons[form].Destroy()
                edit_f_texts1[form].Destroy()
                edit_f_sizer.Remove(edit_f_sizers[form])
                self.delete_form(form)
                edit_f_sizer.Layout()
                edit_f_frame.Upform()
            return on_button

        def add_form_from_text(textctrl):
            def on_button(event):
                new_form = textctrl.GetValue()
                textctrl.Clear()
                self.add_form(new_form)
                edit_f_sizers[new_form] = wx.BoxSizer(wx.HORIZONTAL)
                edit_f_texts1[new_form] = wx.StaticText(edit_f_frame, -1, new_form)
                edit_f_sizers[new_form].Add(edit_f_texts1[new_form], 5)
                edit_f_buttons[new_form] = wx.Button(edit_f_frame, -1, "-")
                edit_f_sizers[new_form].Add(edit_f_buttons[new_form])
                edit_f_buttons[new_form].Bind(wx.EVT_BUTTON, button(new_form))
                edit_f_sizer.Add(edit_f_sizers[new_form], 1)
                edit_f_sizer.Layout()
                edit_f_frame.Upform()
            return on_button

        form_id = 0
        for form in self.db['a']:
            edit_f_sizers[form] = wx.BoxSizer(wx.HORIZONTAL)
            edit_f_texts1[form] = wx.StaticText(edit_f_frame, -1, form)
            edit_f_sizers[form].Add(edit_f_texts1[form], 5)
            edit_f_buttons[form] = wx.Button(edit_f_frame, form_id, "-")
            edit_f_sizers[form].Add(edit_f_buttons[form])
            edit_f_buttons[form].Bind(wx.EVT_BUTTON, button(form))
            edit_f_sizer.Add(edit_f_sizers[form], 1)
            form_id += 1

        edit_f_bottom = wx.BoxSizer(wx.HORIZONTAL)
        edit_f_display = wx.TextCtrl(edit_f_frame, -1, '',  style=wx.TE_RIGHT)
        edit_f_button_bottom = wx.Button(edit_f_frame, -1, "+")
        edit_f_button_bottom.Bind(wx.EVT_BUTTON, add_form_from_text(edit_f_display))
        edit_f_bottom.Add(edit_f_display)
        edit_f_bottom.Add(edit_f_button_bottom)
        edit_f_sizer.Add(edit_f_bottom, 1)
        edit_f_frame.SetSizer(edit_f_sizer)
        edit_f_frame.Show()

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