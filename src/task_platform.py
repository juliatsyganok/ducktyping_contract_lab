from typing import List
from task_source import TaskSource
from class_task import Task

class TaskPlatform:
    """Платформа для сбора задач"""
    
    def __init__(self):
        self._sources = [] 
    
    def add_source(self, source: TaskSource) -> None:
        if not isinstance(source, TaskSource):
            raise TypeError(
                f"{type(source).__name__} не является источником задач\n")
        
        self._sources.append(source)
    
    def collect_all_tasks(self) -> List[Task]:
        all_tasks = []
        
        for source in self._sources:
            tasks = source.get_tasks()
            all_tasks.extend(tasks)
        
        return all_tasks
    
    @property
    def source_count(self) -> int:
        """Количество источников"""
        return len(self._sources)