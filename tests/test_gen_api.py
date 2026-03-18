import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import json
import pytest
from class_task import Task
from sources import FileTaskSource, GeneratorTaskSource, ApiTaskSource


@pytest.fixture
def temp_json_file(tmp_path):
    """Временный JSON-файл с тремя задачами"""
    data = [
        {"id": "1", "payload": {"task": "test1"}},
        {"id": "2", "payload": {"task": "test2"}},
        {"id": "3"}
    ]
    file_path = tmp_path / "tasks.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return str(file_path)


@pytest.fixture
def empty_json_file(tmp_path):
    """Пустой JSON-файл"""
    file_path = tmp_path / "empty.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([], f)
    return str(file_path)


def test_file_read(temp_json_file):
    """Чтение задач из файла"""
    source = FileTaskSource(temp_json_file)
    tasks = source.get_tasks()
    
    assert len(tasks) == 3
    assert tasks[0].id == "1"
    assert tasks[0].payload == {"task": "test1"}
    assert tasks[2].payload == {}


def test_file_empty(empty_json_file):
    """Пустой файл"""
    source = FileTaskSource(empty_json_file)
    tasks = source.get_tasks()
    assert tasks == []


def test_file_missing():
    """Файл не найден"""
    source = FileTaskSource("missing.json")
    with pytest.raises(FileNotFoundError):
        source.get_tasks()


def test_gen_count():
    """Количество задач"""
    source = GeneratorTaskSource(count=5, prefix="test")
    tasks = source.get_tasks()
    assert len(tasks) == 5


def test_gen_struct():
    """Структура задач"""
    source = GeneratorTaskSource(count=2, prefix="test")
    tasks = source.get_tasks()
    
    for i, task in enumerate(tasks):
        assert task.id.startswith("test-")
        assert task.payload == {"gen": True, "index": i}


def test_gen_zero():
    """Ноль задач"""
    source = GeneratorTaskSource(count=0)
    tasks = source.get_tasks()
    assert tasks == []


def test_api_return():
    """API возвращает заглушки"""
    source = ApiTaskSource()
    tasks = source.get_tasks()
    
    assert len(tasks) == 2
    assert tasks[0].payload.get("source") == "external_api"
    assert tasks[1].payload.get("priority") in ["high", "low"]


def test_api_id():
    """ID уникальны"""
    source = ApiTaskSource()
    tasks = source.get_tasks()
    
    assert tasks[0].id != tasks[1].id
    assert tasks[0].id.startswith("api-")

