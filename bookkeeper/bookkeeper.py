"""
Реализация класса Bookkeeper, представляющего собой Presenter-a
в моделе Model-View-Presenter
"""

from typing import Protocol
from bookkeeper.models.category import Category
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

    # def register_cat_modifier(handler: Callable[[Category], None]):
    #     pass


class Bookkeeper:
    """
    Presenter класс, занимается передачей данных View.
    """

    def __init__(
        self, view: AbstractView, repository: AbstractRepository[Category]
    ):
        self.view = view
        self.category_repository = repository
        self.cats = self.category_repository.get_all()
        self.view.set_category_list(self.cats)
        self.view.register_cat_adder(self.modify_cat)

    def modify_cat(self, cat: Category) -> None:
        self.category_repository.update(cat)
        self.view.set_category_list(self.cats)

    def add_category(self, name: str, parent: int | None = None):
        if name in [c.name for c in self.cats]:
            raise RuntimeError(f"Категория {name} уже существует.")

    #     cat = Category(name, parent)
    #     self.category_repository.add(cat)
    #     self.cats.append(cat)
    #     self.view.set_category_list(self.cats)
