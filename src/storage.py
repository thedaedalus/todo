import json
from pathlib import Path

from config import STORAGE_PATH

storage_path = STORAGE_PATH
file = storage_path / "tasks.json"


def load_tasks():
    try:
        if file.exists():
            f = open(file, "r")
            tasks = json.load(f)
            f.close()
            return tasks
        else:
            return []
    except Exception as e:
        print(f"ERROR: {e}")


def save_tasks(tasks):
    try:
        if file.exists():
            f = open(file, "w")

    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    tasks = load_tasks()
    print(json.dumps(tasks, indent=4))
