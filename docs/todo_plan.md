# Simple To‑Do List — Project Plan & Step-by-step Guide

## One-line summary

- A beginner-friendly command-line to‑do list app that saves tasks to a JSON file and supports add/list/complete/delete. No external dependencies required.

## Why this project

- Small scope and immediate feedback.
- Teaches basics: file I/O, data structures (lists/dicts), functions, CLI interaction, datetime handling, and simple testing.
- Useful tool you can actually use.

## Core goals (MVP)

- Add a task with a title (required), optional description, and optional due date.
- List tasks (default: pending only; options to show all or completed).
- Mark a task as completed.
- Delete a task.
- Persist tasks between runs using a single JSON file.

## Simple data model

- Task (stored as a JSON object)
  - `id` — a small unique integer
  - `title` — string (required)
  - `description` — string (optional)
  - `created_at` — ISO date/time string
  - `due_date` — ISO date string (optional)
  - `completed` — boolean

## Suggested file/directory structure

- `todo/`
  - `__init__.py`
  - `cli.py` — minimal command parsing and user interaction
  - `storage.py` — read/write JSON file (create file if missing)
  - `models.py` — task creation/validation helpers
  - `app.py` — core operations: add/list/complete/delete
  - `config.py` — default storage path (e.g., `~/.todo/tasks.json`)
- `tests/`
  - `test_models.py`
  - `test_storage.py`
  - `test_app.py`
- `README.md`

## High-level flow

1. CLI parses a simple command (e.g., `add`, `list`, `complete`, `delete`).
2. CLI delegates to an app function that:
   - Loads tasks from JSON via `storage.py`.
   - Performs the operation (add/list/complete/delete).
   - Writes updated tasks back to the JSON (when needed).
3. CLI prints a friendly result message.

## Design decisions (kept simple)

- Storage format: JSON file containing a list of tasks. One file only.
- IDs: incrementing integer assigned when adding a task (ensure unique by checking existing IDs).
- Dates: use ISO 8601 strings (e.g., `YYYY-MM-DD` for due dates, `YYYY-MM-DDTHH:MM:SS` for `created_at`).
- CLI UX: minimal — plain text prompts and arguments (no external CLI library required).

## Step-by-step guide (no code)

### Phase A — Setup (10–20 minutes)

1. Create project folder and initialize a git repository.
2. Create top-level files: `README.md`, `.gitignore` (ignore the data file), and a `todo/` package folder.
3. Decide where tasks will be stored (suggested default: `~/.todo/tasks.json`). Document this in `README.md`.

### Phase B — Define data model & storage (20–40 minutes)

1. On paper, sketch one example task JSON object with all fields filled.
2. Design `storage.py` responsibilities:
   - `load_tasks()`: if file exists, read JSON and return a list of task dicts; if missing, return an empty list.
   - `save_tasks(tasks)`: write the list of task dicts back to the file, creating parent directories if required.
3. Add simple validation rules: task must have a non-empty `title`; if `due_date` is provided, validate format `YYYY-MM-DD`.

### Phase C — Core app operations (40–60 minutes)

1. Implement `add` flow:
   - Gather required input: `title`.
   - Gather optional input: `description`, `due_date`.
   - Set `created_at` to current datetime string.
   - Assign a new `id` (e.g., max existing id + 1, or 1 if none).
   - Set `completed=False`.
   - Append to tasks and save.
2. Implement `list` flow:
   - Default to listing only pending tasks (`completed == False`).
   - Provide options to show `--all` or `--completed`.
   - Display id, title, due date (if any), and a short description or created date if space allows.
3. Implement `complete` flow:
   - Accept a task `id`.
   - Find the task and set `completed=True`.
   - Save tasks and confirm to the user.
4. Implement `delete` flow:
    - Accept a task `id`.
    - Remove the matching task from the list.
    - Save tasks and confirm deletion.

### Phase D — CLI glue & UX (20–40 minutes)

1. Implement `cli.py` responsibilities:
    - Parse a very small set of command-line arguments (you may parse `sys.argv` manually).
    - Map commands to `app.py` functions.
    - Provide helpful text when the user calls the app with no arguments or with `--help`.
2. Provide clear messages for success and errors:
    - Confirm on add, complete, delete.
    - Show a friendly message when list is empty.
3. Handle the case where the storage file is corrupt: present a readable error and suggest deleting/renaming the file (do not automatically delete).

### Phase E — Manual testing & validation (15–30 minutes)
1. Manually test typical flows:
    - Add multiple tasks.
    - List tasks (pending and all).
    - Complete a task and confirm it no longer appears in pending list.
    - Delete a task and confirm it’s gone.
    - Inspect the JSON file to confirm it updates correctly.
2. Test edge cases:
    - Add a task with empty title (should be rejected).
    - Provide invalid due date format (should be rejected with help text).
    - Try completing or deleting a non-existent id (should show an error).

### Phase F — Unit tests (30–60 minutes)

1. Write tests for model helpers:
    - Creating a valid task produces required fields (`id`, `created_at`, `completed`).
    - Validation rejects empty title and invalid date formats.
2. Write tests for storage:
    - `load_tasks` returns `[]` when file missing.
    - `save_tasks` writes a file that `load_tasks` can read back unchanged.
    - Use temporary file fixtures (e.g., `tempfile` or pytest tmp path).
3. Write tests for app logic:
    - Adding a task increases count and assigns unique id.
    - Completing a task toggles `completed` to `True`.
    - Deleting a task removes it.

### Phase G — Documentation & polish (15–30 minutes)

1. Update `README.md` with:
    - Installation notes (how to run the script).
    - Usage examples (how to add, list, complete, delete).
    - Storage location and how to move it.
2. Add a short troubleshooting section: how to recover if the JSON file is corrupted (backup and recreate).

## Small milestone plan (estimated time)

- Setup & storage: 0.5 hr
- Core operations (add/list/complete/delete): 1–1.5 hr
- Manual testing & simple CLI UX: 0.5 hr
- Unit tests & README: 0.5–1 hr
Total: ~2.5–3.5 hours for a functional MVP

## Acceptance criteria

- You can add a task and see it persisted in the JSON file.
- You can list pending tasks and optionally all tasks.
- You can mark a task completed and see it reflected in the data.
- You can delete a task and it no longer appears.
- A small suite of unit tests covers storage and basic app logic.

## Easy extensions (next steps once comfortable)

- Add `priority` field (low/medium/high) and allow sorting.
- Allow editing a task’s title/description/due date.
- Add tags and allow filtering by tag.
- Add an option to export tasks to CSV.
- Add simple colorized output (green for completed, red for overdue) using a small library or ANSI codes.

## Tips for learning as you build

- Work incrementally: implement one feature, test it manually, then move to the next.
- Keep functions small and focused — one job per function.
- Use print statements for quick debugging; delete or replace them with tests when working.
- Use version control commits for small milestones (e.g., “add storage”, “implement add command”).
