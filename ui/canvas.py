import wx
from wx.lib.floatcanvas import FloatCanvas

from ui.ruler import RulerWidget

class CanvasWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sz = wx.FlexGridSizer(2, 2, 0,0)
        self.hz_ruler = RulerWidget(self, orientation=wx.HORIZONTAL)
        self.vt_ruler = RulerWidget(self, orientation=wx.VERTICAL, invert=True)
        sz.Add(wx.Panel(self), 0)
        sz.Add(self.hz_ruler, 1, wx.EXPAND)
        sz.Add(self.vt_ruler, 1, wx.EXPAND)
        self.canvas = FloatCanvas.FloatCanvas(self, BackgroundColor="WHITE")
        sz.Add(self.canvas, 1, wx.EXPAND)
        sz.AddGrowableRow(1)
        sz.AddGrowableCol(1)
        self.SetSizer(sz)
        self.Layout()
        self.dragged = False
        self.canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.on_left_down)
        self.canvas.Bind(FloatCanvas.EVT_LEFT_UP, self.on_left_up)
        self.canvas.Bind(FloatCanvas.EVT_MOTION, self.on_move)
        self.canvas.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.old_x = 0
        self.old_y = 0
        self.scale = 1.0;
        self.Bind(wx.EVT_PAINT, self.on_paint)

        rect = self.canvas.AddRectangle(
                    XY=(100, 100),  # координаты центра
                    WH=(200, 100),  # ширина и высота
                    LineColor="BLACK",
                    FillColor="YELLOW"
        )

    def on_paint(self, event):
        self.update_rulers()

    def on_mouse_wheel(self, event: wx.MouseEvent):
      self.canvas.Zoom(1.0 + (event.GetWheelRotation() * 0.0001))
      self.update_rulers()

    def update_rulers(self):
        size = self.canvas.GetSize()
        start = self.canvas.PixelToWorld((0, 0))
        end = self.canvas.PixelToWorld((size.GetWidth(), size.GetHeight()))
        hz_pixels = size.GetWidth() / abs(end[0] - start[0])
        vt_pixels = size.GetHeight() / abs(end[1] - start[1])
        self.hz_ruler.set_pixels_on_step(hz_pixels)
        self.vt_ruler.set_pixels_on_step(vt_pixels)
        self.hz_ruler.set_offset(-start[0])
        self.vt_ruler.set_offset(-end[1])
        self.hz_ruler.Refresh()
        self.vt_ruler.Refresh()
        self.hz_ruler.Update()
        self.vt_ruler.Update()

    def on_left_down(self, event):
        self.dragged = True
        self.old_x = event.GetX()
        self.old_y = event.GetY()

    def on_left_up(self, event):
        self.dragged = False

    def on_move(self, event):
        # Update the rulers' positions based on the panel's position
        pos = event.GetPosition()
        self.hz_ruler.set_cursor(pos.x)
        self.vt_ruler.set_cursor(pos.y)
        self.hz_ruler.Refresh()
        self.vt_ruler.Refresh()
        self.hz_ruler.Update()
        self.vt_ruler.Update()
        event.Skip()

        if self.dragged:
            self.canvas.MoveImage((self.old_x - pos.x, self.old_y - pos.y), "Pixel")
            self.old_x = pos.x
            self.old_y = pos.y

            self.update_rulers()
