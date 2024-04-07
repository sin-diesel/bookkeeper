"""
Драйвер для программы.
"""

from .bookkeeper import Bookkeeper
from view.view import View
from repository.memory_repository import MemoryRepository

view = View()
memory_repo = MemoryRepository()
import code

code.interact(local={**locals(), **globals()})
bookkeeper = Bookkeeper(view, memory_repo)
view.exec()
