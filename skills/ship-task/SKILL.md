---
name: ship-task
description: Close out a finished task — flip status to done, fast-forward merge into local main, ask before push.
---

# Ship Task

## Usage

`/ship-task <task-path>`

## Goal

Take a task whose work is on a `task/NNN-...` branch and merge it cleanly into local `main`, leaving the task in `done`. Push and branch deletion are gated on explicit user approval.

Closes the loop opened by `/create-task → /clarify-task → /plan-task → /impl-task → /code-review → /review-task → /ship-task`.

## Guidance (DO NOT IGNORE!)

- Preserve logical commits — do NOT squash. The only commit allowed to be rewritten is the trailing status-flip from `/auto-task` Step 8 (the `ready-for-signoff` one), so that `main` records the final `done` state in a single metadata commit rather than the intermediate `ready-for-signoff` blip.
- Never push without explicit approval in the current turn. Earlier approval does not carry over.
- Never force-push, never reset --hard the working tree.
- `just commit` requires an upstream and will fail on local-only task branches — use plain `git add` + `git commit` for the done-flip.
- Untracked files in the worktree are fine to ignore. Refuse only on modified-but-uncommitted tracked files.

## Prerequisite

- Current repo is on a `task/NNN-<slug>` branch with status `ready-for-signoff` or `done`.
- `just check-all` was green at the end of `/review-task`. Do NOT re-run it here — trust the previous step.

## Protocol

## Step 1: Pre-flight

Refuse and stop if any of:
- Working tree has modified-but-uncommitted tracked files (`git status --porcelain` excluding `??` lines).
- Branch is not `task/NNN-...`.
- Branch has zero commits ahead of `main`.

Untracked files are OK — leave them alone.

## Step 2: Collapse the status flip

If the task status is `ready-for-signoff`:
1. `git reset HEAD~1` only if the last commit is the standalone status-flip (touches only the task file + parent epic file, frontmatter `status:` line). Otherwise leave commits alone.
2. `just task-status <task-file> done` (updates the task frontmatter + parent epic table).
3. `git add <task-file> <epic-file>` and commit with message: `Mark task NNN done (task/NNN)`.

If the task status is already `done`, skip this step.

## Step 3: Verify main hasn't diverged

```
git fetch origin main
git log --oneline main..origin/main
```

If `origin/main` is ahead of local `main`, stop and ask the user how to handle (likely: rebase the task branch onto the new main, then retry). Do not auto-rebase silently.

## Step 4: Fast-forward merge

```
git checkout main
git merge --ff-only task/NNN-<slug>
```

If `--ff-only` fails, stop and report — do not fall back to a merge commit.

## Step 5: Show diff summary and pause

Output:
- The list of commits now on `main` ahead of `origin/main` (`git log --oneline origin/main..HEAD`).
- The shortstat (`git diff --stat origin/main..HEAD`).

Then ask the user one question via `AskUserQuestion` with three options:
- "Push + delete branch" (recommended)
- "Push only"
- "Hold off"

## Step 6: Apply the user's choice

- Push: `git push origin main`.
- Delete branch (only after a successful push, or if the user explicitly chose delete without push): `git branch -d task/NNN-<slug>` (use `-d`, not `-D` — refuse if the branch isn't fully merged into main).

## Step 7: Output

One short summary: what landed on main, push status, branch status. Done.
