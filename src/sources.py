from class_task import Task
import json
import uuid
from typing import List, Any
import requests

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
    


import requests
from typing import Any, List


class ApiTaskSource:
    """Источник задач из API"""
    DEFAULT_PREFIX = "api"
    def __init__(self, api_url: str = "https://dummyjson.com/todos") -> None:
        self.api_url = api_url

    def get_tasks(self) -> List[Task]:
        """Получает задачи из API и преобразует их в Task"""
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status() 
            data = response.json()
            tasks: List[Task] = []
            for item in data.get("todos", [])[:10]: 
                task = Task(
                    id=f"{self.DEFAULT_PREFIX}-{item['id']}",
                    payload={
                        "title": item["todo"],
                        "completed": item["completed"],
                        "user_id": item["userId"],
                        "priority": "high" if not item["completed"] else "low"
                    }
                )
                tasks.append(task)
            return tasks
        except requests.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return []

    def __repr__(self) -> str:
        return f"ApiTaskSource(api_url={self.api_url!r})"
    