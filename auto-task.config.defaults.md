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
create: Create {location}/{NNN}-{slug}.md — {NNN} is the next task number (max existing + 1, zero-padded to three digits); {slug} is a short kebab-case form of the title; the file has frontmatter plus body.
status: Edit the task file's `status:` frontmatter field in place.

## Feedback Snapshots

dir: skipped
exemplar: skipped
