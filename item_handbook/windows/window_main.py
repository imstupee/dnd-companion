from packages.imports import *
from packages.window_manager import wm
from packages.library_manager import lm

from windows import mdi_libraries

class Window(QMainWindow):
    def __init__(self) -> None:
        from ui import ui_main
        super(Window, self).__init__()
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)

        self._connect_signals()
        self._setup_ui()

        wm.mdi_area = self.ui.mdiArea

    def _connect_signals(self):
        self.ui.actionLibraries.triggered.connect(self._on_librariesAction_triggered)

    def _setup_ui(self):
        self.setWindowTitle("Item Handbook App")

    def closeEvent(self, event):
        lm.save()

    def _on_librariesAction_triggered(self):
        child = mdi_libraries.Window()
        wm.open(child)

    def show_window(self):
        self.show()