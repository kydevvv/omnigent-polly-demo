from taskvault.core import Task, search_tasks


def make_tasks() -> list[Task]:
    return [
        Task(id=1, title="Write demo", description="Draft the launch script"),
        Task(id=2, title="Ship it", description="Deploy the DEMO to prod"),
        Task(id=3, title="Buy milk", description="Two percent"),
    ]


def test_match_is_case_insensitive():
    tasks = make_tasks()
    assert [t.id for t in search_tasks(tasks, "DEMO")] == [1, 2]
    assert [t.id for t in search_tasks(tasks, "demo")] == [1, 2]
    assert [t.id for t in search_tasks(tasks, "dEmO")] == [1, 2]


def test_match_via_title_only():
    tasks = make_tasks()
    # "milk" appears in task 3's title but in no description.
    assert [t.id for t in search_tasks(tasks, "milk")] == [3]


def test_match_via_description_only():
    tasks = make_tasks()
    # "percent" appears in task 3's description but in no title.
    assert [t.id for t in search_tasks(tasks, "percent")] == [3]


def test_preserves_input_order():
    tasks = make_tasks()
    reversed_tasks = list(reversed(tasks))
    assert [t.id for t in search_tasks(tasks, "e")] == [1, 2, 3]
    assert [t.id for t in search_tasks(reversed_tasks, "e")] == [3, 2, 1]


def test_empty_query_returns_all_tasks():
    tasks = make_tasks()
    assert search_tasks(tasks, "") == tasks


def test_no_match_returns_empty_list():
    tasks = make_tasks()
    assert search_tasks(tasks, "nonexistent") == []


def test_returns_the_same_task_objects():
    tasks = make_tasks()
    result = search_tasks(tasks, "milk")
    assert result[0] is tasks[2]
