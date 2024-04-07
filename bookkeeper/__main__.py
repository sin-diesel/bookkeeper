"""
Драйвер для программы.
"""

from bookkeeper.models.category import Category
from bookkeeper.bookkeeper import Bookkeeper
from bookkeeper.view.view import View
from bookkeeper.repository.memory_repository import MemoryRepository

view = View()
memory_repo: MemoryRepository[Category] = MemoryRepository()
bookkeeper = Bookkeeper(view, memory_repo)
view.exec()
