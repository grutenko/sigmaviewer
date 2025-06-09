import wx

class ObjectsManager(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sz = wx.BoxSizer(wx.VERTICAL)
        self.tree = wx.TreeCtrl(self)
        sz.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sz)
        self.Layout()

    def update(self, plot):
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("Objects")
        self.tree.Expand(root)
        self.Layout()

    def clear(self):
        self.tree.DeleteAllItems()
        self.Layout()
