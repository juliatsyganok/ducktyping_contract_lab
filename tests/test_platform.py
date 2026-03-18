import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from unittest.mock import Mock
from class_task import Task
from task_platform import TaskPlatform
from task_source import TaskSource


@pytest.fixture
def platform():
    """Пустая платформа"""
    return TaskPlatform()


@pytest.fixture
def mock_source():
    """Мок с двумя задачами"""
    source = Mock(spec=TaskSource)
    source.get_tasks.return_value = [
        Task(id="1", payload={"test": True}),
        Task(id="2", payload={})
    ]
    return source


@pytest.fixture
def empty_source():
    """Мок без задач"""
    source = Mock(spec=TaskSource)
    source.get_tasks.return_value = []
    return source


def test_add_one(platform, mock_source):
    """Добавление одного источника"""
    platform.add_source(mock_source)
    assert platform.source_count == 1


def test_add_two(platform, mock_source, empty_source):
    """Добавление двух источников"""
    platform.add_source(mock_source)
    platform.add_source(empty_source)
    assert platform.source_count == 2


def test_add_bad(platform):
    """Добавление не-источника"""
    with pytest.raises(TypeError):
        platform.add_source(object())


def test_add_no_method(platform):
    """Объект без метода get_tasks"""
    class Fake:
        pass
    
    with pytest.raises(TypeError):
        platform.add_source(Fake())


def test_add_implicit(platform):
    """Объект с get_tasks но без протокола"""
    class Implicit:
        def get_tasks(self):
            return [Task(id="implicit")]
    
    platform.add_source(Implicit())
    assert platform.source_count == 1


def test_collect_none(platform):
    """Сбор без источников"""
    tasks = platform.collect_all_tasks()
    assert tasks == []


def test_collect_one(platform, mock_source):
    """Сбор из одного источника"""
    platform.add_source(mock_source)
    tasks = platform.collect_all_tasks()
    
    assert len(tasks) == 2
    assert tasks[0].id == "1"
    mock_source.get_tasks.assert_called_once()


def test_collect_two(platform, mock_source, empty_source):
    """Сбор из двух источников"""
    platform.add_source(mock_source)
    platform.add_source(empty_source)
    
    tasks = platform.collect_all_tasks()
    
    assert len(tasks) == 2
    mock_source.get_tasks.assert_called_once()
    empty_source.get_tasks.assert_called_once()


def test_collect_order(platform):
    """Порядок задач сохраняется"""
    source1 = Mock(spec=TaskSource)
    source1.get_tasks.return_value = [Task(id="A"), Task(id="B")]
    
    source2 = Mock(spec=TaskSource)
    source2.get_tasks.return_value = [Task(id="C")]
    
    platform.add_source(source1)
    platform.add_source(source2)
    
    tasks = platform.collect_all_tasks()
    ids = [t.id for t in tasks]
    
    assert ids == ["A", "B", "C"]


def test_collect_twice(platform, mock_source):
    """Два сбора подряд"""
    platform.add_source(mock_source)
    
    platform.collect_all_tasks()
    platform.collect_all_tasks()
    
    assert mock_source.get_tasks.call_count == 2


def test_count_init(platform):
    """Начальное количество"""
    assert platform.source_count == 0


def test_count_after(platform, mock_source):
    """Количество после добавления"""
    platform.add_source(mock_source)
    assert platform.source_count == 1