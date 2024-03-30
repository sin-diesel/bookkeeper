"""
Модуль описывает репозиторий, работающий с базой данных SQLite.
"""

import sqlite3
import logging
from inspect import get_annotations
from typing import Any
from pathlib import Path

from bookkeeper.repository.abstract_repository import AbstractRepository, T


_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)


class SqliteRepository(AbstractRepository[T]):
    """
    Репозиторий, работащий с базой данных sqlite.
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self._db_file = db_file
        self._cls = cls
        self._table_name = cls.__name__.lower()
        self._fields = get_annotations(cls)
        self._fields.pop("pk")

        names = ", ".join(self._fields)
        if not Path.exists(Path(self._db_file)):
            _logger.info(
                f"Database not detected at {self._db_file}. A new one will be created."
            )
            with sqlite3.connect(self._db_file) as con:
                cur = con.cursor()
                cur.execute(f"CREATE TABLE {self._table_name}({names})")
            con.close()
        else:
            _logger.info(f"Database at {self._db_file} already exists.")

    def add(self, obj: T) -> int:
        if not isinstance(obj, self._cls):
            raise ValueError(
                f"Passing object of type {obj.__class__} instead of {self._cls}"
            )

        fields = ", ".join("?" * len(self._fields.keys()))
        values = [getattr(obj, x) for x in self._fields]

        with sqlite3.connect(self._db_file) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(
                f"INSERT INTO {self._table_name} VALUES ({fields})", values
            )
            obj.pk = cur.lastrowid  # type: ignore
        con.close()

        return obj.pk  # type: ignore

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self._db_file) as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {self._table_name} WHERE rowid = {pk}")
            data = cur.fetchone()
        if data is None:
            return None
        obj = self._cls(*data, pk)
        con.close()
        return obj  # type: ignore

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        return []

    def update(self, obj: T) -> None:
        fields_stringified = ", ".join(
            [f"{field} = {getattr(obj, field)}" for field in self._fields]
        )
        with sqlite3.connect(self._db_file) as con:
            cur = con.cursor()
            cur.execute(
                f"UPDATE {self._table_name} SET {fields_stringified} "
                f"WHERE rowid = {obj.pk}"
            )
        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self._db_file) as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {self._table_name} WHERE rowid = {pk}")
        con.close()
