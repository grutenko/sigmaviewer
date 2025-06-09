import wx
import wx.aui

from .menu import MainMenu
from .notebook import Notebook
from .objects import ObjectsManager
from .properties import PropertiesManager
from .toolbars import FileToolbar, PlotToolbar
from .plot import PlotWidget, EVT_PLOT_STATE_CHANGED
from .actions import ID_PIN_PLOTS

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
        self.file_toolbar = FileToolbar(self)
        self.plot_toolbar = PlotToolbar(self)
        self.mgr.AddPane(self.file_toolbar, wx.aui.AuiPaneInfo()
          .Name("file_toolbar")
          .Caption("Файл")
          .ToolbarPane()
          .Top().Row(0)
          .PinButton(True)
          .CloseButton(False)
          .MinSize(wx.Size(200, 22)))
        self.mgr.AddPane(self.plot_toolbar, wx.aui.AuiPaneInfo()
          .Name("plot_toolbar")
          .Caption("Файл")
          .ToolbarPane()
          .Top().Row(0)
          .PinButton(True)
          .CloseButton(False)
          .MinSize(wx.Size(200, 22)))
        self.mgr.AddPane(self.notebook, wx.aui.AuiPaneInfo()
          .Name("notebook")
          .Caption("Чертежи")
          .CenterPane()
          .PinButton(True)
          .CloseButton(False)
          .Dockable(False)
          .Movable(False)
          .MinSize(wx.Size(800, 600))
          .BestSize(wx.Size(800, 600)))
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
        
        self.mgr.GetPane("plot_toolbar").Hide()
      
        self.mgr.Update()
        self.Layout()
        self.Show()

        self.bind_all()

    def bind_all(self):
        self.mgr.Bind(wx.aui.EVT_AUI_PANE_BUTTON, self.on_pane_button)
        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_activate_plot_changed)
        self.menu.Bind(wx.EVT_MENU, self.on_pin_plots, id=ID_PIN_PLOTS)
        self.menu.Bind(wx.EVT_MENU, self.on_open, id=wx.ID_OPEN)
        self.file_toolbar.Bind(wx.EVT_TOOL, self.on_open, id=wx.ID_OPEN)
        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.on_page_closed)
        self.notebook.Bind(EVT_PLOT_STATE_CHANGED, self.on_plot_state_changed)

    def on_plot_state_changed(self, event):
        self.update_panels()
        self.update_controls_state()

    def on_page_closed(self, event):
        self.update_panels()
        self.update_controls_state()

    def on_open(self, event):
        with wx.FileDialog(self, "Открыть файл", wildcard="*.dxf", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            
            path = file_dialog.GetPath()
            self.open(path)

    def open(self, path: str):
        if not path:
            wx.MessageBox("Не выбран файл для открытия", "Ошибка", wx.OK | wx.ICON_ERROR)
            return
        import os.path
        plot = PlotWidget(self.notebook, name=os.path.basename(path))
        self.notebook.add_plot(plot)
        plot.load(path)
        self.update_controls_state()

    def on_pane_button(self, event: wx.aui.AuiManagerEvent):
        if event.GetPane().name == "notebook" and event.GetButton() == wx.aui.AUI_BUTTON_PIN:
            item = self.menu.FindItemById(ID_PIN_PLOTS)
            item.Check(True)
            item.SetItemLabel("Закрепить чертежи")
        event.Skip()

    def on_pin_plots(self, event):
        item = self.menu.FindItemById(event.GetId())
        self.mgr.GetPane("notebook").Float() if item.IsChecked() else self.mgr.GetPane("notebook").Dock()
        self.mgr.Update()

    def on_activate_plot_changed(self, event):
        self.update_panels()
        self.update_controls_state()
        event.Skip()

    def update_panels(self):
        props_pane = self.mgr.GetPane("properties")
        plot = self.notebook.get_current()
        if plot is not None:
            if plot.get_selection():
                self.properties_manager.update(plot)
                props_pane.Caption("Свойства")
            else:
                self.properties_manager.clear()
                props_pane.Caption("Свойства - объект не выбран")
            self.objects_manager.update(plot)
        else:
            self.properties_manager.clear()
            self.objects_manager.clear()
            props_pane.Caption("Свойства - объект не выбран")
        self.mgr.Update()

    def update_controls_state(self):
        can_save = self.notebook.can_save()
        can_undo = self.notebook.can_undo()
        can_redo = self.notebook.can_redo()
        can_copy = self.notebook.can_copy()
        can_cut = self.notebook.can_cut()
        can_paste = self.notebook.can_paste()
        self.file_toolbar.EnableTool(wx.ID_SAVE, can_save)
        self.file_toolbar.EnableTool(wx.ID_UNDO, can_undo)
        self.file_toolbar.EnableTool(wx.ID_REDO, can_redo)
        self.file_toolbar.EnableTool(wx.ID_COPY, can_copy)
        self.file_toolbar.EnableTool(wx.ID_CUT, can_cut)
        self.file_toolbar.EnableTool(wx.ID_PASTE, can_paste)
        self.mgr.GetPane("plot_toolbar").Show(not self.notebook.empty())
        self.menu.Enable(wx.ID_SAVEAS, not self.notebook.empty())
        self.menu.Enable(wx.ID_SAVE, can_save)
        self.menu.Enable(wx.ID_COPY, can_copy)
        self.menu.Enable(wx.ID_CUT, can_cut)
        self.menu.Enable(wx.ID_PASTE, can_paste)
        self.menu.Enable(wx.ID_SAVEAS, not self.notebook.empty())
        self.menu.Enable(wx.ID_UNDO, can_undo)
        self.menu.Enable(wx.ID_REDO, can_redo)

        for i in range(self.notebook.notebook.GetPageCount()):
            plot = self.notebook.notebook.GetPage(i)
            self.notebook.set_loading(i, not plot.is_ready())

        label = ""
        if not self.notebook.empty():
            if self.notebook.is_ready():
                label = "Готов"
            else:
                label = "Загружается"
        self.statusbar.SetStatusText(label)

        self.mgr.Update()
