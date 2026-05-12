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

## Guidance (DO NOT IGNORE!)

- Preserve logical commits — do NOT squash.
- Never push without explicit approval in the current turn. Earlier approval does not carry over.
- Never force-push, never reset --hard the working tree.
- Untracked files in the worktree are fine to ignore. Refuse only on modified-but-uncommitted tracked files.
- `/ship-task` is typically invoked from a task worktree. `main` is checked out in the primary worktree, not in the task worktree — so all merge/push/branch operations must run via `git -C "$primary"`. Resolve once at start: `primary=$(git worktree list --porcelain | awk '/^worktree / {print $2; exit}')`.

## Prerequisite

- Current repo is on a `task/NNN-<slug>` branch with status `ready-for-signoff` or `done`.

## Protocol

## Step 1: Pre-flight

Refuse and stop if any of:
- Working tree has modified-but-uncommitted tracked files (`git status --porcelain` excluding `??` lines).
- Branch is not `task/NNN-...`.
- Branch has zero commits ahead of `main`.

Untracked files are OK — leave them alone.

## Step 2: Mark task as done

Update the task status by running `just task-status <task-file> done` and commit.

## Step 3: Verify main hasn't diverged

```
git -C "$primary" fetch origin main
git -C "$primary" log --oneline main..origin/main
```

If `origin/main` is ahead of local `main`, stop and ask the user how to handle (likely: rebase the task branch onto the new main, then retry). Do not auto-rebase silently.

## Step 4: Fast-forward merge

```
git -C "$primary" checkout main  # usually a no-op — main is normally already checked out in the primary worktree
git -C "$primary" merge --ff-only task/NNN-<slug>
```

If `--ff-only` fails, stop and report — do not fall back to a merge commit.

## Step 5: Show diff summary and pause

Output:
- The list of commits now on `main` ahead of `origin/main` (`git log --oneline origin/main..HEAD`).
- The shortstat (`git diff --stat origin/main..HEAD`).

Then ask the user one question via `AskUserQuestion` with three options:
- "Push + cleanup (remove worktree + delete branch)" (recommended)
- "Push only"
- "Hold off"

## Step 6: Apply the user's choice

- Push: `git -C "$primary" push origin main`.
- Remove worktree (only after a successful push, or if the user chose cleanup without push): `git -C "$primary" worktree remove "$task_worktree"`. Refuse if the worktree is dirty.
- Delete branch: `git -C "$primary" branch -d task/NNN-<slug>` (use `-d`, not `-D` — refuse if the branch isn't fully merged into main).

## Step 7: Output

One short summary: what landed on main, push status, branch status. Done.
