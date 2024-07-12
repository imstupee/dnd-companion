from packages.imports import *
from packages.library_manager import lm
from packages.utils import get_libraries_list
from packages.window_manager import wm
from windows import mdi_itemtree

class Window(QMainWindow):
    uid = "window_libraries"
    def __init__(self) -> None:
        from ui import ui_libraries
        super(Window, self).__init__()
        self.ui = ui_libraries.Ui_MainWindow()
        self.ui.setupUi(self)

        self._connect_signals()
        self._setup_ui()

    def _connect_signals(self):
        self.ui.listWidget.itemDoubleClicked.connect(self._on_itemDoubleClicked)

    def _setup_ui(self):
        self.setWindowTitle("Libraries")

    def _load_listWidget(self):
        libraries = get_libraries_list()
        for library_name in libraries:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, library_name)
            item.setText(library_name)
            self.ui.listWidget.addItem(item)

    def _get_item_data(self, item: QListWidgetItem):
        return item.data(Qt.UserRole)
    
    def _on_itemDoubleClicked(self, item: QListWidgetItem):
        library_name = self._get_item_data(item)
        lm.load(library_name)
        child = mdi_itemtree.Window()
        wm.open(child)

    def show_window(self):
        self.show()
        self._load_listWidget()