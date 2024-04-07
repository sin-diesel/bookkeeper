"""
Модуль описывает QT виджеты, использующиеся в программе.
"""

from PySide6 import QtWidgets  # type: ignore


class Window(QtWidgets.QWidget):  # type: ignore
    def __init__(
        self, title: str, size_x: int = 800, size_y: int = 600
    ) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.resize(size_x, size_y)


class Table(QtWidgets.QTableWidget):  # type: ignore
    def __init__(
        self,
        nrows: int,
        header_types: dict[str, QtWidgets.QHeaderView.ResizeMode],
    ) -> None:
        super().__init__()
        ncols = len(header_types)
        self.setColumnCount(ncols)
        self.setRowCount(nrows)
        self.setHorizontalHeaderLabels(header_types.keys())
        headers = self.horizontalHeader()
        for idx, resize_type in enumerate(header_types.values()):
            headers.setSectionResizeMode(idx, resize_type)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()


class LabeledInput(QtWidgets.QWidget):
    def __init__(self, text: str, init: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.input = QtWidgets.QLineEdit(init)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

    def text(self):
        return self.input.text()

class ComboBox(QtWidgets.QComboBox):
    def __init__(self) -> None:
        super().__init__()
