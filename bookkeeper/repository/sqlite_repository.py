"""
Модуль описывает репозиторий, работающий с базой данных SQLite.
"""

import sqlite3
from inspect import getmembers
from inspect import isroutine
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SqliteRepository(AbstractRepository[T]):
    """
    Репозиторий, работащий с базой данных sqlite.
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self._db_file = db_file
        self._cls = cls
        self._table_name = cls.__name__.lower()
        attrs = getmembers(cls, lambda a: not(isroutine(a)))
        self._fields = [a[0] for a in attrs if not(a[0].startswith('__') and a[0].endswith('__'))]
        self._fields.remove("pk")


    def add(self, obj: T) -> int | None:
        if not isinstance(obj, self._cls):
            raise ValueError(f"Passing object of type {obj.__class__} instead of {self._cls}")

        names = ", ".join(self._fields)
        p = ", ".join("?" * len(self._fields))
        values = [getattr(obj, x) for x in self._fields]

        if len(values) == 0:
            return None

        with sqlite3.connect(self._db_file) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(
                f"INSERT INTO {self._table_name} ({names} VALUES ({p}))", values
            )
            obj.pk = cur.lastrowid  # type: ignore
        con.close()

        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self._db_file) as con:
            cur = con.cursor()
            cur.execute(
                f"SELECT * FROM {self._table_name}" f"WHERE row_number() = {pk}"
            )
            data = cur.fetchall()
        con.close()
        obj = None
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        pass

    def update(self, obj: T) -> None:
        pass

    def delete(self, pk: int) -> None:
        pass
