"""
Модуль описывает QT виджеты, использующиеся в программе.
"""

from PySide6 import QtWidgets  # type: ignore


class Window(QtWidgets.QMainWindow):  # type: ignore
    def __init__(
        self, title: str, size_x: int = 800, size_y: int = 600
    ) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.resize(size_x, size_y)


class ExpensesTable(QtWidgets.QTableWidget):  # type: ignore
    def __init__(self, nrows: int, headers: list[str]) -> None:
        super().__init__()
        ncols = len(headers)
        self.setColumnCount(ncols)
        self.setRowCount(nrows)
        self.setHorizontalHeaderLabels(headers)
        header = self.horizontalHeader()
        for col_idx in range(ncols):
            header.setSectionResizeMode(
                col_idx, QtWidgets.QHeaderView.ResizeToContents
            )
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()
