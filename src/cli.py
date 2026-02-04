from typing import Annotated, Any, Dict, List, Optional

import typer
from rich.prompt import Prompt

import storage
from app import add_task, complete_task, delete_task, list_tasks
from storage import save_tasks
from utils import format_date, validate_date

cli_app = typer.Typer()


@cli_app.command()
def new() -> None:
    current_tasks: List[Dict[str, Any]] = storage.load_tasks()
    title: str = Prompt.ask("Enter a title for you task")
    description: str = Prompt.ask("Enter a description of the task")
    due_date: str = Prompt.ask("(Optional) Enter a due date Format YYYY-MM-DD)", default="")

    if due_date != "":
        if validate_date(due_date):
            due_date = str(format_date(due_date))
            current_tasks = add_task(current_tasks, title, description, due_date)
            save_tasks(current_tasks)
            raise typer.Exit()

        else:
            raise ValueError("Invalid Date please use YYYY-MM-DD")
    else:
        current_tasks = add_task(current_tasks, title, description, due_date)
        save_tasks(current_tasks)
        raise typer.Exit()


@cli_app.command()
def list(completed: Annotated[bool, typer.Option(help="Display completed tasks")] = False, show_all: Annotated[bool, typer.Option(help="Display all tasks")] = False):
    current_tasks: List[Dict[str, Any]] = storage.load_tasks()

    if completed:
        print(list_tasks(current_tasks, completed=completed))
        raise typer.Exit()
    elif all:
        print(list_tasks(current_tasks, show_all=show_all))
        raise typer.Exit()
    else:
        print(list_tasks(current_tasks))
        raise typer.Exit()


@cli_app.command()
def complete():
    current_tasks: List[Dict[str, Any]] = storage.load_tasks()
    id: int = int(Prompt.ask("Enter ID of task to complete"))
    current_tasks = complete_task(current_tasks, id)
    save_tasks(current_tasks)
    raise typer.Exit()


@cli_app.command()
def delete():
    current_tasks: List[Dict[str, Any]] = storage.load_tasks()
    id: int = int(Prompt.ask("Enter ID of task to delete"))
    for task in current_tasks:
        if task["id"] == id:
            title: str = task["title"]
    delete: bool = typer.confirm(f"Are you sure you want to delete {id}: {title}")
    if not delete:
        print(f"Not Deleting {id}: {title}")
        raise typer.Abort()
    print(f"Deleting {id}: {title}")
    current_tasks = delete_task(current_tasks, id)
    save_tasks(current_tasks)
    raise typer.Exit()


if __name__ == "__main__":
    cli_app()
