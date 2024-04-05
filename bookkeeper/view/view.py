
from PySide6 import QtWidgets

class Window():
    def __init__(self, title: str, size_x: int = 800, size_y: int = 600) -> None:
        self._window  = QtWidgets.QWidget()
        self._window.setWindowTitle(title)
        self._window.resize(size_x, size_y)

    def show(self) -> None:
        self._window.show()

