from datetime import date, datetime
from typing import Any, Optional


def generate_id(tasks) -> int:
    """
    Generates an integer to be used as an ID.
    - `tasks` is a list of dicts where existing tasks may have an 'id'.
    - Only integer ids are considered. If none exist, returns 1.
    """
    if not tasks:
        return 1
    ids = [t.get("id") for t in tasks if isinstance(t.get("id"), int)]
    return max(ids, default=0) + 1


def validate_date(input_date: Any) -> bool:
    """
    Return True if input_date is a string in YYYY-MM-DD format
    """
    if not isinstance(input_date, str):
        return False
    fmt = "%Y-%m-%d"
    try:
        datetime.strptime(input_date.strip(), fmt)
    except ValueError:
        return False
    return True


def format_date(input_date: Any) -> Optional[str]:
    """
    Normalize input_date to 'YYYY-MM-DD' if valid, otherwise return None.
    - Accepts a string; returns canonical YYYY-MM-DD or None.
    """
    if not isinstance(input_date, str):
        return None
    fmt = "%Y-%m-%d"
    try:
        parsed = datetime.strptime(input_date.strip(), fmt)
    except ValueError:
        return None
    return parsed.date().isoformat()
