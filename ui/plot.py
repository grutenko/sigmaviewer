import wx
import wx.lib.newevent
import util.thread_with_exc
from ui.ruler import RulerWidget

PlotStateChangedEvent, EVT_PLOT_STATE_CHANGED = wx.lib.newevent.NewEvent()

class PlotLoadCancelException(Exception): ...


class PlotWidget(wx.Panel):
    def __init__(self, parent, name=None):
        super().__init__(parent)
        self.load_task = None
        self.dxf = None
        self.selection = None
        self.name = name
        self.init_ui()

    def init_ui(self):
        sz = wx.FlexGridSizer(2, 2, 0, 0)
        self.hz_ruler = RulerWidget(self, orientation=wx.HORIZONTAL)
        self.vt_ruler = RulerWidget(self, orientation=wx.VERTICAL, invert=True)
        sz.Add(wx.Panel(self), 0)
        sz.Add(self.hz_ruler, 1, wx.EXPAND)
        sz.Add(self.vt_ruler, 1, wx.EXPAND)
        self.canvas = wx.Panel(self)
        sz.Add(self.canvas, 1, wx.EXPAND)
        sz.AddGrowableRow(1)
        sz.AddGrowableCol(1)
        self.SetSizer(sz)
        self.Layout()

    def get_selection(self):
        return None

    def get_name(self):
        return self.name
    
    def is_ready(self):
        return self.load_task is not None and not self.load_task.is_alive()
    
    def do_load(self, path):
        try:
            import ezdxf
            self.dxf = ezdxf.readfile(path)
            wx.PostEvent(self, PlotStateChangedEvent(plot=self))
        except PlotLoadCancelException:
            pass

    def load(self, path):
       # Запускаем пропатченый поток с возможностью вызвать асинхронное исключение для прерывания процесса
       # Например при закрытии вкладки во время загрузки https://stackoverflow.com/a/325528
       self.load_task = util.thread_with_exc.ThreadWithExc(target=self.do_load, args=(path, ), daemon=True)
       self.load_task.start()

    def save(self, path):
        pass

    def can_save(self):
        return False

    def can_undo(self):
        return False

    def undo(self):
        pass

    def can_redo(self):
        return False

    def redo(self):
        pass

    def can_copy(self):
        return False

    def copy(self):
        pass

    def can_cut(self):
        return False

    def cut(self):
        pass

    def can_paste(self):
        return False

    def paste(self):
        pass

    def on_close(self):
        if self.load_task is not None and self.load_task.is_alive():
            self.load_task.raise_exc(PlotLoadCancelException)
