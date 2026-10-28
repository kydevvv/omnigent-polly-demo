from taskvault.core import Task, search_tasks


def _tasks():
    return [
        Task(id=1, title="Write Report", description="quarterly numbers"),
        Task(id=2, title="Buy milk", description="from the REPORT stand"),
        Task(id=3, title="Call dentist", description="schedule cleaning"),
    ]


def test_case_insensitive():
    result = search_tasks(_tasks(), "wRiTe rEpOrT")
    assert [t.id for t in result] == [1]


def test_matches_title():
    result = search_tasks(_tasks(), "dentist")
    assert [t.id for t in result] == [3]


def test_matches_description():
    result = search_tasks(_tasks(), "cleaning")
    assert [t.id for t in result] == [3]


def test_preserves_order():
    result = search_tasks(_tasks(), "report")
    assert [t.id for t in result] == [1, 2]


def test_empty_query_returns_all():
    tasks = _tasks()
    assert search_tasks(tasks, "") == tasks


def test_no_match_returns_empty():
    assert search_tasks(_tasks(), "zzz") == []
