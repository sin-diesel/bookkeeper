
import sys

from PySide6 import QtWidgets

def _main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    sys.exit(app.exec())

_main()
