import wx

class ObjectsManager(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sz = wx.BoxSizer(wx.VERTICAL)
        self.tree = wx.TreeCtrl(self)
        sz.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sz)
        self.Layout()

    def update_objects(self, plot):
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("Objects")
        for obj in plot.canvas._DrawList:
            item = self.tree.AppendItem(root, str(obj))
            if obj in plot.selected:
                self.tree.SetItemBold(item, True)
            self.tree.SetItemData(item, obj)
        self.tree.Expand(root)
        self.Layout()

    def clear_objects(self):
        self.tree.DeleteAllItems()
        self.Layout()
