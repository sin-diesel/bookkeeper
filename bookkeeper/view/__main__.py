import sys
from PySide6 import QtWidgets  # type: ignore

from .view import Window
from .view import ExpensesTable


def _main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = Window("The bookkeeper app")

    expences_table = ExpensesTable(
        20, ["Дата", "Сумма", "Категория", "Комментарий"]
    )
    window.setCentralWidget(expences_table)

    window.show()
    sys.exit(app.exec())


_main()
