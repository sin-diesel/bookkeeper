"""
Драйвер для программы.
"""

from bookkeeper.models.category import Category
from bookkeeper.bookkeeper import Bookkeeper
from bookkeeper.view.view import View
from bookkeeper.repository.memory_repository import MemoryRepository

view = View()
memory_repo: MemoryRepository[Category] = MemoryRepository()
goods_pk = memory_repo.add(Category("продукты"))
meat_pk = memory_repo.add(Category("мясо", parent=goods_pk))
memory_repo.add(Category("сырое мясо"))
memory_repo.add(Category("мясные продукты"))
memory_repo.add(Category("сладости", parent=goods_pk))
memory_repo.add(Category("книги"))
memory_repo.add(Category("одежда"))
bookkeeper = Bookkeeper(view, memory_repo)
view.exec()
