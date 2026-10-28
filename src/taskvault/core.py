"""TaskVault core — a tiny, dependency-free task tracker.

The functions here are intentionally small and independent so that
separate features can be built in parallel. See ISSUES.md for the
work items.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

VALID_PRIORITIES = ("low", "medium", "high")


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
        if priority not in VALID_PRIORITIES:
            raise ValueError(
                f"invalid priority {priority!r}; allowed priorities are {VALID_PRIORITIES}"
            )

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
