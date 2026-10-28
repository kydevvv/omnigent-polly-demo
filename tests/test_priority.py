import pytest

from taskvault.core import TaskVault, VALID_PRIORITIES


@pytest.mark.parametrize("priority", VALID_PRIORITIES)
def test_each_valid_priority_is_accepted(priority):
    vault = TaskVault()

    task = vault.add_task("valid priority", priority=priority)

    assert task.priority == priority


def test_invalid_priority_raises_value_error():
    vault = TaskVault()

    with pytest.raises(ValueError) as exc_info:
        vault.add_task("invalid priority", priority="urgent")

    message = str(exc_info.value)
    assert "urgent" in message
    assert repr(VALID_PRIORITIES) in message
