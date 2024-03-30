#!/usr/bin/env python3
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SqliteRepository

import pytest


def custom_class():
    class Custom():
        pk = 0

    return Custom


@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), custom_class),
                                               (SqliteRepository(), custom_class)])
def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None

@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), custom_class),
                                               (SqliteRepository(), custom_class)])
def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)

@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), custom_class),
                                               (SqliteRepository(), custom_class)])
def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)

@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), custom_class),
                                               (SqliteRepository(), custom_class)])
def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)

@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), custom_class),
                                               (SqliteRepository(), custom_class)])
def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)

@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), custom_class),
                                               (SqliteRepository(), custom_class)])
def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects

@pytest.mark.parametrize("repo,custom_class", [(MemoryRepository(), custom_class),
                                               (SqliteRepository(), custom_class)])
def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        o.test = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'name': '0'}) == [objects[0]]
    assert repo.get_all({'test': 'test'}) == objects
