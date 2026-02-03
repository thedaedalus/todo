from datetime import datetime, timezone

import storage
from src.storage import load_tasks, save_tasks

ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def add_task(title: str, description: str, due_date: str, completed: bool = False):
    current_tasks = load_tasks()
    if current_tasks == []:
        new_id = 0
    else:
        new_id = len(current_tasks) + 1

    task_dict = {"id": f"{new_id}", "title": title, "description": description, "created_at": ts, "due_data": due_date, "completed": completed}
    current_tasks.append(task_dict)
    save_tasks(current_tasks)
