from packages.imports import *

class WindowManager:
    def __init__(self) -> None:
        self.mdi_area: QMdiArea = None
        self.windows: dict[str, QMainWindow] = {

        }
    
    def open(self, window: QMainWindow):
        if window.uid in self.windows:
            self.windows[window.uid].raise_()
        else:
            self.mdi_area.addSubWindow(window)
            self.windows[window.uid] = window
            window.show_window()
    
    def close(self, uid: str):
        del self.windows[uid]

wm = WindowManager()