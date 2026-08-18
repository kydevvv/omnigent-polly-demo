# TaskVault

A tiny, dependency-free task tracker in Python — the demo codebase for a
multi-agent [Omnigent](https://github.com/omnigent-ai/omnigent) **Polly**
orchestration run.

Polly acts as tech lead: it reads [`ISSUES.md`](./ISSUES.md), splits the
work across independent coding sub-agents (Claude Code, Codex, Pi) each
in its own git worktree, has a **different-vendor** agent review every
diff, and opens one PR per task.

## Layout

```
src/taskvault/core.py   # Task model + core functions
src/taskvault/cli.py    # minimal CLI
tests/                  # pytest suite (green on main)
ISSUES.md               # the four work items for the demo
```

## Develop

```bash
python -m pytest        # run the test suite
```

The four work items in `ISSUES.md` are deliberately independent so they
can be implemented in parallel and reviewed cross-vendor.

# smoke test (delete me)
