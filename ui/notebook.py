import wx
import wx.aui

from .plot import EVT_PLOT_STATE_CHANGED

class Notebook(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sz = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.aui.AuiNotebook(self)
        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        sz.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sz)
        self.Layout()

    def on_close(self, event):
        self.notebook.GetPage(event.GetSelection()).on_close()
        event.Skip()

    def add_plot(self, plot):
        self.notebook.AddPage(plot, plot.get_name(), select=True)
        plot.Bind(EVT_PLOT_STATE_CHANGED, self.on_state_changed)

    def on_state_changed(self, event):
        wx.PostEvent(self, event)

    def set_loading(self, index, loading):
        if index >= 0 and index < self.notebook.GetPageCount():
            plot = self.notebook.GetPage(index)
            self.notebook.SetPageText(index, plot.get_name() + " (Загружается)" if loading else plot.get_name())

    def get_current(self):
        if self.notebook.GetSelection() > -1:
            return self.notebook.GetPage(self.notebook.GetSelection())
        return None
    
    def empty(self):
        return self.notebook.GetPageCount() == 0

    def save(self, path):
        page = self.get_current()
        if page is not None and page.can_save():
            page.save(path)

    def can_save(self):
        page = self.get_current()
        return page is not None and page.can_save()

    def can_undo(self):
        page = self.get_current()
        return page is not None and page.can_undo()

    def undo(self):
        page = self.get_current()
        if page is not None and page.can_undo():
            page.undo()

    def can_redo(self):
        page = self.get_current()
        return page is not None and page.can_redo()

    def redo(self):
        page = self.get_current()
        if page is not None and page.can_redo():
            page.redo()

    def can_copy(self):
        page = self.get_current()
        return page is not None and page.can_copy()

    def copy(self):
        page = self.get_current()
        if page is not None and page.can_copy():
            page.copy()

    def can_cut(self):
        page = self.get_current()
        return page is not None and page.can_cut()

    def cut(self):
        page = self.get_current()
        if page is not None and page.can_cut():
            page.cut()

    def can_paste(self):
        page = self.get_current()
        return page is not None and page.can_paste()

    def paste(self):
        page = self.get_current()
        if page is not None and page.can_paste():
            page.paste()

    def is_ready(self):
        page = self.get_current()
        return page is not None and page.is_ready()

