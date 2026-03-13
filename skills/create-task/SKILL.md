---
name: create-task
description: Create a task file (standalone, epic, or epic sub-task). Utility — called by /define-task or directly by the user. Related: /define-task.
---

# Create Task

## Usage

`/create-task [optional further user instructions]`

The session context or the optional user instructions should make it clear whether we're creating:
- a standalone task
- an epic task
- a task belonging to an epic

If it's not clear, please stop and ask the user to clarify.

## Standalone task

Create a `tasks/<NNN>-<slug>.md` file where `<NNN>` is the next available zero-padded sequential number and `<slug>` is a short title slug derived from the session context or additional user instructions.

Check `ls tasks/` to find the current highest number.

### Task template

Follow this structure:

```markdown
---
title: <task title>
date: <YYYY-MM-DD>
status: new
---

# [Task title]

TODO: Add Task description

## Acceptance criteria

TODO: Add ACs

## Notes

TODO: Add Notes
```

## Epic

An epic is simply a high-level task that aggregates a number of sub-tasks.

To create an epic, follow the instructions for creating a standalone task. Drop the `Acceptance Criteria` section and instead add a `Tasks` section to the end. Example:

```markdown
## Tasks

| #  | Task                      | File                    | Status |
|----|---------------------------|-------------------------|--------|
| 01 | Implement Reversal Signal | 012.01-signal.md        | new    |
| 02 | Filters and Gates         | 012.02-filters-gates.md | new    |
| 03 | Remove SL/TP              | 012.03-remove-sltp.md   | new    |
| 04 | Multi-Day Holding         | 012.04-multi-day-hold.md| new    |
```

## Epic sub-tasks

Epic sub-tasks are like standalone tasks, except their file name is slightly different to keep them lexicographically close to the epic task.

To create an epic sub-task file, follow the instructions for creating a standalone task, but use the following file format: `<EpicNbr><NN><task slug>.md` (e.g. `012.03-remove-sltp.md`). The numbers of the tasks belonging to the epic are zero-padded (`01`, `02`, ... `10`, `11`). Example:

```
tasks/015-reversal-eval.md        ← epic
tasks/015.01-cli-knobs.md         ← task 1
tasks/015.02-pnl-concentration.md ← task 2
```

**Important**: When creating an epic sub-task, **update the epic's tasks table** so that it includes the new sub-task and status.