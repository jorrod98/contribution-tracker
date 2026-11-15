# AGENTS.md

Shared instructions for AI coding agents (GitHub Copilot, Claude Code, Codex)
working in this repository. This is the single source of truth: edit this file,
not the tool-specific ones that point to it.

## Project

A small command-line app for tracking open-source issues and pull requests to
contribute to. It is also a place to practice Git and GitHub workflow, so small
branches and focused pull requests matter as much as the code.

## Layout

- `contribution_tracker/cli.py`: argument parsing and the `add`, `list`,
  `update`, and `view` commands
- `contribution_tracker/storage.py`: loading and saving the JSON data file
- `contribution_tracker/viewer.py`: HTML rendering for the `view` command
- `tests/test_cli.py`: unittest suite
- `.github/`: CI workflow, issue templates, pull request template

## Commands

```bash
python3 -m contribution_tracker list              # run the app
python3 -m unittest discover -s tests -v          # run the tests
```

## Rules

- Standard library only. Do not add dependencies without an issue discussing it.
- Keep the code compatible with Python 3.9: use `Optional[X]` and `List[X]` from
  `typing` in signatures that are evaluated at runtime, not `X | None`.
- Add or update tests for every behavior change, and run the tests before
  finishing.
- Tests must pass `--data-file` pointing at a temporary directory. Never read or
  write the real `.contribution-tracker.json` or `.contribution-tracker.html`;
  both are local, git-ignored user data.
- Escape all user-supplied values rendered into HTML (see `viewer.py`).
- Update `README.md` when commands, flags, or statuses change.

## Git workflow

- Never commit directly to `main`. Create a branch per issue or change.
- Keep each pull request focused on one issue or improvement.
- Use conventional commit prefixes (`feat:`, `fix:`, `docs:`, `test:`).
- Fill in `.github/pull_request_template.md` when opening a pull request.
- Commit, push, or open a pull request only when asked.

## Handoff between agents

Agents do not share memory, so the repository is the handoff. Before stopping,
leave the work in a state another agent can pick up: changes committed on a
branch (when asked to commit), or a short note in the issue or pull request
saying what is done and what is left. When starting, check `git status`,
`git log`, and the current branch before changing anything.
