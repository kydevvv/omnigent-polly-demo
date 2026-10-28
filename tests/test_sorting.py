from datetime import date

from taskvault.core import Task, sort_by_due_date


def test_sorts_soonest_first():
    late = Task(id=1, title="late", due=date(2026, 12, 1))
    soon = Task(id=2, title="soon", due=date(2026, 1, 5))
    mid = Task(id=3, title="mid", due=date(2026, 6, 15))
    assert sort_by_due_date([late, soon, mid]) == [soon, mid, late]


def test_undated_tasks_sort_last():
    undated = Task(id=1, title="undated")
    late = Task(id=2, title="late", due=date(2026, 12, 1))
    soon = Task(id=3, title="soon", due=date(2026, 1, 5))
    assert sort_by_due_date([undated, late, soon]) == [soon, late, undated]
