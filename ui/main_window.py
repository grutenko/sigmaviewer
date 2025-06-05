import wx
import wx.aui

from .menu import MainMenu
from .notebook import Notebook
from .objects import ObjectsManager
from .properties import PropertiesManager
from .canvas import CanvasWidget

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="SigmaGT Интерполяция", size=wx.Size(1200, 600))
        self.SetMinSize(wx.Size(400, 300))
        self.menu = MainMenu()
        self.SetMenuBar(self.menu)
        self.statusbar = wx.StatusBar(self)
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText("No object selected", 1)
        self.SetStatusBar(self.statusbar)
        self.mgr = wx.aui.AuiManager(self)
        self.notebook = Notebook(self)
        self.objects_manager = ObjectsManager(self)
        self.properties_manager = PropertiesManager(self)
        self.mgr.AddPane(self.notebook, wx.aui.AuiPaneInfo()
          .Name("notebook")
          .Caption("Объекты")
          .Center()
          .PinButton(True)
          .CloseButton(False)
          .MinSize(wx.Size(200, 200)))
        self.notebook.add_page(wx.Panel(self.notebook), "Чертеж 1")
        self.mgr.AddPane(self.objects_manager, wx.aui.AuiPaneInfo()
          .Name("objects")
          .Caption("Объекты")
          .Right()
          .PinButton(True)
          .CloseButton(True)
          .MinSize(wx.Size(250, 250)))
        self.mgr.AddPane(self.properties_manager, wx.aui.AuiPaneInfo()
          .Name("properties")
          .Caption("Свойства - не выбран объект")
          .Right()
          .PinButton(True)
          .CloseButton(True)
          .MinSize(wx.Size(250, 250)))
        self.mgr.Update()
        self.Layout()
        self.Show()

        self.notebook.add_page(CanvasWidget(self.notebook), "Чертеж 2")
