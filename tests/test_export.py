import csv
from datetime import date

from taskvault.core import Task, export_to_csv


def read_export(path):
    with path.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def test_export_has_expected_header_and_columns(tmp_path):
    path = tmp_path / "tasks.csv"

    export_to_csv([], path)

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        assert next(reader) == ["id", "title", "priority", "due", "done"]


def test_export_renders_due_date_as_iso_format(tmp_path):
    path = tmp_path / "tasks.csv"
    task = Task(id=1, title="deadline", due=date(2026, 1, 2))

    export_to_csv([task], path)

    assert read_export(path)[0]["due"] == "2026-01-02"


def test_export_renders_missing_due_date_as_empty_field(tmp_path):
    path = tmp_path / "tasks.csv"
    task = Task(id=1, title="someday")

    export_to_csv([task], path)

    assert read_export(path)[0]["due"] == ""


def test_export_renders_done_flag(tmp_path):
    path = tmp_path / "tasks.csv"
    task = Task(id=1, title="finished", done=True)

    export_to_csv([task], path)

    assert read_export(path)[0]["done"] == "True"
