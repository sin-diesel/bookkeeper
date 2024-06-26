"""
Реализация класса Bookkeeper, представляющего собой Presenter-a
в моделе Model-View-Presenter
"""

from typing import Protocol
from typing import Callable
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.abstract_repository import AbstractRepository


class AbstractView(Protocol):
    """
    Абстрактный класс для GUI.
    """

    def set_category_list(self, categories: list[Category]) -> None:
        """
        Отображает список категорий в GUI.
        """
        pass

    def register_cat_modifier(handler: Callable[[Category], None]):
        """
        Добавляет категории в GUI.
        """
        pass


class Bookkeeper:
    """
    Presenter класс, занимается передачей данных View.
    """

    def __init__(
        self,
        view: AbstractView,
        repository: AbstractRepository[Category],
        expenses_repository: AbstractRepository[Expense],
    ):
        self.view = view
        self.category_repository = repository
        self.expense_repository = expenses_repository
        self.cats = self.category_repository.get_all()
        self.expenses = self.expense_repository.get_all()
        self.view.set_category_list(self.cats)
        self.view.register_cat_adder(self.add_category)
        self.view.register_cat_deleter(self.delete_category)
        self.view.register_exp_adder(self.add_expense)
        self.view.register_exp_deleter(self.delete_expense)

    def modify_cat(self, cat: Category) -> None:
        self.category_repository.update(cat)
        self.view.set_category_list(self.cats)

    def add_category(self, name: str, parent: int | None = None):
        if name in [c.name for c in self.cats]:
            raise RuntimeError(f"Категория {name} уже существует.")
        cat = Category(name, parent)
        self.category_repository.add(cat)
        self.cats.append(cat)
        self.view.set_category_list(self.cats)

    def delete_category(self, category: Category) -> None:
        self.category_repository.delete(category.pk)
        self.cats.remove(category)
        self.view.set_category_list(self.cats)

    def add_expense(
        self, value: float, category: str, comment: str = None
    ) -> None:
        expense = Expense(value, category, comment)
        self.expense_repository.add(expense)
        self.expenses.append(expense)
        self.view.set_expenses_list(self.expenses)

    def delete_expense(self, expense: Expense) -> None:
        self.expense_repository.delete(expense.pk)
        self.expenses.remove(expense)
        self.view.set_expenses_list(self.expenses)
