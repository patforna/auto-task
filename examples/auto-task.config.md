# Auto-Task Project Bindings

Copy this file to `.claude/auto-task.config.md` in your repo, delete the sections where the default suits you, and edit the rest. Every section is optional — the plugin's skills fall back to the defaults noted below.

Bindings are plain markdown read by the agent, not machine-parsed config: write instructions the way you'd brief a colleague. For personal (non-committed) overrides, put the same sections in `.claude/auto-task.config.local.md` and gitignore it — it wins over this file on conflict.

## Task Store

Default: markdown task files in `tasks/` at the repo root, managed by the agent (`{NNN}-{slug}.md`, attachments in `tasks/attachments/{NNN}/`).

Override example: tasks live in a sibling repo at `../my-tasks/`; create them with `just create-task "<title>"`; bump statuses with `just task-status <file> <status>` (auto-commits there). Task-file commits then never land in the code repo.

## Verification

Default: auto-discover — a `just`/`make` check recipe, the CI workflow's steps, or at minimum the full test suite.

Override example: `npm run check` — mirrors CI; safe to run from parallel worktrees.

## Worktrees

Default: `git worktree add` at `../<repo>.worktrees/NNN-<slug>`, then install dependencies and copy gitignored files the app needs (e.g. `.env`).

Override example: create worktrees under `~/worktrees/<repo>/`; initialise with `./scripts/worktree-init.sh` (copies `.env`, seeds the local database).

## Review

Standing context appended verbatim to adversarial reviews, plus any repo-specific review rules on top of `/at:review-code`'s portable core (domain corruption traps, severity overrides, premises findings may be rejected on).

Default: none.

Override example:

> This service is internal-only behind SSO; do not raise public-exposure findings. Flag any unguarded division as Major — silent NaN corruption is our top defect class.

## Design Review

The command that serves the app on deterministic fixture data for `/at:review-design`.

Default: none — the skill fails loudly on UI changes if it can't find a fixture-backed server.

Override example: `npm run serve:fixtures` — prints the app URL; navigate to the printed port.

## Models

Which models fill each role.

Defaults: planning panel = strongest available Claude model + Codex (if the codex plugin is installed); implementer = strongest available model; adversarial reviewer = Codex if installed, else a second fresh-context Claude subagent.

Override example: panel = Claude + Gemini (via my `gemini` CLI); implementer = Sonnet; adversarial reviewer = a fresh Opus subagent.

## Conventions

Commit-message and branch conventions the workflow should follow beyond what the repo's own docs say.

Defaults: follow the repo's existing conventions; append the task-link suffix `(task/NNN)` to commit subjects; squash-merge task branches to the default branch.

Override example: use Conventional Commits (`feat: … [task/NNN]`); merge with merge commits instead of squashing.

## Transcript Capture

Optional command to capture the session transcript at auto-task wrap-up, and where to put it (keep it out of the repo).

Default: skipped.

## Feedback Snapshots

Optional out-of-repo directory where `/at:create-task` offers to snapshot post-clarify task files for later calibration.

Default: skipped.
