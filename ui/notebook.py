import wx
import wx.aui

class Notebook(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sz = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.aui.AuiNotebook(self)
        sz.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sz)
        self.Layout()

    def add_plot(self, plot):
        self.notebook.AddPage(plot, plot.get_name(), select=True)

    def get_current(self):
        if self.notebook.GetSelection() > -1:
            return self.notebook.GetPage(self.notebook.GetSelection())
        return None

    def save(self, path):
        page = self.get_current()
        if page and page.can_save():
            page.save(path)

    def can_save(self):
        page = self.get_current()
        return page and page.can_save()

    def can_undo(self):
        page = self.get_current()
        return page and page.can_undo()

    def undo(self):
        page = self.get_current()
        if page and page.can_undo():
            page.undo()

    def can_redo(self):
        page = self.get_current()
        return page and page.can_redo()

    def redo(self):
        page = self.get_current()
        if page and page.can_redo():
            page.redo()

    def can_copy(self):
        page = self.get_current()
        return page and page.can_copy()

    def copy(self):
        page = self.get_current()
        if page and page.can_copy():
            page.copy()

    def can_cut(self):
        page = self.get_current()
        return page and page.can_cut()

    def cut(self):
        page = self.get_current()
        if page and page.can_cut():
            page.cut()

    def can_paste(self):
        page = self.get_current()
        return page and page.can_paste()

    def paste(self):
        page = self.get_current()
        if page and page.can_paste():
            page.paste()

