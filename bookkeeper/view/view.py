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
