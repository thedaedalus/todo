import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from config import STORAGE_PATH

storage_path = Path(STORAGE_PATH).expanduser()
tasks_file = storage_path / "tasks.json"
ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def load_tasks() -> List[Dict[str, Any]]:
    """
    Loads tasks data from a JSON file.
    - Returns an empty list if the file does not exist.
    - Raises a helpful error message if the file contains invalid JSON or the top level value is not a list.
    """
    if not tasks_file.exists():
        return []
    try:
        with tasks_file.open(mode="r", encoding="utf-8") as json_file:
            content = json.load(json_file)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"failed to parse JSON in {tasks_file}: {e}The file maybe corrupted")
    except Exception as e:
        raise RuntimeError(f"ERROR: Failed to parse JSON in {tasks_file}: {e}. The file maybe corrupt, please backup and recreate ")

    if not isinstance(content, list):
        raise RuntimeError(f"ERROR: Expected a list of tasks in {tasks_file}, got {type(content).__name__}")
    return content


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """
    Saves tasks to a JSON file.
    - Ensures parent dir exists.
    - Creates a backup first
    - Writes pretty JSON
    """
    try:
        storage_path.mkdir(parents=True, exist_ok=True)
        if tasks_file.exists():
            backup_file = storage_path / f"tasks_backup-{ts}.json"
            shutil.copyfile(tasks_file, str(backup_file))
        with backup_file.open(mode="w", encoding="utf-8") as json_file:
            json.dump(tasks, json_file, indent=2, ensure_ascii=False)
        shutil.copy(backup_file, tasks_file)
    except Exception as e:
        raise RuntimeError(f"ERROR: Failed to save tasks to {tasks_file}: {e}")


if __name__ == "__main__":
    try:
        tasks = load_tasks()
    except RuntimeError as e:
        print(f"ERROR: {e}")
    else:
        if tasks:
            print(tasks[0].get("id", "<no id>"))
        else:
            print("No tasks found.")
