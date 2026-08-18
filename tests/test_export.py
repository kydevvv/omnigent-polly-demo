import csv
from datetime import date

from taskvault.cli import build_parser
from taskvault.core import CSV_COLUMNS, Task, export_to_csv


def _read_rows(path):
    """Read a CSV file back as a list of raw rows."""
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.reader(fh))


def test_header_row_and_column_order(tmp_path):
    path = tmp_path / "tasks.csv"
    export_to_csv([], path)

    rows = _read_rows(path)
    assert rows[0] == ["id", "title", "priority", "due", "done"]
    # The exported header must match the documented column order constant.
    assert rows[0] == list(CSV_COLUMNS)


def test_empty_task_list_writes_header_only(tmp_path):
    path = tmp_path / "empty.csv"
    export_to_csv([], path)

    rows = _read_rows(path)
    assert len(rows) == 1
    assert rows[0] == list(CSV_COLUMNS)


def test_due_date_renders_iso(tmp_path):
    path = tmp_path / "dated.csv"
    export_to_csv([Task(id=1, title="ship it", due=date(2026, 1, 31))], path)

    rows = _read_rows(path)
    assert rows[1] == ["1", "ship it", "medium", "2026-01-31", "False"]
    # `due` is exactly date.isoformat().
    assert rows[1][3] == date(2026, 1, 31).isoformat()


def test_unset_due_renders_empty_string(tmp_path):
    path = tmp_path / "undated.csv"
    export_to_csv([Task(id=7, title="someday", due=None)], path)

    rows = _read_rows(path)
    assert rows[1][3] == ""
    assert rows[1] == ["7", "someday", "medium", "", "False"]


def test_done_serializes_as_true_false(tmp_path):
    """Pin the `done` contract: Python's default bool rendering."""
    path = tmp_path / "done.csv"
    export_to_csv(
        [
            Task(id=1, title="finished", done=True),
            Task(id=2, title="pending", done=False),
        ],
        path,
    )

    rows = _read_rows(path)
    assert rows[1][4] == "True"
    assert rows[2][4] == "False"


def test_round_trip_with_dict_reader(tmp_path):
    path = tmp_path / "roundtrip.csv"
    tasks = [
        Task(id=1, title="alpha", priority="high", due=date(2026, 3, 1), done=True),
        Task(id=2, title="beta", priority="low", due=None, done=False),
    ]
    export_to_csv(tasks, path)

    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == list(CSV_COLUMNS)
        records = list(reader)

    assert records[0] == {
        "id": "1",
        "title": "alpha",
        "priority": "high",
        "due": "2026-03-01",
        "done": "True",
    }
    assert records[1] == {
        "id": "2",
        "title": "beta",
        "priority": "low",
        "due": "",
        "done": "False",
    }

    # Values round-trip back into their original Python types.
    assert int(records[0]["id"]) == tasks[0].id
    assert date.fromisoformat(records[0]["due"]) == tasks[0].due
    assert records[1]["due"] == ""


def test_row_order_follows_input_order(tmp_path):
    path = tmp_path / "order.csv"
    export_to_csv(
        [Task(id=3, title="third"), Task(id=1, title="first")],
        path,
    )

    rows = _read_rows(path)
    assert [r[0] for r in rows[1:]] == ["3", "1"]


def test_no_spurious_blank_rows(tmp_path):
    """newline="" means rows are separated by a single \\r\\n, no blanks."""
    path = tmp_path / "newlines.csv"
    export_to_csv([Task(id=1, title="one"), Task(id=2, title="two")], path)

    raw = path.read_bytes().decode("utf-8")
    assert "\r\r\n" not in raw
    assert [line for line in raw.splitlines() if line == ""] == []
    assert len(raw.splitlines()) == 3


def test_titles_with_commas_and_quotes_are_quoted(tmp_path):
    path = tmp_path / "quoting.csv"
    export_to_csv([Task(id=1, title='a, b "c"')], path)

    rows = _read_rows(path)
    assert rows[1][1] == 'a, b "c"'


def test_cli_parser_accepts_export_path():
    args = build_parser().parse_args(["export", "out.csv"])
    assert args.command == "export"
    assert args.path == "out.csv"


def test_cli_export_writes_file(tmp_path):
    from taskvault.cli import main

    path = tmp_path / "cli.csv"
    assert main(["export", str(path)]) == 0

    # main() builds a fresh empty TaskVault, so only the header is written.
    assert _read_rows(path) == [list(CSV_COLUMNS)]
