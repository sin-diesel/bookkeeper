#!/usr/bin/env python3
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SqliteRepository

import pytest
from pathlib import Path

_repo_path = Path(__file__).parent.parent.parent

class Custom():
    value: int
    pk: int
    def __init__(self, value: int = 0, pk: int = 0):
        self.value = value
        self.pk = pk

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Custom):
            raise NotImplementedError
        return self.value == other.value and self.pk == other.pk

def db_name() -> str:
    return _repo_path / "tests" / "test_db.db"


@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), Custom), (SqliteRepository(db_name(), Custom), Custom)])
def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    ret = repo.get(pk)
    assert ret == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj
    repo.delete(pk)
    assert repo.get(pk) is None

@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), Custom), (SqliteRepository(db_name(), Custom), Custom)])
def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)

@pytest.mark.parametrize("repo", [(MemoryRepository()), (SqliteRepository(db_name(), Custom))])
def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)

@pytest.mark.parametrize("repo", [(MemoryRepository()), (SqliteRepository(db_name(), Custom))])
def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)

@pytest.mark.parametrize("repo,custom_class",[(MemoryRepository(), Custom), (SqliteRepository(db_name(), Custom), Custom)])
def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)

@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), Custom), (SqliteRepository(db_name(), Custom), Custom)])
def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects

@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), Custom), (SqliteRepository(db_name(), Custom), Custom)])
def test_get_all_with_condition(repo, custom_class):
    objects = []
    repo.clear()
    for i in range(5):
        o = custom_class()
        o.value = i
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'value': 0}) == [objects[0]]
    assert repo.get_all({'value': 4}) == [objects[-1]]
