from typing import Protocol, runtime_checkable
from typing import List
from class_task import Task

@runtime_checkable 
class TaskSource(Protocol):
    """Протокол источника задач"""
    
    def get_tasks(self) -> List[Task]:
        """Любой источник задач должен уметь возвращать список задач"""
        ...