---
name: ship-task
description: Use to wrap up a finished task - set status to done, merge, clean up.
---

# Ship Task

## Usage

`/auto-task:ship-task <task-path>`

## Goal

Use to wrap up a finished task - set status to done, merge, clean up.

## Context

This skill is typically run as part of a larger workflow:

```text
create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (in the sibling tad-tasks repo, `~/github/tad-tasks/`) plus repo state carry everything the next agent needs.

## Guidance

- Squash-merge by default — the task's commits collapse into a single commit on `main`.
- Push is automatic — invoking ship-task authorises the merge and push. No separate approval needed.
- Untracked files in the worktree are fine. Refuse only on uncommitted tracked changes.
- After the merge, re-install deps in the **primary** repo if the branch changed a dependency manifest — the primary's `node_modules`/`.venv` don't update on merge. Specifically: `bun install --frozen-lockfile` in `frontend/` when `package.json` or `bun.lock` changed; `uv sync` in `backend/` when backend deps changed; `just frontend-types` when `frontend/src/api/openapi.json` changed (`schema.d.ts` is gitignored and goes stale, breaking `just check-all`'s tsc).

## Protocol

## Step 1: Pre-Flight

Branch must be `task/NNN-...` with no uncommitted tracked changes.

## Step 2: Mark Done

`just task-status <task-file> done` — this commits the bump in the **tad-tasks** repo (the task file lives there, not in this repo). No commit in tad.

## Step 3: Merge into Main

Squash the task branch into a single commit on `main`. The squash carries code only — the task file lives in the tad-tasks repo and is committed there separately; the `(task/NNN)` subject suffix is the link between the two.

```text
git -C "$primary" pull --rebase origin main            # bring local main up to date with origin (keeps any unpushed local-main commits)
git -C "$primary" merge --squash task/NNN-<slug>       # stage the task's combined diff onto main — no commit yet
git -C "$primary" commit                               # write the squash commit (message below)
```

`$primary` resolves to the worktree where `main` is checked out — needed because `merge` only updates the branch checked out in the worktree it runs in. See § `$primary` below. The `pull --rebase` first reconciles local `main` with origin (requires the primary worktree to be clean); if origin/main is merely behind local main, it's a no-op.

Squash-commit message — **subject + bullet body**:

- Subject: `<imperative verb> <what the task delivered> (task/NNN)` — the `(task/NNN)` suffix is mandatory.
- Body: one bullet per logical change the task made (derive from the squashed commits' subjects), so the single commit still records what happened.

If `merge --squash` conflicts, stop and flag it to the user.

## Step 4: Verify the Integrated Tree

Run `just check-all` from `$primary` on the post-squash commit, **before** pushing.

A green task branch is not enough: the `pull --rebase` in Step 3 folds in whatever landed on `main` since the branch forked, and a parallel change can break the task's code or tests with **zero textual conflict** (e.g. a column added to a default preset silently invalidates an e2e assertion in an untouched test file). Git merges them cleanly; only re-running check-all on the combined tree catches it.

If check-all fails, **stop and fix on `main`** before pushing — do not push a red tree. (CI is the backstop, not the gate.)

## Step 5: Push

- Push: `git push origin main` (any worktree — push is repo-wide).
- Cleanup (after push): `git -C "$primary" worktree remove --force <task_worktree>` and `git -C "$primary" branch -D task/NNN-<slug>` (`-D`, not `-d` — squash-merge leaves the branch tip a non-ancestor of `main`, so `-d` refuses it as "not merged").

## Step 6: Output

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
