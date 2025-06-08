import wx

class PropertiesManager(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

    def update_properties(self, plot, selection):
        ...

    def clear_properties(self):
        ...