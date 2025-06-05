import wx
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow()
    app.SetTopWindow(frame)
    app.MainLoop()
