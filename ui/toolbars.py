import wx
import wx.aui

from ui.icon import get_icon

class FileToolbar(wx.aui.AuiToolBar):
    def __init__(self, parent):
        super().__init__(parent, style=wx.aui.AUI_TB_DEFAULT_STYLE | wx.aui.AUI_TB_HORIZONTAL)
        self.parent = parent
        self.SetToolBitmapSize(wx.Size(16, 16))
        
        # Add file operations
        self.AddTool(wx.ID_OPEN, "Открыть", get_icon("folder-open"), short_help_string="Открыть файл")
        self.AddSeparator()
        self.AddTool(wx.ID_SAVE, "Сохранить", get_icon("save"), short_help_string="Сохранить файл")
        self.AddTool(wx.ID_SAVEAS, "Сохранить как...", get_icon("save-as"), short_help_string="Сохранить файл под другим именем")
        self.AddTool(wx.ID_PRINT, "Печать", get_icon("print"), short_help_string="Печать документа")
        self.AddSeparator()
        self.AddTool(wx.ID_COPY, "Копировать", get_icon("copy"), short_help_string="Копировать выделенное")
        self.AddTool(wx.ID_CUT, "Вырезать", get_icon("cut"), short_help_string="Вырезать выделенное")
        self.AddTool(wx.ID_PASTE, "Вставить", get_icon("paste"), short_help_string="Вставить из буфера обмена")

        self.EnableTool(wx.ID_PASTE, False)
        self.EnableTool(wx.ID_COPY, False)
        self.EnableTool(wx.ID_CUT, False)
        self.EnableTool(wx.ID_PRINT, False)
        self.EnableTool(wx.ID_SAVE, False)
        self.EnableTool(wx.ID_SAVEAS, False)
        self.AddSeparator()
        
        # Add edit operations
        self.AddTool(wx.ID_UNDO, "Отменить", get_icon("undo"), short_help_string="Отменить последнее действие")
        self.EnableTool(wx.ID_UNDO, False)
        self.AddTool(wx.ID_REDO, "Вернуть", get_icon("redo"),   short_help_string="Вернуть отмененное действие")
        self.EnableTool(wx.ID_REDO, False)
        
        # Finalize toolbar
        self.Realize()

class PlotToolbar(wx.aui.AuiToolBar):
    def __init__(self, parent):
        super().__init__(parent, style=wx.aui.AUI_TB_DEFAULT_STYLE | wx.aui.AUI_TB_HORIZONTAL)
        self.parent = parent
        self.SetToolBitmapSize(wx.Size(16, 16))

        self.AddTool(wx.ID_ZOOM_IN, "Приблизить", get_icon("zoom-in"), short_help_string="Приблизить")
        self.AddTool(wx.ID_ZOOM_OUT, "Отдалить", get_icon("zoom-out"), short_help_string="Отдалить")

        # Finalize toolbar
        self.Realize()