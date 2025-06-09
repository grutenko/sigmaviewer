import wx
import wx.dataview

class ObjectsManager(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sz = wx.BoxSizer(wx.VERTICAL)
        self.current_plot = None
        self.tree = wx.dataview.TreeListCtrl(self, style=wx.dataview.TL_DEFAULT_STYLE | wx.dataview.TL_CHECKBOX)
        self.tree.AppendColumn("Название")
        self.tree.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.on_selection_changed)
        sz.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sz)
        self.Layout()

    def on_selection_changed(self, event):
        if self.current_plot is not None:
            item = self.tree.GetSelection()
            self.current_plot.set_selection(self.tree.GetItemData(item) if item.IsOk() else None)

    def update(self, plot):
        self.current_plot = plot
        self.tree.DeleteAllItems()
        self.tree.SetItemText(self.tree.RootItem, plot.get_name())
        if not plot.is_ready():
            self.tree.AppendItem(self.tree.RootItem, "Загружается...")
        else:
            self.show_items(plot)
        self.Layout()

    def show_items(self, plot):
        layers = {}
        for entity in plot.dxf.modelspace():
            layer = entity.dxf.get("layer", "0")
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(entity)

        root = self.tree.AppendItem(self.tree.RootItem, "DXF")

        for layer, entities in layers.items():
            layerItem = self.tree.AppendItem(root, layer)
            for entity in entities:
                entityItem = self.tree.AppendItem(layerItem, entity.dxftype(), data=entity)
                self.tree.CheckItem(entityItem)
            self.tree.CheckItem(layerItem)

    def clear(self):
        self.tree.DeleteAllItems()
        self.Layout()
