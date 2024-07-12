from packages.imports import *
import packages.config as config

from windows import window_main

class Application(QApplication):
    def __init__(self) -> None:
        super(Application, self).__init__()
    
    def _on_startup(self):
        pass

    def start(self):
        self._on_startup()
        self.mainwindow = window_main.Window()
        self.mainwindow.show_window()
        self.exec()

app = Application()
app.start()