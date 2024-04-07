"""
Модуль описывает QT виджеты, использующиеся в программе.
"""

import sys
from PySide6 import QtWidgets  # type: ignore
from typing import Callable
from bookkeeper.bookkeeper import AbstractView
from bookkeeper.models.category import Category


class Window(QtWidgets.QWidget):  # type: ignore
    """
    Наследник класса QMainWindow с дополненным конструктором.
    """

    def __init__(
        self, title: str, size_x: int = 800, size_y: int = 600
    ) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.resize(size_x, size_y)


class Table(QtWidgets.QTableWidget):  # type: ignore
    """
    Наследник класса QTableWidget, в конструкторе дополнительно настраивает
    заголовки и их размер.
    """

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


class LabeledInput(QtWidgets.QWidget):  # type: ignore
    """
    Реализация окна с вводом.
    """

    def __init__(self, text: str, init: str = ""):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.input = QtWidgets.QLineEdit(init)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

    def text(self) -> str:
        """
        Возвращает текст, на данный момент находящиейся в окне.
        """
        return self.input.text()  # type: ignore


class View(AbstractView):
    """
    Класс задает способ отображения виджетов и их изменению,
    при этом принимает данные от Presenter-а.
    """

    def __init__(self) -> None:
        self._app = QtWidgets.QApplication(sys.argv)
        self._window = Window("The bookkeeper app")
        self._category_window = Window("Список категорий", 300, 300)

        layout = QtWidgets.QVBoxLayout()

        self._expenses_table = Table(
            20,
            {
                "Дата": QtWidgets.QHeaderView.ResizeToContents,
                "Сумма": QtWidgets.QHeaderView.ResizeToContents,
                "Категория": QtWidgets.QHeaderView.ResizeToContents,
                "Комментарий": QtWidgets.QHeaderView.Stretch,
            },
        )
        self._budget_table = Table(
            3,
            {
                "": QtWidgets.QHeaderView.Stretch,
                "Сумма": QtWidgets.QHeaderView.Stretch,
                "Бюджет": QtWidgets.QHeaderView.Stretch,
            },
        )
        self._budget_table.setItem(0, 0, QtWidgets.QTableWidgetItem("День"))
        self._budget_table.setItem(1, 0, QtWidgets.QTableWidgetItem("Неделя"))
        self._budget_table.setItem(2, 0, QtWidgets.QTableWidgetItem("Месяц"))

        self._sum = LabeledInput("Сумма")

        category_layout = QtWidgets.QHBoxLayout()
        self._categories_widget = QtWidgets.QComboBox()

        layout = QtWidgets.QVBoxLayout()
        self._edit_button = QtWidgets.QPushButton("Редактировать")
        self._edit_button.clicked.connect(self.edit_categories)

        category_layout.addWidget(self._categories_widget)
        category_layout.addWidget(self._edit_button)
        self._add_button = QtWidgets.QPushButton("Добавить")

        layout.addWidget(QtWidgets.QLabel("Последние расходы"))
        layout.addWidget(self._expenses_table)
        layout.addWidget(QtWidgets.QLabel("Бюджет"))
        layout.addWidget(self._budget_table)
        layout.addWidget(self._sum)

        layout.addLayout(category_layout)

        layout.addWidget(self._add_button)

        self._window.setLayout(layout)

    def set_category_list(self, categories: list[Category]) -> None:
        """
        Отображает список категорий в QT GUI.
        """
        self._categories = categories
        for category in self._categories:
            self._categories_widget.addItem(category.name)

    def edit_categories(self) -> None:
        layout = QtWidgets.QVBoxLayout()
        categories_table = Table(len(self._categories),
                                 {"Категория": QtWidgets.QHeaderView.ResizeToContents})
        for idx, category in enumerate(self._categories):
            categories_table.setItem(idx, 0, QtWidgets.QTableWidgetItem(category.name))
        layout.addWidget(categories_table)
        self._category_window.setLayout(layout)
        self._category_window.show()

    def show(self) -> None:
        """
        Отображает окно с приложением.
        """
        self._window.show()

    def exec(self) -> None:
        """
        Запускает приложение.
        """
        self.show()
        sys.exit(self._app.exec())

    def register_cat_adder(self, handler: Callable[[object, Category], None]):
        self._cat_adder = handler

    def add_category(self):
        name = ""
        parent = ""
        try:
            self.cat_adder(name, parent)
        except RuntimeError as ex:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))

    # def delete_category(self):
    #     cat = ... # определить выбранную категорию
    #     del_subcats, del_expenses = self.ask_del_cat()
    #     self.cat_deleter(cat, del_subcats, del_expenses)
