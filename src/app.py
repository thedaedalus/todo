import datetime
from typing import Any, Dict, List

import colorama
from prettytable.colortable import ColorTable, Themes

from storage import load_tasks, save_tasks
from utils import format_date, generate_id


def add_task(current_tasks: List[Dict[str, Any]], title: str, description: str, due_date: str, completed: bool = False) -> List[Dict[str, Any]]:
    ts: str = str(datetime.date.today())
    new_id: int = generate_id(current_tasks)
    if due_date:
        due_date: str = str(format_date(due_date))
    else:
        due_date = ""
    task_dict: Dict[str, Any] = {"id": new_id, "title": title, "description": description, "created_at": ts, "due_date": due_date, "completed": completed}
    current_tasks.append(task_dict)
    return current_tasks


def list_tasks(current_tasks: List[Dict[str, Any]], completed=False, show_all=False) -> str:
    tasks_table = ColorTable(theme=Themes.PASTEL)
    tasks_table.field_names = ["ID", "Title", "Due Date", "Description"]
    for task in current_tasks:
        if completed:
            if task["completed"] is True:
                tasks_table.add_row([task["id"], task["title"], task["due_date"], task["description"]])
        elif show_all:
            tasks_table.add_row([task["id"], task["title"], task["due_date"], task["description"]])
        else:
            if task["completed"] is False:
                tasks_table.add_row([task["id"], task["title"], task["due_date"], task["description"]])
    return tasks_table.get_string(sortby="ID")


def complete_task(current_tasks: List[Dict[str, Any]], task_id: int) -> List[Dict[str, Any]]:
    for task in current_tasks:
        if task["id"] == task_id:
            task["completed"] = True
    return current_tasks


def delete_task(current_tasks: List[Dict[str, Any]], task_id: int) -> List[Dict[str, Any]]:
    for task in current_tasks:
        if task["id"] == task_id:
            current_tasks = [task for task in current_tasks if task.get("id") != task_id]
    return current_tasks


if __name__ == "__main__":
    current_tasks: List[Dict[str, Any]] = load_tasks()
    print(list_tasks(current_tasks, completed=True, show_all=False))
