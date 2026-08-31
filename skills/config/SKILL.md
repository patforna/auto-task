---
name: config
description: "Use this skill to resolve auto-task settings. It owns the procedure that merges the shipped defaults file with project and local config, per-leaf, plus the resolved-block contract consumers read. Run it standalone to inspect the resolved settings and where each value came from."
---

# Config

## Usage

`/at:config` — inspect the resolved settings for the current repo, with each value's origin (see § Inspect).

Setting-consuming skills don't call this as a command. They follow § Resolve — via their mandatory Step 0 — to obtain a **resolved block**, then read `settings.*` from it. Every setting's canonical default lives in the shipped defaults file (§ Resolve layer 1) and nowhere else, so a skill never restates a default: change it there and every consumer follows.

## Scope This Slice

This slice populates only the settings `/at:create-task` consumes: `settings.task_store.*` and `settings.feedback_snapshots.*` — their defaults live in the shipped `auto-task.config.defaults.md` (§ Resolve layer 1). Both are static (no environment detection), so § Detection is an empty stub for now.

The other settings still live inline in their own skills and migrate in later slices. Their config-file headings are already **recognised** here (see § Heading → Setting Map) so an existing full config raises no false warnings during migration — they just don't resolve to live settings yet.

## Settings

The settings `/at:config` owns this slice. Their **default values live in the shipped `auto-task.config.defaults.md`** (§ Resolve layer 1), not here — this section maps each setting to its meaning and its override label.

| Setting                                | Meaning                                          | Resolved by | Override (heading → label)             |
| :------------------------------------- | :----------------------------------------------- | :---------- | :------------------------------------- |
| `settings.task_store.location`         | where task files live                            | static      | `## Task Store` → `location:`          |
| `settings.task_store.create`           | how a new task file is created                   | static      | `## Task Store` → `create:`            |
| `settings.task_store.status`           | how a task's status changes                      | static      | `## Task Store` → `status:`            |
| `settings.feedback_snapshots.dir`      | out-of-repo dir for post-clarify snapshots       | static      | `## Feedback Snapshots` → `dir:`       |
| `settings.feedback_snapshots.exemplar` | calibration exemplar read before writing a task  | static      | `## Feedback Snapshots` → `exemplar:`  |

A task's attachments live in `{settings.task_store.location}/attachments/{NNN}/` (derived from `location`, not a separate setting).

An override supplies only the leaves it names (e.g. a `## Task Store` giving just `location:` leaves `create` and `status` at their defaults). See § Resolve for the per-leaf merge.

## Heading → Setting Map

The nine canonical config-file headings and the settings they map to. All nine are **recognised** (never warn); only Task Store and Feedback Snapshots **resolve** to live settings this slice — the rest are recognised-but-inert until their owning skill migrates.

| Config heading         | Setting(s)                                   | Live this slice? |
| :--------------------- | :------------------------------------------- | :--------------- |
| `## Task Store`        | `location:` / `create:` / `status:`          | yes              |
| `## Verification`      | `settings.verify`                            | no               |
| `## Worktrees`         | `path:` / `init:`                            | no               |
| `## Review`            | `settings.review_context`                    | no               |
| `## Design Review`     | `settings.design_review_server`              | no               |
| `## Models`            | `implementer:` / `adversarial:` / `panel:`   | no               |
| `## Conventions`       | `suffix:` / `merge:`                         | no               |
| `## Transcript Capture`| `settings.transcript_capture`                | no               |
| `## Feedback Snapshots`| `dir:` / `exemplar:`                         | yes              |

A heading outside this set is **unrecognised** → warn (see § Inspect). Never guess a near-miss to a canonical heading.

## Detection

**No-op this slice.** Nothing is detected: both live settings (`settings.task_store.*`, `settings.feedback_snapshots.*`) are static, so the resolver runs no environment probes. Real detection (codex presence, a check recipe/script, Chrome DevTools MCP) arrives in Slice 2, when it will resolve only leaves left at `auto` and never clobber an explicit override.

## Resolve

Produce a resolved block for the current repo. Standalone path only this slice (orchestrator injection and resolve-from-primary-before-worktree arrive in Slice 2).

The config chain is **three files of identical format** — `## Heading` sections with labelled sub-lines — read and merged the same way at every layer:

1. Determine the repo root (the current working repo's top level).
2. **Layer 1 — defaults.** Read the shipped `auto-task.config.defaults.md` at the plugin root (`${CLAUDE_PLUGIN_ROOT}` — two levels up from this skill's `skills/config/` directory). Every setting's default value lives here.
3. **Layer 2 — project.** If `.claude/auto-task.config.md` exists at the repo root, read it. Skip silently if absent.
4. **Layer 3 — local.** If `.claude/auto-task.config.local.md` exists at the repo root, read it. Skip silently if absent.
5. **Merge per-leaf — local beats project beats defaults, each leaf independently.** Parse all three files the same way: map each `##` heading to its setting group via § Heading → Setting Map, and each labelled sub-line to a leaf. A layer supplies **only** the leaves it names; unnamed leaves keep the lower layer's value. Never replace a whole section wholesale — that would erase sub-defaults in compound settings. A leaf's provenance is the layer its final value came from: `default` (defaults file), `project`, or `local`.
6. Detection: none this slice (see § Detection).
7. Emit the resolved block per § Resolved-block Grammar. The `run:` field is the passed-in task id if one was given, else `standalone`; the `source:` field is the absolute repo-root path.
8. Report the repo-root path and which of the three config files were found vs absent.

## Resolved-block Grammar

The `v1` contract. **LOCKED** — later slices reproduce it exactly; the `v1` tag gates any future format change. Do not "improve" it without bumping past `v1`.

Header line, then one entry per leaf:

````markdown
Resolved auto-task settings v1 (run: standalone; source: /abs/path/to/repo)
- settings.task_store.location: tasks/ [default]
- settings.task_store.create: [default]
  ```text
  <the create recipe from the defaults file, verbatim — elided here>
  ```
- settings.task_store.status: edit the task file's `status:` frontmatter field in place [default]
- settings.feedback_snapshots.dir: skipped [default]
- settings.feedback_snapshots.exemplar: skipped [default]
````

**Worked example — mixed provenance.** Project config sets only `dir:`, local config sets only `exemplar:`; each leaf resolves independently and carries its own tag (no wholesale replacement drops the other):

````markdown
Resolved auto-task settings v1 (run: standalone; source: /abs/path/to/repo)
- settings.task_store.location: tasks/ [default]
- settings.task_store.create: [default]
  ```text
  <the create recipe from the defaults file, verbatim — elided here>
  ```
- settings.task_store.status: edit the task file's `status:` frontmatter field in place [default]
- settings.feedback_snapshots.dir: ~/snaps/ [project]
- settings.feedback_snapshots.exemplar: ~/snaps/x-after.md [local]
````

Rules:

- **Header:** `Resolved auto-task settings v1 (run: <task-id or standalone>; source: <abs repo-root path>)`.
- **One leaf per line** for scalars: `- settings.x: <value> [provenance]`.
- **Commands** are backticked (e.g. `` `just create-task "<title>"` ``).
- **Provenance** — every leaf carries a `[provenance]` tag from the closed vocabulary `default | detected | project | local`, naming the layer its value came from (`default` = the shipped defaults file). `detected` may append the fact (e.g. `[detected: codex on PATH]`) — unused this slice.
- **Single-line values** (a path, command, or short phrase) render inline: `- settings.x: <value> [provenance]`. **Multi-line / compound values** render as a fenced ` ```text ` sub-block indented under the leaf line (which ends with just its `[provenance]` tag). This slice: `settings.task_store.create` fences (multi-line); `settings.task_store.status` and the two feedback-snapshot paths render inline.
- **The examples above show shape, not content.** A value written as `<…>` stands in for whatever the defaults file (or an override) actually says. Never paste a default's real text into this skill — that restates a default, and the copy drifts.
- **Empty prose** renders inline as `settings.x: "" [default]` (no fenced block). No Slice-1 leaf is empty-prose, but the rule is part of `v1`.
- **Skipped feedback snapshots** render inline per leaf as `settings.feedback_snapshots.dir: skipped [default]` and `settings.feedback_snapshots.exemplar: skipped [default]`.
- Only the five Slice-1 leaves (`settings.task_store.location`, `settings.task_store.create`, `settings.task_store.status`, `settings.feedback_snapshots.dir`, `settings.feedback_snapshots.exemplar`) ever appear this slice.

## Inspect

Run on `/at:config` with no arguments:

1. Follow § Resolve for the current repo (`run: standalone`).
2. Print the resolved block, including the `source:` path, so each leaf shows its origin (`[default]` / `[project]` / `[local]`).
3. **Lint headings.** For each `##` heading in the project and local config files, if it is not one of the nine canonical headings (§ Heading → Setting Map), warn: `unrecognised heading "<heading>" — ignored`. A full nine-section config raises zero warnings; a heading outside the nine warns. Never guess a near-miss to a canonical heading.

Copied-default detection (warning when an override just restates today's default) needs fixtures and arrives in Slice 4.

## Step 0 (for Consumers)

Every setting-consuming skill embeds this block at the top of its steps:

> **Step 0 — Resolve config (mandatory).** If a `Resolved auto-task settings v1` block was passed in, use it verbatim and do NOT re-run detection. Otherwise resolve now by following `/at:config` § Resolve. Do not proceed without a resolved block. At each reference site read `settings.*` from the block; never restate a default.
