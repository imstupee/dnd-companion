from packages.imports import *
from packages.library_manager import lm, Category, Item
from packages.window_manager import wm

from windows.window_dialog import Dialog

class LibraryTreeItem(QTreeWidgetItem):
    def __init__(self, path, name, type_) -> None:
        super(LibraryTreeItem, self).__init__()
        self.path = path
        self.name = name
        self.type_ = type_
        self.setText(0, name)
    
    def set_path(self, path: str):
        self.path = path

class Window(QMainWindow):
    uid = "window_itemtree"
    library_name = ""
    def __init__(self) -> None:
        from ui import ui_itemtree
        super(Window, self).__init__()
        self.ui = ui_itemtree.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.treeWidget.setDragDropMode()


        self._connect_signals()
        self._setup_ui()

    def _connect_signals(self):
        self.ui.treeWidget.customContextMenuRequested.connect(self._treewidget_context_menu_requested)

    def _setup_ui(self):
        self.library_name = lm.metadata["name"]
        self.ui.treeWidget.setHeaderHidden(True)
        self.setWindowTitle(f"{self.library_name} Tree View")
        self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)

    def closeEvent(self, event):
        dlg = Dialog("Closing library", "Close?")
        if dlg.exec():
            wm.close(self.uid)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        source_item: LibraryTreeItem= self.currentItem()
        super().dropEvent(event)
        target_item: LibraryTreeItem = self.itemAt(event.pos())
        target_item = target_item if target_item != None else self.invisibleRootItem()
        if source_item and target_item:
            self._moveTreeItem_requested(source_item.path, target_item.path)
        self._load_tree()

    def _load_tree(self):
        self.ui.treeWidget.clear()
        self.ui.treeWidget.invisibleRootItem().setData(0, Qt.UserRole, lm.storage.path)
        self._populate_tree(lm.storage, self.ui.treeWidget.invisibleRootItem())

    def _populate_tree(self, folder: Category, parent: QTreeWidgetItem=None):
        for item in folder.container:
            if isinstance(item, Category):
                tree_item = LibraryTreeItem(item.path, item.name, "folder")
                parent.addChild(tree_item)
                self._populate_tree(item, tree_item)
            elif isinstance(item, Item):
                tree_item = LibraryTreeItem(item.path, item.data["name"], "item")
                parent.addChild(tree_item)

    def _treewidget_context_menu_requested(self, position: QPoint):
        menu = QMenu()
        if self.itemAt(position) != None:
            if self.itemAt(position).type_ == "folder":
                menu.addAction("Add Item")
                menu.addAction("Add folder")
                menu.addAction("Delete folder")
            elif self.itemAt(position).type_ == "item":
                menu.addAction("Delete Item")
        else:
            menu.addAction("Add Item")
            menu.addAction("Add folder")
        menu.exec(self.mapToGlobal(position))
    
    def _addItemAction_triggered(self, path: str):
        pass
    
    def _addFolderAction_triggered(self, path: str):
        pass

    def _deleteFolderAction_triggered(self, path: str):
        pass

    def _deleteItemAction_triggered(self, path: str):
        pass

    def _moveTreeItem_requested(self, source: str, target: str):
        pass

    def itemAt(self, position: QPoint) -> LibraryTreeItem:
        return self.ui.treeWidget.itemAt(position)

    def show_window(self):
        self.show()
        self._load_tree()