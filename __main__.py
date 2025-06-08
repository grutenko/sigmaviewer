import wx
from ui.main_window import MainWindow

if __name__ == "__main__":
    import libs.litecad as lc

    if lc.lcInitialize() == 0:
        raise RuntimeError(lc.lcGetErrorStr())
    lc.lcPropPutStr(0, lc.LC_PROP_G_REGCODE, "cdda-e9ce-9eb7-1d89")

    app = wx.App()
    frame = MainWindow()
    app.SetTopWindow(frame)
    app.MainLoop()
