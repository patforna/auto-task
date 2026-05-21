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

```text
create-task → clarify-task → plan-task → impl-task → code-review → review-task → ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (stored in `/tasks`) plus repo state carry everything the next agent needs.

## Guidance

- Preserve logical commits — do NOT squash.
- Never push without explicit approval in the current turn. Earlier approval does not carry over.
- Untracked files in the worktree are fine. Refuse only on uncommitted tracked changes.

## Protocol

## Step 1: Pre-Flight

Branch must be `task/NNN-...` with no uncommitted tracked changes.

## Step 2: Mark Done

`just task-status <task-file> done` and commit.

## Step 3: Merge into Main

From the task worktree:

```text
git pull --rebase origin main                          # rebase task branch onto origin/main
git -C "$primary" merge --ff-only task/NNN-<slug>      # fast-forward main
```

`$primary` resolves to the worktree where `main` is checked out — needed because `merge` only updates the branch checked out in the worktree it runs in. See § `$primary` below.

If rebase conflicts, stop and flag it to the user.

## Step 4: Push

- Push: `git push origin main` (any worktree — push is repo-wide).
- Cleanup (after push): `git -C "$primary" worktree remove --force <task_worktree>` and `git -C "$primary" branch -d task/NNN-<slug>`.

## Step 5: Output

One-sentence summary.

## `$primary`

A git repo can have multiple worktrees, each with a different branch checked out. The "primary" is the original one — `~/github/tad` in TAD's case, where `main` lives. Task worktrees under `~/github/.worktrees/tad/<slug>/` have the task branch checked out.

Resolve once:

```text
primary=$(git worktree list --porcelain | awk '/^worktree / {print $2; exit}')
```

Why it's needed:

- `git merge`, `git checkout`, `git rebase` mutate the branch checked out in the worktree they run in. To advance `main`, you must run from the primary worktree (or `-C "$primary"`).
- `git worktree remove <wt>` refuses if you're inside `<wt>`. Call it from the primary.
- `git branch -d <branch>` refuses if `<branch>` is checked out anywhere. Easier to delete from the primary after the task worktree is gone.
- `git push` and `git fetch` are repo-wide — no `$primary` needed.
