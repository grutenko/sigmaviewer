import wx
import wx.dataview

class ObjectsManager(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sz = wx.BoxSizer(wx.VERTICAL)
        self.tree = wx.dataview.TreeListCtrl(self, style=wx.dataview.TL_DEFAULT_STYLE | wx.dataview.TL_CHECKBOX)
        self.tree.AppendColumn("Название")
        sz.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sz)
        self.Layout()

    def update(self, plot):
        self.tree.DeleteAllItems()
        self.tree.SetItemText(self.tree.RootItem, plot.get_name())
        if not plot.is_ready():
            self.tree.AppendItem(self.tree.RootItem, "Загружается...")
        else:
            self.show_items(plot)
        self.Layout()

    def show_items(self, plot):
        for entity in plot.dxf.modelspace():
            item = self.tree.AppendItem(self.tree.RootItem, entity.dxftype())
            self.tree.CheckItem(item)

    def clear(self):
        self.tree.DeleteAllItems()
        self.Layout()
