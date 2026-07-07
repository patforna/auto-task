# Changelog

## 0.4.1 — 2026-07-07

- review-code: new removal-hygiene check — when the diff removes, renames, or supersedes something, trace that no orphaned helpers, dangling references, or stale comments/docs/config survive (lint-caught cases stay tool-owned).

## 0.4.0 — 2026-07-06

Integrates systemic learnings mined from 55 real auto-task run transcripts and a before/after task-file feedback corpus.

- auto-task: lite mode can now auto-downshift on strictly-trivial tasks (announced, reported); parallel-session hygiene (no bare-name `pkill`, scope kills to worktree/port, expect e2e CPU contention); provably-empty stale worktrees are auto-cleaned instead of hard-stopping; rebase at the next green checkpoint when main moves mid-run; the second task review is an independent adversarial gap-check, not a re-run; subagent monitoring relies on completion notifications, not sleep-timer polling; non-Claude panelists get a one-line repo orientation; transcripts re-captured when commits land after capture; long subagent artifacts re-output by reference.
- create-task: audience named explicitly (implementing agent with repo access); example-anchoring qualified (only when intent is non-obvious); epics gain a `Locked Decisions` section so sub-tasks stop re-deriving shared calls; optional calibration exemplar via config § Feedback Snapshots.
- plan-task: epic sub-task planning reads the epic's locked decisions + done siblings' implementation notes.
- impl-task: stage explicitly by path (never `-A`); run the formatter before final verification; `Implementation Notes` heading title-cased.
- ship-task: refreshes the captured transcript after the merge (the wrap-up capture goes stale once ship commits land).
- Step 5 reviews the merge-base range when main has advanced since branching, so review diffs contain only the task's commits.

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
