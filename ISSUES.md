# TaskVault — work items

Four independent, well-scoped tasks. They touch different functions and
can be built in parallel. Every change must keep the existing test suite
green (`python -m pytest`) and add tests for the new behavior.

## Issue #1 — Feature: `search_tasks`
Add `search_tasks(tasks, query)` to `src/taskvault/core.py`.
- Case-insensitive substring match against each task's `title` **and**
  `description`.
- Returns a list of matching `Task` objects, preserving input order.
- Empty query returns all tasks.
- Add tests in `tests/test_search.py`.

## Issue #2 — Bug: `sort_by_due_date` orders tasks wrong
`sort_by_due_date` in `src/taskvault/core.py` currently returns tasks
**latest-first**, and tasks without a due date sort **first** instead of
last.
- Fix it to return **soonest-first**, with undated tasks **last**.
- Add a regression test in `tests/test_sorting.py`.

## Issue #3 — Feature: validate task priority
Add priority validation to `TaskVault.add_task` in
`src/taskvault/core.py`.
- Allowed values live in `VALID_PRIORITIES` (`low`, `medium`, `high`).
- An invalid priority must raise `ValueError` with a helpful message.
- Add tests in `tests/test_priority.py`.

## Issue #4 — Feature: CSV export
Add `export_to_csv(tasks, path)` to `src/taskvault/core.py` and wire up
an `export <path>` subcommand in `src/taskvault/cli.py`.
- CSV columns: `id,title,priority,due,done`.
- `due` is ISO format or empty when unset.
- Use only the standard library (`csv`).
- Add tests in `tests/test_export.py`.
