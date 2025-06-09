import wx

class PropertiesManager(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

    def update(self, plot):
        ...

    def clear(self):
        ...