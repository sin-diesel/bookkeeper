"""
Модуль описывает репозиторий, работающий с базой данных SQLite. 
"""

import sqlite3
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SqliteRepository(AbstractRepository[T]):
    """
    Репозиторий, работащий с базой данных sqlite.
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self._db_file = db_file
        self._table_name = cls.__name__.lower()
        self._fields = get_annotations(cls, eval_str=True)
        self._fields.pop("pk")

    def add(self, obj: T) -> int:
        names = ", ".join(self.fields.keys())
        p = ", ".join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]

        with sqlite3.connect(self._db_file) as con:
            cur = con.cursor()
            cur.execute("PRAGME foreign_keys = ON")
            cur.execute(
                f"INSERT INTO {self._table_name} ({names} VALUES ({p}))", values
            )
            obj.pk = cur.lastrowid
        con.close()

        return obj.pk
