import wx
import math


class RulerWidget(wx.Panel):
    def __init__(self, parent, threshold=50, orientation=wx.HORIZONTAL, invert=False):
        super().__init__(parent)
        self.SetDoubleBuffered(True)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.orientation = orientation
        self.threshold = threshold
        self.pixels_on_step = 20
        self.invert = invert
        self.offset = 0.0
        self.cursor = None
        self.SetMinSize(
            wx.Size(20, 20) if orientation == wx.HORIZONTAL else wx.Size(20, 20)
        )
        self.SetSize(
            wx.Size(-1, 20) if orientation == wx.HORIZONTAL else wx.Size(20, -1)
        )
        self.Layout()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_size(self, event):
        self.Refresh()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        available_steps = [5, 10, 20, 50, 100, 500, 1000, 10000, 100000, 1000000]
        step = 1
        i = 0
        while step * self.pixels_on_step < self.threshold:
            step = available_steps[i]
            i += 1

        w, h = self.GetSize()
        gc.SetFont(
            wx.Font(
                8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
            ),
            wx.Colour(0, 0, 0),
        )
        if self.orientation == wx.HORIZONTAL:
            brush = gc.CreateLinearGradientBrush(
                0, 0, 0, h, wx.Colour(255, 255, 255), wx.Colour(220, 220, 220)
            )
            gc.SetBrush(brush)
            gc.DrawRectangle(0, 0, w, h)
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), width=1))
            if self.offset >= 0:
                i = (self.offset * self.pixels_on_step) % (step * self.pixels_on_step)
            else:
                i = -(
                    abs(self.offset * self.pixels_on_step)
                    % (step * self.pixels_on_step)
                )
            index = round((i - self.offset * self.pixels_on_step) / self.pixels_on_step)
            if not self.invert:
                while i < w:
                    gc.DrawText(str(index), i + 2, 6)
                    gc.StrokeLine(i, 0, i, h)
                    i += self.pixels_on_step * step
                    index += step
            else:
                while i < w:
                    gc.DrawText(str(index), (w - i) + 2, 6)
                    gc.StrokeLine((w - i), h, (w - i), 0)
                    i += self.pixels_on_step * step
                    index -= step
            if self.offset >= 0:
                i = (self.offset * self.pixels_on_step) % (
                    step * self.pixels_on_step / 10
                )
            else:
                i = -(
                    abs(self.offset * self.pixels_on_step)
                    % (step * self.pixels_on_step / 10)
                )
            if not self.invert:
                while i < w:
                    gc.StrokeLine(i, 0, i, h / 2)
                    i += step * self.pixels_on_step / 10
            else:
                while i < w:
                    gc.StrokeLine(w - i, h / 2, w - i, h)
                    i += step * self.pixels_on_step / 10
            if self.cursor is not None:
                gc.StrokeLine(self.cursor, 0, self.cursor, h)
        else:
            brush = gc.CreateLinearGradientBrush(
                0, 0, w, 0, wx.Colour(255, 255, 255), wx.Colour(220, 220, 220)
            )
            gc.SetBrush(brush)
            gc.DrawRectangle(0, 0, w, h)
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), width=1))
            if self.offset >= 0:
                i = (self.offset * self.pixels_on_step) % (step * self.pixels_on_step)
            else:
                i = -(
                    abs(self.offset * self.pixels_on_step)
                    % (step * self.pixels_on_step)
                )
            index = round((i - self.offset * self.pixels_on_step) / self.pixels_on_step)
            while i < h:
                gc.PushState()
                if not self.invert:
                    gc.Translate(8, i)
                else:
                    gc.Translate(8, h - i)
                gc.Rotate(-math.pi / 2)
                gc.DrawText(str(index), 0, 0)
                gc.PopState()
                if not self.invert:
                    gc.StrokeLine(0, i, w, i)
                    index += step
                else:
                    gc.StrokeLine(w, h - i, 0, h - i)
                    index += step
                i += self.pixels_on_step * step
            if self.offset >= 0:
                i = (self.offset * self.pixels_on_step) % (
                    step * self.pixels_on_step / 10
                )
            else:
                i = -(
                    abs(self.offset * self.pixels_on_step)
                    % (step * self.pixels_on_step / 10)
                )
            while i < h:
                if not self.invert:
                    gc.StrokeLine(w / 2, i, w, i)
                else:
                    gc.StrokeLine(w / 2, h - i, w, h - i)
                i += step * self.pixels_on_step / 10
            if self.cursor is not None:
                gc.StrokeLine(0, self.cursor, w, self.cursor)

    def set_pixels_on_step(self, pixels: float):
        self.pixels_on_step = pixels

    def set_offset(self, axis_value: float):
        """Sets the offset of the ruler in coords."""
        self.offset = axis_value

    def set_cursor(self, axis_value: float | None):
        """Sets the cursor position on the ruler. in pixels."""
        self.cursor = axis_value
