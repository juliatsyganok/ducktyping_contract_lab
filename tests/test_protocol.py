import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from class_task import Task
from task_source import TaskSource
from task_platform import TaskPlatform


class ValidSource:
    """Есть get_tasks"""
    def get_tasks(self):
        return [Task(id="valid")]


class InvalidSource:
    """Нет get_tasks"""
    pass


class DiffSig:
    """Другая сигнатура"""
    def get_tasks(self, extra):
        return [Task(id="different")]


class StaticSrc:
    """Статический метод"""
    @staticmethod
    def get_tasks():
        return [Task(id="static")]


class ClassSrc:
    """Класс-метод"""
    @classmethod
    def get_tasks(cls):
        return [Task(id="class")]


def test_isinstance_valid():
    """Проверка корректного источника"""
    assert isinstance(ValidSource(), TaskSource)


def test_isinstance_invalid():
    """Проверка некорректного источника"""
    assert not isinstance(InvalidSource(), TaskSource)


def test_isinstance_sig():
    """Проверка с другой сигнатурой"""
    assert isinstance(DiffSig(), TaskSource)


def test_isinstance_static():
    """Проверка статического метода"""
    assert isinstance(StaticSrc(), TaskSource)


def test_isinstance_class():
    """Проверка класс-метода"""
    assert isinstance(ClassSrc(), TaskSource)


def test_subclass_valid():
    """issubclass с корректным"""
    assert issubclass(ValidSource, TaskSource)


def test_subclass_invalid():
    """issubclass с некорректным"""
    assert not issubclass(InvalidSource, TaskSource)


def test_platform_valid():
    """Платформа принимает ValidSource"""
    platform = TaskPlatform()
    platform.add_source(ValidSource())
    assert platform.source_count == 1


def test_platform_duck():
    """Платформа принимает утку"""
    platform = TaskPlatform()
    
    class Duck:
        def get_tasks(self):
            return [Task(id="duck")]
    
    platform.add_source(Duck())
    tasks = platform.collect_all_tasks()
    assert tasks[0].id == "duck"


def test_platform_invalid():
    """Платформа не принимает InvalidSource"""
    platform = TaskPlatform()
    
    with pytest.raises(TypeError):
        platform.add_source(InvalidSource())


def test_platform_static():
    """Платформа работает со статикой"""
    platform = TaskPlatform()
    platform.add_source(StaticSrc())
    tasks = platform.collect_all_tasks()
    assert tasks[0].id == "static"


def test_runtime():
    """runtime_checkable работает"""
    class Simple:
        def get_tasks(self):
            return []
    
    obj = Simple()
    assert isinstance(obj, TaskSource)