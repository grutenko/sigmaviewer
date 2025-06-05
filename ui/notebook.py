import wx
import wx.aui
import wx.lib.agw.flatmenu

class Notebook(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sz = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.aui.AuiNotebook(self)
        sz.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sz)
        self.Layout()

    def add_page(self, page, title):
        self.notebook.AddPage(page, title)
