"""A minimal CLI for TaskVault.

Intentionally small. Issue #4 asks for a new `export` subcommand.
"""

from __future__ import annotations

import argparse

from taskvault.core import TaskVault


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskvault")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    add.add_argument("--priority", default="medium")

    sub.add_parser("list", help="list open tasks")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    vault = TaskVault()
    if args.command == "add":
        task = vault.add_task(args.title, priority=args.priority)
        print(f"added task {task.id}: {task.title}")
    elif args.command == "list":
        for t in vault.open_tasks():
            print(f"[{t.id}] {t.title} ({t.priority})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
