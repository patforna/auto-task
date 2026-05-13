---
name: ship-task
description: Use to wrap up a finished task - set status to done, merge, clean up.
---

# Ship Task

## Usage

`/ship-task <task-path>`

## Goal

Use to wrap up a finished task - set status to done, merge, clean up.

## Context

This skill is typically run as part of a larger workflow:

```
create-task → clarify-task → plan-task → impl-task → code-review → review-task → ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (stored in `/tasks`) plus repo state carry everything the next agent needs.

## Guidance

- Preserve logical commits — do NOT squash.
- Never push without explicit approval in the current turn. Earlier approval does not carry over.
- Untracked files in the worktree are fine. Refuse only on uncommitted tracked changes.

## Protocol

## Step 1: Pre-flight

Branch must be `task/NNN-...` with no uncommitted tracked changes.

## Step 2: Mark done

`just task-status <task-file> done` and commit.

## Step 3: Land on main

From the task worktree:

```
git fetch origin
git rebase origin/main                                        # rebase task branch
git -C "$primary" merge --ff-only task/NNN-<slug>             # ff main forward
```

where `$primary=$(git worktree list --porcelain | awk '/^worktree / {print $2; exit}')`.

If rebase conflicts, stop — don't auto-resolve.

## Step 4: Confirm

Show `git log --oneline origin/main..main` and `git diff --stat origin/main..main`, then ask via `AskUserQuestion`:

- Push + cleanup (recommended)
- Push only
- Hold off

## Step 5: Apply

- Push: `git -C "$primary" push origin main`
- Cleanup (after push): `git -C "$primary" worktree remove --force <task_worktree>` and `git -C "$primary" branch -d task/NNN-<slug>`

## Step 6: Output

One-sentence summary.
