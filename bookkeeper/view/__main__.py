import sys
from PySide6 import QtWidgets  # type: ignore

from .view import Window
from .view import Table
from .view import LabeledInput


def _main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = Window("The bookkeeper app")

    layout = QtWidgets.QVBoxLayout()
    window.setLayout(layout)

    expences_table = Table(
        20,
        {
            "Дата": QtWidgets.QHeaderView.ResizeToContents,
            "Сумма": QtWidgets.QHeaderView.ResizeToContents,
            "Категория": QtWidgets.QHeaderView.ResizeToContents,
            "Комментарий": QtWidgets.QHeaderView.Stretch,
        },
    )
    budget_table = Table(
        3,
        {
            "": QtWidgets.QHeaderView.Stretch,
            "Сумма": QtWidgets.QHeaderView.Stretch,
            "Бюджет": QtWidgets.QHeaderView.Stretch,
        },
    )
    budget_table.setItem(0, 0, QtWidgets.QTableWidgetItem("День"))
    budget_table.setItem(1, 0, QtWidgets.QTableWidgetItem("Неделя"))
    budget_table.setItem(2, 0, QtWidgets.QTableWidgetItem("Месяц"))

    sum = LabeledInput("Сумма")

    category_layout = QtWidgets.QHBoxLayout()
    categories = QtWidgets.QComboBox()
    categories.addItem("Продукты")
    edit_button = QtWidgets.QPushButton("Редактировать")
    category_layout.addWidget(categories)
    category_layout.addWidget(edit_button)
    add_button = QtWidgets.QPushButton("Добавить")

    layout.addWidget(QtWidgets.QLabel("Последние расходы"))
    layout.addWidget(expences_table)
    layout.addWidget(QtWidgets.QLabel("Бюджет"))
    layout.addWidget(budget_table)
    layout.addWidget(sum)

    layout.addLayout(category_layout)

    layout.addWidget(add_button)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())


_main()
