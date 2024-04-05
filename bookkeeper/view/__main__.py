
import sys
from PySide6 import QtWidgets

from .view import Window

def _main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = Window("The bookkeeper app")
    window.show()
    sys.exit(app.exec())

_main()
