---
title: Introduce /at:config and migrate create-task (Slice 1)
date: 2026-07-10
status: done
type: tech
---

## Introduce /at:config and Migrate create-task (Slice 1)

Introduce a new `/at:config` skill that owns every auto-task setting's default and the procedure for resolving config, then migrate `create-task` to read its settings through it instead of restating defaults inline.

First slice of a staged refactor — full design and all four slices are in the attachment (`config-refactor-plan.md`). It builds the reusable machinery but wires up only create-task's settings.

### Acceptance Criteria

- A new `/at:config` skill documents each setting with its default and defines how config resolves (project and local overrides beat the default), the resolved-settings format a consumer reads, and the mandatory step a skill runs to resolve. Only the task-store and feedback-snapshot settings are populated this slice.
- The default task-file behaviour currently spelled out inside create-task — file location, name and numbering, and the attachments path — is defined in /at:config and no longer restated in create-task.
- create-task resolves config through /at:config before doing its work and reads settings from the resolved values.
- With no project config, create-task behaves exactly as today.
- A project config that overrides the task store is honoured: create-task creates tasks at an overridden `location:` and via an overridden `create:` command. An overridden `status:` command is resolved correctly by /at:config (per-leaf) for the later-slice skills that transition status — create-task itself only writes the initial `status: new` this slice, so it doesn't consume it. Leaves not mentioned fall back to the default.
- Run on its own, /at:config prints the resolved settings with each value's origin (default, project, or local). It recognises all nine canonical section headings — only task store and feedback snapshots resolve this slice — and warns only on headings outside that set, so an existing full config raises no false warnings during migration.
- The example config's Task Store and Feedback Snapshots sections are in the new overrides-only form; its other sections are untouched.
- The orchestrator and all other skills are unchanged.

### Notes

- Keep create-task's "Task Store and Project Config" heading — six other skills link to it by name this slice; replace only its body with a pointer to /at:config.
- Out of scope: the --init scaffolder and lazy capture (Slice 3).

## Implementation Plan

### TLDR

Add `/at:config` as the single source of truth for create-task's task-store and feedback-snapshot settings — defaults + standalone resolve procedure + the locked `v1` resolved-block contract + inspect — then migrate `create-task` to resolve through it and stop restating those defaults. Standalone path only; orchestrator, the other six skills, README and CLAUDE.md untouched.

### Steps

1. **Create `skills/config/SKILL.md`** (invoked `/at:config`; auto-discovered — no manifest edit; `description:` starts with "Use…"). Sections: § Settings & Defaults, § Detection (explicit no-op stub), § Resolve, § Resolved-block grammar, § Inspect, the mandatory Step-0 consumer template, and the heading→setting map. Defer § Init to Slice 3 (don't stub it).

2. **§ Settings & Defaults — populate only `settings.task_store.*` and `settings.feedback_snapshots`,** copying today's create-task semantics verbatim so migrated == legacy:
   - `settings.task_store.location` — `tasks/` at repo root.
   - `settings.task_store.create` — `{location}/{NNN}-{slug}.md`; `{NNN}` = max existing + 1, zero-padded to 3 digits; `{slug}` = kebab-case title; frontmatter + body; attachments in `{location}/attachments/{NNN}/`.
   - `settings.task_store.status` — edit the task file's `status:` frontmatter field in place.
   - `settings.feedback_snapshots` — default skipped; when set, an out-of-repo snapshot directory + optional calibration-exemplar path.
   Include the human at-a-glance doc and the heading→setting map listing all nine canonical headings (Task Store, Verification, Worktrees, Review, Design Review, Models, Conventions, Transcript Capture, Feedback Snapshots); only `## Task Store` (→ location/create/status) and `## Feedback Snapshots` (→ dir + exemplar) resolve to live settings this slice, the other seven are recognised-but-inert. Check: a full nine-section config produces zero warnings; a heading outside the nine warns.

3. **§ Detection — explicit no-op stub.** State nothing is detected this slice (both live settings static); detection populated in Slice 2. No probes (a premature probe would pre-empt "detection never clobbers an override" before that logic exists).

4. **§ Resolve — standalone path only.** Read `.claude/auto-task.config.md` then `.claude/auto-task.config.local.md` from the current repo root (skip missing); layer defaults → project → local, **per-leaf** (local beats project beats default; an override section supplies only the leaves it names; unnamed leaves fall through — no wholesale section replacement). Emit the resolved block; report the repo-root path resolved from. (Orchestrator injection / resolve-from-primary is Slice 2 — the Step-0 template tolerates a passed-in block, but nothing produces one yet.)

5. **§ Resolved-block grammar — pin the `v1` contract (LOCKED; later slices reproduce exactly).** Header `Resolved auto-task settings v1 (run: <task-id or standalone>; source: <abs repo-root path>)`; one leaf per line for scalars; commands backticked; every leaf carries a `[provenance]` tag from the closed vocabulary `default | detected | project | local` (`detected` may append the fact, e.g. `[detected: codex on PATH]` — unused this slice); prose/compound leaves render as a fenced `text` sub-block indented under the leaf; empty prose renders inline as `settings.x: "" [default]`; skipped feedback snapshots render as `settings.feedback_snapshots: skipped [default]`. Only the four Slice-1 leaves ever appear this slice. The `v1` tag gates any future format change.

6. **§ Inspect (no args).** Resolve, print the resolved block (provenance = origin) with the source path, then lint headings — warn only on headings outside the canonical nine. Unknown-heading detection only this slice; copied-default detection needs fixtures → Slice 4.

7. **Define the mandatory Step-0 template** in `/at:config` for consumers to embed (wording per design §2.5): if a `Resolved auto-task settings v1` block was passed in, use it verbatim and don't re-run detection; else resolve now via `/at:config` § Resolve; don't proceed without a resolved block.

8. **Migrate `create-task`:**
   - Insert the Step-0 block above Step 1.
   - Step 2: delete the inline default prose (file location, `{NNN}-{slug}.md`, "max existing + 1, zero-padded to 3 digits", attachments path, and the "if the project config defines a create-task command" clause); read `settings.task_store.location`/`.create`. Keep the `status: new` initial frontmatter, the Task-states note, and the Committing/`(task/NNN)` note inline (status-edit mechanism and Conventions are later-slice consumers).
   - Steps 3 & 8: replace the "project config (§ Feedback Snapshots)" references with `settings.feedback_snapshots`.
   - Replace the **body** of `## Task Store and Project Config` with a one-line pointer to `/at:config`; **keep the heading verbatim** (six skills link to it by name, unchanged this slice).

9. **Convert `examples/auto-task.config.md` — Task Store and Feedback Snapshots sections only — to overrides-only.** Drop each section's `Default:` line; present overrides as labelled sub-lines matching the heading→setting map (`location:`/`create:`/`status:`; dir + `exemplar:`). Leave the preamble and the seven other sections byte-for-byte untouched (full rewrite is Slice 4).

10. **Verify (behaviour-specific):**
    - No config: `/at:create-task` creates `tasks/{NNN}-{slug}.md` + `tasks/attachments/{NNN}/` exactly as before.
    - Per-leaf override: a `## Task Store` naming only `location:` routes new tasks + attachments there while numbering/attachments-naming still follow the default `create` leaf; a `create:`/`status:` override is honoured; local beats project leaf-by-leaf.
    - `/at:config` inspect: prints the block with correct provenance + source; nine-section config → no warnings; out-of-set heading → warns.
    - Greps: `skills/create-task/SKILL.md` no longer restates task-store defaults (`tasks/{NNN}`, "zero-padded", `attachments/{NNN}`); the `## Task Store and Project Config` heading still present; only `/at:config`, create-task, and the two example-config sections changed.

### Notes

- The `v1` resolved-block grammar (Step 5) is the locked cross-boundary contract; Slices 2–4 depend on byte-level stability — don't "improve" it later without bumping past `v1`.
- Coexistence safety hinges on migrated defaults equalling legacy defaults verbatim (Step 2) — the un-migrated seven skills still read their inline defaults, so drift here silently changes behaviour.
- `create-task` consumes `location`, `create`, `feedback_snapshots`; `status` is defined now for later-slice consumers (create-task only writes initial `status: new`). Intentional, not scope creep.
- No `plugin.json`/`marketplace.json` version bump or re-vendor in scope (release mechanics, outside the ACs; skills auto-discover).
- Repo has no machine parser or test harness — keep `/at:config` markdown-readable; "verification" is the Step 10 behavioural checks.

## Implementation Notes

- Built `skills/config/SKILL.md` with sections: Usage, Scope This Slice, Settings & Defaults, Heading → Setting Map, Detection (no-op stub), Resolve, Resolved-block Grammar, Inspect, Step 0 (for Consumers). § Init deliberately absent (deferred to Slice 3, not stubbed).
- Migrated `create-task`: added a `## Step 0: Resolve Config (Mandatory)` section above Step 1; Step 2 now reads `settings.task_store.create`/`.location`; the Attachments note points at `settings.task_store.create` instead of the literal path; Steps 3 and 8 read `settings.feedback_snapshots`. The `## Task Store and Project Config` heading is kept verbatim (six skills link to it) with its body replaced by a pointer to `/at:config`. Kept inline per plan: initial `status: new` frontmatter, the Task-states note, the Committing/`(task/NNN)` note.
- Converted only the Task Store and Feedback Snapshots sections of `examples/auto-task.config.md` to overrides-only labelled sub-lines (`location:`/`create:`/`status:`; `dir:`/`exemplar:`); dropped their `Default:` lines. The file is now mixed-form (seven sections still use the old Default/Override-example prose) — expected; full rewrite is Slice 4.
- Behavioural simulation (Step 10, applying the skill's § Resolve + grammar + § Inspect):
  1. No config → all four leaves `[default]`; create-task creates `tasks/{NNN}-{slug}.md` + `tasks/attachments/{NNN}/` as today. Pass.
  2. `## Task Store` with only `location:` → location `[project]`, create/status stay `[default]` (per-leaf, no wholesale replacement); new tasks route to the new location but keep default numbering/attachments naming. Pass.
  3. `create:`/`status:` command overrides honoured; local beats project leaf-by-leaf. Pass.
  4. Full nine-section config → zero warnings; a heading outside the nine → warns. Pass.
- Grep gate: `create-task` no longer contains `tasks/{NNN}`, `attachments/{NNN}`, or `max existing` (0 matches each). The lone `zero-padded` hit is in the Epic Sub-Tasks appendix (epic child indices `01`/`02`) — a distinct convention from the task-store `{NNN}` default, out of scope for this slice, left untouched. `## Task Store and Project Config` heading still present.
- Diff scope: the branch touches only the four in-scope files (`skills/config/SKILL.md`, `skills/create-task/SKILL.md`, `examples/auto-task.config.md`, and this task file).
- The resolved-block grammar example nests a ```` ```text ```` fence (part of the locked contract) inside a documentation wrapper. The wrapper is a four-backtick ```` ````markdown ```` fence so the inner three-backtick fence can't prematurely close it (see post-review fix below).

### Post-Review Fixes

Two accepted `/at:review-code` findings addressed after the initial implementation:

- **Split `settings.feedback_snapshots` into two independent leaves** — `settings.feedback_snapshots.dir` and `settings.feedback_snapshots.exemplar`, each with its own default (unset → skipped) and its own `[provenance]` tag, mirroring the `settings.task_store.*` split. The old single compound leaf carried two labels (`dir:` + `exemplar:`) under one provenance tag, which the per-leaf precedence rule couldn't represent: a project setting only `dir:` and a local setting only `exemplar:` would collide (wholesale replacement could drop the dir, misrouting create-task's snapshot step). Updated § Scope, § Settings & Defaults (table + at-a-glance), § Detection, and the `v1` grammar (rules + example) in config; added a mixed-provenance worked example (project `dir:` + local `exemplar:`) to the grammar; retargeted create-task's two references (Step 3 reads `.exemplar`, Step 8 gated on `.dir`). Stays `v1` — this is defining the locked contract correctly the first time, not a format break. `examples/auto-task.config.md` needed no change (its `dir:`/`exemplar:` lines already map cleanly).
- **Fixed the broken doc-wrapper fence** — the grammar example's outer ```` ```markdown ```` wrapper (three backticks) was prematurely closed by its inner ```` ```text ```` fence, breaking human markdown rendering. Changed the outer wrapper to four backticks (```` ````markdown ```` / ```` ```` ````); the inner ```` ```text ```` fence (part of the contract) is untouched.
- **Reworded AC5 for precision (no implementation change)** — task-review flagged that "a status command … honoured by create-task" overreached for Slice 1: create-task writes only the initial `status: new` and does no status transitions, so it never consumes `settings.task_store.status`. `/at:config` resolves the status leaf correctly (per-leaf provenance) for later-slice consumers (impl/ship do the bumps). AC5 reworded to separate "honoured by create-task" (location + create) from "resolved by /at:config" (status); the resolver behaviour was already correct.
- **Adversarial gap-check fixes (Step 7.3)** — four minor accuracy/contract refinements, still `v1`: (1) create-task's config pointer now points at § Heading → Setting Map for the recognised-section list and scopes the § Settings & Defaults claim to the settings it owns (it previously overclaimed "every recognised section", untrue while 7 of 9 defaults remain inline in their own skills); (2) the `v1` grammar rule now discriminates single-line (inline) from multi-line/compound (fenced) values, resolving the `status`-leaf tension (a single-line phrase rendered inline); (3) attachments now derive from `settings.task_store.location`, not `.create`, so the path stays defined under a bare `create:` command override; (4) removed an inaccurate diff-scope note.
- **Defaults moved into a config file (post-review correction)** — the defaults had been living as a prose table inside `/at:config`, so they loaded differently from the project/local overrides. Extracted them into a shipped `auto-task.config.defaults.md` (same `## Heading` + labelled-line format as the override files). `§ Resolve` now reads all three layers identically — **defaults ← project ← local**, per-leaf, one mechanism. The skill's `§ Settings & Defaults` became a value-free `§ Settings` (meaning + override map); `[default]` provenance now means "resolved from the defaults file". This is the change that makes "defaults completely factored out and loaded like overrides" actually true.
