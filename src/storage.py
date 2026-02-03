import json
from pathlib import Path

from config import STORAGE_PATH

storage_path = STORAGE_PATH
tasks_file = storage_path / "tasks.json"


def load_tasks():
    try:
        if tasks_file.exists():
            with tasks_file.open(mode="r", encoding="utf-8") as json_file:
                content = json.load(json_file)
                if content is None:
                    raise Exception(f"ERROR: {tasks} is either empty or malformed")
            return tasks
        else:
            return []
    except Exception as e:
        print(f"ERROR: {e}")


def save_tasks(tasks):
    try:
        if tasks_file.exists():
            with tasks_file.open(mode="w", encoding="utf-8") as json_file:
                json.dump(tasks, json_file)
        else:
            tasks_file.touch(exist_ok=False)
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    tasks = load_tasks()
    print(tasks[0]["title"])
    # print(json.dumps(tasks, indent=4))
