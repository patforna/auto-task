---
name: ship-task
description: Use to wrap up a finished task - set status to done, merge, clean up.
---

# Ship Task

## Usage

`/at:ship-task <task-path>`

## Goal

Use to wrap up a finished task - set status to done, merge, clean up.

## Context

This skill is typically run as part of a larger workflow:

```text
create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file plus repo state carry everything the next agent needs.

Task files live in the project's task store — `tasks/` in the repo by default. Project bindings can override this and other defaults: read `.claude/auto-task.config.md` (project, committed) and `.claude/auto-task.config.local.md` (personal overrides — win on conflict) if they exist. See `/at:create-task` § Task Store and Project Bindings.

## Guidance

- `main` throughout this skill means the repo's default branch — substitute yours (e.g. `master`) if it differs.
- Squash-merge by default — the task's commits collapse into a single commit on `main`.
- Push is automatic — invoking ship-task authorises the merge and push. No separate approval needed.
- Untracked files in the worktree are fine. Refuse only on uncommitted tracked changes.
- After the merge, re-install dependencies in the **primary** repo if the branch changed a dependency manifest — the primary's installed deps (`node_modules/`, a virtualenv, etc.) don't update on merge. Run the ecosystem's install for each changed manifest (e.g. lockfile → package-manager install; regenerate any gitignored generated artefacts that depend on changed sources). The project bindings may list the exact commands.

## Protocol

## Step 1: Pre-Flight

Branch must be `task/NNN-...` with no uncommitted tracked changes.

## Step 2: Mark Done

Set the task status to `done`. By default (in-repo task store), edit the frontmatter `status:` field and commit on the task branch with a `(task/NNN)` subject suffix — the squash in Step 3 carries it to `main`. If the bindings route tasks to a separate repo, use their task-status command; the bump then commits there and the squash carries code only.

## Step 3: Merge into Main

Squash the task branch into a single commit on `main`.

```text
git -C "$primary" pull --rebase origin main            # bring local main up to date with origin (keeps any unpushed local-main commits)
git -C "$primary" merge --squash task/NNN-<slug>       # stage the task's combined diff onto main — no commit yet
git -C "$primary" commit                               # write the squash commit (message below)
```

`$primary` resolves to the worktree where `main` is checked out — needed because `merge` only updates the branch checked out in the worktree it runs in. See § `$primary` below. The `pull --rebase` first reconciles local `main` with origin (requires the primary worktree to be clean); if origin/main is merely behind local main, it's a no-op. (No remote configured? Skip the pull and the Step 5 push.)

Squash-commit message — follow the repo's own commit conventions first (style, tense, prefixes). Defaults where the repo has none:

- Subject: a concise summary of what the task delivered, ending with the task-link suffix (default `(task/NNN)`; bindings can change or drop it — it's what ties the commit back to the task).
- Body: one bullet per logical change the task made (derive from the squashed commits' subjects), so the single commit still records what happened.

If `merge --squash` conflicts, stop and flag it to the user.

## Step 4: Verify the Integrated Tree

Run the project's verification command from `$primary` on the post-squash commit, **before** pushing. The command comes from the bindings; absent that, use the project's canonical check (a `just`/`make` check recipe, the CI workflow's steps, or at minimum the full test suite).

A green task branch is not enough: the `pull --rebase` in Step 3 folds in whatever landed on `main` since the branch forked, and a parallel change can break the task's code or tests with **zero textual conflict** (e.g. a renamed helper silently invalidates an assertion in an untouched test file). Git merges them cleanly; only re-running the verification on the combined tree catches it.

If verification fails, **stop and fix on `main`** before pushing — do not push a red tree. (CI is the backstop, not the gate.)

## Step 5: Push

- Push: `git push origin main` (any worktree — push is repo-wide).
- Cleanup (after push): `git -C "$primary" worktree remove --force <task_worktree>` and `git -C "$primary" branch -D task/NNN-<slug>` (`-D`, not `-d` — squash-merge leaves the branch tip a non-ancestor of `main`, so `-d` refuses it as "not merged").

## Step 6: Output

One-sentence summary.

## `$primary`

A git repo can have multiple worktrees, each with a different branch checked out. The "primary" is the original one — where `main` lives. Task worktrees have the task branch checked out.

Resolve once:

```text
primary=$(git worktree list --porcelain | awk '/^worktree / {print $2; exit}')
```

Why it's needed:

- `git merge`, `git checkout`, `git rebase` mutate the branch checked out in the worktree they run in. To advance `main`, you must run from the primary worktree (or `-C "$primary"`).
- `git worktree remove <wt>` refuses if you're inside `<wt>`. Call it from the primary.
- `git branch -d <branch>` refuses if `<branch>` is checked out anywhere. Easier to delete from the primary after the task worktree is gone.
- `git push` and `git fetch` are repo-wide — no `$primary` needed.
