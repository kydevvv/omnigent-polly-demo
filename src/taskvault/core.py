"""TaskVault core — a tiny, dependency-free task tracker.

The functions here are intentionally small and independent so that
separate features can be built in parallel. See ISSUES.md for the
work items.
"""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

VALID_PRIORITIES = ("low", "medium", "high")

#: Column order for :func:`export_to_csv`, also used as the header row.
CSV_COLUMNS = ("id", "title", "priority", "due", "done")


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    priority: str = "medium"
    due: Optional[date] = None
    done: bool = False


@dataclass
class TaskVault:
    """An in-memory collection of tasks."""

    _tasks: list[Task] = field(default_factory=list)
    _next_id: int = 1

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due: Optional[date] = None,
    ) -> Task:
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            due=due,
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def complete(self, task_id: int) -> Task:
        for t in self._tasks:
            if t.id == task_id:
                t.done = True
                return t
        raise KeyError(f"no task with id {task_id}")

    def all_tasks(self) -> list[Task]:
        return list(self._tasks)

    def open_tasks(self) -> list[Task]:
        return [t for t in self._tasks if not t.done]


def sort_by_due_date(tasks: list[Task]) -> list[Task]:
    """Return tasks sorted by due date, soonest first.

    Tasks without a due date should sort AFTER all dated tasks.

    NOTE: this currently has a bug — see ISSUES.md issue #2.
    """
    # BUG: reverse=True sorts latest-first, and undated tasks (sorted as
    # date.max) end up first instead of last.
    return sorted(tasks, key=lambda t: t.due or date.max, reverse=True)


def export_to_csv(tasks: list[Task], path: str | os.PathLike[str]) -> None:
    """Write ``tasks`` to ``path`` as CSV, with a header row.

    Columns are written in the order given by :data:`CSV_COLUMNS`:
    ``id,title,priority,due,done``.

    Serialization contract:

    * ``due`` is ``date.isoformat()`` (``YYYY-MM-DD``) when set, and the
      empty string when it is ``None``.
    * ``done`` is written as ``True`` / ``False`` — the default rendering
      of Python's ``bool`` via the :mod:`csv` module's ``str()`` coercion.

    The file is opened with ``newline=""`` as the :mod:`csv` docs require,
    so no spurious blank rows appear on any platform.
    """
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(CSV_COLUMNS)
        for t in tasks:
            writer.writerow(
                [
                    t.id,
                    t.title,
                    t.priority,
                    t.due.isoformat() if t.due is not None else "",
                    t.done,
                ]
            )
