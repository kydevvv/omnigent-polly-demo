import pytest

from taskvault.core import TaskVault, VALID_PRIORITIES


def test_each_valid_priority_is_accepted():
    vault = TaskVault()

    for priority in VALID_PRIORITIES:
        task = vault.add_task(f"task {priority}", priority=priority)
        assert task.priority == priority

    assert [task.priority for task in vault.all_tasks()] == list(VALID_PRIORITIES)


def test_invalid_priority_raises_helpful_value_error():
    vault = TaskVault()

    with pytest.raises(
        ValueError,
        match="invalid priority 'urgent'; allowed values are: low, medium, high",
    ):
        vault.add_task("bad priority", priority="urgent")


def test_default_priority_still_works():
    vault = TaskVault()

    task = vault.add_task("default priority")

    assert task.priority == "medium"


def test_invalid_priority_does_not_mutate_vault():
    vault = TaskVault()
    existing = vault.add_task("existing", priority="low")
    tasks_before = vault.all_tasks()
    next_id_before = vault._next_id

    with pytest.raises(ValueError):
        vault.add_task("bad priority", priority="urgent")

    assert vault.all_tasks() == tasks_before == [existing]
    assert vault._next_id == next_id_before


def test_priority_validation_is_case_sensitive():
    vault = TaskVault()

    with pytest.raises(
        ValueError,
        match="invalid priority 'HIGH'; allowed values are: low, medium, high",
    ):
        vault.add_task("uppercase priority", priority="HIGH")
