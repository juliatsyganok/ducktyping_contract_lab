from class_task import Task
import json
import uuid
from typing import List, Any

class FileTaskSource:
    """Источник задач из JSON-файла"""
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath

    def get_tasks(self) -> list[Task]:
        with open(self._filepath, "r", encoding="utf-8") as f:
            raw_tasks = json.load(f)
        return [Task(id=item["id"], payload=item.get("payload", {})) for item in raw_tasks]

    def __repr__(self) -> str:
        return f"FileTaskSource(filepath={self._filepath!r})"
    


class GeneratorTaskSource:
    """Генерирует задачи программно"""
    
    def __init__(self, count: int, prefix: str = "gen"):
        self.count = count
        self.prefix = prefix
    
    def get_tasks(self) -> List[Task]:
        """Создает count задач с ID"""
        tasks = []
        for i in range(self.count):
            task_id = f"{self.prefix}-{uuid.uuid4().hex[:8]}"
            payload = {
                "gen": True,
                "index": i
            }
            task = Task(id=task_id, payload=payload)
            tasks.append(task)
        
        return tasks
    
    def __repr__(self):
        return f"GeneratorTaskSource(count={self.count}, prefix='{self.prefix}')"
    


class ApiTaskSource:
    """Источник задач из API-заглушки"""
    DEFAULT_PREFIX="api"

    def __init__(self, api_url: str = "https://api.example.com/tasks") -> None:
        self._api_url = api_url
        self._stub_data: list[dict[str, Any]] = [
            {"id": f"{self.DEFAULT_PREFIX}-{uuid.uuid4().hex[:8]}", "payload": {"source": "external_api", "priority": "high"}},
            {"id": f"{self.DEFAULT_PREFIX}-{uuid.uuid4().hex[:8]}", "payload": {"source": "external_api", "priority": "low"}},
        ]

    def get_tasks(self) -> list[Task]:
        return [Task(id=item["id"], payload=item.get("payload", {})) for item in self._stub_data]

    def __repr__(self) -> str:
        return f"ApiTaskSource(api_url={self._api_url!r})"
    


    