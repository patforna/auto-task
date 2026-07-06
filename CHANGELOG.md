# Changelog

## 0.3.2 — 2026-07-06

- README workflow diagram now shows ownership lanes (human → agents → human) instead of a skill bracket.
- Terminology: "bindings" → "config" throughout the docs and skills.

## 0.3.1 — 2026-07-03

- Renamed the bindings files to make their role obvious: `.claude/auto-task.config.md` (project) and `.claude/auto-task.config.local.md` (personal); template is now `examples/auto-task.config.md`.
- Demo GIF + full asciinema cast of a real run embedded in the README.

## 0.3.0 — 2026-07-02

- Bindings now layer: plugin defaults ← `.claude/auto-task.md` (project, committed) ← `.claude/auto-task.local.md` (personal, gitignored).
- New bindings: Models (panel / implementer / adversarial reviewer) and Conventions (commit style, task-link suffix).
- `examples/auto-task.md` copy-paste bindings template; `examples/sample-run.md` real-run report.
- Commit-message and default-branch assumptions now defer to the consuming repo.

## 0.2.0 — 2026-07-02

- Decoupled all skills from their origin project: portable defaults (in-repo `tasks/` store, sibling worktrees, auto-discovered verification, optional Codex) + project bindings.
- MIT licence; validated end-to-end on a fresh non-origin repo.

## 0.1.X — 2026-06

- Initial extraction of the task-lifecycle skills from the origin codebase into a standalone plugin; vendored `panel`/`synthesize`/`tdd` from core-skills.
