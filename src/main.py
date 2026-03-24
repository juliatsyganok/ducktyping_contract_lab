from class_task import Task
from task_source import TaskSource
from sources import FileTaskSource, GeneratorTaskSource, ApiTaskSource
from task_platform import TaskPlatform

def main():
    platform = TaskPlatform()
    file_source = FileTaskSource("tasks.json")
    gen_source = GeneratorTaskSource(count=3, prefix="demo")
    api_source = ApiTaskSource()
    platform.add_source(file_source)
    platform.add_source(gen_source)
    platform.add_source(api_source)

    tasks = platform.collect_all_tasks()

    for i, task in enumerate(tasks, 1):
        print(f"{i}. ID: {task.id}")
        print(f"Данные: {task.payload}")
        print()
    
    print(f"Всего задач: {len(tasks)}")

if __name__ == "__main__":
    main()