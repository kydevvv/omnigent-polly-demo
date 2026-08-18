from datetime import date

from taskvault.core import Task, sort_by_due_date


def test_sort_by_due_date_orders_dated_tasks_soonest_first():
    tasks = [
        Task(id=1, title="later", due=date(2026, 3, 15)),
        Task(id=2, title="soon", due=date(2026, 1, 10)),
        Task(id=3, title="middle", due=date(2026, 2, 20)),
    ]

    assert sort_by_due_date(tasks) == [tasks[1], tasks[2], tasks[0]]


def test_sort_by_due_date_puts_undated_tasks_last():
    dated = Task(id=1, title="dated", due=date(2026, 1, 10))
    undated = Task(id=2, title="undated")

    assert sort_by_due_date([undated, dated]) == [dated, undated]


def test_sort_by_due_date_handles_mixed_and_empty_lists_without_mutating():
    undated = Task(id=1, title="undated")
    dated = Task(id=2, title="dated", due=date(2026, 1, 10))
    tasks = [undated, dated]

    result = sort_by_due_date(tasks)

    assert result == [dated, undated]
    assert result is not tasks
    assert tasks == [undated, dated]
    assert sort_by_due_date([]) == []
