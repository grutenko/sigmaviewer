import wx
import wx.lib.newevent
import ctypes.wintypes as wt
import ctypes as ct
import libs.litecad as lc

from ui.ruler import RulerWidget

PlotSelectionChangedEvent, EVT_PLOT_SELECTION_CHANGED = wx.lib.newevent.NewEvent()
PlotMoveEvent, EVT_PLOT_MOVE = wx.lib.newevent.NewEvent()
PlotScaleEvent, EVT_PLOT_SCALE = wx.lib.newevent.NewEvent()


class PlotWidget(wx.Panel):
    def __init__(self, parent, name=None):
        super().__init__(parent)
        self.name = name
        sz = wx.FlexGridSizer(2, 2, 0, 0)
        self.hz_ruler = RulerWidget(self, orientation=wx.HORIZONTAL)
        self.vt_ruler = RulerWidget(self, orientation=wx.VERTICAL, invert=True)
        sz.Add(wx.Panel(self), 0)
        sz.Add(self.hz_ruler, 1, wx.EXPAND)
        sz.Add(self.vt_ruler, 1, wx.EXPAND)
        self.canvas = wx.Panel(self)
        self.lc_wnd = lc.lcCreateWindow(self.canvas.GetHandle(), lc.LC_WS_DEFAULT)
        if self.lc_wnd == 0:
            raise Exception(lc.lcGetErrorStr())
        lc.lcPropPutBool(self.lc_wnd, lc.LC_PROP_WND_SELECT, True)
        lc.lcPropPutBool(self.lc_wnd, lc.LC_PROP_SEL_PICKBYRECT, True)
        lc.lcPropPutBool(self.lc_wnd, lc.LC_PROP_WND_GRIDSHOW, True)
        self.lc_drw = lc.lcCreateDrawing()
        if self.lc_drw == 0:
            raise Exception(lc.lcGetErrorStr())
        lc.lcWndSetFocus(self.lc_wnd)
        lc.lcPropPutInt(self.lc_wnd, lc.LC_PROP_WND_COLORBG, 255 * 65536 + 255 * 256 + 255)
        lc.lcPropPutInt(self.lc_drw, lc.LC_PROP_DRW_COLORBACKM, 255 * 65536 + 255 * 256 + 255)
        lc.lcPropPutInt(self.lc_wnd, lc.LC_PROP_WND_GRIDCOLOR, 150 * 65536 + 150 * 256 + 150)
        lc.lcPropPutBool(self.lc_drw, lc.LC_PROP_WND_DRAWPAPER, False)
        lc.lcPropPutBool(self.lc_drw, lc.LC_PROP_DRW_LOCKSEL, True)
        hBlock = lc.lcPropGetHandle(self.lc_drw, lc.LC_PROP_DRW_BLOCK_MODEL)
        lc.lcWndSetBlock(self.lc_wnd, hBlock)
        lc.lcPropPutBool(self.lc_wnd, lc.LC_PROP_WND_STDBLKFRAME, False)
        lc.lcPropPutFloat(self.lc_wnd, lc.LC_PROP_WND_GRIDDX, 10.0)
        lc.lcPropPutFloat(self.lc_wnd, lc.LC_PROP_WND_GRIDDY, 10.0)
        lc.lcPropPutBool(self.lc_wnd, lc.LC_PROP_WND_GRIDDOTTED, True)
        lc.lcBlockUpdate(hBlock, True, 0)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Layout()
        sz.Add(self.canvas, 1, wx.EXPAND)
        sz.AddGrowableRow(1)
        sz.AddGrowableCol(1)
        self.SetSizer(sz)
        self.Layout()
        self.dragged = False
        self.old_x = 0
        self.old_y = 0
        self.scale = 1.0

    def on_size(self, event):
        rc = lc.lcWndResize(self.lc_wnd, 0, 0, event.GetSize().GetWidth(), event.GetSize().GetHeight())
        if rc == 0:
            raise Exception(lc.lcGetErrorStr())
        event.Skip()
        self.update_rulers()

    def get_name(self):
        return self.name

    def update_rulers(self):
        size = self.canvas.GetSize()
        xmin = ct.c_double(0.0)
        ymin = ct.c_double(0.0)
        lc.lcWndCoordToDrw(self.lc_wnd, 0, 0, ct.byref(xmin), ct.byref(ymin))
        xmax = ct.c_double(0.0)
        ymax = ct.c_double(0.0)
        lc.lcWndCoordToDrw(self.lc_wnd, size.GetWidth(), size.GetHeight(), ct.byref(xmax), ct.byref(ymax))
        xmin = xmin.value
        ymin = ymin.value
        xmax = xmax.value
        ymax = ymax.value
        self.hz_ruler.set_scale(size.GetWidth() / abs(xmax - xmin), False)
        self.vt_ruler.set_scale(size.GetHeight() / abs(ymax - ymin), False)
        self.hz_ruler.set_offset(-xmin, False)
        self.vt_ruler.set_offset(-ymax, False)
        self.hz_ruler.draw()
        self.vt_ruler.draw()

    def load(self, path):
        # Placeholder for loading logic
        pass

    def save(self, path): ...

    def can_save(self):
        return False

    def can_undo(self):
        return False

    def can_redo(self):
        return False

    def undo(self):
        pass

    def redo(self):
        pass

    def can_copy(self):
        return False

    def copy(self):
        pass

    def move(self, xy): ...

    def scale(self, factor): ...
