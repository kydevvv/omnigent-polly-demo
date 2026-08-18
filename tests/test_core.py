from datetime import date

from taskvault.core import TaskVault


def test_add_and_list():
    vault = TaskVault()
    t = vault.add_task("write demo", priority="high")
    assert t.id == 1
    assert t.title == "write demo"
    assert t.priority == "high"
    assert vault.open_tasks() == [t]


def test_complete():
    vault = TaskVault()
    t = vault.add_task("ship it")
    vault.complete(t.id)
    assert vault.open_tasks() == []
    assert vault.all_tasks()[0].done is True


def test_ids_increment():
    vault = TaskVault()
    a = vault.add_task("a")
    b = vault.add_task("b")
    assert (a.id, b.id) == (1, 2)


def test_due_dates_are_stored():
    vault = TaskVault()
    t = vault.add_task("deadline", due=date(2026, 1, 1))
    assert t.due == date(2026, 1, 1)
