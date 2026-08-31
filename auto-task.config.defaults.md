# Auto-Task Config — Defaults

The base layer of the config resolve chain. `/at:config` reads three files of this
**identical format** — `## Heading` sections with labelled sub-lines — and merges
them per-leaf:

> **defaults (this file) ← project (`.claude/auto-task.config.md`) ← local (`.claude/auto-task.config.local.md`)**

To change a default, edit it here — nowhere else. A consuming skill never restates a
default; it reads the resolved value.

Only the sections `/at:config` owns this slice appear below. Later slices add the
remaining sections (Verification, Worktrees, Review, Design Review, Models,
Conventions, Transcript Capture) here as their owning skills migrate.

## Task Store

location: tasks/
create: Write the task file (frontmatter plus body) to a temp file, then place it by running `${CLAUDE_PLUGIN_ROOT}/skills/create-task/scripts/alloc-task.sh --dir {location} --slug {slug} --from {tempfile}` — `${CLAUDE_PLUGIN_ROOT}` is a template placeholder, not a shell var: substitute the resolved plugin root before running. {slug} is a short kebab-case form of the title. The script prints the allocated basename, e.g. `104-add-widget.md`, on stdout — its leading number is {NNN}.
status: Edit the task file's `status:` frontmatter field in place.

## Feedback Snapshots

dir: skipped
exemplar: skipped
