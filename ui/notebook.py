import wx
import wx.aui

from ui.plot import EVT_PLOT_SELECTION_CHANGED, EVT_PLOT_MOVE, EVT_PLOT_SCALE

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
        plot.Bind(EVT_PLOT_SELECTION_CHANGED, self.on_selection_changed)
        plot.Bind(EVT_PLOT_MOVE, self.on_move)
        plot.Bind(EVT_PLOT_SCALE, self.on_scale)

    def on_selection_changed(self, event):
        wx.PostEvent(self, event)  # Forward the event to the parent frame

    def on_move(self, event):
        wx.PostEvent(self, event)

    def on_scale(self, event):
        wx.PostEvent(self, event)
