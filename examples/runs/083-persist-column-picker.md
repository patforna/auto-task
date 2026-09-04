# Example run: task 083

A real _auto-task_ run on a private codebase, exported from the Claude Code session transcript with `claude-replay --recurse-subagents` and paths scrubbed. 17 Jun 2026, 29 minutes wall-clock, no gap over a minute — it ran unattended.

The task: add localStorage persistence for column-picker overrides per preset. Every step is on show, including a disagreement between the two reviewers.

| Section                          | What happens                                                                                                                                    |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Plan (Subagents 1–2)              | Two models (Opus, Codex) independently plan; a synthesis merges them.                                                                          |
| Implement (Subagent 3)            | A fresh-context subagent implements test-first, committing as it goes.                                                                          |
| Review, triage, fix (Subagents 4–5) | Opus reviews clean; the Codex adversarial pass raises one high finding; synthesis and triage accept it; a fix subagent resolves it, re-reviewed. |
| Verify (Subagents 6–7)            | Two independent task reviews, both PASS.                                                                                                        |

---

# Claude Code Session Db10f97d-2486-440C-Bfd3-Ae18acef7527

Project: ~/github/tad Started: 2026-06-17T12:10:35.850Z

---

## Main-Thread Message

Time: 2026-06-17T12:10:39.484Z

I'll start by finding task 083 and confirming its details.

---

## Bash Call

Time: 2026-06-17T12:10:40.311Z Description: Find and read task 083

### Command

```text
ls tasks/ | grep -i 083 && echo "---" && cat tasks/083*.md 2>/dev/null | head -100
```

### Output

```text
083-persist-column-picker.md
---
---
title: "Persist Column Picker Overrides Per Preset"
date: 2026-06-17
status: ready-for-dev
type: feat
---

## Persist Column Picker Overrides per Preset

The ticker-table column picker lets you toggle columns on top of the active preset, but those overrides are session-only React state — a page refresh throws them away and falls back to the preset's columns.

This task makes the overrides stick across reloads (and browser restarts) by persisting them in localStorage, keyed per preset, so each view remembers its own column set.

### Acceptance Criteria

- After toggling columns and reloading the page, the picker and table show the toggled set, not the preset's base set.
- Overrides are remembered per preset: customise view A, switch to view B, switch back — A still shows its saved columns. B keeps its own (saved or base).
- Reset immediately restores the active preset's base columns and clears its stored override — so a reload afterwards stays on the base set, not the discarded override.
- A stored override that references a column no longer in the schema falls back gracefully (unknown fields dropped; an empty or now-equal-to-preset result behaves as no override).
- The modified marker and Reset button reflect the restored set after reload (a restored override shows as modified).

### Notes

- Decision (locked): localStorage, not URL. Column visibility is a personal sticky preference, not shareable view state. URL was considered and rejected (reverses the deliberate "columns out of the URL" choice, bloats the URL).
- Semantics (locked): "each view remembers its own columns across reloads AND tab switches." This is a behaviour change — today a tab switch discards overrides (reseeds from the preset); after this, the reseed reads the stored override first.
- Per-preset keying is forced: column sets are preset-shaped and Reset is per-preset, so a single global key can't be coherent.
- Precedent to mirror: the theme toggle in AppShell already persists to localStorage (`tad.theme`) with a JS read + guarded fallback. Same pattern, same test/determinism constraints already solved.
- The current behaviour is pinned by an e2e test asserting overrides do NOT survive a reload — flip it.
- Determinism: Playwright contexts are isolated per test; jsdom shares localStorage within a file, so clear it between unit tests that exercise persistence.
```

---

## Main-Thread Message

Time: 2026-06-17T12:10:46.287Z

Let me read the rest of the task and check the uncommitted changes on main, which look related.

---

## Bash Call

Time: 2026-06-17T12:10:47.609Z Description: Read task tail and check uncommitted changes

### Command

```text
echo "=== rest of task ===" && tail -30 tasks/083-persist-column-picker.md && echo "" && echo "=== git status ===" && git status --short && echo "" && echo "=== diff stat ===" && git diff --stat
```

### Output

```text
=== rest of task ===
---
title: "Persist Column Picker Overrides Per Preset"
date: 2026-06-17
status: ready-for-dev
type: feat
---

## Persist Column Picker Overrides per Preset

The ticker-table column picker lets you toggle columns on top of the active preset, but those overrides are session-only React state — a page refresh throws them away and falls back to the preset's columns.

This task makes the overrides stick across reloads (and browser restarts) by persisting them in localStorage, keyed per preset, so each view remembers its own column set.

### Acceptance Criteria

- After toggling columns and reloading the page, the picker and table show the toggled set, not the preset's base set.
- Overrides are remembered per preset: customise view A, switch to view B, switch back — A still shows its saved columns. B keeps its own (saved or base).
- Reset immediately restores the active preset's base columns and clears its stored override — so a reload afterwards stays on the base set, not the discarded override.
- A stored override that references a column no longer in the schema falls back gracefully (unknown fields dropped; an empty or now-equal-to-preset result behaves as no override).
- The modified marker and Reset button reflect the restored set after reload (a restored override shows as modified).

### Notes

- Decision (locked): localStorage, not URL. Column visibility is a personal sticky preference, not shareable view state. URL was considered and rejected (reverses the deliberate "columns out of the URL" choice, bloats the URL).
- Semantics (locked): "each view remembers its own columns across reloads AND tab switches." This is a behaviour change — today a tab switch discards overrides (reseeds from the preset); after this, the reseed reads the stored override first.
- Per-preset keying is forced: column sets are preset-shaped and Reset is per-preset, so a single global key can't be coherent.
- Precedent to mirror: the theme toggle in AppShell already persists to localStorage (`tad.theme`) with a JS read + guarded fallback. Same pattern, same test/determinism constraints already solved.
- The current behaviour is pinned by an e2e test asserting overrides do NOT survive a reload — flip it.
- Determinism: Playwright contexts are isolated per test; jsdom shares localStorage within a file, so clear it between unit tests that exercise persistence.

=== git status ===
 M frontend/src/components/GroupBand.tsx
 M frontend/src/components/TickerTable.tsx
 M frontend/src/components/cells/TickerCell.tsx
 M frontend/src/lib/columns.ts
 M frontend/tests/e2e/columns-picker.spec.ts
 M frontend/tests/e2e/tickers.spec.ts
 M frontend/tests/e2e/views.spec.ts
 M frontend/tests/unit/TickerTable.test.tsx

=== diff stat ===
 frontend/src/components/GroupBand.tsx        |  5 ++++-
 frontend/src/components/TickerTable.tsx      | 23 ++++++++++++++++-------
 frontend/src/components/cells/TickerCell.tsx | 18 ++++++++++++++----
 frontend/src/lib/columns.ts                  |  2 --
 frontend/tests/e2e/columns-picker.spec.ts    |  8 ++++----
 frontend/tests/e2e/tickers.spec.ts           | 20 ++++++++++++--------
 frontend/tests/e2e/views.spec.ts             |  2 +-
 frontend/tests/unit/TickerTable.test.tsx     | 20 +++++++++++---------
 8 files changed, 62 insertions(+), 36 deletions(-)
```

---

## Main-Thread Message

Time: 2026-06-17T12:10:55.999Z

There are pre-existing uncommitted changes on `main` (not mine). They look related to column work. Let me understand them before proceeding, since the worktree branches from `main`'s committed HEAD and won't include them.

---

## Bash Call

Time: 2026-06-17T12:10:56.349Z Description: Inspect uncommitted diff content

### Command

```text
git diff frontend/src/lib/columns.ts frontend/src/components/TickerTable.tsx
```

### Output

```text
diff --git a/frontend/src/components/TickerTable.tsx b/frontend/src/components/TickerTable.tsx
index d487fc3..c660d0e 100644
--- a/frontend/src/components/TickerTable.tsx
+++ b/frontend/src/components/TickerTable.tsx
@@ -119,7 +119,7 @@ function renderCell(field: TickerField, row: TickerSnapshot): ReactNode {

   switch (kind) {
     case "ticker":
-      return <TickerCell value={String(v)} />;
+      return <TickerCell value={String(v)} name={row.name} />;
     case "sector":
       return <SectorCell value={v as string | null} />;
     case "usd":
@@ -150,14 +150,15 @@ function renderCell(field: TickerField, row: TickerSnapshot): ReactNode {
     case "text": {
       // Under the table's fixed layout a column is a hard width cap, so a long
       // value (e.g. a verbose company name) would otherwise overflow into the
-      // next column. Clip with an ellipsis; the full text reaches sighted
-      // users via the shared sans tooltip (`data-tip`) and assistive tech via
-      // the sr-only sibling.
+      // next column. Clip with an ellipsis. The full name's hover tooltip lives
+      // on the always-present ticker column (see TickerCell), not here, so this
+      // cell carries no `data-tip`; the sr-only sibling still exposes the full
+      // (possibly clipped) text to assistive tech.
       if (v == null)
         return <span className="block truncate text-fg-subtle">{EM_DASH}</span>;
       const text = String(v);
       return (
-        <span className="block truncate" data-tip={text}>
+        <span className="block truncate">
           <span aria-hidden="true">{text}</span>
           <span className="sr-only">{text}</span>
         </span>
@@ -535,7 +536,12 @@ export function TickerTable({
                           "left-0 z-[3] shadow-[1px_0_0_var(--border-strong)]",
                         // Group seam: 1px --border-strong on the run's first
                         // column, continuous with the band and body cells.
-                        seams.has(header.column.id) && "border-l border-border-strong",
+                        // Side-specific colour (border-l-*, not all-sides
+                        // border-border-strong) so tailwind-merge can't collapse
+                        // it with the cell's subtle bottom border into one
+                        // all-sides strong colour (which darkened the bottom too).
+                        seams.has(header.column.id) &&
+                          "border-l border-l-border-strong",
                         // Sorted column: faint accent wash composited over the
                         // sticky --surface-sunken band (background-image, not a
                         // background swap, so the band shows through the 6% tint).
@@ -616,7 +622,10 @@ export function TickerTable({
                           reserveInfoGutter && "pr-[28px]",
                           // Group seam: continuous with the band and header
                           // cells — one unbroken vertical at the boundary.
-                          seams.has(field) && "border-l border-border-strong",
+                          // Side-specific colour (border-l-*) so tailwind-merge
+                          // can't fold it into the subtle bottom border as one
+                          // all-sides strong colour (which darkened the bottom).
+                          seams.has(field) && "border-l border-l-border-strong",
                           spec.sticky &&
                             "sticky left-0 z-[1] shadow-[1px_0_0_var(--border-strong)]",
                           sortedCol
diff --git a/frontend/src/lib/columns.ts b/frontend/src/lib/columns.ts
index d574be0..b30a8d5 100644
--- a/frontend/src/lib/columns.ts
+++ b/frontend/src/lib/columns.ts
@@ -479,8 +479,6 @@ export const PRESETS: readonly PresetView[] = [
     label: "Default",
     columns: [
       "ticker",
-      "name",
-      "gics_sector",
       "close",
       "ret_1d",
       "ret_21d",
```

---

## Main-Thread Message

Time: 2026-06-17T12:11:02.693Z

These uncommitted changes are unrelated WIP (moving the company-name tooltip to the ticker cell, trimming the Default preset, a tailwind-merge border fix) — not task 083, and not mine. The worktree branches from `main`'s committed HEAD, so they're correctly excluded. I'll leave them untouched and flag at the end.

## Step 1: Confirm

---

## Bash Call

Time: 2026-06-17T12:11:03.933Z Description: Confirm task with figlet

### Command

```text
figlet -w 120 "Task 083" 2>/dev/null || echo "Task 083"; echo ""; echo "Title : Persist Column Picker Overrides Per Preset"; echo "Status: ready-for-dev"; echo "Type  : feat"
```

### Output

```text
 _____         _       ___   ___ _____ 
|_   _|_ _ ___| | __  / _ \ ( _ )___ / 
  | |/ _` / __| |/ / | | | |/ _ \ |_ \ 
  | | (_| \__ \   <  | |_| | (_) |__) |
  |_|\__,_|___/_|\_\  \___/ \___/____/ 


Title : Persist Column Picker Overrides Per Preset
Status: ready-for-dev
Type  : feat
```

---

## Main-Thread Message

Time: 2026-06-17T12:11:05.899Z

## Step 2: Worktree

---

## Bash Call

Time: 2026-06-17T12:11:07.114Z Description: Create worktree for task 083

### Command

```text
git worktree add -b task/083-persist-column-picker ~/github/.worktrees/tad/083-persist-column-picker main 2>&1 && echo "WORKTREE_CREATED"
```

### Output

```text
Preparing worktree (new branch 'task/083-persist-column-picker')
HEAD is now at df77f86 Add task 083: persist column picker overrides per preset (task/083)
WORKTREE_CREATED
```

---

## Bash Call

Time: 2026-06-17T12:11:09.678Z Description: Initialise worktree

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && pwd && just worktree-init 2>&1 | tail -20
```

### Output

```text
~/github/.worktrees/tad/083-persist-column-picker
+ vite@8.0.16
+ vitest@4.1.9
+ @base-ui/react@1.5.0
+ @fontsource-variable/inter@5.2.8
+ @fontsource-variable/inter-tight@5.2.7
+ @fontsource-variable/jetbrains-mono@5.2.8
+ @tanstack/react-query@5.101.0
+ @tanstack/react-router@1.170.15
+ @tanstack/react-table@8.21.3
+ clsx@2.1.1
+ lucide-react@1.18.0
+ openapi-fetch@0.17.0
+ react@19.2.7
+ react-dom@19.2.7
+ tailwind-merge@3.6.0
+ tailwindcss@4.3.1
+ tw-animate-css@1.4.0

465 packages installed [2.58s]
Installed: frontend node_modules (bun, frozen lockfile) ← frontend/
Shell cwd was reset to ~/github/tad
```

---

## Main-Thread Message

Time: 2026-06-17T12:11:23.112Z

Worktree ready. Now Step 3: planning via panel + synthesis. Let me read the relevant skills to invoke them correctly.

---

## Bash Call

Time: 2026-06-17T12:11:24.271Z Description: Read panel and plan-task skills

### Command

```text
cat ~/github/tad/.claude/skills/panel/SKILL.md 2>/dev/null | head -60; echo "=== PLAN-TASK ==="; cat ~/github/tad/.claude/skills/plan-task/SKILL.md 2>/dev/null | head -80
```

### Output

```text
---
name: panel
description: Use to get independent perspectives on a topic from multiple models (opus + codex). Use with /synthesize to merge.
---

# Panel

## Precondition

Must be run from main thread (reason: subagents can't spawn other subagents)

## Usage

`/panel <prompt>`

Prompt is mandatory — if missing, fail loudly; don't infer.

## Goal

Get independent perspectives on a topic from multiple models (opus + codex).

## Step 1: Expand Skill References

If the prompt invokes a skill (explicit `/name` only — not bare names in prose/diagrams), inline its `SKILL.md`, clearly fenced, after the instruction. Recurse into `/name` invocations found inside, but inline each skill at most once — never re-expand one already present (terminates; prevents cycles and bloat).

Example: `/panel please /plan-task 054 but don't write to the task file.`

Expanded prompt:

""" Please /plan-task 054 but don't write to the task file.

Skill references: === BEGIN plan-task SKILL.md === [full content of ~/github/tad/.claude/skills/plan-task/SKILL.md] === END plan-task SKILL.md === """

## Step 2: Append Anti-Sycophancy Block

Append the block below to the prompt:

> Answer directly and honestly. Do not hedge or soften to be agreeable. If your honest answer differs substantively from what the prompt seems to expect, give that one.

## Step 3: Dispatch

Spawn a Codex (via `codex:codex-rescue`) and an Opus subagent in parallel and pass through the prompt.

If Codex is unavailable (e.g. usage limit), fail loudly — do not substitute or skip.

Write the responses to `/tmp/panel-<timestamp>-<slot>.md`.

## Step 4: Deliver

Present both responses verbatim, each directly attributed to its model (Codex / Opus), including the paths to the raw responses.

Do not synthesise, reconcile, or edit.
=== PLAN-TASK ===
---
name: plan-task
description: Write an implementation plan for a well-defined task. Typical workflow: create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task.
---

# Plan Task

## Usage

`/plan-task <task-path> [further user instructions]`

## Goal

Given a well-defined task (the "why" and "what"), write an implementation plan (the "how") that closes the decision space for an implementing agent.

## Context

This skill is typically run as part of a larger workflow:

```text
create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (stored in `tasks/`) plus repo state carry everything the next agent needs.

## Guidance (DO NOT IGNORE!)

<!-- Curate as we go along. -->

These rules govern what belongs in the plan and how to write it. Internalise and follow them throughout.

- Write for a competent outsider. They can write code, name things, follow patterns but they don't have in-team context beyond what's in the task and the repo.
- Be maximally succinct. Capture the plan with the fewest words that remove ambiguity. Plan length obviously follows complexity but don't pad.
- What would you be nervous about if you gave the agent only the task and codebase but no plan? Address those (and only those) things.
- If (and only if) load-bearing, add pointers to existing code (modules, classes, functions, utilities, etc. to consider), sequencing when ordering matters for correctness, constraints on approach when more than one is plausible.
- Lock down details of cross-boundary contracts in the plan (e.g. API shapes, DB/parquet schemas, symbols reachable across package boundaries, etc.).
- Leave decision on internal details to the implementer - no pseudocode, no names for new files/classes/functions, no exact line numbers, no details that will go stale quickly.
- Do not restate universal truths ("write tests", "handle errors", "follow patterns", "run the build").
- Avoid placeholders, i.e. no "TBD"s, no "handle edge cases", no "similar to step 3". If it's worth writing down, be concrete.
- Use plain English and write like a senior engineer briefing a teammate, not like an AI producing a spec. Avoid AI-slop language and padding.

### Anti-Patterns

Real failures observed in past plans. Don't repeat:

- Don't add "write unit tests" or similar steps
- Don't add "run just check-all before commit" or similar steps

## Step 1: Check Task Readiness

If the task's status is not `ready-for-dev` (usually set at the end of `/clarify-task`), flag it to the user and ask how to proceed.

## Step 2: Build Context

Read the task and the code the plan will likely touch. If in doubt, err on the side of reading too much. Ensure you fully understand the task and current state of the codebase before proceeding.

## Step 3: Write the Plan

Write a plan using the structure below (drop sections that aren't needed):

```markdown
## Implementation Plan

### TLDR

[One short sentence or paragraph summarising the plan. Omit for trivial plans.]

### Steps

[Numbered list of steps - imperative, specific, terse]

### Notes

[Only add as short bullets when truly valuable:

- Things you'd be nervous whether a new agent gets right if not written down.
- Not yet captured insights, assumptions, flags, constraints, decisions, etc.
- Anything worth capturing for posterity.]

## Step 4: Self-Audit
```

---

## Main-Thread Message

Time: 2026-06-17T12:11:36.097Z

Let me read the rest of plan-task and locate the column-picker code so I can ground the planning and synthesis.

---

## Bash Call

Time: 2026-06-17T12:11:36.186Z Description: Read plan-task tail, check codex, find picker code

### Command

```text
cat ~/github/tad/.claude/skills/plan-task/SKILL.md | tail -30; echo "=== codex check ==="; ls ~/.claude/plugins/cache/**/commands/ 2>/dev/null | grep -i adversarial; echo "=== find column picker code ==="; cd ~/github/.worktrees/tad/083-persist-column-picker && grep -rln "column" frontend/src/components frontend/src/lib --include=*.tsx --include=*.ts -i | head -20
```

### Output

```text
### TLDR

[One short sentence or paragraph summarising the plan. Omit for trivial plans.]

### Steps

[Numbered list of steps - imperative, specific, terse]

### Notes

[Only add as short bullets when truly valuable:

- Things you'd be nervous whether a new agent gets right if not written down.
- Not yet captured insights, assumptions, flags, constraints, decisions, etc.
- Anything worth capturing for posterity.]

## Step 4: Self-Audit

Re-read the Guidance section (incl. Anti-Patterns). For each step in the plan, ask whether it violates the Guidance. If it does and there's no strong reason for doing so, re-work the plan once.

<!-- Note: According to research, additional self-reflection loops without external signal degrades quality more often than it helps -->

## Step 5: Present

Present the plan to the user.

## Step 6: Write Plan to Task (Optional)

If the user instructed you to do so, write the Implementation Plan section to the task file.
=== codex check ===
adversarial-review.md
=== find column picker code ===
(eval):1: no matches found: --include=*.tsx
Shell cwd was reset to ~/github/tad
```

---

## Bash Call

Time: 2026-06-17T12:11:40.658Z Description: Locate picker and localStorage precedent

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -rln -i "picker\|columnOverride\|preset\|visibleColumns" frontend/src | head -20; echo "=== theme persist precedent ==="; grep -rln "tad.theme\|localStorage" frontend/src | head
```

### Output

```text
frontend/src/components/ColumnsMenu.tsx
frontend/src/components/ViewBar.tsx
frontend/src/components/TickerTable.tsx
frontend/src/components/GroupBand.tsx
frontend/src/components/ui/checkbox.tsx
frontend/src/lib/views.ts
frontend/src/lib/visibleColumns.ts
frontend/src/lib/columns.ts
frontend/src/routes/index.tsx
=== theme persist precedent ===
frontend/src/components/AppShell.tsx
Shell cwd was reset to ~/github/tad
```

---

## Bash Call

Time: 2026-06-17T12:11:51.183Z Description: Read theme precedent and views exports

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && echo "=== AppShell theme persist ==="; grep -n "tad.theme\|localStorage\|function.*[Tt]heme\|getItem\|setItem" frontend/src/components/AppShell.tsx; echo ""; echo "=== views.ts exports ==="; grep -n "export" frontend/src/lib/views.ts
```

### Output

```text
=== AppShell theme persist ===
13:// screenshot/Storybook links — falling back to localStorage, then the
14:// OS-level preference. Only an explicit toggle persists to localStorage:
29:const STORAGE_KEY = "tad.theme";
31:function readInitialTheme(): "light" | "dark" {
35:  const saved = window.localStorage.getItem(STORAGE_KEY);
63:    window.localStorage.setItem(STORAGE_KEY, next);

=== views.ts exports ===
12:export const DEFAULT_VIEW_ID = "default";
19:export type GroupRun = {
26:export type GroupedColumn = { field: string; group: string };
33:export function groupRuns(columns: readonly GroupedColumn[]): GroupRun[] {
53:export function seamFields(
75:export function widestPreset(presets: readonly PresetView[]): PresetView | null {
88:export function canonicalColumnOrder(
100:export function resolveActivePreset(
Shell cwd was reset to ~/github/tad
```

---

## Bash Call

Time: 2026-06-17T12:11:55.384Z Description: Read theme code and pinning e2e

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && echo "=== e2e test that pins current behaviour ==="; grep -n "reload\|localStorage\|survive\|persist\|override" frontend/tests/e2e/columns-picker.spec.ts
```

### Output

```text
=== e2e test that pins current behaviour ===
96:test("the picker closes on Escape and overrides do not survive a reload", async ({
110:  // Session-only: a reload restores the base ?view (no Open, no override in URL).
111:  await page.reload();
Shell cwd was reset to ~/github/tad
```

---

## Main-Thread Message

Time: 2026-06-17T12:12:02.678Z

I have strong context now. Dispatching the planning panel (Opus + Codex in parallel) per Step 3.

---

## Subagent 1: Plan Task 083 (Opus) [General-Purpose]

Time: 2026-06-17T12:12:26.212Z

### Prompt

You are writing an IMPLEMENTATION PLAN (the "how") for a well-defined task in the TAD codebase. Do NOT write code — produce a plan only.

Working directory / worktree root: ~/github/.worktrees/tad/083-persist-column-picker Task file: ~/github/.worktrees/tad/083-persist-column-picker/tasks/083-persist-column-picker.md

Read the task file end-to-end, then read the code the plan will touch before writing anything. Key files I've already located (read them yourself to verify):

- frontend/src/routes/index.tsx — `ScreenerBody` owns the SESSION visible-column set (useState seeded from `activePreset.columns`; reseeded synchronously via the prev-id-in-state pattern when `activePreset.id` changes; restored on `onReset`). This is the heart of the change.
- frontend/src/lib/visibleColumns.ts — pure helpers (isColumnSetModified, toggleColumnOn/Off, toggleGroup).
- frontend/src/lib/views.ts — resolveActivePreset, canonicalColumnOrder, DEFAULT_VIEW_ID.
- frontend/src/lib/columns.ts — PRESETS, GROUPS, TickerField type. Each preset has `id`, `label`, `columns`.
- frontend/src/components/ColumnsMenu.tsx — the picker UI (onVisibleColumnsChange, onReset, isModified).
- frontend/src/components/AppShell.tsx — THE localStorage precedent to mirror: `STORAGE_KEY = "tad.theme"`, `readInitialTheme()` with `typeof window === "undefined"` guard + `window.localStorage.getItem`, explicit-action-only writes via `setItem`. Mirror this pattern (JS read + guarded fallback, deterministic, SSR-safe).
- frontend/tests/e2e/columns-picker.spec.ts — line ~96 the test "the picker closes on Escape and overrides do not survive a reload" PINS the current (to-be-flipped) behaviour. Must be flipped.

The task requires: persist column-picker overrides to localStorage, keyed PER PRESET, so each view remembers its own column set across reloads AND tab switches. Reset clears the stored override. A stored override referencing a column no longer in the schema must drop unknown fields and fall back gracefully (empty or now-equal-to-preset => behaves as no override). The modified marker + Reset button must reflect the restored set after reload.

Follow these plan-writing rules (from TAD's /plan-task skill) — internalise them:

- Write for a competent outsider with no in-team context beyond task + repo.
- Be maximally succinct; capture the plan with the fewest words that remove ambiguity. No padding.
- Address only what you'd be nervous a new agent gets wrong without the plan.
- Add load-bearing pointers to existing code, sequencing where order matters for correctness, and constraints on approach when more than one is plausible.
- Lock down cross-boundary contracts (the localStorage key shape/scheme, the serialised value shape, the read/validate/fallback semantics).
- Leave internal details to the implementer — no pseudocode, no new file/function names, no line numbers.
- Do NOT restate universal truths ("write tests", "handle errors", "run the build"). Do NOT add "write unit tests" or "run just check-all" steps.

Decide and lock these design questions in the plan (this is where the value is):

1. localStorage key scheme — single key holding a map {presetId: columns[]} vs one key per preset. Recommend one and say why.
2. WHERE the read/write lives — a small framework-free module (mirroring the visibleColumns.ts style, unit-testable without rendering) vs inline in ScreenerBody. The seed AND every override mutation (toggle + reset) must round-trip through it.
3. How the seed/reseed in ScreenerBody changes: today it seeds `useState(activePreset.columns)` and reseeds on preset-id change to `activePreset.columns`. After: both must read the stored override for that preset id first, validated against the schema, falling back to base. Watch the prev-id-in-state synchronous reseed path — both the initial seed and the reseed must go through the same "load override or base" function.
4. Validation/sanitisation: dropping unknown fields, and the rule that an override equal to the preset base (or empty) is treated as "no override" (don't show modified, don't persist a redundant entry).
5. Reset semantics: clear the stored entry for the active preset so a later reload stays on base.
6. Determinism for tests: jsdom shares localStorage within a file (clear between unit tests); Playwright contexts are isolated.

Output format:

## Implementation Plan

### TLDR

### Steps

### Notes

Answer directly and honestly. Do not hedge or soften to be agreeable. If your honest answer differs substantively from what the prompt seems to expect, give that one.

### Response

I have a full picture. Here is the plan.

## Implementation Plan

### TLDR

Add a small framework-free persistence module (sibling to `visibleColumns.ts`) that stores per-preset column-set overrides in localStorage under a single key holding a `{ [presetId]: TickerField[] }` map. Route every seed/reseed/mutation/reset in `ScreenerBody` through it: seeding (initial + the prev-id-in-state reseed) reads-and-validates the stored override (falling back to the preset base); the picker's change handler and group-toggle persist; Reset deletes the entry. Sanitise on read (drop unknown fields; treat empty / equal-to-base as no override). Flip the e2e test that pins the old "overrides die on reload" behaviour.

### Steps

1. **New persistence module** (`frontend/src/lib/`, framework-free, unit-testable without rendering — mirror `visibleColumns.ts` style and the AppShell localStorage pattern). It owns the entire localStorage contract. Expose three operations the body needs:
   - **Resolve** a preset's effective starting set: given a preset id, that preset's base columns, and the canonical column universe (the set of currently-valid fields), return the validated override if one exists, else the base.
   - **Persist** an override for a preset id (called on every toggle/group mutation and from Reset's caller only when not resetting — see step 4).
   - **Clear** a preset id's stored entry (Reset).

   All three read/write the single key. Reads must be SSR-safe and corruption-safe: `typeof window === "undefined"` guard returning "no override", and a `try/catch` around `getItem` + `JSON.parse` that treats any malformed blob as empty (do not throw). Writes likewise guard `window` and wrap `setItem` in `try/catch` (quota/availability) — a failed write must not break a toggle.

2. **Key + value contract (locked).** Use ONE key, `tad.columns` (matches the `tad.theme` namespace), holding a JSON object map `{ [presetId: string]: string[] }`. One key, not one-key-per-preset: the whole map round-trips in a single read/write, Reset is a single-property delete, and there's no key-enumeration to clear. Values are arrays of field-id strings (the `TickerField` string literals), order-significant (order is part of "modified" and the render order). Absent preset id ⇒ no override. Do not store presets that equal their base.

3. **Validation / sanitisation (locked, lives in the resolve path).** When resolving a stored array:
   - Drop any field not in the canonical universe (the `canonicalColumnOrder(PRESETS)` set — the authoritative current schema). This handles a renamed/removed column.
   - Always keep the locked `ticker` field present and first is NOT required by the resolver — but the stored set must still be coherent; simplest correct rule: filter to known fields, preserve stored order.
   - After filtering, if the result is empty OR equals the preset's base columns (use `isColumnSetModified` — equal ⇒ not modified), return the base and treat it as "no override" (the caller renders unmodified; nothing needs re-persisting on mount). Returning base here is what makes a now-degenerate override behave as none.

4. **`ScreenerBody` wiring** (`frontend/src/routes/index.tsx`) — the heart. Today: `useState(activePreset.columns)` + the `prevPresetId` synchronous reseed to `activePreset.columns` + `onReset` setting `activePreset.columns`. Change so:
   - **Initial seed** (`useState` initialiser) calls the module's resolve for `activePreset` instead of using `activePreset.columns` raw. Use the lazy initialiser form so the read runs once.
   - **Reseed** (the `prevPresetId !== activePreset.id` block) sets `visibleColumns` to the module's resolve for the NEW preset — same function as the seed. This is the behaviour change: a tab switch now restores that preset's saved override, not its base. Keep it in the same synchronous render-phase block; do not convert to `useEffect`.
   - **Persist on mutation.** The picker calls `onVisibleColumnsChange` (currently `setVisibleColumns` directly) for both per-column toggles and group toggles. Replace that prop with a handler that both `setVisibleColumns(next)` AND persists `next` for `activePreset.id`. The handler must persist the *exact* set the picker computed (the toggle helpers already produce the canonical-ordered result) — so persistence captures order. If `next` equals base, the module should delete rather than write a redundant entry (fold this into the persist op or the handler — keep it in the module so the "equal-to-base ⇒ no override" invariant has one home).
   - **Reset.** `onReset` keeps `setVisibleColumns(activePreset.columns)` + nonce bump + `onResetPage()`, and additionally calls the module's clear for `activePreset.id`. Order doesn't matter (state vs storage are independent), but clear must happen so a later reload stays on base.
   - `isModified` stays `isColumnSetModified(visibleColumns, activePreset.columns)` — unchanged; it now reads true after a reload because the seed restored the override. The modified marker + Reset-enabled both derive from it, so AC "reflect restored set after reload" falls out for free.

5. **Pass the canonical universe to the module.** The resolver needs the valid-field set. `canonicalColumnOrder(PRESETS)` (already memoised in `ScreenerBody` as `canonicalOrder`) is that set — thread it into resolve. Keep the module free of a hard import of `PRESETS`/`columns.ts` if cheap (take the universe as a parameter, mirroring `visibleColumns.ts`'s generic-over-field style); that keeps it pure and unit-testable with synthetic field lists.

6. **Flip the e2e test** (`columns-picker.spec.ts`, the "overrides do not survive a reload" test). After Esc + reload, assert the OPPOSITE: the `Open` column header IS still visible, the count reads `12/28`, and the `Default — modified` tab marker is present. Keep the Esc-closes-popover assertions. Rename the test title to reflect persistence. Playwright contexts are isolated per test, so no explicit storage clearing is needed there. Re-scan the rest of this spec and `tickers.spec.ts` / `views.spec.ts` for any other assertion that a reload returns to base — those are already modified in the working tree per `git status`, so reconcile with what's there rather than assuming the committed versions.

7. **Unit tests for the module** (`frontend/tests/unit/`, new file beside `visibleColumns.test.ts`). Cover: round-trip persist→resolve; unknown-field drop; empty-after-filter ⇒ base; equal-to-base ⇒ not persisted / resolves as no override; clear removes only the targeted preset; corrupt/absent localStorage ⇒ base. jsdom shares localStorage across tests in a file — clear it in a `beforeEach` (or `afterEach`).

### Notes

- **Why per-preset map, not per-preset state in React:** the override universe is small and preset-keyed; the body only ever holds the *active* preset's set in React state and re-resolves from storage on switch. Don't try to hold all presets' overrides in React — storage is the source of truth across presets, state is just the active working copy.
- **The "equal-to-base ⇒ no override" invariant has exactly one home** (the module). Both the persist path (don't write a redundant entry; delete instead) and the resolve path (a stored set that filters down to base resolves as base) enforce it. This keeps the modified marker honest: toggling a column on then off returns to base and clears the marker *and* clears storage, so a reload stays on base.
- **Locked `ticker` column:** the picker never lets you remove it, so a persisted set will normally contain it. The resolver should not special-case re-inserting it; just filter to known fields. If a corrupt stored set somehow lacks ticker, that's a degenerate override — acceptable, the table still renders the remaining known columns; don't add reconstruction logic for a state the UI can't produce.
- **Don't touch `TickerTable`/sort:** sort reseed already keys off `activePreset` and the `resetNonce`; persistence is columns-only. The existing comment in `ScreenerBody` ("picker overrides are discarded on a tab switch with no extra logic") becomes false — update it to describe the new restore-from-storage behaviour.
- **Validate the in-repo working-tree state first:** `index.tsx`, `columns.ts`, and the three e2e specs already show as modified in `git status` from prior task work (column reclassification). Read them as they are in the worktree (done) — the universe is now 28 columns and groups were split, so any test count literals (`11/28`, `12/28`) reflect current reality; keep them consistent.
- **`.env.example` / docs:** localStorage keys are not env vars and there's no README catalogue for them; the `tad.theme` precedent adds no doc entry, so none is needed here.
agentId: accadbdb1746f8b4e (use SendMessage with to: 'accadbdb1746f8b4e' to continue this agent) <usage>subagent_tokens: 73497 tool_uses: 9 duration_ms: 66911</usage>

---

<details><summary>Inner trace (subagent session agent-accadbdb1746f8b4e, depth 1)</summary>

## Main-Thread Message

Time: 2026-06-17T12:12:28.571Z

I'll read the task file and the key code before writing the plan.

---

## Main-Thread Message

Time: 2026-06-17T12:12:38.451Z

Let me read the remaining key files: AppShell (localStorage precedent), ColumnsMenu, columns.ts, and the e2e test.

---

## Main-Thread Message

Time: 2026-06-17T12:12:44.368Z

I have everything I need. Let me check the existing unit test file structure for visibleColumns to understand test conventions and confirm there's no existing storage test.

---

## Bash Call

Time: 2026-06-17T12:12:45.576Z Description: List unit tests and lib files

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && ls frontend/tests/unit/ && echo "---lib---" && ls frontend/src/lib/
```

### Output

```text
BoolBadge.test.tsx
Checkbox.test.tsx
columns.test.ts
ColumnsMenu.test.tsx
format.test.ts
GroupBand.test.tsx
HeaderInfoCard.test.tsx
LoadStatus.test.tsx
MarketSummary.test.tsx
PercentCell.test.tsx
routerContext.tsx
setup.ts
shortcuts.test.ts
ShortcutsDialog.test.tsx
TablePagination.test.tsx
tickerMatchesQuery.test.ts
TickerTable.test.tsx
ViewBar.test.tsx
views.test.ts
visibleColumns.test.ts
ZScoreCell.test.tsx
---lib---
columns.ts
format.ts
pagination.ts
shortcuts.ts
utils.ts
views.ts
visibleColumns.ts
```

---

## Main-Thread Message

Time: 2026-06-17T12:13:32.993Z

I have a full picture. Here is the plan.

## Implementation Plan

### TLDR

Add a small framework-free persistence module (sibling to `visibleColumns.ts`) that stores per-preset column-set overrides in localStorage under a single key holding a `{ [presetId]: TickerField[] }` map. Route every seed/reseed/mutation/reset in `ScreenerBody` through it: seeding (initial + the prev-id-in-state reseed) reads-and-validates the stored override (falling back to the preset base); the picker's change handler and group-toggle persist; Reset deletes the entry. Sanitise on read (drop unknown fields; treat empty / equal-to-base as no override). Flip the e2e test that pins the old "overrides die on reload" behaviour.

### Steps

1. **New persistence module** (`frontend/src/lib/`, framework-free, unit-testable without rendering — mirror `visibleColumns.ts` style and the AppShell localStorage pattern). It owns the entire localStorage contract. Expose three operations the body needs:
   - **Resolve** a preset's effective starting set: given a preset id, that preset's base columns, and the canonical column universe (the set of currently-valid fields), return the validated override if one exists, else the base.
   - **Persist** an override for a preset id (called on every toggle/group mutation and from Reset's caller only when not resetting — see step 4).
   - **Clear** a preset id's stored entry (Reset).

   All three read/write the single key. Reads must be SSR-safe and corruption-safe: `typeof window === "undefined"` guard returning "no override", and a `try/catch` around `getItem` + `JSON.parse` that treats any malformed blob as empty (do not throw). Writes likewise guard `window` and wrap `setItem` in `try/catch` (quota/availability) — a failed write must not break a toggle.

2. **Key + value contract (locked).** Use ONE key, `tad.columns` (matches the `tad.theme` namespace), holding a JSON object map `{ [presetId: string]: string[] }`. One key, not one-key-per-preset: the whole map round-trips in a single read/write, Reset is a single-property delete, and there's no key-enumeration to clear. Values are arrays of field-id strings (the `TickerField` string literals), order-significant (order is part of "modified" and the render order). Absent preset id ⇒ no override. Do not store presets that equal their base.

3. **Validation / sanitisation (locked, lives in the resolve path).** When resolving a stored array:
   - Drop any field not in the canonical universe (the `canonicalColumnOrder(PRESETS)` set — the authoritative current schema). This handles a renamed/removed column.
   - Always keep the locked `ticker` field present and first is NOT required by the resolver — but the stored set must still be coherent; simplest correct rule: filter to known fields, preserve stored order.
   - After filtering, if the result is empty OR equals the preset's base columns (use `isColumnSetModified` — equal ⇒ not modified), return the base and treat it as "no override" (the caller renders unmodified; nothing needs re-persisting on mount). Returning base here is what makes a now-degenerate override behave as none.

4. **`ScreenerBody` wiring** (`frontend/src/routes/index.tsx`) — the heart. Today: `useState(activePreset.columns)` + the `prevPresetId` synchronous reseed to `activePreset.columns` + `onReset` setting `activePreset.columns`. Change so:
   - **Initial seed** (`useState` initialiser) calls the module's resolve for `activePreset` instead of using `activePreset.columns` raw. Use the lazy initialiser form so the read runs once.
   - **Reseed** (the `prevPresetId !== activePreset.id` block) sets `visibleColumns` to the module's resolve for the NEW preset — same function as the seed. This is the behaviour change: a tab switch now restores that preset's saved override, not its base. Keep it in the same synchronous render-phase block; do not convert to `useEffect`.
   - **Persist on mutation.** The picker calls `onVisibleColumnsChange` (currently `setVisibleColumns` directly) for both per-column toggles and group toggles. Replace that prop with a handler that both `setVisibleColumns(next)` AND persists `next` for `activePreset.id`. The handler must persist the *exact* set the picker computed (the toggle helpers already produce the canonical-ordered result) — so persistence captures order. If `next` equals base, the module should delete rather than write a redundant entry (fold this into the persist op or the handler — keep it in the module so the "equal-to-base ⇒ no override" invariant has one home).
   - **Reset.** `onReset` keeps `setVisibleColumns(activePreset.columns)` + nonce bump + `onResetPage()`, and additionally calls the module's clear for `activePreset.id`. Order doesn't matter (state vs storage are independent), but clear must happen so a later reload stays on base.
   - `isModified` stays `isColumnSetModified(visibleColumns, activePreset.columns)` — unchanged; it now reads true after a reload because the seed restored the override. The modified marker + Reset-enabled both derive from it, so AC "reflect restored set after reload" falls out for free.

5. **Pass the canonical universe to the module.** The resolver needs the valid-field set. `canonicalColumnOrder(PRESETS)` (already memoised in `ScreenerBody` as `canonicalOrder`) is that set — thread it into resolve. Keep the module free of a hard import of `PRESETS`/`columns.ts` if cheap (take the universe as a parameter, mirroring `visibleColumns.ts`'s generic-over-field style); that keeps it pure and unit-testable with synthetic field lists.

6. **Flip the e2e test** (`columns-picker.spec.ts`, the "overrides do not survive a reload" test). After Esc + reload, assert the OPPOSITE: the `Open` column header IS still visible, the count reads `12/28`, and the `Default — modified` tab marker is present. Keep the Esc-closes-popover assertions. Rename the test title to reflect persistence. Playwright contexts are isolated per test, so no explicit storage clearing is needed there. Re-scan the rest of this spec and `tickers.spec.ts` / `views.spec.ts` for any other assertion that a reload returns to base — those are already modified in the working tree per `git status`, so reconcile with what's there rather than assuming the committed versions.

7. **Unit tests for the module** (`frontend/tests/unit/`, new file beside `visibleColumns.test.ts`). Cover: round-trip persist→resolve; unknown-field drop; empty-after-filter ⇒ base; equal-to-base ⇒ not persisted / resolves as no override; clear removes only the targeted preset; corrupt/absent localStorage ⇒ base. jsdom shares localStorage across tests in a file — clear it in a `beforeEach` (or `afterEach`).

### Notes

- **Why per-preset map, not per-preset state in React:** the override universe is small and preset-keyed; the body only ever holds the *active* preset's set in React state and re-resolves from storage on switch. Don't try to hold all presets' overrides in React — storage is the source of truth across presets, state is just the active working copy.
- **The "equal-to-base ⇒ no override" invariant has exactly one home** (the module). Both the persist path (don't write a redundant entry; delete instead) and the resolve path (a stored set that filters down to base resolves as base) enforce it. This keeps the modified marker honest: toggling a column on then off returns to base and clears the marker *and* clears storage, so a reload stays on base.
- **Locked `ticker` column:** the picker never lets you remove it, so a persisted set will normally contain it. The resolver should not special-case re-inserting it; just filter to known fields. If a corrupt stored set somehow lacks ticker, that's a degenerate override — acceptable, the table still renders the remaining known columns; don't add reconstruction logic for a state the UI can't produce.
- **Don't touch `TickerTable`/sort:** sort reseed already keys off `activePreset` and the `resetNonce`; persistence is columns-only. The existing comment in `ScreenerBody` ("picker overrides are discarded on a tab switch with no extra logic") becomes false — update it to describe the new restore-from-storage behaviour.
- **Validate the in-repo working-tree state first:** `index.tsx`, `columns.ts`, and the three e2e specs already show as modified in `git status` from prior task work (column reclassification). Read them as they are in the worktree (done) — the universe is now 28 columns and groups were split, so any test count literals (`11/28`, `12/28`) reflect current reality; keep them consistent.
- **`.env.example` / docs:** localStorage keys are not env vars and there's no README catalogue for them; the `tad.theme` precedent adds no doc entry, so none is needed here.

---

</details>

## Subagent 2: Plan Task 083 (Codex) [Codex:codex-Rescue]

Time: 2026-06-17T12:12:37.264Z

### Prompt

Write an IMPLEMENTATION PLAN (the "how") for a well-defined task in the TAD codebase. Do NOT write code — produce a plan only. Read files, do not modify them.

Worktree root (cd here): ~/github/.worktrees/tad/083-persist-column-picker Task file: tasks/083-persist-column-picker.md (read it end-to-end first)

The task: persist ticker-table column-picker overrides to localStorage, keyed PER PRESET, so each view (preset) remembers its own column set across page reloads AND tab/view switches. Today overrides are session-only React state (discarded on reload and on tab switch). Acceptance criteria are in the task file — read them.

Key code to read before planning:

- frontend/src/routes/index.tsx — `ScreenerBody` owns the session visible-column set: `useState(activePreset.columns)`, reseeded synchronously when `activePreset.id` changes (prev-id-in-state pattern, NOT useEffect), restored on `onReset`. This is the heart of the change.
- frontend/src/lib/visibleColumns.ts — pure, unit-testable column helpers (the style to mirror for any new pure module).
- frontend/src/lib/views.ts, frontend/src/lib/columns.ts — PRESETS (each has id/label/columns), TickerField type, canonicalColumnOrder.
- frontend/src/components/ColumnsMenu.tsx — picker UI.
- frontend/src/components/AppShell.tsx — the localStorage precedent to mirror: `tad.theme` key, `readInitialTheme()` with `typeof window === "undefined"` guard, explicit-write-only via setItem.
- frontend/tests/e2e/columns-picker.spec.ts (~line 96) — a test currently PINS "overrides do not survive a reload"; it must be flipped.

Lock these decisions in the plan (this is the value):

1. localStorage key scheme: one key holding {presetId: columns[]} map vs one key per preset — recommend one, justify briefly.
2. Where read/write lives: a small framework-free module (mirroring visibleColumns.ts) vs inline. Seed + every mutation (toggle, reset) must round-trip through it.
3. Seed/reseed change in ScreenerBody: initial seed AND the prev-id-in-state reseed must both read the validated stored override-or-base. Don't break the synchronous reseed.
4. Validation: drop unknown fields (column removed from schema); an override equal to base or empty => treat as "no override" (not modified, don't persist redundant entry).
5. Reset clears the stored entry for the active preset.
6. Test determinism: jsdom shares localStorage within a file (clear between unit tests); Playwright isolated per test.

Keep it succinct. No pseudocode, no new file/function names, no line numbers. Don't restate universal truths or add "write tests"/"run check-all" steps. Output as: ## Implementation Plan / ### TLDR / ### Steps / ### Notes.

Answer directly and honestly. If your honest answer differs from what the prompt expects, give that one.

### Response

Now I have everything I need. Here is the plan:

---

## Implementation Plan

### TLDR

Add a thin, framework-free `columnPickerStorage` module (mirroring `visibleColumns.ts`) that reads and writes a single `tad.columnOverrides` localStorage key holding a `Record<presetId, TickerField[]>` map. Thread it into the three mutation sites in `ScreenerBody` (initial seed, prev-id reseed, reset) and flip the one e2e test that currently pins the old behaviour.

---

### Steps

**1. New storage module (`frontend/src/lib/columnPickerStorage.ts`)**

- Key: single string `tad.columnOverrides`, value shape: `Record<string, string[]>` (the full map, one entry per preset id).
- A single-key map is the right choice over per-preset keys: it's one atomic read on init, one atomic write on every mutation, trivially cleared in tests, and naturally handles presets being added/removed without key-soup proliferation. The only tradeoff (one large JSON blob) is irrelevant at a few dozen columns × ~6 presets.
- Export three pure functions (all guarded with `typeof window === "undefined"` to survive SSR/test environments that lack `window`):
  - `readOverride(presetId, baseColumns, knownFields)` → reads the map, finds the entry for `presetId`, drops unknown fields (i.e. fields not in `knownFields`), returns `null` if the entry is absent, empty after filtering, or equals `baseColumns` element-wise (no override to apply).
  - `writeOverride(presetId, columns, baseColumns)` → if `columns` equals `baseColumns` element-wise, call `clearOverride` instead (no redundant entry); otherwise upsert the entry and `setItem` the whole map.
  - `clearOverride(presetId)` → reads the map, deletes the key for `presetId`, and `setItem` the updated map (or removes the key entirely if the map is now empty, as a micro-hygiene).
- No React import; no side effects at module load time.

**2. Seed and reseed in `ScreenerBody`**

- `knownFields` is derived from `canonicalColumnOrder(PRESETS)` — already computed in `ScreenerBody` as `canonicalOrder`. Pass it to `readOverride`.
- Initial `useState` seed: replace `activePreset.columns` with `readOverride(activePreset.id, activePreset.columns, canonicalOrder) ?? activePreset.columns`.
- Prev-id-in-state reseed block (the synchronous render-time branch): replace `setVisibleColumns(activePreset.columns)` with `setVisibleColumns(readOverride(activePreset.id, nextPreset.columns, canonicalOrder) ?? nextPreset.columns)`. This preserves the synchronous reseed — no useEffect introduced.
- Every `setVisibleColumns` call that comes from `onVisibleColumnsChange` (the picker toggle path, wired through `ColumnsMenu`) must also write storage. The cleanest place: wrap `setVisibleColumns` in `ScreenerBody` with a one-liner that calls `writeOverride` and then `setVisibleColumns`. The `ColumnsMenu`'s `onVisibleColumnsChange` prop already points at `setVisibleColumns` — redirect it to the wrapper.

## 3. Reset Clears Stored Override

- In `onReset`, call `clearOverride(activePreset.id)` before (or alongside) `setVisibleColumns(activePreset.columns)`. Order doesn't matter; both are synchronous.

## 4. Flip the E2e Test

- The test at ~line 96 (`"the picker closes on Escape and overrides do not survive a reload"`) must become two separate tests:
  - One testing only the Escape-closes-picker behaviour (keep the Esc assertion; drop the reload and column-absence assertions).
  - One new test asserting that toggling a column on, reloading, and switching views all persist/restore correctly — verifying: (a) toggled column survives reload, (b) switching to another view and back restores the saved override for the original view, (c) Reset clears it so a subsequent reload returns to the base set.
- No new test infrastructure needed: Playwright contexts are isolated per test, so localStorage starts clean for each.

## 5. Unit Test Coverage for the Storage Module

- Tests live in a new `frontend/tests/unit/columnPickerStorage.test.ts` file.
- Use `vitest`'s built-in localStorage mock (jsdom provides `window.localStorage`); call `localStorage.clear()` in `beforeEach` to isolate tests within the file.
- Cover: read when empty → null; write then read → round-trips; unknown fields stripped on read; entry equal to base → null (no override); clear removes entry; other preset entries survive a clear.

---

### Notes

- `canonicalOrder` in `ScreenerBody` is already computed via `useMemo` — safe to read for the `knownFields` argument in the storage calls without adding a new memo.
- The `isModified` computation (`isColumnSetModified`) is unchanged — it compares `visibleColumns` against `activePreset.columns`, which is the right semantic (modified = differs from base, regardless of what's stored).
- The restored override that differs from base correctly shows the modified marker and enables Reset on reload — falls out naturally from the unchanged `isModified` logic once the seed reads from storage.
- No change needed in `ColumnsMenu`, `TickerTable`, `ViewBar`, or any other component.
- The AppShell `tad.theme` precedent covers the SSR guard, explicit-write-only pattern, and `typeof window` check — follow it exactly.
agentId: a7dc6b7558739a03b (use SendMessage with to: 'a7dc6b7558739a03b' to continue this agent) <usage>subagent_tokens: 34602 tool_uses: 8 duration_ms: 77320</usage>

---

<details><summary>Inner trace (subagent session agent-a7dc6b7558739a03b, depth 1)</summary>

## Main-Thread Message

Time: 2026-06-17T12:12:39.937Z

I'll read the task file and key source files before writing the plan.

---

## Bash Call

Time: 2026-06-17T12:12:40.767Z Description: Read task file

### Command

```text
cat ~/github/.worktrees/tad/083-persist-column-picker/tasks/083-persist-column-picker.md
```

### Output

```text
---
title: "Persist Column Picker Overrides Per Preset"
date: 2026-06-17
status: ready-for-dev
type: feat
---

## Persist Column Picker Overrides per Preset

The ticker-table column picker lets you toggle columns on top of the active preset, but those overrides are session-only React state — a page refresh throws them away and falls back to the preset's columns.

This task makes the overrides stick across reloads (and browser restarts) by persisting them in localStorage, keyed per preset, so each view remembers its own column set.

### Acceptance Criteria

- After toggling columns and reloading the page, the picker and table show the toggled set, not the preset's base set.
- Overrides are remembered per preset: customise view A, switch to view B, switch back — A still shows its saved columns. B keeps its own (saved or base).
- Reset immediately restores the active preset's base columns and clears its stored override — so a reload afterwards stays on the base set, not the discarded override.
- A stored override that references a column no longer in the schema falls back gracefully (unknown fields dropped; an empty or now-equal-to-preset result behaves as no override).
- The modified marker and Reset button reflect the restored set after reload (a restored override shows as modified).

### Notes

- Decision (locked): localStorage, not URL. Column visibility is a personal sticky preference, not shareable view state. URL was considered and rejected (reverses the deliberate "columns out of the URL" choice, bloats the URL).
- Semantics (locked): "each view remembers its own columns across reloads AND tab switches." This is a behaviour change — today a tab switch discards overrides (reseeds from the preset); after this, the reseed reads the stored override first.
- Per-preset keying is forced: column sets are preset-shaped and Reset is per-preset, so a single global key can't be coherent.
- Precedent to mirror: the theme toggle in AppShell already persists to localStorage (`tad.theme`) with a JS read + guarded fallback. Same pattern, same test/determinism constraints already solved.
- The current behaviour is pinned by an e2e test asserting overrides do NOT survive a reload — flip it.
- Determinism: Playwright contexts are isolated per test; jsdom shares localStorage within a file, so clear it between unit tests that exercise persistence.
```

---

## Bash Call

Time: 2026-06-17T12:12:44.167Z Description: Read ScreenerBody component

### Command

```text
cat ~/github/.worktrees/tad/083-persist-column-picker/frontend/src/routes/index.tsx
```

### Output

```text
import {
  createFileRoute,
  type SearchSchemaInput,
  stripSearchParams,
  useNavigate,
} from "@tanstack/react-router";
import { useMemo, useState } from "react";

import { AppShell } from "@/components/AppShell";
import { ColumnsMenu } from "@/components/ColumnsMenu";
import { MarketSummary } from "@/components/MarketSummary";
import { TickerTable } from "@/components/TickerTable";
import { ViewBar } from "@/components/ViewBar";
import { GROUPS, PRESETS, type PresetView, type TickerField } from "@/lib/columns";
import { DEFAULT_PAGE_SIZE, PAGE_SIZES } from "@/lib/pagination";
import {
  canonicalColumnOrder,
  DEFAULT_VIEW_ID,
  resolveActivePreset,
} from "@/lib/views";
import { isColumnSetModified } from "@/lib/visibleColumns";

// Screener route — full app shell wrapping the existing tables, restyled.
//
// The `?q` / `?page` / `?rows` search params are the single source of truth
// for the ticker table filter and pagination: validated here, read once
// below, threaded down as props. Siblings (the top-bar search box and the
// table) stay decoupled and the view is shareable/bookmarkable.

export const Route = createFileRoute("/")({
  // All four are optional on input (a bare "/" is valid) but always present
  // on output — defaulted here so `useSearch` returns the full set. The
  // optional input is what lets `stripSearchParams` below recognise them as
  // strippable defaults. Invalid deep links are coerced, not rejected: a
  // non-positive-integer `page` falls back to 1 (the upper clamp happens at
  // render, where the total is known), a `rows` value outside the allowed
  // set falls back to the 100 default. `view` stays a loose string here and is
  // coerced to Default in IndexComponent if it names no known preset (an
  // unknown id resolves to the Default preset). A non-string `view` defaults to
  // the stripped "default".
  validateSearch: (
    search: {
      q?: string;
      page?: number;
      rows?: number;
      view?: string;
    } & SearchSchemaInput,
  ): { q: string; page: number; rows: number; view: string } => ({
    q: typeof search.q === "string" ? search.q : "",
    page:
      Number.isInteger(search.page) && (search.page as number) >= 1
        ? (search.page as number)
        : 1,
    rows: (PAGE_SIZES as readonly number[]).includes(search.rows as number)
      ? (search.rows as number)
      : DEFAULT_PAGE_SIZE,
    view: typeof search.view === "string" ? search.view : DEFAULT_VIEW_ID,
  }),
  // Strip the defaults so a bare "/" stays clean — clearing the box, page 1,
  // 100 rows, and the Default view never serialise. Non-default values still do.
  search: {
    middlewares: [
      stripSearchParams({
        q: "",
        page: 1,
        rows: DEFAULT_PAGE_SIZE,
        view: DEFAULT_VIEW_ID,
      }),
    ],
  },
  component: IndexComponent,
});

function IndexComponent() {
  const { q, page, rows, view } = Route.useSearch();
  const navigate = useNavigate({ from: "/" });

  // History contract: discrete pagination actions push an entry apiece — the
  // footer steppers are router <Link>s, and a rows-per-page change pushes
  // here — so browser Back walks them. A view switch is a destination too, so
  // it pushes. Live search typing and the sort-driven page reset use `replace`:
  // refinements of the current view, not destinations (Back must not step
  // through keystrokes). Functional updaters preserve unrelated params either
  // way. Search, rows-per-page, and view changes restart at page 1 in the same
  // navigate call; the sort-driven reset lives in TickerTable, which owns the
  // sorting state and reseeds it from the new preset's default.
  function onQueryChange(next: string) {
    navigate({ search: (prev) => ({ ...prev, q: next, page: 1 }), replace: true });
  }

  // Sort reset only — stepper navigation lives in the footer's Links.
  function onPageChange(next: number) {
    navigate({ search: (prev) => ({ ...prev, page: next }), replace: true });
  }

  function onRowsChange(next: number) {
    navigate({ search: (prev) => ({ ...prev, rows: next, page: 1 }) });
  }

  // A tab switch is a destination (push, like a page step — Back walks view
  // changes) and resets to page 1. The table reseeds the sort from the new
  // preset on its own (see TickerTable), and the new preset-id reseeds the
  // session visible set in ScreenerBody — so picker overrides are discarded on a
  // tab switch with no extra logic. This only owns the view + page.
  function onViewChange(next: string) {
    navigate({ search: (prev) => ({ ...prev, view: next, page: 1 }) });
  }

  // Reset to page 1 — used by the picker's Reset (alongside the column + sort
  // restore that ScreenerBody owns).
  function onResetPage() {
    navigate({ search: (prev) => ({ ...prev, page: 1 }), replace: true });
  }

  // Presets and groups are frontend-owned (the IA constant), so the active
  // preset resolves synchronously — the body mounts directly (the tickers query
  // owns its own pending/error inside TickerTable). An unknown ?view id resolves
  // to the Default preset, which always exists.
  const activePreset = resolveActivePreset(PRESETS, view);

  return (
    <AppShell q={q} onQueryChange={onQueryChange}>
      <MarketSummary />
      {activePreset === null ? (
        <p className="px-4 py-3 text-sm text-loss-strong">Error</p>
      ) : (
        <ScreenerBody
          activePreset={activePreset}
          q={q}
          page={page}
          rows={rows}
          onPageChange={onPageChange}
          onRowsChange={onRowsChange}
          onViewChange={onViewChange}
          onResetPage={onResetPage}
        />
      )}
    </AppShell>
  );
}

// The screener body — owns the SESSION visible-column set: seeded from the
// active preset, mutated by the Columns picker, re-seeded whenever the active
// preset changes (a tab switch / fresh ?view), and restored on Reset. The set
// is session-only — never URL-encoded, so a reload restores the base ?view
// preset (the seed re-derives from `activePreset`).
function ScreenerBody({
  activePreset,
  q,
  page,
  rows,
  onPageChange,
  onRowsChange,
  onViewChange,
  onResetPage,
}: {
  activePreset: PresetView;
  q: string;
  page: number;
  rows: number;
  onPageChange: (page: number) => void;
  onRowsChange: (rows: number) => void;
  onViewChange: (id: string) => void;
  onResetPage: () => void;
}) {
  // The session visible-column set, seeded from the active preset.
  const [visibleColumns, setVisibleColumns] = useState<readonly TickerField[]>(
    activePreset.columns,
  );
  // A monotonic signal the table watches to reseed its sort on Reset (the
  // columns reset is `setVisibleColumns` below; sort lives in TickerTable).
  const [resetNonce, setResetNonce] = useState(0);

  // Re-seed the visible set the instant the active preset changes — synchronously
  // during render via the previous-id-in-state pattern (NOT a useEffect),
  // matching TickerTable's sort reseed. Both fire on `activePreset.id`, which is
  // exactly why a tab switch discards picker modifications with no extra logic.
  const [prevPresetId, setPrevPresetId] = useState(activePreset.id);
  if (prevPresetId !== activePreset.id) {
    setPrevPresetId(activePreset.id);
    setVisibleColumns(activePreset.columns);
  }

  // The picker's column universe + order: the canonical order (the widest
  // preset's columns). Per-field metadata comes from the IA constant, so the
  // picker renders fully on mount — no async metadata join.
  const canonicalOrder = useMemo(() => canonicalColumnOrder(PRESETS), []);

  const isModified = isColumnSetModified(visibleColumns, activePreset.columns);

  function onReset() {
    setVisibleColumns(activePreset.columns);
    setResetNonce((n) => n + 1);
    onResetPage();
  }

  return (
    <>
      <ViewBar
        presets={PRESETS}
        activeId={activePreset.id}
        onViewChange={onViewChange}
        modified={isModified}
        rightSlot={
          <ColumnsMenu
            columns={canonicalOrder}
            total={canonicalOrder.length}
            groups={GROUPS}
            visibleColumns={visibleColumns}
            onVisibleColumnsChange={setVisibleColumns}
            onReset={onReset}
            activePresetLabel={activePreset.label}
            isModified={isModified}
          />
        }
      />
      <TickerTable
        q={q}
        page={page}
        rows={rows}
        onPageChange={onPageChange}
        onRowsChange={onRowsChange}
        activePreset={activePreset}
        visibleColumns={visibleColumns}
        resetNonce={resetNonce}
        groups={GROUPS}
      />
    </>
  );
}
```

---

## Bash Call

Time: 2026-06-17T12:12:48.411Z Description: Read visibleColumns.ts, views.ts, AppShell localStorage precedent

### Command

```text
cat ~/github/.worktrees/tad/083-persist-column-picker/frontend/src/lib/visibleColumns.ts && echo "---" && cat ~/github/.worktrees/tad/083-persist-column-picker/frontend/src/lib/views.ts && echo "---" && cat ~/github/.worktrees/tad/083-persist-column-picker/frontend/src/components/AppShell.tsx | head -80
```

### Output

```text
// Visible-column-set machinery for the columns picker (079.03).
//
// The visible column set is session-local state seeded from the active preset.
// The picker mutates it via these pure helpers: a toggle-on inserts a field at
// its canonical position within its group; a toggle-off removes it. Kept
// framework-free so they're unit-testable without rendering the picker.
//
// "Modified" means the visible set differs from the preset's columns as an
// ORDERED sequence — order matters because a toggle-on inserts positionally.

// The helpers are generic over the field type — they stay decoupled from the
// generated `TickerField` enum yet preserve whatever string-literal type the
// caller passes (so a `TickerField[]` in yields a `TickerField[]` out).

/**
 * True when the visible set differs from the preset's column sequence — by
 * length OR element-wise. An equal-length reorder counts as modified.
 */
export function isColumnSetModified<T extends string>(
  visible: readonly T[],
  presetColumns: readonly T[],
): boolean {
  if (visible.length !== presetColumns.length) return true;
  return visible.some((field, i) => field !== presetColumns[i]);
}

/**
 * Toggle a column ON: insert `field` so its group's visible run stays in
 * canonical order. The insertion lands after the last visible column of the
 * same group that is canonically-earlier than `field` (so it follows the
 * group's last visible member in the common case), and before the first
 * canonically-later same-group member. When no column of the field's group is
 * visible, the field is appended. A no-op if `field` is already visible.
 *
 * `canonicalOrder` is the registry's canonical column order (the Everything
 * preset); `groupOf` maps a field to its group id.
 */
export function toggleColumnOn<T extends string>(
  visible: readonly T[],
  field: T,
  canonicalOrder: readonly T[],
  groupOf: (field: T) => string,
): T[] {
  if (visible.includes(field)) return [...visible];

  const group = groupOf(field);
  const canonicalIndex = (f: T) => canonicalOrder.indexOf(f);
  const fieldRank = canonicalIndex(field);

  // Insert after the last visible same-group column that is canonically before
  // `field`. That keeps the group run in canonical order and, when the field is
  // the group's new last member, lands right after the group's last visible
  // column (the spec's "after the last visible column of its group").
  let insertAt = -1;
  for (let i = 0; i < visible.length; i++) {
    if (groupOf(visible[i]) === group && canonicalIndex(visible[i]) < fieldRank) {
      insertAt = i;
    }
  }

  if (insertAt >= 0) {
    const next = [...visible];
    next.splice(insertAt + 1, 0, field);
    return next;
  }

  // No canonically-earlier same-group member is visible. If a LATER same-group
  // member is visible, slot in just before it (keeps the run ordered); else the
  // group has no visible member → append per the contract.
  const laterSameGroup = visible.findIndex(
    (f) => groupOf(f) === group && canonicalIndex(f) > fieldRank,
  );
  if (laterSameGroup >= 0) {
    const next = [...visible];
    next.splice(laterSameGroup, 0, field);
    return next;
  }
  return [...visible, field];
}

/** Toggle a column OFF: remove `field`. A no-op if it isn't visible. */
export function toggleColumnOff<T extends string>(
  visible: readonly T[],
  field: T,
): T[] {
  return visible.filter((f) => f !== field);
}

/**
 * Bulk-toggle a whole group. `members` are the group's TOGGLEABLE fields (the
 * caller excludes the locked Ticker). When every member is already visible the
 * group turns fully off (all removed); otherwise (none or partial) it turns
 * fully on — each missing member inserted at its canonical position, so the run
 * lands in canonical order.
 */
export function toggleGroup<T extends string>(
  visible: readonly T[],
  members: readonly T[],
  canonicalOrder: readonly T[],
  groupOf: (field: T) => string,
): T[] {
  const allOn = members.every((m) => visible.includes(m));
  if (allOn) {
    const drop = new Set(members);
    return visible.filter((f) => !drop.has(f));
  }
  let next = [...visible];
  for (const m of members) {
    next = toggleColumnOn(next, m, canonicalOrder, groupOf);
  }
  return next;
}
---
// Screener view registry — pure logic for the preset/group machinery.
//
// Presets and groups are owned by the frontend IA constant (`lib/columns.ts`):
// a preset carries the ordered visible-column set, the default sort, and an
// optional derivation chain; groups carry the band labels. This module holds the
// framework-free helpers the view bar and group band build on — kept here so
// they're unit-testable without rendering the table.

import type { PresetView } from "@/lib/columns";

// The literal preset id that maps to a bare URL — the stripped `?view` default.
export const DEFAULT_VIEW_ID = "default";

/**
 * A contiguous run of columns sharing one group, over the *visible* column set.
 * Drives the band's `colspan` cells and the seam markers. `firstIndex` is the
 * position of the run's first column in the visible-column array.
 */
export type GroupRun = {
  group: string;
  span: number;
  firstIndex: number;
};

/** The minimal per-column shape the band logic reads: field id + its group. */
export type GroupedColumn = { field: string; group: string };

/**
 * Walk the ordered visible columns, coalescing each maximal contiguous block of
 * the same group into one run. A group that recurs non-contiguously yields
 * separate runs (the band must not span across a gap).
 */
export function groupRuns(columns: readonly GroupedColumn[]): GroupRun[] {
  const runs: GroupRun[] = [];
  let i = 0;
  while (i < columns.length) {
    const group = columns[i].group;
    let span = 1;
    while (i + span < columns.length && columns[i + span].group === group) span++;
    runs.push({ group, span, firstIndex: i });
    i += span;
  }
  return runs;
}

/**
 * The fields that carry a group seam — a `--border-strong` left border running
 * continuously through the band, header, and body. The seam sits on the first
 * column of every run except the leading run (the identity span, also the
 * table's outer edge — no seam there, none inside a group, none at the edges).
 * Chain views suppress every seam (the rail must not chop the lineage).
 */
export function seamFields(
  runs: readonly GroupRun[],
  columns: readonly GroupedColumn[],
  isChain: boolean,
): Set<string> {
  const seams = new Set<string>();
  if (isChain) return seams;
  runs.forEach((run, runIndex) => {
    if (runIndex > 0) seams.add(columns[run.firstIndex].field);
  });
  return seams;
}

/**
 * The full-column preset — the one spanning the most columns (the "Everything"
 * view). Identified structurally, not by id, so the IA constant stays the single
 * source. On a tie the first preset reaching the maximum wins (deterministic);
 * null only for an empty preset list. This is the single definition of "the
 * full-column preset": canonical column order, the picker's universe size, and
 * the view bar's column-count badge all derive from it — no open-coded width
 * scans elsewhere.
 */
export function widestPreset(presets: readonly PresetView[]): PresetView | null {
  let widest: PresetView | null = null;
  for (const p of presets) {
    if (widest === null || p.columns.length > widest.columns.length) widest = p;
  }
  return widest;
}

/**
 * The canonical column universe + order — the full-column preset's `columns`.
 * The Columns picker draws its universe and ordering from this; `total` (the
 * shown/total denominator) is its length. Empty for an empty preset list.
 */
export function canonicalColumnOrder(
  presets: readonly PresetView[],
): PresetView["columns"] {
  return widestPreset(presets)?.columns ?? [];
}

/**
 * Resolve the active preset for a (possibly unknown) `?view` id. An unknown id
 * — or the literal default id — resolves to the `default` preset. Returns null
 * only if there is no default preset (a contract violation the caller surfaces
 * as an error rather than guessing).
 */
export function resolveActivePreset(
  presets: readonly PresetView[],
  viewId: string,
): PresetView | null {
  const exact = presets.find((p) => p.id === viewId);
  if (exact && viewId !== DEFAULT_VIEW_ID) return exact;
  return presets.find((p) => p.id === DEFAULT_VIEW_ID) ?? null;
}
---
import { type ReactNode, useCallback, useEffect, useRef, useState } from "react";

import { SharedTooltip } from "@/components/SharedTooltip";
import { ShortcutsDialog } from "@/components/ShortcutsDialog";
import { Sidebar } from "@/components/Sidebar";
import { TopBar } from "@/components/TopBar";
import { useGlobalShortcuts } from "@/hooks/useGlobalShortcuts";

// Top-level shell: top bar + left sidebar + canvas slot.
//
// Owns the light/dark theme toggle. Reads an initial preference from the
// `theme` query param if present (`?theme=dark`) — useful for
// screenshot/Storybook links — falling back to localStorage, then the
// OS-level preference. Only an explicit toggle persists to localStorage:
// opening a `?theme=` link or following the OS preference must not
// overwrite a saved choice. The same precedence runs pre-paint in
// index.html (FOUC guard) — keep the two in sync.
//
// Also owns the global keyboard shortcuts: the once-mounted keydown
// dispatcher (useGlobalShortcuts), the shortcuts dialog and its open state,
// and the filter-input ref the focus-filter action drives.

type Props = {
  children: ReactNode;
  q: string;
  onQueryChange: (next: string) => void;
};

const STORAGE_KEY = "tad.theme";

function readInitialTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "light";
  const q = new URLSearchParams(window.location.search).get("theme");
  if (q === "dark" || q === "light") return q;
  const saved = window.localStorage.getItem(STORAGE_KEY);
  if (saved === "dark" || saved === "light") return saved;
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function focusAndSelect(input: HTMLInputElement | null) {
  // Select the existing text so typing replaces it — for both ⌘K and "/".
  input?.focus();
  input?.select();
}

export function AppShell({ children, q, onQueryChange }: Props) {
  const [theme, setTheme] = useState<"light" | "dark">(readInitialTheme);
  const [shortcutsOpen, setShortcutsOpen] = useState(false);
  const searchInputRef = useRef<HTMLInputElement | null>(null);
  // ⌘K with the shortcuts dialog open closes it and then focuses the filter.
  // The dialog's default close behaviour would restore focus to the
  // pre-open element, so this flag redirects its finalFocus to the input.
  const closingForFilter = useRef(false);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.toggle("dark", theme === "dark");
    root.dataset.theme = theme;
  }, [theme]);

  function toggle() {
    const next = theme === "light" ? "dark" : "light";
    window.localStorage.setItem(STORAGE_KEY, next);
    setTheme(next);
  }

  const focusFilter = useCallback(() => {
    if (shortcutsOpen) {
      closingForFilter.current = true;
      setShortcutsOpen(false);
      return;
    }
    focusAndSelect(searchInputRef.current);
  }, [shortcutsOpen]);

  const toggleShortcutsDialog = useCallback(() => setShortcutsOpen((o) => !o), []);

  useGlobalShortcuts({
    shortcutsDialogOpen: shortcutsOpen,
    toggleShortcutsDialog,
```

---

## Bash Call

Time: 2026-06-17T12:12:52.254Z Description: Find the pinned reload test in e2e spec

### Command

```text
cat ~/github/.worktrees/tad/083-persist-column-picker/frontend/tests/e2e/columns-picker.spec.ts | grep -n "reload\|persist\|surviv\|localStorage" | head -30
```

### Output

```text
96:test("the picker closes on Escape and overrides do not survive a reload", async ({
110:  // Session-only: a reload restores the base ?view (no Open, no override in URL).
111:  await page.reload();
```

---

## Bash Call

Time: 2026-06-17T12:12:55.255Z Description: Read the test to flip

### Command

```text
sed -n '90,135p' ~/github/.worktrees/tad/083-persist-column-picker/frontend/tests/e2e/columns-picker.spec.ts
```

### Output

```text
  await expect(page.getByRole("columnheader", { name: "Ret 5d (z)" })).toHaveCount(0);
  await expect(
    page.locator("thead th[aria-sort='descending'], thead th[aria-sort='ascending']"),
  ).toHaveCount(0);
});

test("the picker closes on Escape and overrides do not survive a reload", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();

  await columnsButton(page).click();
  await page.getByRole("checkbox", { name: "Open" }).click();
  await expect(page.getByRole("columnheader", { name: "Open" })).toBeVisible();

  // Esc closes the popover (the find field is gone from the DOM).
  await page.keyboard.press("Escape");
  await expect(page.getByRole("searchbox", { name: /find a column/i })).toHaveCount(0);

  // Session-only: a reload restores the base ?view (no Open, no override in URL).
  await page.reload();
  await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();
  await expect(page.getByRole("columnheader", { name: "Open" })).toHaveCount(0);
  await expect(page).toHaveURL((url) => !url.search.includes("view"));
});
```

---

## Bash Call

Time: 2026-06-17T12:12:58.232Z Description: Check for any existing localStorage or reset test patterns

### Command

```text
grep -n "localStorage\|storageState\|resetNonce\|onReset\|isModified\|modified" ~/github/.worktrees/tad/083-persist-column-picker/frontend/tests/e2e/columns-picker.spec.ts | head -20
```

### Output

```text
5:// active tab modified and enables a footer Reset; hiding the sorted column
28:test("toggling a column on marks the tab modified, shows it, and updates the count", async ({
43:  // The active tab gains the modified marker (its accessible name carries it).
44:  await expect(page.getByRole("tab", { name: /Default — modified/i })).toBeVisible();
47:test("Reset restores the preset's columns and sort, clearing the modified marker", async ({
64:  // Back to the Default column set + sort, modified marker gone.
67:  await expect(page.getByRole("tab", { name: /Default — modified/i })).toHaveCount(0);
```

---

## Bash Call

Time: 2026-06-17T12:13:16.225Z Description: Check unit test for relevant patterns

### Command

```text
cat ~/github/.worktrees/tad/083-persist-column-picker/frontend/tests/unit/TickerTable.test.tsx | grep -n "localStorage\|visibleColumns\|persist" | head -20
```

### Output

```text
180:    const visibleColumns = p.visibleColumns ?? activePreset.columns;
193:          visibleColumns={visibleColumns}
1031:      visibleColumns: cols,
1044:    view.update({ visibleColumns: ["ticker", "name"] });
1107:      visibleColumns: ["ticker", "name", "ret_21d"],
```

---

## Bash Call

Time: 2026-06-17T12:13:19.614Z Description: Skim columns.ts for TickerField and PRESETS shape

### Command

```text
grep -n "TickerField\|PRESETS\|columns" ~/github/.worktrees/tad/083-persist-column-picker/frontend/src/lib/columns.ts | head -40
```

### Output

```text
2:// ticker columns are labelled, grouped, role-tagged, rendered, ordered, and
11://             width, sticky). Keyed off TickerField (the snapshot's field set) so
16://   PRESETS — the curated views: ordered columns, default sort, optional
31:export type TickerField = keyof TickerSnapshot;
33:// A feature's pipeline role. Identity columns (ticker/name/gics_sector) carry no
110:  /** Pipeline role; `null` for identity columns. */
132:  column: TickerField;
142:  steps: TickerField[];
143:  terminus: TickerField;
146:// A curated screener view: ordered columns, a default sort, and an optional
151:  columns: TickerField[];
156:// Per-column definitions. Keyed off TickerField so adding a snapshot column
157:// without its definition is a compile error. Identity columns (ticker / name /
160:export const COLUMNS: Record<TickerField, ColumnConfig> = {
417:// the Everything preset's columns. A unit test asserts this matches
434:const CANONICAL_COLUMNS: TickerField[] = [
476:export const PRESETS: readonly PresetView[] = [
480:    columns: [
499:    columns: [
532:    columns: [
549:    columns: [
566:    columns: [
580:    columns: CANONICAL_COLUMNS,
609:export const TICKER_COLUMNS: Record<TickerField, ColumnSpec> = Object.fromEntries(
621:) as Record<TickerField, ColumnSpec>;
```

---

## Main-Thread Message

Time: 2026-06-17T12:13:54.421Z

Now I have everything I need. Here is the plan:

---

## Implementation Plan

### TLDR

Add a thin, framework-free `columnPickerStorage` module (mirroring `visibleColumns.ts`) that reads and writes a single `tad.columnOverrides` localStorage key holding a `Record<presetId, TickerField[]>` map. Thread it into the three mutation sites in `ScreenerBody` (initial seed, prev-id reseed, reset) and flip the one e2e test that currently pins the old behaviour.

---

### Steps

**1. New storage module (`frontend/src/lib/columnPickerStorage.ts`)**

- Key: single string `tad.columnOverrides`, value shape: `Record<string, string[]>` (the full map, one entry per preset id).
- A single-key map is the right choice over per-preset keys: it's one atomic read on init, one atomic write on every mutation, trivially cleared in tests, and naturally handles presets being added/removed without key-soup proliferation. The only tradeoff (one large JSON blob) is irrelevant at a few dozen columns × ~6 presets.
- Export three pure functions (all guarded with `typeof window === "undefined"` to survive SSR/test environments that lack `window`):
  - `readOverride(presetId, baseColumns, knownFields)` → reads the map, finds the entry for `presetId`, drops unknown fields (i.e. fields not in `knownFields`), returns `null` if the entry is absent, empty after filtering, or equals `baseColumns` element-wise (no override to apply).
  - `writeOverride(presetId, columns, baseColumns)` → if `columns` equals `baseColumns` element-wise, call `clearOverride` instead (no redundant entry); otherwise upsert the entry and `setItem` the whole map.
  - `clearOverride(presetId)` → reads the map, deletes the key for `presetId`, and `setItem` the updated map (or removes the key entirely if the map is now empty, as a micro-hygiene).
- No React import; no side effects at module load time.

**2. Seed and reseed in `ScreenerBody`**

- `knownFields` is derived from `canonicalColumnOrder(PRESETS)` — already computed in `ScreenerBody` as `canonicalOrder`. Pass it to `readOverride`.
- Initial `useState` seed: replace `activePreset.columns` with `readOverride(activePreset.id, activePreset.columns, canonicalOrder) ?? activePreset.columns`.
- Prev-id-in-state reseed block (the synchronous render-time branch): replace `setVisibleColumns(activePreset.columns)` with `setVisibleColumns(readOverride(activePreset.id, nextPreset.columns, canonicalOrder) ?? nextPreset.columns)`. This preserves the synchronous reseed — no useEffect introduced.
- Every `setVisibleColumns` call that comes from `onVisibleColumnsChange` (the picker toggle path, wired through `ColumnsMenu`) must also write storage. The cleanest place: wrap `setVisibleColumns` in `ScreenerBody` with a one-liner that calls `writeOverride` and then `setVisibleColumns`. The `ColumnsMenu`'s `onVisibleColumnsChange` prop already points at `setVisibleColumns` — redirect it to the wrapper.

## 3. Reset Clears Stored Override

- In `onReset`, call `clearOverride(activePreset.id)` before (or alongside) `setVisibleColumns(activePreset.columns)`. Order doesn't matter; both are synchronous.

## 4. Flip the E2e Test

- The test at ~line 96 (`"the picker closes on Escape and overrides do not survive a reload"`) must become two separate tests:
  - One testing only the Escape-closes-picker behaviour (keep the Esc assertion; drop the reload and column-absence assertions).
  - One new test asserting that toggling a column on, reloading, and switching views all persist/restore correctly — verifying: (a) toggled column survives reload, (b) switching to another view and back restores the saved override for the original view, (c) Reset clears it so a subsequent reload returns to the base set.
- No new test infrastructure needed: Playwright contexts are isolated per test, so localStorage starts clean for each.

## 5. Unit Test Coverage for the Storage Module

- Tests live in a new `frontend/tests/unit/columnPickerStorage.test.ts` file.
- Use `vitest`'s built-in localStorage mock (jsdom provides `window.localStorage`); call `localStorage.clear()` in `beforeEach` to isolate tests within the file.
- Cover: read when empty → null; write then read → round-trips; unknown fields stripped on read; entry equal to base → null (no override); clear removes entry; other preset entries survive a clear.

---

### Notes

- `canonicalOrder` in `ScreenerBody` is already computed via `useMemo` — safe to read for the `knownFields` argument in the storage calls without adding a new memo.
- The `isModified` computation (`isColumnSetModified`) is unchanged — it compares `visibleColumns` against `activePreset.columns`, which is the right semantic (modified = differs from base, regardless of what's stored).
- The restored override that differs from base correctly shows the modified marker and enables Reset on reload — falls out naturally from the unchanged `isModified` logic once the seed reads from storage.
- No change needed in `ColumnsMenu`, `TickerTable`, `ViewBar`, or any other component.
- The AppShell `tad.theme` precedent covers the SSR guard, explicit-write-only pattern, and `typeof window` check — follow it exactly.

---

</details>

## Main-Thread Message

Time: 2026-06-17T12:14:08.165Z

Both plans converge strongly. Synthesising into a single locked plan and writing it to the task file.

---

## Main-Thread Message

Time: 2026-06-17T12:14:46.125Z

Plan written to the task file. Both planners converged; key locked decisions: single `tad.columns` key holding a `{presetId: columns[]}` map, a framework-free persistence module owning all validation (drop-unknown + equal-to-base⇒no-override), and routing the three `ScreenerBody` seed/mutate/reset sites through it.

Now Step 4: Implement. Let me read the impl-task skill to brief the implementer accurately.

---

## Main-Thread Message

Time: 2026-06-17T12:14:48.521Z

Now spawning the Opus implementer.

---

## Subagent 3: Implement Task 083 [General-Purpose]

Time: 2026-06-17T12:15:13.962Z

### Prompt

Implement TAD task 083 by executing its implementation plan, following the `/impl-task` skill (inlined below). You are running inside a git worktree — ALL file paths must root at the worktree.

WORKTREE ROOT (cd here first; every Read/Edit/Write path must start with this): ~/github/.worktrees/tad/083-persist-column-picker TASK FILE: tasks/083-persist-column-picker.md (read it fully — it contains the Acceptance Criteria AND the locked Implementation Plan).

=== BEGIN impl-task SKILL.md ===

## Goal

Implement a task by executing its implementation plan.

## Guidance (DO NOT IGNORE!)

- Commit early and often.
- Include `(task/NNN)` in the commit subject.
- Look for and internalise existing style, patterns, conventions. Don't deviate unless the plan explicitly asks for it.
- Maintain the testing pyramid. Test at the lowest possible level. Few, mostly happy-path tests at the top of the pyramid (e2e, component).
- Do not use I/O, randomness, or real date/time in unit tests.
- Take small steps when uncertain; bigger steps when confident. An unexpected red means shift down. An unexpected green means review your test for gaps.

## Step 1: Task Readiness

Update the task status: `just task-status tasks/083-persist-column-picker.md in-dev`.

## Step 2: Build Context

Read the task and the code the plan will touch. Err on the side of reading too much.

## Step 3: Implement

Work through the plan step by step. Re-read the plan before each step. Use `/tdd` discipline (inlined below): do NOT write or modify production code without a failing test first (red → green → refactor).

- If a plan step seems wrong/missing, resolve it and note it in `## Implementation notes`.
- If tests keep failing after 3 attempts, revert to last green and take a smaller step.

## Step 4: Self-Review

Review `git diff` from your first commit to HEAD: diff touches only what the plan requires; each AC is demonstrably met; no leftovers (debug prints, TODOs, commented-out/obsolete code).

## Step 5: Wrap Up

Add an `## Implementation notes` section to the END of the task file (plain English): deviations from plan, surprises, learnings, non-obvious assumptions, follow-ups. Commit the task update. === END impl-task SKILL.md ===

=== /tdd discipline (Beck-style) === Red: write the smallest failing test that expresses the next increment of behaviour. Green: smallest code to pass. Refactor: clean up with tests green. Never write production code without a failing test demanding it.

PROJECT CONVENTIONS (CLAUDE.md — load-bearing):

- Frontend numbers via `frontend/src/lib/format.ts` (en-US pinned) — not relevant here but don't introduce bare locale.
- Commit with `just commit "<subject incl. (task/083)>" <files>`. The recipe pulls, stages the LISTED files, and commits — but it stages whatever is currently staged too, so do NOT pre-stage anything; pass only the files you intend per logical commit. Pass subject+body as ONE quoted multi-line arg, then the file list. When invoking from the shell, SINGLE-quote the message so $()/backticks stay literal.
- One commit per logical change.
- Markdown: title-case headings (MD063), soft-wrap (one line per paragraph), aligned table pipes, no emphasis-as-heading. The task file plan/notes you write must comply.
- Run frontend checks as you go. To validate the full suite at the end run `just check-all` from the worktree (it draws random free ports, safe in parallel). Do NOT skip it.

KEY POINTERS (verify by reading):

- `frontend/src/routes/index.tsx` — `ScreenerBody` owns the session visible-column set. The three sites to change: lazy `useState` initial seed, the synchronous `prevPresetId !== activePreset.id` reseed block (keep it synchronous, NOT useEffect), and `onReset`. Plus wrap the `onVisibleColumnsChange` prop passed to `ColumnsMenu` to persist.
- `frontend/src/lib/visibleColumns.ts` — the style to mirror for the new framework-free persistence module (generic over field type, unit-testable).
- `frontend/src/components/AppShell.tsx` — the localStorage precedent (`tad.theme`, `typeof window === "undefined"` guard, explicit-write-only). Mirror it.
- `frontend/src/lib/views.ts` — `canonicalColumnOrder(PRESETS)` is the valid-field universe; it's already memoised as `canonicalOrder` in `ScreenerBody`.
- `frontend/tests/e2e/columns-picker.spec.ts` (~line 96) — the test pinning "overrides do not survive a reload"; flip it per the plan.
- Unit tests live in `frontend/tests/unit/`; mirror an existing one (e.g. visibleColumns test) for structure. jsdom shares localStorage within a file — clear it in beforeEach.

Locked contract (from the plan): single key `tad.columns` holding `{ [presetId]: string[] }`; order-significant arrays; validation drops unknown fields; empty-or-equal-to-base ⇒ no override (resolve returns base, persist deletes rather than writes redundant); reads SSR/corruption-safe, writes guarded.

Execute the full plan, commit in logical increments (each with `(task/083)`), run `just check-all` until green, write Implementation notes, and commit the task update. Then report back: a summary of what you implemented, the commits you made (hashes + subjects), the final `just check-all` result, and anything you flagged or deviated on.

### Response

Clean working tree, status `in-dev` (correct for impl-task; ship-task moves it to done). Task 083 is fully implemented.

## Summary

Implemented TAD task 083 — column picker overrides now persist per preset across reloads and tab switches via localStorage.

What was built:

- New framework-free module `frontend/src/lib/columnOverrides.ts` (`resolveColumnOverride` / `persistColumnOverride` / `clearColumnOverride`) owning the single `tad.columns` key holding a `{ [presetId]: field[] }` map. It is the one home for the "equal-to-base or empty ⇒ no override" invariant (resolve returns base for a degenerate set; persist deletes rather than writes redundant). Reads are SSR/corruption-safe; writes swallow quota/availability failures. TDD'd with 14 unit tests.
- Wired `ScreenerBody` in `frontend/src/routes/index.tsx`: lazy seed and the synchronous reseed-on-tab-switch block both resolve via the module; a new `onVisibleColumnsChange` wrapper persists every picker mutation; `onReset` clears the stored entry. `canonicalOrder` moved above state to serve as the valid-field universe. `isModified` is unchanged and now reads true after reload for free.
- Flipped the e2e: the old "overrides do not survive a reload" test became a focused Escape-close test plus three persistence tests (reload restores override + modified marker; per-preset memory across Default→Returns→Default; Reset clears so reload returns to base).

Commits (newest first):

- `5c0cee0` Add task 083 implementation notes (task/083)
- `2d16654` Persist column picker overrides per preset in ScreenerBody (task/083)
- `ad55e28` Add per-preset column-override persistence module (task/083)

`just check-all`: green end-to-end (backend, openapi-drift, frontend-check incl. 61 e2e, workflow-lint, markdown).

Deviations / flags:

- Plan assumed jsdom `localStorage.clear()` works in unit tests, but this repo's vitest env is happy-dom whose `window.localStorage` exposes no working methods (no prior test used it). The unit test installs a minimal in-memory `Storage` stub in `beforeEach` — deterministic, no real I/O. Production guards are unchanged.
- `ColumnsMenu`'s prop is `(next: TickerField[]) => void` (mutable), so the wrapper takes a mutable array, not `readonly`.
- One transient first-run e2e failure (dev-server warmup losing the AAPL row); reliably green on warm runs and under full check-all.
- Status left at `in-dev` (ship-task will move it to `done`).

All work is committed on branch `task/083-persist-column-picker` in the worktree; nothing pushed. agentId: ab80ba36312f15776 (use SendMessage with to: 'ab80ba36312f15776' to continue this agent) <usage>subagent_tokens: 99863 tool_uses: 56 duration_ms: 444656</usage>

---

<details><summary>Inner trace (subagent session agent-ab80ba36312f15776, depth 1)</summary>

## Main-Thread Message

Time: 2026-06-17T12:15:16.188Z

I'll start by reading the task file fully to understand the acceptance criteria and implementation plan.

---

## Bash Call

Time: 2026-06-17T12:15:17.524Z Description: Verify worktree path and git state

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && pwd && git status && git log --oneline -3
```

### Output

```text
~/github/.worktrees/tad/083-persist-column-picker
On branch task/083-persist-column-picker
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   tasks/083-persist-column-picker.md

no changes added to commit (use "git add" and/or "git commit -a")
df77f86 Add task 083: persist column picker overrides per preset (task/083)
4e96000 Reclassify columns: features vs signals, split liquidity/turnover groups
ccefbea Fix turnover denominator double-counting share classes (task/082)
```

---

## Main-Thread Message

Time: 2026-06-17T12:15:19.743Z

Now let me read the key files mentioned in the plan.

---

## Main-Thread Message

Time: 2026-06-17T12:15:26.256Z

Now let me read the views.ts, the columns lib for TickerField, an existing unit test for structure, and the e2e test to flip.

---

## Main-Thread Message

Time: 2026-06-17T12:15:30.076Z

Let me look at the columns.ts to understand TickerField and presets, and find an existing unit test to mirror.

---

## Bash Call

Time: 2026-06-17T12:15:31.984Z Description: List unit tests and find preset ids

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && ls frontend/tests/unit/ && echo "---PRESETS---" && grep -n "id:" frontend/src/lib/columns.ts | head -30
```

### Output

```text
BoolBadge.test.tsx
Checkbox.test.tsx
columns.test.ts
ColumnsMenu.test.tsx
format.test.ts
GroupBand.test.tsx
HeaderInfoCard.test.tsx
LoadStatus.test.tsx
MarketSummary.test.tsx
PercentCell.test.tsx
routerContext.tsx
setup.ts
shortcuts.test.ts
ShortcutsDialog.test.tsx
TablePagination.test.tsx
tickerMatchesQuery.test.ts
TickerTable.test.tsx
ViewBar.test.tsx
views.test.ts
visibleColumns.test.ts
ZScoreCell.test.tsx
---PRESETS---
121:  id: string;
149:  id: string;
420:  { id: "identity", label: "Identity", bandShort: "" },
421:  { id: "price_volume", label: "Price & Volume", bandShort: "Price" },
422:  { id: "returns", label: "Returns", bandShort: "Returns" },
423:  { id: "earnings", label: "Earnings", bandShort: "Earnings" },
424:  { id: "sector_relative", label: "Sector-relative", bandShort: "Sector" },
425:  { id: "signals", label: "Signals", bandShort: "Signals" },
426:  { id: "liquidity", label: "Liquidity", bandShort: "Liquidity" },
427:  { id: "turnover", label: "Turnover", bandShort: "Turnover" },
478:    id: "default",
497:    id: "reversal",
530:    id: "liquidity",
547:    id: "returns",
564:    id: "earnings",
578:    id: "everything",
```

---

## Main-Thread Message

Time: 2026-06-17T12:15:34.349Z

Now I have enough context. Let me update the task status, then start TDD. First the status update.

---

## Bash Call

Time: 2026-06-17T12:15:35.243Z Description: Set task status to in-dev

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just task-status tasks/083-persist-column-picker.md in-dev
```

### Output

```text
Updated 083-persist-column-picker.md → in-dev
```

---

## Main-Thread Message

Time: 2026-06-17T12:15:37.595Z

Now let me check the columns.ts default preset columns count (e2e says "11/28") to confirm counts in this worktree.

---

## Main-Thread Message

Time: 2026-06-17T12:15:41.149Z

Default has 11 columns, confirmed. Now let me write the persistence module test first (TDD red). Let me create the unit test for the new module.

---

## Bash Call

Time: 2026-06-17T12:16:01.437Z Description: Run new test (expect red - module missing)

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run vitest run tests/unit/columnOverrides.test.ts 2>&1 | tail -20
```

### Output

```text
     |                                                                                     ^
  3  |  // The persistence module owns the `tad.columns` localStorage contract: one key
  4  |  // holding a `{ [presetId]: field[] }` map. The "equal-to-base or empty ⇒ no
 ❯ TransformPluginContext._formatLog node_modules/vite/dist/node/chunks/node.js:30602:39
 ❯ TransformPluginContext.error node_modules/vite/dist/node/chunks/node.js:30599:14
 ❯ normalizeUrl node_modules/vite/dist/node/chunks/node.js:27842:18
 ❯ node_modules/vite/dist/node/chunks/node.js:27905:30
 ❯ TransformPluginContext.transform node_modules/vite/dist/node/chunks/node.js:27873:4
 ❯ EnvironmentPluginContainer.transform node_modules/vite/dist/node/chunks/node.js:30387:14
 ❯ loadAndTransform node_modules/vite/dist/node/chunks/node.js:24646:26

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed (1)
      Tests  no tests
   Start at  14:16:03
   Duration  555ms (transform 12ms, setup 80ms, import 0ms, tests 0ms, environment 296ms)

error: "vitest" exited with code 1
```

---

## Main-Thread Message

Time: 2026-06-17T12:16:05.945Z

Red as expected (module doesn't exist). Now create the module.

---

## Main-Thread Message

Time: 2026-06-17T12:16:24.144Z

I accidentally left in some confused shim code. Let me clean up `persistColumnOverride` and remove the dead probe helper.

---

## Bash Call

Time: 2026-06-17T12:16:32.623Z Description: Run new test (expect green)

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run vitest run tests/unit/columnOverrides.test.ts 2>&1 | tail -15
```

### Output

```text
     19| beforeEach(() => {
     20|   window.localStorage.clear();
       |                       ^
     21| });
     22|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/14]⎯


 Test Files  1 failed (1)
      Tests  14 failed (14)
   Start at  14:16:33
   Duration  478ms (transform 32ms, setup 63ms, import 26ms, tests 5ms, environment 211ms)

error: "vitest" exited with code 1
```

---

## Main-Thread Message

Time: 2026-06-17T12:16:36.909Z

`window.localStorage` is undefined — the test environment for this file isn't jsdom. Let me check the vitest config/setup.

---

## Bash Call

Time: 2026-06-17T12:16:37.706Z Description: Check vitest test environment config

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && cat vitest.config.ts 2>/dev/null; cat vite.config.ts 2>/dev/null | grep -A15 "test:"; echo "---SETUP---"; cat tests/unit/setup.ts
```

### Output

```text
  test: {
    environment: "happy-dom",
    globals: true,
    setupFiles: ["./tests/unit/setup.ts"],
    include: ["tests/unit/**/*.test.ts", "tests/unit/**/*.test.tsx"],
  },
});
---SETUP---
import "@testing-library/jest-dom/vitest";
```

---

## Main-Thread Message

Time: 2026-06-17T12:16:39.959Z

happy-dom is the environment. The error must be something else. Let me see the full error.

---

## Bash Call

Time: 2026-06-17T12:16:40.886Z Description: Show error detail

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run vitest run tests/unit/columnOverrides.test.ts 2>&1 | grep -A8 "FAIL\|TypeError\|Error:" | head -30
```

### Output

```text
 FAIL  tests/unit/columnOverrides.test.ts > resolveColumnOverride > returns the base set when no override is stored
 FAIL  tests/unit/columnOverrides.test.ts > resolveColumnOverride > returns a validated stored override, preserving its order
 FAIL  tests/unit/columnOverrides.test.ts > resolveColumnOverride > drops unknown fields, preserving stored order
 FAIL  tests/unit/columnOverrides.test.ts > resolveColumnOverride > returns base when the stored override is empty after filtering
 FAIL  tests/unit/columnOverrides.test.ts > resolveColumnOverride > returns base when the stored override equals the base set
 FAIL  tests/unit/columnOverrides.test.ts > resolveColumnOverride > keys overrides per preset
 FAIL  tests/unit/columnOverrides.test.ts > resolveColumnOverride > treats a corrupt blob as no override
 FAIL  tests/unit/columnOverrides.test.ts > resolveColumnOverride > treats a non-array entry as no override
 FAIL  tests/unit/columnOverrides.test.ts > persistColumnOverride > stores an override that differs from the base
 FAIL  tests/unit/columnOverrides.test.ts > persistColumnOverride > deletes rather than writes an entry equal to the base
 FAIL  tests/unit/columnOverrides.test.ts > persistColumnOverride > preserves other presets' overrides when writing one
 FAIL  tests/unit/columnOverrides.test.ts > clearColumnOverride > removes a preset's stored override
 FAIL  tests/unit/columnOverrides.test.ts > clearColumnOverride > leaves other presets' overrides intact
 FAIL  tests/unit/columnOverrides.test.ts > clearColumnOverride > is a no-op when nothing is stored
TypeError: window.localStorage.clear is not a function
 ❯ tests/unit/columnOverrides.test.ts:20:23
     18| // jsdom shares localStorage within a file — clear it between persiste…
     19| beforeEach(() => {
     20|   window.localStorage.clear();
       |                       ^
     21| });
     22|
```

---

## Main-Thread Message

Time: 2026-06-17T12:16:44.150Z

happy-dom's localStorage may not implement `.clear()`. Let me check how other tests handle localStorage, e.g. AppShell theme tests.

---

## Bash Call

Time: 2026-06-17T12:16:45.234Z Description: Find localStorage usage in tests

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && grep -rn "localStorage" tests/ src/ | grep -i "clear\|removeItem\|setItem\|getItem" | head
```

### Output

```text
tests/unit/columnOverrides.test.ts:18:// jsdom shares localStorage within a file — clear it between persistence tests.
tests/unit/columnOverrides.test.ts:20:  window.localStorage.clear();
tests/unit/columnOverrides.test.ts:38:    window.localStorage.setItem(
tests/unit/columnOverrides.test.ts:46:    window.localStorage.setItem(
tests/unit/columnOverrides.test.ts:54:    window.localStorage.setItem(
tests/unit/columnOverrides.test.ts:67:    window.localStorage.setItem("tad.columns", "{not json");
tests/unit/columnOverrides.test.ts:72:    window.localStorage.setItem("tad.columns", JSON.stringify({ default: "nope" }));
tests/unit/columnOverrides.test.ts:80:    expect(JSON.parse(window.localStorage.getItem("tad.columns") ?? "{}")).toEqual({
tests/unit/columnOverrides.test.ts:88:    expect(JSON.parse(window.localStorage.getItem("tad.columns") ?? "{}")).toEqual({});
tests/unit/columnOverrides.test.ts:94:    expect(JSON.parse(window.localStorage.getItem("tad.columns") ?? "{}")).toEqual({
```

---

## Main-Thread Message

Time: 2026-06-17T12:16:48.550Z

No precedent in this codebase. Let me check whether happy-dom has localStorage at all.

---

## Bash Call

Time: 2026-06-17T12:16:51.155Z Description: Probe happy-dom localStorage API

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && cat > /tmp/ls-probe.test.ts <<'EOF'
import { describe, expect, it } from "vitest";
describe("probe", () => {
  it("has localStorage", () => {
    expect(typeof window.localStorage).toBe("object");
    expect(typeof window.localStorage.setItem).toBe("function");
    expect(typeof window.localStorage.removeItem).toBe("function");
    expect(typeof window.localStorage.clear).toBe("function");
  });
});
EOF
cp /tmp/ls-probe.test.ts tests/unit/_probe.test.ts && bun run vitest run tests/unit/_probe.test.ts 2>&1 | grep -E "expected|✓|✗|passed|failed|toBe" | head; rm tests/unit/_probe.test.ts
```

### Output

```text
 ❯ tests/unit/_probe.test.ts (1 test | 1 failed) 5ms
AssertionError: expected 'undefined' to be 'function' // Object.is equality
      4|     expect(typeof window.localStorage).toBe("object");
      5|     expect(typeof window.localStorage.setItem).toBe("function");
      6|     expect(typeof window.localStorage.removeItem).toBe("function");
      7|     expect(typeof window.localStorage.clear).toBe("function");
 Test Files  1 failed (1)
      Tests  1 failed (1)
```

---

## Bash Call

Time: 2026-06-17T12:16:57.063Z Description: Probe localStorage member types

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && cat > tests/unit/_probe.test.ts <<'EOF'
import { describe, expect, it } from "vitest";
describe("probe", () => {
  it("shape", () => {
    expect(typeof window.localStorage).toMatchInlineSnapshot();
    expect(typeof window.localStorage.setItem).toMatchInlineSnapshot();
    expect(typeof window.localStorage.getItem).toMatchInlineSnapshot();
    expect(typeof window.localStorage.removeItem).toMatchInlineSnapshot();
    expect(typeof window.localStorage.clear).toMatchInlineSnapshot();
  });
});
EOF
bun run vitest run tests/unit/_probe.test.ts 2>&1 | grep -E "toMatchInlineSnapshot|string|object|function|undefined" | head; rm tests/unit/_probe.test.ts
```

### Output

```text
(Bash completed with no output)
```

---

## Bash Call

Time: 2026-06-17T12:17:02.635Z Description: Log localStorage member types

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && cat > tests/unit/_probe.test.ts <<'EOF'
import { describe, it } from "vitest";
describe("probe", () => {
  it("shape", () => {
    console.log("localStorage:", typeof window.localStorage);
    if (window.localStorage) {
      console.log("getItem:", typeof window.localStorage.getItem);
      console.log("setItem:", typeof window.localStorage.setItem);
      console.log("removeItem:", typeof window.localStorage.removeItem);
      console.log("clear:", typeof window.localStorage.clear);
    }
  });
});
EOF
bun run vitest run tests/unit/_probe.test.ts 2>&1 | grep -E "localStorage:|getItem:|setItem:|removeItem:|clear:"; rm tests/unit/_probe.test.ts
```

### Output

```text
(Bash completed with no output)
```

---

## Bash Call

Time: 2026-06-17T12:17:08.510Z Description: Force-print localStorage shape via assertion diff

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && cat > tests/unit/_probe.test.ts <<'EOF'
import { describe, it, expect } from "vitest";
describe("probe", () => {
  it("shape", () => {
    const ls = window.localStorage as Storage | undefined;
    const shape = ls
      ? {
          getItem: typeof ls.getItem,
          setItem: typeof ls.setItem,
          removeItem: typeof ls.removeItem,
          clear: typeof ls.clear,
        }
      : "no localStorage";
    expect(JSON.stringify(shape)).toBe("PROBE");
  });
});
EOF
bun run vitest run tests/unit/_probe.test.ts 2>&1 | grep -A3 "Expected\|Received\|to be"; rm tests/unit/_probe.test.ts
```

### Output

```text
AssertionError: expected '{"getItem":"undefined","setItem":"und…' to be 'PROBE' // Object.is equality

Expected: "PROBE"
Received: "{"getItem":"undefined","setItem":"undefined","removeItem":"undefined","clear":"undefined"}"

 ❯ tests/unit/_probe.test.ts:13:35
     11|         }
```

---

## Main-Thread Message

Time: 2026-06-17T12:17:13.490Z

So happy-dom exposes `window.localStorage` as an object but with undefined methods in this version — effectively no working localStorage. That's why no existing test exercises it. The cleanest approach: provide a small in-memory localStorage stub in the test file itself (deterministic, no I/O). Let me update the test to install a stub in `beforeEach`. This keeps the unit test pure and deterministic.

---

## Bash Call

Time: 2026-06-17T12:17:22.334Z Description: Run new test (expect green)

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run vitest run tests/unit/columnOverrides.test.ts 2>&1 | tail -8
```

### Output

```text
 RUN  v4.1.9 ~/github/.worktrees/tad/083-persist-column-picker/frontend


 Test Files  1 passed (1)
      Tests  14 passed (14)
   Start at  14:17:22
   Duration  354ms (transform 25ms, setup 41ms, import 19ms, tests 3ms, environment 162ms)
```

---

## Main-Thread Message

Time: 2026-06-17T12:17:25.219Z

All 14 green. Let me commit the module + test.

---

## Bash Call

Time: 2026-06-17T12:17:27.997Z Description: Commit persistence module and test

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just commit 'Add per-preset column-override persistence module (task/083)

Why: column picker overrides were session-only React state; this thin
framework-free module owns the tad.columns localStorage contract so they
can survive reloads and tab switches. Carries the equal-to-base-or-empty
=> no-override invariant in one home.' frontend/src/lib/columnOverrides.ts frontend/tests/unit/columnOverrides.test.ts 2>&1 | tail -6
```

### Output

```text
 frontend/tests/unit/columnOverrides.test.ts | 141 ++++++++++++++++++++++++++++
 2 files changed, 242 insertions(+)
[task/083-persist-column-picker 0a2443a] Add per-preset column-override persistence module (task/083)
 2 files changed, 242 insertions(+)
 create mode 100644 frontend/src/lib/columnOverrides.ts
 create mode 100644 frontend/tests/unit/columnOverrides.test.ts
```

---

## Main-Thread Message

Time: 2026-06-17T12:17:33.251Z

Now wire `ScreenerBody` in `routes/index.tsx`. This is a React component; the e2e test covers the behaviour end-to-end. Let me make the four changes: imports, initial seed, reseed, persist-on-mutation wrapper, and reset.

---

## Main-Thread Message

Time: 2026-06-17T12:17:40.445Z

Now update the `onViewChange` doc comment (the now-false "discarded on a tab switch"), the `ScreenerBody` doc comment, the seed, reseed, persist wrapper, and reset. Note `canonicalOrder` is memoised inside `ScreenerBody` but the seed/reseed happen before it's declared. The valid-field universe is `canonicalColumnOrder(PRESETS)` — I can compute it inline for the seed or move the memo up. Let me move `canonicalOrder` above the state so seed/reseed can use it.

---

## Main-Thread Message

Time: 2026-06-17T12:17:55.019Z

Now restructure the state seed/reseed and move `canonicalOrder` up.

---

## Main-Thread Message

Time: 2026-06-17T12:18:15.815Z

Now flip the e2e test. Let me check the ColumnsMenu prop signature for `onVisibleColumnsChange` to confirm the type matches `(next: readonly TickerField[]) => void`.

---

## Bash Call

Time: 2026-06-17T12:18:16.449Z Description: Check ColumnsMenu prop type

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && grep -n "onVisibleColumnsChange" src/components/ColumnsMenu.tsx
```

### Output

```text
40:  onVisibleColumnsChange: (next: TickerField[]) => void;
67:  onVisibleColumnsChange,
139:    onVisibleColumnsChange(
225:                      onVisibleColumnsChange(
```

---

## Main-Thread Message

Time: 2026-06-17T12:18:19.663Z

The prop is `(next: TickerField[]) => void` (mutable array). My wrapper takes `readonly TickerField[]` which is contravariantly incompatible when assigned to that prop. Let me make the wrapper take `TickerField[]` to match.

---

## Main-Thread Message

Time: 2026-06-17T12:18:23.040Z

Now run tsc + the existing unit tests for routes/views to make sure nothing broke, then commit the wiring.

---

## Bash Call

Time: 2026-06-17T12:18:23.826Z Description: Typecheck frontend

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run tsc --noEmit 2>&1 | head -20
```

### Output

```text
(Bash completed with no output)
```

---

## Main-Thread Message

Time: 2026-06-17T12:18:30.995Z

Typecheck clean. Now flip the e2e test. The current last test mixes Escape-closing and "overrides do not survive reload". Per the plan, I'll split into a dedicated Escape test plus persistence tests covering: reload restores override, switch-away-and-back restores, and Reset clears so reload returns to base.

---

## Main-Thread Message

Time: 2026-06-17T12:18:55.410Z

Now let me run the e2e for this spec file to validate the behaviour. Let me check the e2e run recipe.

---

## Bash Call

Time: 2026-06-17T12:18:56.369Z Description: Find e2e recipe

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -nE "e2e|frontend-e2e" justfile | head
```

### Output

```text
85:# frontend e2e tests
86:frontend-e2e:
87:    cd frontend && bun run e2e
89:# frontend format, lint, tsc, test (excl. e2e)
132:# ‼️ run before every commit, incl. e2e tests (mostly mirrors CI, except CI does it in parallel)
138:    just frontend-e2e
```

---

## Bash Call

Time: 2026-06-17T12:18:58.928Z Description: Run columns-picker e2e spec

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run e2e columns-picker 2>&1 | tail -30
```

### Output

```text
    Error: expect(locator).toBeVisible() failed

    Locator: getByRole('row').filter({ hasText: 'AAPL' })
    Expected: visible
    Timeout: 5000ms
    Error: element(s) not found

    Call log:
      - Expect "toBeVisible" with timeout 5000ms
      - waiting for getByRole('row').filter({ hasText: 'AAPL' })


      152 | }) => {
      153 |   await page.goto("/");
    > 154 |   await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();
          |                                                                   ^
      155 |
      156 |   await columnsButton(page).click();
      157 |   await page.getByRole("checkbox", { name: "Open" }).click();
        at ~/github/.worktrees/tad/083-persist-column-picker/frontend/tests/e2e/columns-picker.spec.ts:154:67

    Error Context: test-results/columns-picker-Reset-clear-1a600-ater-reload-returns-to-base/error-context.md

  4 failed
    tests/e2e/columns-picker.spec.ts:97:1 › the picker closes on Escape ────────────────────────────
    tests/e2e/columns-picker.spec.ts:109:1 › a column override survives a reload, with the modified marker 
    tests/e2e/columns-picker.spec.ts:130:1 › overrides are remembered per preset across a tab switch 
    tests/e2e/columns-picker.spec.ts:150:1 › Reset clears the stored override so a later reload returns to base 
  4 passed (26.5s)
error: script "e2e" exited with code 1
```

---

## Main-Thread Message

Time: 2026-06-17T12:19:29.954Z

The 4 original tests passed; my 4 new tests fail with "AAPL row not found" — looks like a fixture/data loading issue, possibly only on these later tests. Let me look at the error context and check whether it's a flake or a real issue. The first test ("the Columns button...") passed, which also waits for AAPL. Let me re-run just the failing spec in isolation.

---

## Bash Call

Time: 2026-06-17T12:19:30.679Z Description: Run single new e2e test in isolation

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run e2e columns-picker -g "survives a reload" 2>&1 | tail -25
```

### Output

```text
$ playwright test columns-picker -g "survives a reload"
[WebServer] INFO:     Started server process [21534]
[WebServer] INFO:     Waiting for application startup.
[WebServer] INFO:     Application startup complete.
[WebServer] INFO:     Uvicorn running on http://127.0.0.1:53336 (Press CTRL+C to quit)
[WebServer] INFO:     127.0.0.1:53343 - "GET /docs HTTP/1.1" 200 OK
[WebServer] 
[WebServer]   VITE v8.0.16  ready in 400 ms
[WebServer] 
[WebServer]   ➜  Local:   http://localhost:53337/
[WebServer]   ➜  Network: use --host to expose

Running 1 test using 1 worker

[WebServer] INFO:     127.0.0.1:53361 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:53362 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:53364 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:53372 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:53374 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:53375 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  1 tests/e2e/columns-picker.spec.ts:109:1 › a column override survives a reload, with the modified marker (1.0s)

  1 passed (4.0s)
```

---

## Main-Thread Message

Time: 2026-06-17T12:19:38.743Z

Passes in isolation. The full-spec failure is a data-loading issue when run together — likely the tickers query fails intermittently, or the dev server got overwhelmed. Let me re-run the whole spec file once more to see if it's a flake.

---

## Bash Call

Time: 2026-06-17T12:19:39.593Z Description: Re-run full columns-picker spec

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run e2e columns-picker 2>&1 | tail -15
```

### Output

```text
  ✓  5 tests/e2e/columns-picker.spec.ts:97:1 › the picker closes on Escape (796ms)
[WebServer] INFO:     127.0.0.1:53493 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:53495 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:53496 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:53506 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:53502 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:53505 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  7 tests/e2e/columns-picker.spec.ts:130:1 › overrides are remembered per preset across a tab switch (1.0s)
  ✓  6 tests/e2e/columns-picker.spec.ts:109:1 › a column override survives a reload, with the modified marker (1.1s)
[WebServer] INFO:     127.0.0.1:53513 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:53514 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:53516 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  8 tests/e2e/columns-picker.spec.ts:150:1 › Reset clears the stored override so a later reload returns to base (1.1s)

  8 passed (6.0s)
```

---

## Main-Thread Message

Time: 2026-06-17T12:19:50.725Z

All 8 pass. The earlier failure was a startup flake (initial server warmup). Let me commit the wiring + e2e changes (one logical change: the persistence wiring + its e2e coverage). Actually these are two distinct files but one logical feature increment. I'll commit them together.

---

## Bash Call

Time: 2026-06-17T12:19:53.601Z Description: Commit wiring and e2e changes

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just commit 'Persist column picker overrides per preset in ScreenerBody (task/083)

Why: route the seed, reseed-on-tab-switch, every picker mutation, and
Reset through the columnOverrides module so each view remembers its own
column set across reloads and tab switches. Flip the e2e that pinned the
old session-only behaviour into persistence coverage.' frontend/src/routes/index.tsx frontend/tests/e2e/columns-picker.spec.ts 2>&1 | tail -6
```

### Output

```text
Staged changes:
 frontend/src/routes/index.tsx             | 61 ++++++++++++++++++---------
 frontend/tests/e2e/columns-picker.spec.ts | 68 +++++++++++++++++++++++++++----
 2 files changed, 103 insertions(+), 26 deletions(-)
[task/083-persist-column-picker 8dc1b4d] Persist column picker overrides per preset in ScreenerBody (task/083)
 2 files changed, 103 insertions(+), 26 deletions(-)
```

---

## Main-Thread Message

Time: 2026-06-17T12:19:55.804Z

Now self-review the diff from first commit, then run full check-all.

---

## Bash Call

Time: 2026-06-17T12:19:56.994Z Description: Review production diff from base

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git diff df77f86 HEAD -- frontend/src/lib/columnOverrides.ts frontend/src/routes/index.tsx
```

### Output

```text
diff --git a/frontend/src/lib/columnOverrides.ts b/frontend/src/lib/columnOverrides.ts
new file mode 100644
index 0000000..c1b5f68
--- /dev/null
+++ b/frontend/src/lib/columnOverrides.ts
@@ -0,0 +1,101 @@
+// Per-preset column-picker persistence (083).
+//
+// The visible-column override for each preset survives reloads and tab switches
+// via ONE localStorage key, `tad.columns` (the `tad.theme` namespace), holding a
+// `{ [presetId]: field[] }` map. Values are order-significant — order is part of
+// "modified" and the render order. An absent id means no override; an entry is
+// never stored equal to its preset base.
+//
+// This module is the single home for the "equal-to-base or empty ⇒ no override"
+// invariant: `resolve` returns the base for a degenerate stored set, `persist`
+// deletes rather than writes a redundant entry. Framework-free and generic over
+// the field type, mirroring `visibleColumns.ts` — unit-testable with synthetic
+// field lists.
+//
+// All reads are SSR/test-safe (`typeof window` guard) and corruption-safe (any
+// malformed blob is treated as no override, never throws); writes guard `window`
+// and swallow a failed `setItem` (quota/availability) so a toggle can't break.
+
+import { isColumnSetModified } from "@/lib/visibleColumns";
+
+const STORAGE_KEY = "tad.columns";
+
+type OverrideMap = Record<string, string[]>;
+
+function readMap(): OverrideMap {
+  if (typeof window === "undefined") return {};
+  try {
+    const raw = window.localStorage.getItem(STORAGE_KEY);
+    if (raw === null) return {};
+    const parsed = JSON.parse(raw) as unknown;
+    if (typeof parsed !== "object" || parsed === null) return {};
+    return parsed as OverrideMap;
+  } catch {
+    return {};
+  }
+}
+
+function writeMap(map: OverrideMap): void {
+  if (typeof window === "undefined") return;
+  try {
+    if (Object.keys(map).length === 0) {
+      window.localStorage.removeItem(STORAGE_KEY);
+    } else {
+      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(map));
+    }
+  } catch {
+    // Quota/availability — a failed persist must not break the toggle.
+  }
+}
+
+/**
+ * The effective starting set for a preset: the validated stored override, else
+ * the preset's base. The stored array is sanitised — any field not in `universe`
+ * is dropped (preserving stored order). If the result is empty OR equals the
+ * base (`isColumnSetModified` ⇒ not modified), the base is returned and the
+ * stored entry is treated as no override.
+ */
+export function resolveColumnOverride<T extends string>(
+  presetId: string,
+  base: readonly T[],
+  universe: readonly T[],
+): readonly T[] {
+  const stored = readMap()[presetId];
+  if (!Array.isArray(stored)) return base;
+
+  const known = new Set<string>(universe);
+  const filtered = stored.filter((f): f is T => known.has(f));
+  if (filtered.length === 0) return base;
+  if (!isColumnSetModified(filtered, base)) return base;
+  return filtered;
+}
+
+/**
+ * Store an override for a preset. Enforces the invariant: an override equal to
+ * (or degenerate against) the base deletes the entry rather than writing a
+ * redundant one. The exact `next` set is stored — order-significant.
+ */
+export function persistColumnOverride<T extends string>(
+  presetId: string,
+  next: readonly T[],
+  base: readonly T[],
+  universe: readonly T[],
+): void {
+  const map = readMap();
+  const known = new Set<string>(universe);
+  const filtered = next.filter((f) => known.has(f));
+  if (filtered.length === 0 || !isColumnSetModified(filtered, base)) {
+    delete map[presetId];
+  } else {
+    map[presetId] = [...filtered];
+  }
+  writeMap(map);
+}
+
+/** Clear a preset's stored override (Reset). */
+export function clearColumnOverride(presetId: string): void {
+  const map = readMap();
+  if (!(presetId in map)) return;
+  delete map[presetId];
+  writeMap(map);
+}
diff --git a/frontend/src/routes/index.tsx b/frontend/src/routes/index.tsx
index bd57e54..0904e6e 100644
--- a/frontend/src/routes/index.tsx
+++ b/frontend/src/routes/index.tsx
@@ -11,6 +11,11 @@ import { ColumnsMenu } from "@/components/ColumnsMenu";
 import { MarketSummary } from "@/components/MarketSummary";
 import { TickerTable } from "@/components/TickerTable";
 import { ViewBar } from "@/components/ViewBar";
+import {
+  clearColumnOverride,
+  persistColumnOverride,
+  resolveColumnOverride,
+} from "@/lib/columnOverrides";
 import { GROUPS, PRESETS, type PresetView, type TickerField } from "@/lib/columns";
 import { DEFAULT_PAGE_SIZE, PAGE_SIZES } from "@/lib/pagination";
 import {
@@ -100,8 +105,9 @@ function IndexComponent() {
   // A tab switch is a destination (push, like a page step — Back walks view
   // changes) and resets to page 1. The table reseeds the sort from the new
   // preset on its own (see TickerTable), and the new preset-id reseeds the
-  // session visible set in ScreenerBody — so picker overrides are discarded on a
-  // tab switch with no extra logic. This only owns the view + page.
+  // visible set in ScreenerBody — which now restores that preset's saved
+  // column override from storage (see ScreenerBody). This only owns the view +
+  // page.
   function onViewChange(next: string) {
     navigate({ search: (prev) => ({ ...prev, view: next, page: 1 }) });
   }
@@ -139,11 +145,14 @@ function IndexComponent() {
   );
 }

-// The screener body — owns the SESSION visible-column set: seeded from the
-// active preset, mutated by the Columns picker, re-seeded whenever the active
-// preset changes (a tab switch / fresh ?view), and restored on Reset. The set
-// is session-only — never URL-encoded, so a reload restores the base ?view
-// preset (the seed re-derives from `activePreset`).
+// The screener body — owns the active preset's visible-column working set:
+// seeded from the active preset (or its saved override), mutated by the Columns
+// picker, re-seeded whenever the active preset changes (a tab switch / fresh
+// ?view), and restored on Reset. The set is never URL-encoded; instead each
+// mutation persists a per-preset override to localStorage (see lib/columnOverrides),
+// so a reload or tab switch restores that preset's saved columns rather than the
+// preset base. Storage is the cross-preset source of truth; React state holds
+// only the active preset's working copy and re-resolves from storage on switch.
 function ScreenerBody({
   activePreset,
   q,
@@ -163,9 +172,16 @@ function ScreenerBody({
   onViewChange: (id: string) => void;
   onResetPage: () => void;
 }) {
-  // The session visible-column set, seeded from the active preset.
-  const [visibleColumns, setVisibleColumns] = useState<readonly TickerField[]>(
-    activePreset.columns,
+  // The picker's column universe + order: the canonical order (the widest
+  // preset's columns). Per-field metadata comes from the IA constant, so the
+  // picker renders fully on mount — no async metadata join. Also the valid-field
+  // universe the override resolver sanitises stored sets against.
+  const canonicalOrder = useMemo(() => canonicalColumnOrder(PRESETS), []);
+
+  // The active preset's visible-column working set, seeded from its saved
+  // override (or the preset base when none/degenerate) — see lib/columnOverrides.
+  const [visibleColumns, setVisibleColumns] = useState<readonly TickerField[]>(() =>
+    resolveColumnOverride(activePreset.id, activePreset.columns, canonicalOrder),
   );
   // A monotonic signal the table watches to reseed its sort on Reset (the
   // columns reset is `setVisibleColumns` below; sort lives in TickerTable).
@@ -173,23 +189,30 @@ function ScreenerBody({

   // Re-seed the visible set the instant the active preset changes — synchronously
   // during render via the previous-id-in-state pattern (NOT a useEffect),
-  // matching TickerTable's sort reseed. Both fire on `activePreset.id`, which is
-  // exactly why a tab switch discards picker modifications with no extra logic.
+  // matching TickerTable's sort reseed. Both fire on `activePreset.id`. The
+  // reseed restores the NEW preset's saved override (same resolve as the seed),
+  // so a tab switch returns each view to its own remembered columns.
   const [prevPresetId, setPrevPresetId] = useState(activePreset.id);
   if (prevPresetId !== activePreset.id) {
     setPrevPresetId(activePreset.id);
-    setVisibleColumns(activePreset.columns);
+    setVisibleColumns(
+      resolveColumnOverride(activePreset.id, activePreset.columns, canonicalOrder),
+    );
   }

-  // The picker's column universe + order: the canonical order (the widest
-  // preset's columns). Per-field metadata comes from the IA constant, so the
-  // picker renders fully on mount — no async metadata join.
-  const canonicalOrder = useMemo(() => canonicalColumnOrder(PRESETS), []);
-
   const isModified = isColumnSetModified(visibleColumns, activePreset.columns);

+  // Persist every picker mutation as the active preset's override. The module
+  // enforces equal-to-base ⇒ delete, so toggling a column on then off clears the
+  // entry (and the marker) rather than storing a redundant set.
+  function onVisibleColumnsChange(next: TickerField[]) {
+    setVisibleColumns(next);
+    persistColumnOverride(activePreset.id, next, activePreset.columns, canonicalOrder);
+  }
+
   function onReset() {
     setVisibleColumns(activePreset.columns);
+    clearColumnOverride(activePreset.id);
     setResetNonce((n) => n + 1);
     onResetPage();
   }
@@ -207,7 +230,7 @@ function ScreenerBody({
             total={canonicalOrder.length}
             groups={GROUPS}
             visibleColumns={visibleColumns}
-            onVisibleColumnsChange={setVisibleColumns}
+            onVisibleColumnsChange={onVisibleColumnsChange}
             onReset={onReset}
             activePresetLabel={activePreset.label}
             isModified={isModified}
```

---

## Main-Thread Message

Time: 2026-06-17T12:20:01.920Z

Diff is clean and matches the plan. The `OverrideMap` cast in `readMap` returns `parsed as OverrideMap` without validating value shapes, but `resolveColumnOverride` defends with `Array.isArray(stored)` and `persistColumnOverride`/`clearColumnOverride` only read keys — so a malformed value can't cause a throw. Good.

Now run full check-all.

---

## Bash Call

Time: 2026-06-17T12:20:03.218Z Description: Run full check-all suite

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just check-all 2>&1 | tail -40
```

### Output

```text
  > 22 │     "enabled": true,
  > 23 │     "rules": {
  > 24 │       "recommended": true
  > 25 │     }
  > 26 │   },
       │   ^
    27 │   "javascript": {
    28 │     "formatter": {

  i Migrate the configuration with the proper command

  $ biome migrate


tests/unit/columnOverrides.test.ts format ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × Formatter would have printed the following content:

     60  60 │         JSON.stringify({ default: ["ticker", "gone", "open"] }),
     61  61 │       );
     62     │ - ····expect(resolveColumnOverride("default",·BASE,·UNIVERSE)).toEqual(["ticker",·"open"]);
         62 │ + ····expect(resolveColumnOverride("default",·BASE,·UNIVERSE)).toEqual([
         63 │ + ······"ticker",
         64 │ + ······"open",
         65 │ + ····]);
     63  66 │     });
     64  67 │   


Checked 86 files in 56ms. No fixes applied.
Found 1 error.
Found 2 infos.
check ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × Some errors were emitted while running checks.


error: script "check" exited with code 1
error: Recipe `frontend-check` failed on line 91 with exit code 1
error: Recipe `check-all` failed on line 137 with exit code 1
```

---

## Main-Thread Message

Time: 2026-06-17T12:20:39.023Z

A formatting issue in my test. The frontend has an autoformat. Let me run the formatter.

---

## Bash Call

Time: 2026-06-17T12:20:39.997Z Description: Run frontend formatter

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run format 2>&1 | tail -5 || grep -nE "\"format\"|biome|check:" package.json
```

### Output

```text
error: Script not found "format"
```

---

## Bash Call

Time: 2026-06-17T12:20:42.861Z Description: Find format/fix scripts

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && grep -nE "\"(format|lint|check|fix)\"" package.json
```

### Output

```text
11:    "check": "biome check && tsc --noEmit && vitest run",
```

---

## Bash Call

Time: 2026-06-17T12:20:50.388Z Description: Auto-fix formatting in test file

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bunx biome check --write tests/unit/columnOverrides.test.ts 2>&1 | tail -5
```

### Output

```text
Checked 1 file in 10ms. Fixed 1 file.
[This command modified 1 file you've previously read: ../.worktrees/tad/083-persist-column-picker/frontend/tests/unit/columnOverrides.test.ts. Call Read before editing.]
```

---

## Main-Thread Message

Time: 2026-06-17T12:20:55.762Z

The test file was already committed unformatted. I need to amend that commit — but it's already pushed... actually it's a worktree branch, not pushed. Let me re-run check-all to confirm green, then I'll commit the format fix. Since the test file was committed in the first commit, I'll add the format fix as part of finishing. Best to amend the first commit to keep history clean. Let me check if it's safe to amend (the wiring commit is on top).

The cleanest path: the format-only change is to a file already committed. I'll commit it as a fixup. But two commits touching the same test file is messy. Let me re-run check-all first to ensure that's the only failure.

---

## Bash Call

Time: 2026-06-17T12:20:57.121Z Description: Re-run check-all

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just check-all 2>&1 | tail -25
```

### Output

```text
  ✓  58 tests/e2e/views.spec.ts:128:1 › the chain rail's leading cell stays pinned over the sticky ticker on horizontal scroll (670ms)
[WebServer] INFO:     127.0.0.1:54459 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:54460 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:54461 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:54469 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:54472 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:54473 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  59 tests/e2e/views.spec.ts:162:1 › a chain view swaps the band for the derivation rail (637ms)
  ✓  60 tests/e2e/views.spec.ts:176:1 › the Liquidity chain sorts by its signal, not its boolean terminus (482ms)
[WebServer] INFO:     127.0.0.1:54475 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:54477 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:54479 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  61 tests/e2e/views.spec.ts:193:1 › the active view survives a manual sort and a page step in the URL (641ms)

  61 passed (16.1s)
just workflow-lint
actionlint
just md-format
rumdl fmt .

Success: No issues found in 273 files (174ms)
just md-check
rumdl check .

Success: No issues found in 273 files (25ms)
```

---

## Main-Thread Message

Time: 2026-06-17T12:21:33.651Z

check-all is green now. The only remaining issue is that the formatted test file is uncommitted. Since it's purely a format fix to a file from the first commit, I'll amend that commit so history is clean (this branch hasn't been pushed).

---

## Bash Call

Time: 2026-06-17T12:21:34.452Z Description: Check current state before amend

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git log --oneline -3 && echo "---" && git diff --stat
```

### Output

```text
8dc1b4d Persist column picker overrides per preset in ScreenerBody (task/083)
0a2443a Add per-preset column-override persistence module (task/083)
df77f86 Add task 083: persist column picker overrides per preset (task/083)
---
 frontend/tests/unit/columnOverrides.test.ts |  5 +++-
 tasks/083-persist-column-picker.md          | 38 ++++++++++++++++++++++++++++-
 2 files changed, 41 insertions(+), 2 deletions(-)
```

---

## Main-Thread Message

Time: 2026-06-17T12:21:40.655Z

The format fix is in the first commit's file but the wiring commit is on top. Amending the first commit requires a rebase. Simpler and cleaner: since both commits are part of task/083 and unpushed, I'll just use an interactive-free approach — stage only the test file and fixup-squash it into 0a2443a via `git commit --fixup` + autosquash rebase. But CLAUDE.md says no interactive rebase support.

The pragmatic clean approach: reset soft to before the two commits, re-stage logically. Actually that's overkill. The format change is trivial whitespace. I'll just commit it onto the first commit's logical scope as a small follow-up — but that creates a noisy "format" commit.

Better: non-interactive autosquash works without `-i` via `GIT_SEQUENCE_EDITOR=true git rebase --autosquash`. Let me do that.

---

## Bash Call

Time: 2026-06-17T12:21:42.333Z Description: Create fixup commit for format fix

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git stash push -- tasks/083-persist-column-picker.md && git add frontend/tests/unit/columnOverrides.test.ts && git commit --fixup=0a2443a 2>&1 | tail -3
```

### Output

```text
Saved working directory and index state WIP on task/083-persist-column-picker: 8dc1b4d Persist column picker overrides per preset in ScreenerBody (task/083)
[task/083-persist-column-picker 17746ea] fixup! Add per-preset column-override persistence module (task/083)
 1 file changed, 4 insertions(+), 1 deletion(-)
[This command modified 1 file you've previously read: ../.worktrees/tad/083-persist-column-picker/tasks/083-persist-column-picker.md. Call Read before editing.]
```

---

## Bash Call

Time: 2026-06-17T12:21:49.099Z Description: Autosquash fixup into first commit and restore stash

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && GIT_SEQUENCE_EDITOR=true git rebase --autosquash df77f86 2>&1 | tail -5 && echo "---LOG---" && git log --oneline -3 && echo "---STASH---" && git stash pop 2>&1 | tail -3
```

### Output

```text
Rebasing (2/3)Rebasing (3/3)Successfully rebased and updated refs/heads/task/083-persist-column-picker.
---LOG---
2d16654 Persist column picker overrides per preset in ScreenerBody (task/083)
ad55e28 Add per-preset column-override persistence module (task/083)
df77f86 Add task 083: persist column picker overrides per preset (task/083)
---STASH---

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (9924c768991980039a962da93d00bd58f7278fa3)
```

---

## Main-Thread Message

Time: 2026-06-17T12:21:51.597Z

Clean two-commit history, format fix folded in. Let me verify the test file is now the formatted version in the committed tree.

---

## Bash Call

Time: 2026-06-17T12:21:52.516Z Description: Confirm no frontend diff remains, only task file

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git diff HEAD -- frontend/ | head && echo "===status===" && git status --short
```

### Output

```text
===status===
 M tasks/083-persist-column-picker.md
```

---

## Main-Thread Message

Time: 2026-06-17T12:21:55.508Z

Frontend is fully committed and clean. Now write the Implementation notes and commit the task file. Let me read the current task file tail to append correctly.

---

## Main-Thread Message

Time: 2026-06-17T12:22:15.892Z

Now format the markdown and commit the task file.

---

## Bash Call

Time: 2026-06-17T12:22:16.896Z Description: Lint task markdown

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && rumdl check tasks/083-persist-column-picker.md 2>&1 | tail -5
```

### Output

```text
Success: No issues found in 1 file (20ms)
```

---

## Bash Call

Time: 2026-06-17T12:22:20.833Z Description: Commit task file with implementation notes

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just commit 'Add task 083 implementation notes (task/083)' tasks/083-persist-column-picker.md 2>&1 | tail -5 && echo "===" && git log --oneline -4
```

### Output

```text
Staged changes:
 tasks/083-persist-column-picker.md | 46 +++++++++++++++++++++++++++++++++++++-
 1 file changed, 45 insertions(+), 1 deletion(-)
[task/083-persist-column-picker 5c0cee0] Add task 083 implementation notes (task/083)
 1 file changed, 45 insertions(+), 1 deletion(-)
===
5c0cee0 Add task 083 implementation notes (task/083)
2d16654 Persist column picker overrides per preset in ScreenerBody (task/083)
ad55e28 Add per-preset column-override persistence module (task/083)
df77f86 Add task 083: persist column picker overrides per preset (task/083)
```

---

## Main-Thread Message

Time: 2026-06-17T12:22:24.399Z

Wait — the task file still shows `status: in-dev` from the recipe but I should double-check the status field wasn't reset. The commit captured the implementation notes. Let me verify final state.

---

## Bash Call

Time: 2026-06-17T12:22:25.114Z Description: Verify clean tree and status field

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git status --short && echo "---status field---" && grep "^status:" tasks/083-persist-column-picker.md
```

### Output

```text
---status field---
status: in-dev
```

---

## Main-Thread Message

Time: 2026-06-17T12:22:38.550Z

Clean working tree, status `in-dev` (correct for impl-task; ship-task moves it to done). Task 083 is fully implemented.

## Summary

Implemented TAD task 083 — column picker overrides now persist per preset across reloads and tab switches via localStorage.

What was built:

- New framework-free module `frontend/src/lib/columnOverrides.ts` (`resolveColumnOverride` / `persistColumnOverride` / `clearColumnOverride`) owning the single `tad.columns` key holding a `{ [presetId]: field[] }` map. It is the one home for the "equal-to-base or empty ⇒ no override" invariant (resolve returns base for a degenerate set; persist deletes rather than writes redundant). Reads are SSR/corruption-safe; writes swallow quota/availability failures. TDD'd with 14 unit tests.
- Wired `ScreenerBody` in `frontend/src/routes/index.tsx`: lazy seed and the synchronous reseed-on-tab-switch block both resolve via the module; a new `onVisibleColumnsChange` wrapper persists every picker mutation; `onReset` clears the stored entry. `canonicalOrder` moved above state to serve as the valid-field universe. `isModified` is unchanged and now reads true after reload for free.
- Flipped the e2e: the old "overrides do not survive a reload" test became a focused Escape-close test plus three persistence tests (reload restores override + modified marker; per-preset memory across Default→Returns→Default; Reset clears so reload returns to base).

Commits (newest first):

- `5c0cee0` Add task 083 implementation notes (task/083)
- `2d16654` Persist column picker overrides per preset in ScreenerBody (task/083)
- `ad55e28` Add per-preset column-override persistence module (task/083)

`just check-all`: green end-to-end (backend, openapi-drift, frontend-check incl. 61 e2e, workflow-lint, markdown).

Deviations / flags:

- Plan assumed jsdom `localStorage.clear()` works in unit tests, but this repo's vitest env is happy-dom whose `window.localStorage` exposes no working methods (no prior test used it). The unit test installs a minimal in-memory `Storage` stub in `beforeEach` — deterministic, no real I/O. Production guards are unchanged.
- `ColumnsMenu`'s prop is `(next: TickerField[]) => void` (mutable), so the wrapper takes a mutable array, not `readonly`.
- One transient first-run e2e failure (dev-server warmup losing the AAPL row); reliably green on warm runs and under full check-all.
- Status left at `in-dev` (ship-task will move it to `done`).

All work is committed on branch `task/083-persist-column-picker` in the worktree; nothing pushed.

---

</details>

## Main-Thread Message

Time: 2026-06-17T12:22:45.846Z

Implementation is green. Now **Step 5: Review Code** (full mode) — Opus `/review-code` and Codex adversarial review in parallel. Let me read both skill/command definitions.

---

## Bash Call

Time: 2026-06-17T12:22:45.883Z Description: Read codex adversarial-review command

### Command

```text
echo "=== codex adversarial-review command ==="; cat ~/.claude/plugins/cache/**/commands/adversarial-review.md 2>/dev/null | head -60
```

### Output

```text
=== codex adversarial-review command ===
---
description: Run a Codex review that challenges the implementation approach and design choices
argument-hint: '[--wait|--background] [--base <ref>] [--scope auto|working-tree|branch] [focus ...]'
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(node:*), Bash(git:*), AskUserQuestion
---

Run an adversarial Codex review through the shared plugin runtime.
Position it as a challenge review that questions the chosen implementation, design choices, tradeoffs, and assumptions.
It is not just a stricter pass over implementation defects.

Raw slash-command arguments:
`$ARGUMENTS`

Core constraint:
- This command is review-only.
- Do not fix issues, apply patches, or suggest that you are about to make changes.
- Your only job is to run the review and return Codex's output verbatim to the user.
- Keep the framing focused on whether the current approach is the right one, what assumptions it depends on, and where the design could fail under real-world conditions.

Execution mode rules:
- If the raw arguments include `--wait`, do not ask. Run in the foreground.
- If the raw arguments include `--background`, do not ask. Run in a Claude background task.
- Otherwise, estimate the review size before asking:
  - For working-tree review, start with `git status --short --untracked-files=all`.
  - For working-tree review, also inspect both `git diff --shortstat --cached` and `git diff --shortstat`.
  - For base-branch review, use `git diff --shortstat <base>...HEAD`.
  - Treat untracked files or directories as reviewable work for auto or working-tree review even when `git diff --shortstat` is empty.
  - Only conclude there is nothing to review when the relevant scope is actually empty.
  - Recommend waiting only when the scoped review is clearly tiny, roughly 1-2 files total and no sign of a broader directory-sized change.
  - In every other case, including unclear size, recommend background.
  - When in doubt, run the review instead of declaring that there is nothing to review.
- Then use `AskUserQuestion` exactly once with two options, putting the recommended option first and suffixing its label with `(Recommended)`:
  - `Wait for results`
  - `Run in background`

Argument handling:
- Preserve the user's arguments exactly.
- Do not strip `--wait` or `--background` yourself.
- Do not weaken the adversarial framing or rewrite the user's focus text.
- The companion script parses `--wait` and `--background`, but Claude Code's `Bash(..., run_in_background: true)` is what actually detaches the run.
- `/codex:adversarial-review` uses the same review target selection as `/codex:review`.
- It supports working-tree review, branch review, and `--base <ref>`.
- It does not support `--scope staged` or `--scope unstaged`.
- Unlike `/codex:review`, it can still take extra focus text after the flags.

Foreground flow:
- Run:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" adversarial-review "$ARGUMENTS"
```

- Return the command stdout verbatim, exactly as-is.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not fix any issues mentioned in the review output.

Background flow:

- Launch the review with `Bash` in the background:

```typescript
Bash({
  command: `node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" adversarial-review "$ARGUMENTS"`,
```

---

## Bash Call

Time: 2026-06-17T12:22:49.064Z Description: Locate codex-companion script

### Command

```text
ls -d ~/.claude/plugins/cache/*/*/scripts/codex-companion.mjs 2>/dev/null; echo "---"; find ~/.claude/plugins/cache -name codex-companion.mjs 2>/dev/null
```

### Output

```text
(eval):1: no matches found: ~/.claude/plugins/cache/*/*/scripts/codex-companion.mjs
---
~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs
```

---

## Main-Thread Message

Time: 2026-06-17T12:22:55.277Z

Plugin root resolved. Launching Codex adversarial review in the background and the Opus `/review-code` reviewer in parallel. Let me read the review-code skill first to brief the Opus reviewer.

---

## Main-Thread Message

Time: 2026-06-17T12:22:58.587Z

Now launching both reviews in parallel — Codex adversarial in the background, Opus `/review-code` as a subagent.

---

## Bash Call

Time: 2026-06-17T12:23:00.695Z Description: Launch codex adversarial review in background

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" adversarial-review "--background --base main"
```

### Output

```text
Command running in background with ID: bjnpxqs8i. Output is being written to: /private/tmp/claude-501/-Users-patric-github-tad/0cada52f-e4c7-4492-be3d-393ac0f59cd6/tasks/bjnpxqs8i.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

---

## Subagent 4: Review Code Task 083 [General-Purpose]

Time: 2026-06-17T12:23:20.045Z

### Prompt

Run `/review-code main..HEAD` on the TAD task 083 implementation. You are a fresh-session reviewer (you did NOT author this diff), so run the full open correctness/logic/security/design pass.

WORKTREE ROOT (cd here; all paths root here): ~/github/.worktrees/tad/083-persist-column-picker Diff target: main..HEAD Task/spec file (read for intent FIRST — intent lives here, not in the code): tasks/083-persist-column-picker.md

Follow the `/review-code` skill exactly. Its key rules (inlined):

GOAL: Surface the small set of findings a competent author would fix; capture mechanically-certain trivia as ready-to-apply `Autofix:` patches. You classify, you do NOT fix.

DO-NOT-FLAG (drop, don't surface): pre-existing issues not introduced/worsened by this diff; tool-owned (lint/format/type/test-failures — a separate deterministic gate covers these); correct-but-unusual; framework-handled; speculative (no concrete file:line + failure mechanism); judgement-bound taste trivia. "Trivial is not drop": a mechanical, certain, non-judgement fix → Autofix lane (even a one-char typo). Judgement needed + immaterial → drop.

WHAT TO EXAMINE (blocking tier, co-equal): correctness & logic (boundaries, null/index, off-by-one, invalid-state, idempotency); API/contract/design (interface completeness, coupling, SRP, over-engineering, fit with codebase); security; concurrency. Then descending: tests (coverage at right level, assert behaviour not mocks) → error handling → performance (hot paths only) → docs/naming (low) → style (never).

AI-CODE FOCUS: intensify correctness/security; explicitly check convention conformance and abstraction duplication (re-implementing an existing util instead of reusing is a characteristic AI failure). Keep comments terse.

SCOPE DISCIPLINE: cover every changed file (read its diff or state why skipped); recover intent from task file + tests before judging; verify by tracing call sites, not speculating.

VERIFY BEFORE POST: second pass over candidates; drop unless concrete file:line + traced causal chain. Confidence 0-100: surface ~80+; collect 50-79 in a below_threshold bucket; drop <50.

SEVERITY: Critical (correctness/security/data-safety, unsafe to ship — blocks) / Major (likely incorrect under realistic input — blocks) / Minor (advisory) / Nit (advisory). AUTOFIX-eligible only when ALL hold: single exact text transform needing no judgement; essentially certain; touches only this diff's code; no behavioural ambiguity. Minor/Nit only carry the bypass; Major/Critical keep their fix on the Fix: line but stay gating.

TAD APPENDIX: look for silent corruption (unguarded division, NaN-leaking paths — guarded division must yield None not NaN); flag those Critical/Major. Stay in the code-review lane — do NOT re-check acceptance criteria / task completion (that's /review-task).

This diff is primarily frontend TypeScript/React (a new localStorage persistence module, ScreenerBody wiring in routes/index.tsx, an e2e test flip, unit tests). Pay attention to: localStorage read/write correctness and guards (SSR/corruption/quota); the resolve/persist/clear contract and its "equal-to-base or empty ⇒ no override" invariant; order-significance of the stored arrays; the synchronous reseed path in ScreenerBody (must not regress the prev-id-in-state pattern); and whether the new module duplicates existing helpers (e.g. isColumnSetModified in lib/visibleColumns.ts) rather than reusing them.

OUTPUT per finding: [Severity] path/to/file:NN Issue: <one line> Why: <traced failure mechanism / blast radius> Fix: <copy-pasteable instruction — do NOT apply> Autofix: <exact old → new; Minor/Nit only; omit line entirely unless eligible>

End with the machine-readable tally line: {"critical":N,"major":N,"minor":N,"nit":N,"autofix":N,"below_threshold":N}. "No findings" is a valid, complete review — say so in one line if so. Do not invent findings.

### Response

Default has 11 columns → `11/28` base, `12/28` after adding Open. Consistent. The implementation notes confirm `just check-all` passes including e2e.

The implementation is clean, correct, and faithful to the locked spec. The module reuses `isColumnSetModified` rather than reimplementing it (the exact AI-duplication trap the prompt flagged — avoided). Guards for SSR, corruption, and quota are all present and stronger than the AppShell precedent. The synchronous reseed preserves the prev-id-in-state pattern. No correctness, security, or design defects rise to the threshold.

---

## Review: Task 083 (Persist Column Picker Overrides per Preset)

No findings.

Every changed file was examined: `columnOverrides.ts` (new module), `routes/index.tsx` (wiring), `columnOverrides.test.ts` (unit), `columns-picker.spec.ts` (e2e flip). The diff is faithful to the locked spec and clean.

Checks that passed:

- **Reuse, not reimplementation** — the module imports `isColumnSetModified` from `visibleColumns.ts` for its "equal-to-base ⇒ no override" invariant rather than re-deriving it (the characteristic AI duplication trap; avoided).
- **localStorage guards** — `readMap`/`writeMap` both guard `typeof window === "undefined"` and wrap `getItem`+`JSON.parse` / `setItem` in `try/catch`; malformed blobs and quota/availability failures degrade to "no override" without throwing. Stronger than the `tad.theme` precedent it mirrors.
- **Resolve/persist/clear contract** — sanitises against `universe`, drops unknown fields preserving order, returns base when empty-after-filter or equal-to-base; persist deletes rather than writes a redundant entry; the empty-map case removes the key entirely. Single home for the invariant, as specified.
- **Order-significance** — `filter` preserves stored order throughout; `isColumnSetModified` is element-wise, so a reorder counts as modified. Consistent.
- **Synchronous reseed** — the prev-id-in-state render-phase block is preserved (not converted to `useEffect`); both seed and reseed call the same `resolveColumnOverride`. `canonicalOrder` correctly hoisted above the state declarations so it can feed the lazy initialiser. `isModified` unchanged, so the marker/Reset state follow for free.
- **Tests** — unit suite covers no-override, validated round-trip, unknown-field drop, empty-after-filter, equal-to-base, per-preset keying, corrupt blob, non-array entry, persist-delete, multi-preset isolation, clear. The happy-dom `localStorage` stub (noted as a deviation) is a sound deterministic substitute. E2e count literals (`11/28` base, `12/28` +Open) match the worktree's Default preset (11 columns).

Below-threshold items considered and dropped: `readMap` would accept a top-level JSON **array** as an `OverrideMap` (`typeof [] === "object"`); it degrades gracefully to base on resolve and string-key writes still serialise correctly — no real-world path produces this, confidence < 50. Minor `known`-Set + filter duplication between `resolve` and `persist` is immaterial intra-module repetition, not worth a finding.

{"critical":0,"major":0,"minor":0,"nit":0,"autofix":0,"below_threshold":1} agentId: aff0df7b27d348016 (use SendMessage with to: 'aff0df7b27d348016' to continue this agent) <usage>subagent_tokens: 64613 tool_uses: 12 duration_ms: 68298</usage>

---

<details><summary>Inner trace (subagent session agent-aff0df7b27d348016, depth 1)</summary>

## Main-Thread Message

Time: 2026-06-17T12:23:22.265Z

I'll review the task 083 implementation. Let me start by reading the spec and the diff.

---

## Bash Call

Time: 2026-06-17T12:23:23.682Z Description: Show worktree, commits, diff stat

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && pwd && git log --oneline main..HEAD && echo "---DIFF STAT---" && git diff --stat main..HEAD
```

### Output

```text
~/github/.worktrees/tad/083-persist-column-picker
5c0cee0 Add task 083 implementation notes (task/083)
2d16654 Persist column picker overrides per preset in ScreenerBody (task/083)
ad55e28 Add per-preset column-override persistence module (task/083)
---DIFF STAT---
 frontend/src/lib/columnOverrides.ts         | 101 +++++++++++++++++++
 frontend/src/routes/index.tsx               |  61 ++++++++----
 frontend/tests/e2e/columns-picker.spec.ts   |  68 +++++++++++--
 frontend/tests/unit/columnOverrides.test.ts | 144 ++++++++++++++++++++++++++++
 tasks/083-persist-column-picker.md          |  46 ++++++++-
 5 files changed, 393 insertions(+), 27 deletions(-)
```

---

## Main-Thread Message

Time: 2026-06-17T12:23:25.976Z

Let me read the core implementation files.

---

## Bash Call

Time: 2026-06-17T12:23:27.928Z Description: Diff of index.tsx

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git diff main..HEAD -- frontend/src/routes/index.tsx
```

### Output

```text
diff --git a/frontend/src/routes/index.tsx b/frontend/src/routes/index.tsx
index bd57e54..0904e6e 100644
--- a/frontend/src/routes/index.tsx
+++ b/frontend/src/routes/index.tsx
@@ -11,6 +11,11 @@ import { ColumnsMenu } from "@/components/ColumnsMenu";
 import { MarketSummary } from "@/components/MarketSummary";
 import { TickerTable } from "@/components/TickerTable";
 import { ViewBar } from "@/components/ViewBar";
+import {
+  clearColumnOverride,
+  persistColumnOverride,
+  resolveColumnOverride,
+} from "@/lib/columnOverrides";
 import { GROUPS, PRESETS, type PresetView, type TickerField } from "@/lib/columns";
 import { DEFAULT_PAGE_SIZE, PAGE_SIZES } from "@/lib/pagination";
 import {
@@ -100,8 +105,9 @@ function IndexComponent() {
   // A tab switch is a destination (push, like a page step — Back walks view
   // changes) and resets to page 1. The table reseeds the sort from the new
   // preset on its own (see TickerTable), and the new preset-id reseeds the
-  // session visible set in ScreenerBody — so picker overrides are discarded on a
-  // tab switch with no extra logic. This only owns the view + page.
+  // visible set in ScreenerBody — which now restores that preset's saved
+  // column override from storage (see ScreenerBody). This only owns the view +
+  // page.
   function onViewChange(next: string) {
     navigate({ search: (prev) => ({ ...prev, view: next, page: 1 }) });
   }
@@ -139,11 +145,14 @@ function IndexComponent() {
   );
 }

-// The screener body — owns the SESSION visible-column set: seeded from the
-// active preset, mutated by the Columns picker, re-seeded whenever the active
-// preset changes (a tab switch / fresh ?view), and restored on Reset. The set
-// is session-only — never URL-encoded, so a reload restores the base ?view
-// preset (the seed re-derives from `activePreset`).
+// The screener body — owns the active preset's visible-column working set:
+// seeded from the active preset (or its saved override), mutated by the Columns
+// picker, re-seeded whenever the active preset changes (a tab switch / fresh
+// ?view), and restored on Reset. The set is never URL-encoded; instead each
+// mutation persists a per-preset override to localStorage (see lib/columnOverrides),
+// so a reload or tab switch restores that preset's saved columns rather than the
+// preset base. Storage is the cross-preset source of truth; React state holds
+// only the active preset's working copy and re-resolves from storage on switch.
 function ScreenerBody({
   activePreset,
   q,
@@ -163,9 +172,16 @@ function ScreenerBody({
   onViewChange: (id: string) => void;
   onResetPage: () => void;
 }) {
-  // The session visible-column set, seeded from the active preset.
-  const [visibleColumns, setVisibleColumns] = useState<readonly TickerField[]>(
-    activePreset.columns,
+  // The picker's column universe + order: the canonical order (the widest
+  // preset's columns). Per-field metadata comes from the IA constant, so the
+  // picker renders fully on mount — no async metadata join. Also the valid-field
+  // universe the override resolver sanitises stored sets against.
+  const canonicalOrder = useMemo(() => canonicalColumnOrder(PRESETS), []);
+
+  // The active preset's visible-column working set, seeded from its saved
+  // override (or the preset base when none/degenerate) — see lib/columnOverrides.
+  const [visibleColumns, setVisibleColumns] = useState<readonly TickerField[]>(() =>
+    resolveColumnOverride(activePreset.id, activePreset.columns, canonicalOrder),
   );
   // A monotonic signal the table watches to reseed its sort on Reset (the
   // columns reset is `setVisibleColumns` below; sort lives in TickerTable).
@@ -173,23 +189,30 @@ function ScreenerBody({

   // Re-seed the visible set the instant the active preset changes — synchronously
   // during render via the previous-id-in-state pattern (NOT a useEffect),
-  // matching TickerTable's sort reseed. Both fire on `activePreset.id`, which is
-  // exactly why a tab switch discards picker modifications with no extra logic.
+  // matching TickerTable's sort reseed. Both fire on `activePreset.id`. The
+  // reseed restores the NEW preset's saved override (same resolve as the seed),
+  // so a tab switch returns each view to its own remembered columns.
   const [prevPresetId, setPrevPresetId] = useState(activePreset.id);
   if (prevPresetId !== activePreset.id) {
     setPrevPresetId(activePreset.id);
-    setVisibleColumns(activePreset.columns);
+    setVisibleColumns(
+      resolveColumnOverride(activePreset.id, activePreset.columns, canonicalOrder),
+    );
   }

-  // The picker's column universe + order: the canonical order (the widest
-  // preset's columns). Per-field metadata comes from the IA constant, so the
-  // picker renders fully on mount — no async metadata join.
-  const canonicalOrder = useMemo(() => canonicalColumnOrder(PRESETS), []);
-
   const isModified = isColumnSetModified(visibleColumns, activePreset.columns);

+  // Persist every picker mutation as the active preset's override. The module
+  // enforces equal-to-base ⇒ delete, so toggling a column on then off clears the
+  // entry (and the marker) rather than storing a redundant set.
+  function onVisibleColumnsChange(next: TickerField[]) {
+    setVisibleColumns(next);
+    persistColumnOverride(activePreset.id, next, activePreset.columns, canonicalOrder);
+  }
+
   function onReset() {
     setVisibleColumns(activePreset.columns);
+    clearColumnOverride(activePreset.id);
     setResetNonce((n) => n + 1);
     onResetPage();
   }
@@ -207,7 +230,7 @@ function ScreenerBody({
             total={canonicalOrder.length}
             groups={GROUPS}
             visibleColumns={visibleColumns}
-            onVisibleColumnsChange={setVisibleColumns}
+            onVisibleColumnsChange={onVisibleColumnsChange}
             onReset={onReset}
             activePresetLabel={activePreset.label}
             isModified={isModified}
```

---

## Main-Thread Message

Time: 2026-06-17T12:23:30.934Z

Now let me look at `visibleColumns.ts` to understand `isColumnSetModified`, and check the existing structure.

---

## Bash Call

Time: 2026-06-17T12:23:32.854Z Description: Diff of test files

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git diff main..HEAD -- frontend/tests/unit/columnOverrides.test.ts frontend/tests/e2e/columns-picker.spec.ts
```

### Output

```text
diff --git a/frontend/tests/e2e/columns-picker.spec.ts b/frontend/tests/e2e/columns-picker.spec.ts
index c266dc3..b7dc486 100644
--- a/frontend/tests/e2e/columns-picker.spec.ts
+++ b/frontend/tests/e2e/columns-picker.spec.ts
@@ -3,8 +3,9 @@ import { expect, test } from "@playwright/test";
 // The Columns picker (079.03): a button in the view bar shows a shown/total
 // count and opens a popover to toggle which columns show. Toggling marks the
 // active tab modified and enables a footer Reset; hiding the sorted column
-// clears the sort. Overrides are session-only (no URL param). Registry-driven —
-// these specs name a few stable columns, not the full set.
+// clears the sort. Overrides persist per preset in localStorage (083), so they
+// survive a reload and a tab switch (no URL param). Registry-driven — these
+// specs name a few stable columns, not the full set.

 function columnsButton(page: import("@playwright/test").Page) {
   return page.getByRole("button", { name: /Columns/ });
@@ -93,23 +94,76 @@ test("hiding the currently-sorted column clears the sort", async ({ page }) => {
   ).toHaveCount(0);
 });

-test("the picker closes on Escape and overrides do not survive a reload", async ({
+test("the picker closes on Escape", async ({ page }) => {
+  await page.goto("/");
+  await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();
+
+  await columnsButton(page).click();
+  await expect(page.getByRole("searchbox", { name: /find a column/i })).toBeVisible();
+
+  // Esc closes the popover (the find field is gone from the DOM).
+  await page.keyboard.press("Escape");
+  await expect(page.getByRole("searchbox", { name: /find a column/i })).toHaveCount(0);
+});
+
+test("a column override survives a reload, with the modified marker", async ({
   page,
 }) => {
   await page.goto("/");
   await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();

+  // Toggle Open on (not in Default).
   await columnsButton(page).click();
   await page.getByRole("checkbox", { name: "Open" }).click();
   await expect(page.getByRole("columnheader", { name: "Open" })).toBeVisible();
+  await page.keyboard.press("Escape");

-  // Esc closes the popover (the find field is gone from the DOM).
+  // Persisted (no URL param): a reload restores the override, count and marker.
+  await page.reload();
+  await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();
+  await expect(page.getByRole("columnheader", { name: "Open" })).toBeVisible();
+  await expect(columnsButton(page)).toContainText("12/28");
+  await expect(page.getByRole("tab", { name: /Default — modified/i })).toBeVisible();
+  await expect(page).toHaveURL((url) => !url.search.includes("view"));
+});
+
+test("overrides are remembered per preset across a tab switch", async ({ page }) => {
+  await page.goto("/");
+  await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();
+
+  // Customise Default: add Open.
+  await columnsButton(page).click();
+  await page.getByRole("checkbox", { name: "Open" }).click();
+  await expect(page.getByRole("columnheader", { name: "Open" })).toBeVisible();
   await page.keyboard.press("Escape");
-  await expect(page.getByRole("searchbox", { name: /find a column/i })).toHaveCount(0);

-  // Session-only: a reload restores the base ?view (no Open, no override in URL).
+  // Switch to Returns — its own base set, no Open.
+  await page.getByRole("tab", { name: "Returns" }).click();
+  await expect(page.getByRole("columnheader", { name: "Open" })).toHaveCount(0);
+
+  // Back to Default — its saved override (with Open) is restored.
+  await page.getByRole("tab", { name: "Default" }).click();
+  await expect(page.getByRole("columnheader", { name: "Open" })).toBeVisible();
+  await expect(page.getByRole("tab", { name: /Default — modified/i })).toBeVisible();
+});
+
+test("Reset clears the stored override so a later reload returns to base", async ({
+  page,
+}) => {
+  await page.goto("/");
+  await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();
+
+  await columnsButton(page).click();
+  await page.getByRole("checkbox", { name: "Open" }).click();
+  await expect(page.getByRole("columnheader", { name: "Open" })).toBeVisible();
+
+  await page.getByRole("button", { name: /Reset to Default/ }).click();
+  await expect(page.getByRole("columnheader", { name: "Open" })).toHaveCount(0);
+
+  // Reset cleared storage too — the reload stays on the base set.
   await page.reload();
   await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();
   await expect(page.getByRole("columnheader", { name: "Open" })).toHaveCount(0);
-  await expect(page).toHaveURL((url) => !url.search.includes("view"));
+  await expect(columnsButton(page)).toContainText("11/28");
+  await expect(page.getByRole("tab", { name: /Default — modified/i })).toHaveCount(0);
 });
diff --git a/frontend/tests/unit/columnOverrides.test.ts b/frontend/tests/unit/columnOverrides.test.ts
new file mode 100644
index 0000000..2020823
--- /dev/null
+++ b/frontend/tests/unit/columnOverrides.test.ts
@@ -0,0 +1,144 @@
+import { beforeEach, describe, expect, it } from "vitest";
+
+import {
+  clearColumnOverride,
+  persistColumnOverride,
+  resolveColumnOverride,
+} from "@/lib/columnOverrides";
+
+// The persistence module owns the `tad.columns` localStorage contract: one key
+// holding a `{ [presetId]: field[] }` map. The "equal-to-base or empty ⇒ no
+// override" invariant lives here — resolve returns the base for a degenerate
+// stored set, persist deletes rather than writes a redundant entry. Generic
+// over the field type, so these tests use a synthetic field universe.
+
+const UNIVERSE = ["ticker", "name", "close", "open", "volume"] as const;
+const BASE = ["ticker", "name", "close"] as const;
+
+// happy-dom in this version exposes `localStorage` without working methods, so
+// install a minimal in-memory stub — deterministic, no real I/O. Storage is
+// shared across a file, so reset it between tests that exercise persistence.
+function installLocalStorage() {
+  const store = new Map<string, string>();
+  const stub: Storage = {
+    get length() {
+      return store.size;
+    },
+    clear: () => store.clear(),
+    getItem: (k) => (store.has(k) ? (store.get(k) as string) : null),
+    key: (i) => Array.from(store.keys())[i] ?? null,
+    removeItem: (k) => void store.delete(k),
+    setItem: (k, v) => void store.set(k, String(v)),
+  };
+  Object.defineProperty(window, "localStorage", {
+    configurable: true,
+    value: stub,
+  });
+}
+
+beforeEach(() => {
+  installLocalStorage();
+});
+
+describe("resolveColumnOverride", () => {
+  it("returns the base set when no override is stored", () => {
+    expect(resolveColumnOverride("default", BASE, UNIVERSE)).toEqual(BASE);
+  });
+
+  it("returns a validated stored override, preserving its order", () => {
+    persistColumnOverride("default", ["ticker", "open", "name"], BASE, UNIVERSE);
+    expect(resolveColumnOverride("default", BASE, UNIVERSE)).toEqual([
+      "ticker",
+      "open",
+      "name",
+    ]);
+  });
+
+  it("drops unknown fields, preserving stored order", () => {
+    window.localStorage.setItem(
+      "tad.columns",
+      JSON.stringify({ default: ["ticker", "gone", "open"] }),
+    );
+    expect(resolveColumnOverride("default", BASE, UNIVERSE)).toEqual([
+      "ticker",
+      "open",
+    ]);
+  });
+
+  it("returns base when the stored override is empty after filtering", () => {
+    window.localStorage.setItem(
+      "tad.columns",
+      JSON.stringify({ default: ["gone", "missing"] }),
+    );
+    expect(resolveColumnOverride("default", BASE, UNIVERSE)).toEqual(BASE);
+  });
+
+  it("returns base when the stored override equals the base set", () => {
+    window.localStorage.setItem(
+      "tad.columns",
+      JSON.stringify({ default: ["ticker", "name", "close"] }),
+    );
+    expect(resolveColumnOverride("default", BASE, UNIVERSE)).toEqual(BASE);
+  });
+
+  it("keys overrides per preset", () => {
+    persistColumnOverride("default", ["ticker", "open"], BASE, UNIVERSE);
+    expect(resolveColumnOverride("other", BASE, UNIVERSE)).toEqual(BASE);
+  });
+
+  it("treats a corrupt blob as no override", () => {
+    window.localStorage.setItem("tad.columns", "{not json");
+    expect(resolveColumnOverride("default", BASE, UNIVERSE)).toEqual(BASE);
+  });
+
+  it("treats a non-array entry as no override", () => {
+    window.localStorage.setItem("tad.columns", JSON.stringify({ default: "nope" }));
+    expect(resolveColumnOverride("default", BASE, UNIVERSE)).toEqual(BASE);
+  });
+});
+
+describe("persistColumnOverride", () => {
+  it("stores an override that differs from the base", () => {
+    persistColumnOverride("default", ["ticker", "open"], BASE, UNIVERSE);
+    expect(JSON.parse(window.localStorage.getItem("tad.columns") ?? "{}")).toEqual({
+      default: ["ticker", "open"],
+    });
+  });
+
+  it("deletes rather than writes an entry equal to the base", () => {
+    persistColumnOverride("default", ["ticker", "open"], BASE, UNIVERSE);
+    persistColumnOverride("default", ["ticker", "name", "close"], BASE, UNIVERSE);
+    expect(JSON.parse(window.localStorage.getItem("tad.columns") ?? "{}")).toEqual({});
+  });
+
+  it("preserves other presets' overrides when writing one", () => {
+    persistColumnOverride("a", ["ticker", "open"], BASE, UNIVERSE);
+    persistColumnOverride("b", ["ticker", "volume"], BASE, UNIVERSE);
+    expect(JSON.parse(window.localStorage.getItem("tad.columns") ?? "{}")).toEqual({
+      a: ["ticker", "open"],
+      b: ["ticker", "volume"],
+    });
+  });
+});
+
+describe("clearColumnOverride", () => {
+  it("removes a preset's stored override", () => {
+    persistColumnOverride("default", ["ticker", "open"], BASE, UNIVERSE);
+    clearColumnOverride("default");
+    expect(resolveColumnOverride("default", BASE, UNIVERSE)).toEqual(BASE);
+  });
+
+  it("leaves other presets' overrides intact", () => {
+    persistColumnOverride("a", ["ticker", "open"], BASE, UNIVERSE);
+    persistColumnOverride("b", ["ticker", "volume"], BASE, UNIVERSE);
+    clearColumnOverride("a");
+    expect(JSON.parse(window.localStorage.getItem("tad.columns") ?? "{}")).toEqual({
+      b: ["ticker", "volume"],
+    });
+  });
+
+  it("is a no-op when nothing is stored", () => {
+    clearColumnOverride("default");
+    expect(window.localStorage.getItem("tad.columns")).toBeNull();
+  });
+});
```

---

## Main-Thread Message

Time: 2026-06-17T12:23:36.628Z

Now let me verify a few things. Let me check the `canonicalColumnOrder` import in index.tsx and confirm `activePreset.id` exists, and how `PRESETS` ids work.

---

## Bash Call

Time: 2026-06-17T12:23:38.371Z Description: Head of index.tsx imports

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && sed -n '1,40p' frontend/src/routes/index.tsx
```

### Output

```text
import {
  createFileRoute,
  type SearchSchemaInput,
  stripSearchParams,
  useNavigate,
} from "@tanstack/react-router";
import { useMemo, useState } from "react";

import { AppShell } from "@/components/AppShell";
import { ColumnsMenu } from "@/components/ColumnsMenu";
import { MarketSummary } from "@/components/MarketSummary";
import { TickerTable } from "@/components/TickerTable";
import { ViewBar } from "@/components/ViewBar";
import {
  clearColumnOverride,
  persistColumnOverride,
  resolveColumnOverride,
} from "@/lib/columnOverrides";
import { GROUPS, PRESETS, type PresetView, type TickerField } from "@/lib/columns";
import { DEFAULT_PAGE_SIZE, PAGE_SIZES } from "@/lib/pagination";
import {
  canonicalColumnOrder,
  DEFAULT_VIEW_ID,
  resolveActivePreset,
} from "@/lib/views";
import { isColumnSetModified } from "@/lib/visibleColumns";

// Screener route — full app shell wrapping the existing tables, restyled.
//
// The `?q` / `?page` / `?rows` search params are the single source of truth
// for the ticker table filter and pagination: validated here, read once
// below, threaded down as props. Siblings (the top-bar search box and the
// table) stay decoupled and the view is shareable/bookmarkable.

export const Route = createFileRoute("/")({
  // All four are optional on input (a bare "/" is valid) but always present
  // on output — defaulted here so `useSearch` returns the full set. The
  // optional input is what lets `stripSearchParams` below recognise them as
  // strippable defaults. Invalid deep links are coerced, not rejected: a
  // non-positive-integer `page` falls back to 1 (the upper clamp happens at
```

---

## Bash Call

Time: 2026-06-17T12:23:39.136Z Description: Inspect columns.ts structure

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -n "id\|columns\|export\|PresetView\|canonicalColumnOrder" frontend/src/lib/columns.ts | head -50
```

### Output

```text
2:// ticker columns are labelled, grouped, role-tagged, rendered, ordered, and
11://             width, sticky). Keyed off TickerField (the snapshot's field set) so
16://   PRESETS — the curated views: ordered columns, default sort, optional
17://             derivation chain. The widest preset (Everything) is the canonical
31:export type TickerField = keyof TickerSnapshot;
33:// A feature's pipeline role. Identity columns (ticker/name/gics_sector) carry no
36:export type Role = "raw" | "intermediate" | "signal" | "gate";
38:export type Align = "left" | "right" | "center";
52://   tradeside — directional action arrow (↑ long / ↓ short / • no trade)
54:export type CellKind =
66:  | "tradeside"
72:export type ColumnSpec = {
75:  /** Column width in px. The ticker table is `table-fixed`, so this is the
76:   * authoritative rendered width (not a min); their sum is the table width. */
77:  width: number;
103:export type ColumnInfo = {
108:  /** Group id — a key in GROUPS. */
110:  /** Pipeline role; `null` for identity columns. */
116:export type ColumnConfig = ColumnInfo & RawSpec;
119:// spans a single column in the band (identity's is the empty string).
120:export type GroupInfo = {
121:  id: string;
126:export type SortDirection = "asc" | "desc";
127:export type SortNulls = "first" | "last";
131:export type SortSpec = {
139:// `defaultSort.column` (Liquidity sorts on its continuous signal, not its
141:export type ChainSpec = {
146:// A curated screener view: ordered columns, a default sort, and an optional
148:export type PresetView = {
149:  id: string;
151:  columns: TickerField[];
157:// without its definition is a compile error. Identity columns (ticker / name /
160:export const COLUMNS: Record<TickerField, ColumnConfig> = {
164:    group: "identity",
168:    width: 80,
174:    group: "identity",
178:    width: 240,
183:    group: "identity",
187:    width: 116,
196:    width: 92,
205:    width: 98,
214:    width: 106,
223:    width: 80,
232:    width: 100,
241:    width: 80,
250:    width: 84,
259:    width: 84,
268:    width: 84,
277:    width: 88,
286:    width: 120,
```

---

## Main-Thread Message

Time: 2026-06-17T12:23:47.075Z

The wiring looks correct. Let me verify the `resolveColumnOverride` return-type interaction with `useState<readonly TickerField[]>` and the reseed. The function returns `readonly T[]`, which is fine for state typed `readonly TickerField[]`.

Now let me think about one subtle correctness concern: `readMap()` returns `parsed as OverrideMap` after checking `typeof parsed === "object" && parsed !== null`. But arrays pass that check (`typeof [] === "object"`). If the stored blob is a JSON array, `readMap` returns it as an OverrideMap. Then `readMap()[presetId]` on an array with a string key returns undefined, so `resolve` returns base. In `persist`, `map = readMap()` would be an array; `delete map[presetId]`/`map[presetId] = ...` on an array with string key works (adds a property), then `writeMap` serialises. Minor but not a real-world path. Let me check the more important order-significance concern in `isColumnSetModified` and the persist filter.

Let me verify the e2e count literals against actual presets to confirm the tests are internally consistent (not a review blocker per se, but checking for off-by-one).

---

## Bash Call

Time: 2026-06-17T12:23:49.119Z Description: Check vitest env and AppShell localStorage precedent

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -rn "happy-dom\|environment" frontend/vitest.config.ts frontend/vite.config.ts 2>/dev/null; echo "---"; grep -rn "localStorage" frontend/src/components/AppShell.tsx | head
```

### Output

```text
frontend/vite.config.ts:39:    environment: "happy-dom",
---
frontend/src/components/AppShell.tsx:13:// screenshot/Storybook links — falling back to localStorage, then the
frontend/src/components/AppShell.tsx:14:// OS-level preference. Only an explicit toggle persists to localStorage:
frontend/src/components/AppShell.tsx:35:  const saved = window.localStorage.getItem(STORAGE_KEY);
frontend/src/components/AppShell.tsx:63:    window.localStorage.setItem(STORAGE_KEY, next);
```

---

## Main-Thread Message

Time: 2026-06-17T12:23:51.896Z

Let me check the AppShell precedent more fully to see if the new module diverges from the established pattern (e.g. whether AppShell guards `setItem` in try/catch — the task says "same pattern").

---

## Main-Thread Message

Time: 2026-06-17T12:24:00.054Z

The new module is actually more defensive than the AppShell precedent (try/catch on both read and write), which is fine and an improvement. Note AppShell's `readInitialTheme` doesn't guard `getItem` in try/catch but the new module does — no concern.

Now let me consider the key correctness concerns:

1. **`readMap` accepts JSON arrays as objects** — edge case, degrades gracefully (resolve returns base). Not a real-world path; below threshold.

2. **Reseed during render calls `resolveColumnOverride` which reads localStorage synchronously on every preset switch** — this is during the render phase. It's a synchronous localStorage read, fine performance-wise and matches the intended design (storage is source of truth). Not a finding.

3. **Order-significance / `persist` filter could reorder?** No — `next.filter` preserves order.

Let me verify there are no other callers of the old behaviour and that `activePreset.id` is always defined. Let me check `resolveActivePreset`.

---

## Bash Call

Time: 2026-06-17T12:24:02.035Z Description: Check preset ids and resolveActivePreset

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -n "id\b" frontend/src/lib/views.ts | head; echo "---PRESET IDS---"; grep -n "id:" frontend/src/lib/columns.ts
```

### Output

```text
11:// The literal preset id that maps to a bare URL — the stripped `?view` default.
25:/** The minimal per-column shape the band logic reads: field id + its group. */
68: * view). Identified structurally, not by id, so the IA constant stays the single
95: * Resolve the active preset for a (possibly unknown) `?view` id. An unknown id
96: * — or the literal default id — resolves to the `default` preset. Returns null
104:  const exact = presets.find((p) => p.id === viewId);
106:  return presets.find((p) => p.id === DEFAULT_VIEW_ID) ?? null;
---PRESET IDS---
121:  id: string;
149:  id: string;
420:  { id: "identity", label: "Identity", bandShort: "" },
421:  { id: "price_volume", label: "Price & Volume", bandShort: "Price" },
422:  { id: "returns", label: "Returns", bandShort: "Returns" },
423:  { id: "earnings", label: "Earnings", bandShort: "Earnings" },
424:  { id: "sector_relative", label: "Sector-relative", bandShort: "Sector" },
425:  { id: "signals", label: "Signals", bandShort: "Signals" },
426:  { id: "liquidity", label: "Liquidity", bandShort: "Liquidity" },
427:  { id: "turnover", label: "Turnover", bandShort: "Turnover" },
478:    id: "default",
497:    id: "reversal",
530:    id: "liquidity",
547:    id: "returns",
564:    id: "earnings",
578:    id: "everything",
```

---

## Main-Thread Message

Time: 2026-06-17T12:24:09.403Z

`activePreset.id` is always a non-empty string (resolveActivePreset returns a real preset or null, and the component receives a non-null `activePreset`). Good.

I have enough to conclude. Let me do a final verification pass on the one subtle thing: the `persist` filters `next` against `universe` and reorders nothing, but it drops unknown fields before the modified check. In normal operation `next` only contains known fields (the toggle helpers operate on `canonicalOrder`), so filtering is a no-op. Consistent with resolve. No issue.

Let me double-check there's no stale/duplicated logic — does `persist` re-implement what `resolve` does on its sanitisation? It shares `isColumnSetModified` (reused, not reimplemented). The filter logic is duplicated between resolve and persist (build `known` Set, filter), but that is minor internal duplication within one small module, not worth flagging as a finding (judgement-bound, immaterial).

Let me verify the e2e count `12/28` and `11/28` consistency by checking the default preset column count quickly.

---

## Bash Call

Time: 2026-06-17T12:24:10.176Z Description: Default preset columns

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && sed -n '478,500p' frontend/src/lib/columns.ts
```

### Output

```text
    id: "default",
    label: "Default",
    columns: [
      "ticker",
      "name",
      "gics_sector",
      "close",
      "ret_1d",
      "ret_21d",
      "ret_252d",
      "ret5d_z",
      "volume_ratio",
      "is_abnormal_volume",
      "is_near_earnings",
    ],
    defaultSort: { column: "ret5d_z", direction: "desc", nulls: "last" },
    chain: null,
  },
  {
    id: "reversal",
    label: "Reversal",
    columns: [
      "ticker",
```

---

## Main-Thread Message

Time: 2026-06-17T12:24:28.252Z

Default has 11 columns → `11/28` base, `12/28` after adding Open. Consistent. The implementation notes confirm `just check-all` passes including e2e.

The implementation is clean, correct, and faithful to the locked spec. The module reuses `isColumnSetModified` rather than reimplementing it (the exact AI-duplication trap the prompt flagged — avoided). Guards for SSR, corruption, and quota are all present and stronger than the AppShell precedent. The synchronous reseed preserves the prev-id-in-state pattern. No correctness, security, or design defects rise to the threshold.

---

## Review: Task 083 (Persist Column Picker Overrides per Preset)

No findings.

Every changed file was examined: `columnOverrides.ts` (new module), `routes/index.tsx` (wiring), `columnOverrides.test.ts` (unit), `columns-picker.spec.ts` (e2e flip). The diff is faithful to the locked spec and clean.

Checks that passed:

- **Reuse, not reimplementation** — the module imports `isColumnSetModified` from `visibleColumns.ts` for its "equal-to-base ⇒ no override" invariant rather than re-deriving it (the characteristic AI duplication trap; avoided).
- **localStorage guards** — `readMap`/`writeMap` both guard `typeof window === "undefined"` and wrap `getItem`+`JSON.parse` / `setItem` in `try/catch`; malformed blobs and quota/availability failures degrade to "no override" without throwing. Stronger than the `tad.theme` precedent it mirrors.
- **Resolve/persist/clear contract** — sanitises against `universe`, drops unknown fields preserving order, returns base when empty-after-filter or equal-to-base; persist deletes rather than writes a redundant entry; the empty-map case removes the key entirely. Single home for the invariant, as specified.
- **Order-significance** — `filter` preserves stored order throughout; `isColumnSetModified` is element-wise, so a reorder counts as modified. Consistent.
- **Synchronous reseed** — the prev-id-in-state render-phase block is preserved (not converted to `useEffect`); both seed and reseed call the same `resolveColumnOverride`. `canonicalOrder` correctly hoisted above the state declarations so it can feed the lazy initialiser. `isModified` unchanged, so the marker/Reset state follow for free.
- **Tests** — unit suite covers no-override, validated round-trip, unknown-field drop, empty-after-filter, equal-to-base, per-preset keying, corrupt blob, non-array entry, persist-delete, multi-preset isolation, clear. The happy-dom `localStorage` stub (noted as a deviation) is a sound deterministic substitute. E2e count literals (`11/28` base, `12/28` +Open) match the worktree's Default preset (11 columns).

Below-threshold items considered and dropped: `readMap` would accept a top-level JSON **array** as an `OverrideMap` (`typeof [] === "object"`); it degrades gracefully to base on resolve and string-key writes still serialise correctly — no real-world path produces this, confidence < 50. Minor `known`-Set + filter duplication between `resolve` and `persist` is immaterial intra-module repetition, not worth a finding.

{"critical":0,"major":0,"minor":0,"nit":0,"autofix":0,"below_threshold":1}

---

</details>

## Main-Thread Message

Time: 2026-06-17T12:24:32.626Z

Opus `/review-code`: **No findings** (clean — confirmed reuse of `isColumnSetModified`, strong guards, preserved synchronous reseed). Now waiting on the Codex adversarial review running in background. Let me check its progress.

---

## Bash Call

Time: 2026-06-17T12:24:34.639Z Description: Check codex review progress

### Command

```text
sleep 45; cat /private/tmp/claude-501/-Users-patric-github-tad/0cada52f-e4c7-4492-be3d-393ac0f59cd6/tasks/bjnpxqs8i.output 2>/dev/null | tail -40
```

### Output

```text
<tool_use_error>Blocked: sleep 45 followed by: cat /private/tmp/claude-501/-Users-patric-github-tad/0cada52f-e4c7-4492-be3d-393ac0f59cd6/tasks/bjnpxqs8i.output tail -40. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
```

---

## Bash Call

Time: 2026-06-17T12:24:39.579Z Description: Check codex review interim output

### Command

```text
cat /private/tmp/claude-501/-Users-patric-github-tad/0cada52f-e4c7-4492-be3d-393ac0f59cd6/tasks/bjnpxqs8i.output 2>/dev/null | tail -40
```

### Output

```text
[codex] Running command: /bin/zsh -lc "sed -n '1,320p' frontend/src/components/TickerTable.tsx"
[codex] Running command: /bin/zsh -lc "sed -n '1,260p' frontend/src/components/ColumnsMenu.tsx"
[codex] Command completed: /bin/zsh -lc "sed -n '1,320p' frontend/src/components/TickerTable.tsx" (exit 0)
[codex] Command completed: /bin/zsh -lc "sed -n '1,260p' frontend/src/components/ColumnsMenu.tsx" (exit 0)
[codex] Running command: /bin/zsh -lc "sed -n '320,520p' frontend/src/components/TickerTable.tsx"
[codex] Command completed: /bin/zsh -lc "sed -n '320,520p' frontend/src/components/TickerTable.tsx" (exit 0)
[codex] Running command: /bin/zsh -lc "sed -n '1,260p' frontend/src/lib/columns.ts"
[codex] Running command: /bin/zsh -lc "sed -n '1,260p' frontend/src/lib/views.ts"
[codex] Command completed: /bin/zsh -lc "sed -n '1,260p' frontend/src/lib/views.ts" (exit 0)
[codex] Command completed: /bin/zsh -lc "sed -n '1,260p' frontend/src/lib/columns.ts" (exit 0)
[codex] Running command: /bin/zsh -lc "rg -n \"localStorage|tad.theme|theme\" frontend/src/components/AppShell.tsx fro...
[codex] Command completed: /bin/zsh -lc "rg -n \"localStorage|tad.theme|theme\" frontend/src/components/AppShell.tsx fro... (exit 0)
[codex] Running command: /bin/zsh -lc "sed -n '1,120p' frontend/src/components/AppShell.tsx"
[codex] Command completed: /bin/zsh -lc "sed -n '1,120p' frontend/src/components/AppShell.tsx" (exit 0)
[codex] Running command: /bin/zsh -lc "nl -ba frontend/src/routes/index.tsx | sed -n '140,240p'"
[codex] Running command: /bin/zsh -lc "nl -ba frontend/src/lib/columnOverrides.ts | sed -n '1,140p'"
[codex] Command completed: /bin/zsh -lc "nl -ba frontend/src/routes/index.tsx | sed -n '140,240p'" (exit 0)
[codex] Command completed: /bin/zsh -lc "nl -ba frontend/src/lib/columnOverrides.ts | sed -n '1,140p'" (exit 0)
[codex] Running command: /bin/zsh -lc "nl -ba frontend/src/components/TickerTable.tsx | sed -n '225,360p'"
[codex] Command completed: /bin/zsh -lc "nl -ba frontend/src/components/TickerTable.tsx | sed -n '225,360p'" (exit 0)
[codex] Running command: /bin/zsh -lc "nl -ba frontend/src/components/ColumnsMenu.tsx | sed -n '18,80p'"
[codex] Command completed: /bin/zsh -lc "nl -ba frontend/src/components/ColumnsMenu.tsx | sed -n '18,80p'" (exit 0)
[codex] Assistant message captured: {"verdict":"needs-attention","summary":"No-ship: the new localStorage restore path trusts sem...
[codex] Turn completed.
# Codex Adversarial Review

Target: branch diff against main
Verdict: needs-attention

No-ship: the new localStorage restore path trusts semantically invalid saved arrays, so one bad `tad.columns` entry can restore an impossible column set and break the picker/table invariants on every reload.

Findings:
- [high] Stored overrides can hide the locked `ticker` column or reintroduce duplicate column ids (frontend/src/lib/columnOverrides.ts:66-70)
  `resolveColumnOverride` only filters to known field names and otherwise returns the stored array as-is. That means a syntactically valid but semantically invalid blob like `{default:["open","close"]}` restores a view with no `ticker`, even though the picker contract says Ticker is always shown, and a blob with duplicates like `{default:["ticker","open","open"]}` restores duplicate column ids. This is not just theoretical corruption: `localStorage` is untrusted persisted state, and this code explicitly advertises corruption-safe handling. Downstream, `ScreenerBody` seeds `visibleColumns` from this result and `TickerTable` maps it directly into React/TanStack column ids, so the bad state becomes user-visible and can produce a persistently broken table after reload. Normalize restored arrays to the valid invariant before returning them: de-duplicate, require mandatory columns such as `ticker`, and fall back to the preset base when the stored set cannot satisfy those invariants. Add regression tests for missing-`ticker` and duplicate-field blobs.
  Recommendation: Validate restored overrides against the full column-set invariants, not just membership in `universe`: remove duplicates, ensure required columns are present, and discard the stored override to `base` when the normalized result is invalid.

Next steps:
- Harden `resolveColumnOverride` to enforce uniqueness and mandatory columns before seeding React state.
- Add unit coverage for corrupt-but-parseable storage blobs, especially missing `ticker` and duplicated fields.
- Re-run the picker e2e flow with a preloaded invalid `tad.columns` value to confirm the UI recovers to the preset base instead of rendering a broken table.
```

---

## Main-Thread Message

Time: 2026-06-17T12:25:22.148Z

Codex returned one `[high]` finding (Opus dropped it below-threshold). Before triaging, let me verify the codebase's locked-column model so any fix is principled, not hardcoded.

---

## Bash Call

Time: 2026-06-17T12:25:24.595Z Description: Investigate locked column model

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && echo "=== locked/always-on concept ==="; grep -rn "lock\|always\|ticker" frontend/src/components/ColumnsMenu.tsx frontend/src/lib/columns.ts | grep -i "lock\|always\|sticky\|required" | head; echo ""; echo "=== does every preset start with ticker? ==="; grep -n "id:\|columns:\|\"ticker\"" frontend/src/lib/columns.ts | grep -A1 "id:" | head -40
```

### Output

```text
=== locked/always-on concept ===
frontend/src/components/ColumnsMenu.tsx:13:// checkboxes and role tags, the locked Ticker, and a footer Reset. The picker
frontend/src/components/ColumnsMenu.tsx:19:// labelShort / role / group) comes from COLUMNS. Only Ticker is locked.
frontend/src/components/ColumnsMenu.tsx:21:// The one locked identity column — always shown, never toggleable. Every other
frontend/src/components/ColumnsMenu.tsx:23:// "always-on tier" is about default visibility, not a lock.
frontend/src/components/ColumnsMenu.tsx:24:const LOCKED_FIELD: TickerField = "ticker";
frontend/src/components/ColumnsMenu.tsx:56:// signal/gate are the always-on tier — rendered at full `--fg`; raw/interm at
frontend/src/components/ColumnsMenu.tsx:261:                        {/* Assistive-tech equivalent of the lock affordance. */}
frontend/src/components/ColumnsMenu.tsx:262:                        <span className="sr-only">{info.label} is always shown</span>
frontend/src/lib/columns.ts:129:// A preset's default sort. `nulls` is always present so the table never infers

=== does every preset start with ticker? ===
121:  id: string;
149:  id: string;
151:  columns: TickerField[];
--
420:  { id: "identity", label: "Identity", bandShort: "" },
421:  { id: "price_volume", label: "Price & Volume", bandShort: "Price" },
422:  { id: "returns", label: "Returns", bandShort: "Returns" },
423:  { id: "earnings", label: "Earnings", bandShort: "Earnings" },
424:  { id: "sector_relative", label: "Sector-relative", bandShort: "Sector" },
425:  { id: "signals", label: "Signals", bandShort: "Signals" },
426:  { id: "liquidity", label: "Liquidity", bandShort: "Liquidity" },
427:  { id: "turnover", label: "Turnover", bandShort: "Turnover" },
436:  "ticker",
478:    id: "default",
480:    columns: [
--
497:    id: "reversal",
499:    columns: [
--
530:    id: "liquidity",
532:    columns: [
--
547:    id: "returns",
549:    columns: [
--
564:    id: "earnings",
566:    columns: [
--
578:    id: "everything",
580:    columns: CANONICAL_COLUMNS,
Shell cwd was reset to ~/github/tad
```

---

## Main-Thread Message

Time: 2026-06-17T12:26:08.097Z

Both reviews are in. Re-outputting for visibility:

**Opus `/review-code`** — No findings (clean). Explicitly verified reuse of `isColumnSetModified`, the SSR/corruption/quota guards, the synchronous reseed, and order-significance. It *considered* the duplicate-acceptance case and dropped it below-threshold (confidence <50, "no real-world path produces this").

**Codex adversarial review** — Verdict `needs-attention`, one finding:

- **[high] `columnOverrides.ts` — `resolveColumnOverride` trusts semantically-invalid arrays.** It filters to known field names but doesn't enforce set invariants: a syntactically-valid blob like `{default:["open","close"]}` restores a view with no locked `ticker`; `{default:["ticker","open","open"]}` restores duplicate column ids (→ duplicate React/TanStack keys → broken table). Recommends normalising restored arrays: de-duplicate, require mandatory columns (`ticker`), fall back to base when invariants can't be met; add regression tests.

**Synthesis** (one finding to triage). The two reviewers genuinely disagree on severity. Codex's "high/no-ship" leans on an untrusted-persisted-state threat model; the app's own persist path never writes such a blob (the picker locks `ticker` and `toggleColumnOn` dedupes), so the only trigger is manual localStorage tampering or a future regression. But the de-dup half is a real broken-render guard and cheap, and the module explicitly advertises corruption-safety — so completing it is honest. Realistic severity: **Minor hardening**, not a ship-blocker.

I verified the locked-column model: `LOCKED_FIELD = "ticker"` is a private constant in `ColumnsMenu`; ticker is the one locked identity column, present in every preset.

## Step 6: Review Design — Skipped

No visual change: persistence alters *which* columns appear after reload, but the rendering, layout, spacing, colour, typography and interaction states (modified marker, Reset) are all pre-existing and unchanged. No new visual surface to review.

## Step 7.1: Triage

| #   | Finding (one line)                                                              | Disposition | Reason                                                                                                                                                                                                                                                                                                    |
| --- | ------------------------------------------------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `resolveColumnOverride` doesn't enforce set invariants (dedup, locked `ticker`) | Accept      | De-dup prevents a genuinely broken render (duplicate React/TanStack column ids); locked-ticker presence completes the module's advertised corruption-safety. Cheap, scoped to the new module. Realistic severity Minor, not the no-ship Codex framed — but accepting is the safe call and closes the gap. |

Accepting → spawning the fix agent (Step 7.2).

---

## Main-Thread Message

Time: 2026-06-17T12:26:33.511Z

The module is clear. I'll hand the fix to an Opus subagent with a precise, bounded spec: de-dup always, enforce the locked column present, fall back to base otherwise — implemented generically (locked field passed as a parameter, with `LOCKED_FIELD` promoted from `ColumnsMenu` to the shared `columns.ts` so the route can supply it).

---

## Subagent 5: Fix Review Finding Task 083 [General-Purpose]

Time: 2026-06-17T12:26:55.065Z

### Prompt

Apply ONE accepted code-review fix to TAD task 083, following `/impl-task` + `/tdd` discipline (test first). You are in a git worktree — all paths root at the worktree.

WORKTREE ROOT (cd here; every path starts here): ~/github/.worktrees/tad/083-persist-column-picker Task file: tasks/083-persist-column-picker.md

THE FINDING (accepted in triage): `frontend/src/lib/columnOverrides.ts` `resolveColumnOverride` sanitises a stored override only by dropping fields not in `universe`. It does NOT enforce the column-set invariants the picker guarantees, so a syntactically-valid but semantically-invalid localStorage blob (manual tampering or a future regression) can restore a broken set:

- `{default:["ticker","open","open"]}` → duplicate column ids → duplicate React/TanStack keys → broken table render.
- `{default:["open","close"]}` → the locked `ticker` identity column missing, violating the "Ticker always shown" contract.

REQUIRED FIX (scope-bounded — do exactly this, no more):

1. Promote the locked-column constant to a shared home. Today `frontend/src/components/ColumnsMenu.tsx` defines `const LOCKED_FIELD: TickerField = "ticker";` (private). Move it to `frontend/src/lib/columns.ts` as an exported constant (pick a name consistent with that file's style, e.g. `LOCKED_COLUMN`), and update `ColumnsMenu.tsx` to import it instead of its local definition. Keep its meaning/value identical. Match the existing comment/style density in columns.ts; don't over-document.

2. Harden `resolveColumnOverride` in `frontend/src/lib/columnOverrides.ts`:
   - Add a parameter for the required/locked field(s) so the module stays generic over the field type (e.g. `required: readonly T[]`). Do NOT hardcode "ticker" inside the generic module.
   - After filtering the stored array to `universe`, ALSO de-duplicate it (preserve first-occurrence order — a valid column set never repeats an id).
   - If any `required` field is absent from the sanitised result, fall back to `base` (treat the stored override as invalid).
   - Keep the existing empty-after-sanitise ⇒ base and equal-to-base (`isColumnSetModified`) ⇒ base checks. Apply them to the sanitised (deduped) array.
   - Update the function's docstring to reflect the added invariant enforcement (dedup + required-present), concisely.
   - Consider whether `persistColumnOverride` should share the same sanitise (it currently filters to universe but doesn't dedupe). The picker never produces duplicates, so persist's input is always valid — but factoring the filter+dedupe into one small internal helper used by both keeps the invariant in one place. Do this ONLY if it stays simple; do not pass `required` to persist (persist's input is trusted picker output). Don't over-engineer.

3. Wire the new parameter at the single call site in `frontend/src/routes/index.tsx` (`ScreenerBody`): pass the locked column (imported from columns.ts) to `resolveColumnOverride` for both the initial lazy seed and the synchronous prev-id reseed. Do NOT change anything else about the seed/reseed structure.

4. Add unit tests in `frontend/tests/unit/columnOverrides.test.ts` (the existing test file) for the two new cases: a stored blob with duplicate fields resolves to a deduped set (or base if that's the correct expected behaviour given equal-to-base/required rules — reason it through), and a stored blob missing the required locked field falls back to base. Follow the existing test file's structure and its localStorage stub pattern (this repo's vitest env is happy-dom; the test installs a minimal in-memory Storage stub in beforeEach — reuse it, do NOT use real I/O).

CONSTRAINTS:

- TDD: write the failing test(s) first, then the production change.
- Do not change the localStorage key, the map shape, or any other behaviour.
- Match existing code style/conventions exactly. British spelling in prose/comments.
- Commit with `just commit "<subject incl. (task/083)>" <files>` — pass only the files for this logical change; do NOT pre-stage. Single-quote the message at the shell so $()/backticks stay literal. One commit (or two if the constant-move is cleaner separate). Title-case any heading; soft-wrap.
- Run `just check-all` from the worktree until green before finishing.

Report back: what you changed, the exact final signature of `resolveColumnOverride`, the commit hash(es)+subjects, the new test names, and the `just check-all` result.

### Response

Committed as `e9c0dcf`. Done.

## Report

Applied the accepted code-review fix to task 083 under TDD discipline (tests written first and confirmed red, then production change made them green).

### What Changed

1. **`frontend/src/lib/columns.ts`** — added exported `LOCKED_COLUMN: TickerField = "ticker"` (with a concise comment matching the file's density).
2. **`frontend/src/components/ColumnsMenu.tsx`** — removed the private `LOCKED_FIELD`, imported `LOCKED_COLUMN` from columns.ts, updated its two usages. Value/meaning unchanged.
3. **`frontend/src/lib/columnOverrides.ts`** — added an internal `sanitiseColumns` helper (filter-to-universe + de-dup, first-occurrence order) shared by both `resolveColumnOverride` and `persistColumnOverride`. `resolveColumnOverride` gained a `required` param and now falls back to `base` when the sanitised set is empty, missing any required field, or equals base. Docstring updated to reflect dedup + required-present. `persistColumnOverride` reuses the helper (no `required` passed — its input is trusted picker output).
4. **`frontend/src/routes/index.tsx`** — imported `LOCKED_COLUMN`, memoised `requiredColumns = [LOCKED_COLUMN]`, threaded it into both `resolveColumnOverride` call sites (lazy seed + synchronous prev-id reseed). No other seed/reseed structure changed.

### Final Signature of `resolveColumnOverride`

```ts
export function resolveColumnOverride<T extends string>(
  presetId: string,
  base: readonly T[],
  universe: readonly T[],
  required: readonly T[],
): readonly T[]
```

### New Tests (In `frontend/tests/unit/columnOverrides.test.ts`)

- `de-duplicates a stored override, preserving first-occurrence order` — `["ticker","open","open"]` → `["ticker","open"]`.
- `returns base when a required field is missing from the stored override` — `["open","close"]` (no ticker) → base.

Added a `REQUIRED = ["ticker"]` const and updated all existing `resolveColumnOverride` calls in the file to pass it.

### Commit

- `e9c0dcf` — Enforce column-set invariants when restoring overrides (task/083)

### Verification

`just check-all` ran fully green from the worktree (backend check, openapi-drift, frontend-check, 61 e2e, workflow-lint, markdown). columnOverrides unit suite: 16/16 pass. Working tree clean apart from the committed files. agentId: a0d6ea9456893d998 (use SendMessage with to: 'a0d6ea9456893d998' to continue this agent) <usage>subagent_tokens: 80688 tool_uses: 25 duration_ms: 208595</usage>

---

<details><summary>Inner trace (subagent session agent-a0d6ea9456893d998, depth 1)</summary>

## Main-Thread Message

Time: 2026-06-17T12:26:56.947Z

I'll start by reading the task file and the relevant source files to understand the current state.

---

## Bash Call

Time: 2026-06-17T12:26:58.388Z Description: Verify worktree and git status

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && pwd && git status
```

### Output

```text
~/github/.worktrees/tad/083-persist-column-picker
On branch task/083-persist-column-picker
nothing to commit, working tree clean
```

---

## Main-Thread Message

Time: 2026-06-17T12:27:01.245Z

Now let me look at the call site and the ColumnsMenu and columns.ts files.

---

## Main-Thread Message

Time: 2026-06-17T12:27:06.724Z

Now I have full context. Let me check `isColumnSetModified` to understand the dedup interaction.

---

## Main-Thread Message

Time: 2026-06-17T12:27:11.639Z

Now I understand everything. Let me reason through the test expectations:

- **Duplicate case `{default:["ticker","open","open"]}`** with BASE=`["ticker","name","close"]`, required=`["ticker"]`: filter→`["ticker","open","open"]`, dedup→`["ticker","open"]`, not empty, ticker present, not equal to base → resolves to `["ticker","open"]`.
- **Missing-required case `{default:["open","close"]}`** required=`["ticker"]`: filter→`["open","close"]`, dedup→`["open","close"]`, not empty, ticker absent → falls back to base.

Now, TDD: write failing tests first. Let me add the tests.

---

## Main-Thread Message

Time: 2026-06-17T12:27:16.197Z

Now I need to update all `resolveColumnOverride` call sites in the test to pass `REQUIRED`, and add the two new tests. Let me update each call.

---

## Main-Thread Message

Time: 2026-06-17T12:27:34.102Z

Now the two clearColumnOverride test call sites also use resolveColumnOverride.

---

## Main-Thread Message

Time: 2026-06-17T12:27:37.901Z

Now run the tests to confirm they fail (red).

---

## Bash Call

Time: 2026-06-17T12:27:39.014Z Description: Run columnOverrides tests (expect red)

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run test --run columnOverrides 2>&1 | tail -30
```

### Output

```text
 FAIL  tests/unit/columnOverrides.test.ts > resolveColumnOverride > returns base when a required field is missing from the stored override
AssertionError: expected [ 'open', 'close' ] to deeply equal [ 'ticker', 'name', 'close' ]

- Expected
+ Received

  [
-   "ticker",
-   "name",
+   "open",
    "close",
  ]

 ❯ tests/unit/columnOverrides.test.ts:85:72
     83|       JSON.stringify({ default: ["open", "close"] }),
     84|     );
     85|     expect(resolveColumnOverride("default", BASE, UNIVERSE, REQUIRED))…
       |                                                                        ^
     86|   });
     87|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/2]⎯


 Test Files  1 failed (1)
      Tests  2 failed | 14 passed (16)
   Start at  14:27:39
   Duration  448ms (transform 31ms, setup 59ms, import 23ms, tests 8ms, environment 211ms)

error: script "test" exited with code 1
```

---

## Main-Thread Message

Time: 2026-06-17T12:27:43.433Z

Both new tests fail as expected (dedup test and missing-required test). The duplicate test passes the dedup-less version returning `["ticker","open","open"]`? Let me confirm — actually it shows 2 failed. Good, red confirmed. Now make the production change.

First, promote the locked constant to columns.ts.

---

## Main-Thread Message

Time: 2026-06-17T12:28:01.565Z

Now replace the two `LOCKED_FIELD` usages in ColumnsMenu with `LOCKED_COLUMN`.

---

## Main-Thread Message

Time: 2026-06-17T12:28:09.018Z

Now harden `columnOverrides.ts`. I'll add a small internal `sanitise` helper (filter + dedup) used by both resolve and persist, add the `required` param to resolve.

---

## Main-Thread Message

Time: 2026-06-17T12:28:21.613Z

Now factor `persistColumnOverride` to use the shared helper (filter+dedup in one place, no `required`).

---

## Main-Thread Message

Time: 2026-06-17T12:28:27.431Z

Now wire the new param at the call site in index.tsx (two spots: lazy seed + reseed). Pass `[LOCKED_COLUMN]`.

---

## Main-Thread Message

Time: 2026-06-17T12:28:33.663Z

Now I'll define the required-columns constant once in ScreenerBody and use it in both spots, to avoid a fresh array literal each render. Let me add it near `canonicalOrder`.

---

## Main-Thread Message

Time: 2026-06-17T12:28:44.644Z

Now run the unit tests (green check).

---

## Bash Call

Time: 2026-06-17T12:28:45.562Z Description: Run columnOverrides tests (expect green)

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run test --run columnOverrides 2>&1 | tail -12
```

### Output

```text
$ vitest run --run columnOverrides

 RUN  v4.1.9 ~/github/.worktrees/tad/083-persist-column-picker/frontend


 Test Files  1 passed (1)
      Tests  16 passed (16)
   Start at  14:28:46
   Duration  358ms (transform 27ms, setup 43ms, import 22ms, tests 4ms, environment 155ms)
```

---

## Main-Thread Message

Time: 2026-06-17T12:28:49.488Z

Green. Now run full check-all from the worktree.

---

## Bash Call

Time: 2026-06-17T12:28:50.586Z Description: Run full check-all

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just check-all 2>&1 | tail -40
```

### Output

```text
[WebServer] INFO:     127.0.0.1:56508 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:56510 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  54 tests/e2e/views.spec.ts:59:1 › a fresh ?view URL loads that preset's columns and default sort (503ms)
  ✓  55 tests/e2e/views.spec.ts:77:1 › an unknown ?view falls back to Default (517ms)
[WebServer] INFO:     127.0.0.1:56534 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:56536 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:56538 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:56542 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:56535 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:56540 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  56 tests/e2e/views.spec.ts:84:1 › the group band names the column families above the headers (539ms)
[WebServer] INFO:     127.0.0.1:56553 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:56555 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:56554 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  57 tests/e2e/views.spec.ts:97:1 › the group band stays pinned when the table body scrolls vertically (566ms)
[WebServer] INFO:     127.0.0.1:56558 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:56562 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:56561 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  58 tests/e2e/views.spec.ts:128:1 › the chain rail's leading cell stays pinned over the sticky ticker on horizontal scroll (660ms)
  ✓  59 tests/e2e/views.spec.ts:162:1 › a chain view swaps the band for the derivation rail (561ms)
[WebServer] INFO:     127.0.0.1:56577 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:56579 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:56581 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:56583 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:56587 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:56586 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  60 tests/e2e/views.spec.ts:176:1 › the Liquidity chain sorts by its signal, not its boolean terminus (430ms)
  ✓  61 tests/e2e/views.spec.ts:193:1 › the active view survives a manual sort and a page step in the URL (604ms)

  61 passed (16.1s)
just workflow-lint
actionlint
just md-format
rumdl fmt .

Success: No issues found in 273 files (56ms)
just md-check
rumdl check .

Success: No issues found in 273 files (25ms)
```

---

## Main-Thread Message

Time: 2026-06-17T12:29:28.221Z

All green. Let me verify the full output didn't hide an earlier failure and check git status.

---

## Bash Call

Time: 2026-06-17T12:29:30.011Z Description: Confirm no failures and show git status

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just check-all 2>&1 | grep -iE "error|fail|✗|FAIL" | head -20; echo "---exit check done---"; git status --short
```

### Output

```text
---exit check done---
 M frontend/src/components/ColumnsMenu.tsx
 M frontend/src/lib/columnOverrides.ts
 M frontend/src/lib/columns.ts
 M frontend/src/routes/index.tsx
 M frontend/tests/unit/columnOverrides.test.ts
```

---

## Main-Thread Message

Time: 2026-06-17T12:30:08.103Z

Clean — no failures, only my five files. Now commit. This is one logical change (the constant move is small and tightly coupled to the harden), so a single commit.

---

## Bash Call

Time: 2026-06-17T12:30:12.025Z Description: Commit the change

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just commit 'Enforce column-set invariants when restoring overrides (task/083)

Why: resolveColumnOverride only dropped fields outside the universe, so a
tampered/corrupt localStorage blob could restore a broken set — duplicate
column ids (duplicate React keys) or a missing locked Ticker. Now sanitise
also de-duplicates (first-occurrence order) and falls back to the preset base
when a required field is absent. Promote the locked-column constant to
columns.ts (LOCKED_COLUMN) so the route can pass it as the required field
without the generic module hardcoding "ticker".' frontend/src/components/ColumnsMenu.tsx frontend/src/lib/columnOverrides.ts frontend/src/lib/columns.ts frontend/src/routes/index.tsx frontend/tests/unit/columnOverrides.test.ts 2>&1 | tail -15
```

### Output

```text
Staged changes:
 frontend/src/components/ColumnsMenu.tsx     | 20 +++++++------
 frontend/src/lib/columnOverrides.ts         | 44 +++++++++++++++++++++--------
 frontend/src/lib/columns.ts                 |  5 ++++
 frontend/src/routes/index.tsx               | 26 +++++++++++++++--
 frontend/tests/unit/columnOverrides.test.ts | 38 +++++++++++++++++++------
 5 files changed, 100 insertions(+), 33 deletions(-)
[task/083-persist-column-picker e9c0dcf] Enforce column-set invariants when restoring overrides (task/083)
 5 files changed, 100 insertions(+), 33 deletions(-)
```

---

## Main-Thread Message

Time: 2026-06-17T12:30:23.561Z

Committed as `e9c0dcf`. Done.

## Report

Applied the accepted code-review fix to task 083 under TDD discipline (tests written first and confirmed red, then production change made them green).

### What Changed

1. **`frontend/src/lib/columns.ts`** — added exported `LOCKED_COLUMN: TickerField = "ticker"` (with a concise comment matching the file's density).
2. **`frontend/src/components/ColumnsMenu.tsx`** — removed the private `LOCKED_FIELD`, imported `LOCKED_COLUMN` from columns.ts, updated its two usages. Value/meaning unchanged.
3. **`frontend/src/lib/columnOverrides.ts`** — added an internal `sanitiseColumns` helper (filter-to-universe + de-dup, first-occurrence order) shared by both `resolveColumnOverride` and `persistColumnOverride`. `resolveColumnOverride` gained a `required` param and now falls back to `base` when the sanitised set is empty, missing any required field, or equals base. Docstring updated to reflect dedup + required-present. `persistColumnOverride` reuses the helper (no `required` passed — its input is trusted picker output).
4. **`frontend/src/routes/index.tsx`** — imported `LOCKED_COLUMN`, memoised `requiredColumns = [LOCKED_COLUMN]`, threaded it into both `resolveColumnOverride` call sites (lazy seed + synchronous prev-id reseed). No other seed/reseed structure changed.

### Final Signature of `resolveColumnOverride`

```ts
export function resolveColumnOverride<T extends string>(
  presetId: string,
  base: readonly T[],
  universe: readonly T[],
  required: readonly T[],
): readonly T[]
```

### New Tests (In `frontend/tests/unit/columnOverrides.test.ts`)

- `de-duplicates a stored override, preserving first-occurrence order` — `["ticker","open","open"]` → `["ticker","open"]`.
- `returns base when a required field is missing from the stored override` — `["open","close"]` (no ticker) → base.

Added a `REQUIRED = ["ticker"]` const and updated all existing `resolveColumnOverride` calls in the file to pass it.

### Commit

- `e9c0dcf` — Enforce column-set invariants when restoring overrides (task/083)

### Verification

`just check-all` ran fully green from the worktree (backend check, openapi-drift, frontend-check, 61 e2e, workflow-lint, markdown). columnOverrides unit suite: 16/16 pass. Working tree clean apart from the committed files.

---

</details>

## Main-Thread Message

Time: 2026-06-17T12:30:31.047Z

Fix committed (`e9c0dcf`), check-all green. Per Step 7.2, reviewing the fix with a single Codex reviewer scoped to the fix commit.

---

## Bash Call

Time: 2026-06-17T12:30:33.813Z Description: Codex review of fix commit

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git log --oneline -1 HEAD~1 && echo "--- launching codex review of fix (base=HEAD~1) ---" && node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" adversarial-review "--background --base HEAD~1"
```

### Output

```text
Command running in background with ID: bk88nipyl. Output is being written to: /private/tmp/claude-501/-Users-patric-github-tad/0cada52f-e4c7-4492-be3d-393ac0f59cd6/tasks/bk88nipyl.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

---

## Main-Thread Message

Time: 2026-06-17T12:30:48.961Z

I'll wait for the Codex fix-review to complete (I'll be notified). Let me check interim output meanwhile.

---

## Main-Thread Message

Time: 2026-06-17T12:30:52.057Z

Codex is still analysing the fix. I'll wait for the completion notification.

---

## Main-Thread Message

Time: 2026-06-17T12:31:02.064Z

I'll wait for the Codex fix-review to finish before proceeding to Step 8.

---

## Main-Thread Message

Time: 2026-06-17T12:31:05.836Z

Still running. Waiting for the monitor to signal completion.

---

## Main-Thread Message

Time: 2026-06-17T12:31:14.459Z

I've over-scheduled — the monitor notification (and the background task completion) is the real signal and will fire well before that fallback. Waiting for the Codex fix-review to complete.

---

## Bash Call

Time: 2026-06-17T12:31:43.232Z Description: Read codex fix review verdict

### Command

```text
cat /private/tmp/claude-501/-Users-patric-github-tad/0cada52f-e4c7-4492-be3d-393ac0f59cd6/tasks/bk88nipyl.output | sed -n '/# Codex Adversarial Review/,$p'
```

### Output

```text
# Codex Adversarial Review

Target: branch diff against HEAD~1
Verdict: needs-attention

No-ship: restoring a malformed saved column override now discards the entire user customization and silently reverts to the preset base.

Findings:
- [medium] Invalid saved overrides are dropped wholesale instead of being minimally repaired (frontend/src/lib/columnOverrides.ts:87-90)
  `resolveColumnOverride` now returns the preset base whenever a stored override is missing a required field. In practice, the only required field is the locked `ticker`, so any browser that already has a persisted override from the prior bad state loses the rest of that preset's custom column choices on the next reload or view switch. This is user-visible state loss, not just validation: the code has enough information (`universe` / canonical order / required fields) to repair the saved set by re-inserting the missing locked column, but instead it throws away the whole override. I am inferring prior malformed entries are plausible because this commit is explicitly fixing restore-time invariant handling for persisted overrides.
  Recommendation: When a stored override is missing required columns, repair it instead of falling back to `base`: insert each missing required field at its canonical position, then compare the repaired sequence to `base` and persist the repaired value back to storage.

Next steps:
- Change override restoration to repair missing required columns rather than resetting to the preset base.
- Add a unit test covering a stored override that omits `ticker` but otherwise contains a valid customized order, and assert the customization survives with `ticker` restored.
```

---

## Main-Thread Message

Time: 2026-06-17T12:32:11.901Z

**Codex fix-review** returned one `[medium]` finding: the fix drops a malformed override to base instead of *repairing* it (re-inserting the missing locked `ticker` and persisting the repaired set back).

I'm **rejecting** this one, with cited reasoning:

| #   | Finding (one line)                                                       | Disposition | Reason                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| --- | ------------------------------------------------------------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Repair invalid overrides (re-insert `ticker`) instead of falling to base | Reject      | No code path produces a `ticker`-less override — the picker locks `ticker` and `persistColumnOverride` only ever writes picker output, so the "browsers with prior bad state" premise (which Codex itself hedges as inferred) doesn't exist for this solo/local app. Fall-back-to-base is the deliberate, recoverable behaviour for a degenerate set. The proposed repair also wants a `localStorage` write inside `resolveColumnOverride`, which runs in the lazy `useState` initialiser + synchronous reseed — i.e. a side-effect during React render. The cure is worse than the (non-existent) disease. |

It's `[medium]`, so rejecting is within bounds (never auto-reject Critical/Major). Recording the rejection as a follow-up note, then moving to Step 8.

---

## Main-Thread Message

Time: 2026-06-17T12:32:32.383Z

Note recorded. Committing it, then doing the Step 8 sync (rebase onto latest main).

---

## Bash Call

Time: 2026-06-17T12:32:33.080Z Description: Commit task note

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just commit 'Note rejected override-repair review follow-up (task/083)' tasks/083-persist-column-picker.md 2>&1 | tail -8
```

### Output

```text
Success: No issues found in 1 file (15ms)
Staged changes:
 tasks/083-persist-column-picker.md | 4 ++++
 1 file changed, 4 insertions(+)
[task/083-persist-column-picker 21571f7] Note rejected override-repair review follow-up (task/083)
 1 file changed, 4 insertions(+)
Shell cwd was reset to ~/github/tad
```

---

## Main-Thread Message

Time: 2026-06-17T12:32:37.931Z

## Step 8: Review Task

First, sync — rebase the worktree branch onto latest main.

---

## Bash Call

Time: 2026-06-17T12:32:38.741Z Description: Pull latest main in primary repo

### Command

```text
cd ~/github/tad && git pull --rebase origin main 2>&1 | tail -5; echo "=== main HEAD ==="; git -C ~/github/tad rev-parse --short main
```

### Output

```text
From github.com:patforna/tad
 * branch            main       -> FETCH_HEAD
Already up to date.
=== main HEAD ===
9358c06
```

---

## Main-Thread Message

Time: 2026-06-17T12:32:45.085Z

Main has advanced (`df77f86` → `9358c06`) since the worktree was created. Let me see what landed, then rebase the branch onto it.

---

## Bash Call

Time: 2026-06-17T12:32:45.914Z Description: Show new main commits and rebase worktree

### Command

```text
cd ~/github/tad && git log --oneline df77f86..9358c06; echo "=== rebasing worktree branch onto main ==="; cd ~/github/.worktrees/tad/083-persist-column-picker && git rebase main 2>&1 | tail -15
```

### Output

```text
9358c06 Hide name and sector by default across all presets
=== rebasing worktree branch onto main ===
Rebasing (1/5)Rebasing (2/5)Rebasing (3/5)Rebasing (4/5)Rebasing (5/5)Successfully rebased and updated refs/heads/task/083-persist-column-picker.
Shell cwd was reset to ~/github/tad
```

---

## Main-Thread Message

Time: 2026-06-17T12:32:56.087Z

Main's new commit "Hide name and sector by default across all presets" is the WIP I flagged at the start — now committed by Patric. It changes the Default preset's column count and touches the e2e specs. My branch rebased cleanly textually, but my e2e count literals (`11/28`, `12/28`) were written against the *old* Default preset — likely now stale. Running `just check-all` to surface any integration drift.

---

## Bash Call

Time: 2026-06-17T12:32:57.268Z Description: Run check-all after rebase

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just check-all 2>&1 | tail -40
```

### Output

```text
      127 |   await expect(page).toHaveURL((url) => !url.search.includes("view"));
      128 | });
        at ~/github/.worktrees/tad/083-persist-column-picker/frontend/tests/e2e/columns-picker.spec.ts:125:37

    Error Context: test-results/columns-picker-a-column-ov-6f809-ad-with-the-modified-marker/error-context.md

  2) tests/e2e/columns-picker.spec.ts:150:1 › Reset clears the stored override so a later reload returns to base 

    Error: expect(locator).toContainText(expected) failed

    Locator: getByRole('button', { name: /Columns/ })
    Expected substring: "11/28"
    Received string:    "Columns9/28"
    Timeout: 5000ms

    Call log:
      - Expect "toContainText" with timeout 5000ms
      - waiting for getByRole('button', { name: /Columns/ })
        14 × locator resolved to <button tabindex="0" type="button" id="base-ui-_r_8_" aria-expanded="false" aria-haspopup="dialog" data-slot="popover-trigger" data-base-ui-click-trigger="" class="inline-flex h-7 items-center gap-1.5 rounded-md border border-border-strong bg-surface px-3 text-sm font-medium whitespace-nowrap text-primary transition-colors duration-[var(--dur-fast)] ease-[var(--ease-out)] motion-reduce:transition-none hover:bg-surface-alt data-[popup-open]:bg-surface-sunken focus-visible:outline-none focus-visible:rin…>…</button>
           - unexpected value "Columns9/28"


      165 |   await expect(page.getByRole("row").filter({ hasText: "AAPL" })).toBeVisible();
      166 |   await expect(page.getByRole("columnheader", { name: "Open" })).toHaveCount(0);
    > 167 |   await expect(columnsButton(page)).toContainText("11/28");
          |                                     ^
      168 |   await expect(page.getByRole("tab", { name: /Default — modified/i })).toHaveCount(0);
      169 | });
      170 |
        at ~/github/.worktrees/tad/083-persist-column-picker/frontend/tests/e2e/columns-picker.spec.ts:167:37

    Error Context: test-results/columns-picker-Reset-clear-1a600-ater-reload-returns-to-base/error-context.md

  2 failed
    tests/e2e/columns-picker.spec.ts:109:1 › a column override survives a reload, with the modified marker 
    tests/e2e/columns-picker.spec.ts:150:1 › Reset clears the stored override so a later reload returns to base 
  59 passed (17.3s)
error: script "e2e" exited with code 1
error: Recipe `frontend-e2e` failed on line 87 with exit code 1
error: Recipe `check-all` failed on line 138 with exit code 1
Shell cwd was reset to ~/github/tad
```

---

## Main-Thread Message

Time: 2026-06-17T12:33:36.790Z

Confirmed drift: main's new commit dropped Default from 11 to 9 columns, so my e2e count literals are stale (`Columns9/28` now). Let me read the spec and fix the literals.

---

## Main-Thread Message

Time: 2026-06-17T12:33:49.500Z

New Default base is 9 (was 11), so +Open = 10. Let me check for all count literals in the file before fixing, to avoid a second round.

---

## Bash Call

Time: 2026-06-17T12:33:51.100Z Description: Find all count literals in spec

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -n "/28\|/2[0-9]\|[0-9]\{1,2\}/[0-9]" frontend/tests/e2e/columns-picker.spec.ts
```

### Output

```text
21:  await expect(columnsButton(page)).toContainText("9/28");
43:  await expect(columnsButton(page)).toContainText("10/28");
67:  await expect(columnsButton(page)).toContainText("9/28");
125:  await expect(columnsButton(page)).toContainText("12/28");
167:  await expect(columnsButton(page)).toContainText("11/28");
Shell cwd was reset to ~/github/tad
```

---

## Main-Thread Message

Time: 2026-06-17T12:33:56.981Z

Clear: the pre-existing tests (lines 21/43/67) already use the new `9/28` base. Only my two additions are stale. Fixing them — base+Open = `10/28`, base = `9/28`.

---

## Main-Thread Message

Time: 2026-06-17T12:34:09.197Z

Re-running check-all to confirm the rebase + literal fixes are green.

---

## Bash Call

Time: 2026-06-17T12:34:09.941Z Description: Re-run check-all after fixing literals

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just check-all 2>&1 | tail -25
```

### Output

```text
[WebServer] INFO:     127.0.0.1:59467 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:59471 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:59469 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  58 tests/e2e/views.spec.ts:128:1 › the chain rail's leading cell stays pinned over the sticky ticker on horizontal scroll (644ms)
  ✓  59 tests/e2e/views.spec.ts:162:1 › a chain view swaps the band for the derivation rail (481ms)
[WebServer] INFO:     127.0.0.1:59480 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:59482 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:59484 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:59487 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:59488 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:59490 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  60 tests/e2e/views.spec.ts:176:1 › the Liquidity chain sorts by its signal, not its boolean terminus (475ms)
  ✓  61 tests/e2e/views.spec.ts:193:1 › the active view survives a manual sort and a page step in the URL (591ms)

  61 passed (15.6s)
just workflow-lint
actionlint
just md-format
rumdl fmt .

Success: No issues found in 273 files (61ms)
just md-check
rumdl check .

Success: No issues found in 273 files (22ms)
Shell cwd was reset to ~/github/tad
```

---

## Main-Thread Message

Time: 2026-06-17T12:34:49.802Z

All 61 e2e pass, check-all fully green after the rebase. Committing the integration fix.

---

## Bash Call

Time: 2026-06-17T12:34:52.363Z Description: Commit e2e count fix

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just commit 'Update column-picker e2e counts after Default preset shrank (task/083)

Why: rebase onto main pulled in "Hide name and sector by default", dropping Default from 11 to 9 columns; the persistence specs added in this branch still asserted the old 11/12 counts.' frontend/tests/e2e/columns-picker.spec.ts 2>&1 | tail -8
```

### Output

```text
Staged changes:
 frontend/tests/e2e/columns-picker.spec.ts | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
[task/083-persist-column-picker 21383dd] Update column-picker e2e counts after Default preset shrank (task/083)
 1 file changed, 2 insertions(+), 2 deletions(-)
Shell cwd was reset to ~/github/tad
```

---

## Main-Thread Message

Time: 2026-06-17T12:35:08.606Z

Now the actual Step 8 task review. Let me read the review-task skill, then spawn the Opus reviewer.

---

## Subagent 6: Review Task 083 Completion [General-Purpose]

Time: 2026-06-17T12:35:27.743Z

### Prompt

Run `/review-task` for TAD task 083 — verify the task is COMPLETE per its intent and acceptance criteria. You did NOT implement this; review independently. Flag issues, do NOT fix them.

WORKTREE ROOT (cd here; all paths root here): ~/github/.worktrees/tad/083-persist-column-picker TASK FILE (read fully — intent + ACs + Implementation Notes live here): tasks/083-persist-column-picker.md DIFF under review: `git -C ~/github/.worktrees/tad/083-persist-column-picker log --oneline main..HEAD` and `git diff main..HEAD`.

Follow the `/review-task` skill:

STEP 1 — Build context: read the task and the implemented code (`frontend/src/lib/columnOverrides.ts`, `frontend/src/routes/index.tsx` ScreenerBody wiring, `frontend/src/lib/columns.ts` LOCKED_COLUMN, `frontend/src/components/ColumnsMenu.tsx`, the unit tests `frontend/tests/unit/columnOverrides.test.ts`, the e2e `frontend/tests/e2e/columns-picker.spec.ts`). Understand intent and what was built.

STEP 2 — Verify each Acceptance Criterion as pass / fail / unclear. A criterion passes ONLY with specific evidence (a test that exercises it, or observable behaviour traced in the code) — "looks like it would work" is NOT evidence; a passing test is. The five ACs:

1. After toggling columns and reloading, the picker and table show the toggled set, not the preset base.
2. Overrides remembered per preset: customise A, switch to B, switch back — A still shows its saved columns; B keeps its own.
3. Reset immediately restores the active preset's base columns AND clears its stored override — a reload afterwards stays on base, not the discarded override.
4. A stored override referencing a column no longer in the schema falls back gracefully (unknown fields dropped; empty or now-equal-to-preset behaves as no override).
5. The modified marker and Reset button reflect the restored set after reload (a restored override shows as modified).
Map each AC to the specific unit/e2e test(s) or code that demonstrate it. Note any AC with no covering test.

STEP 3 — Verify intent: does the implementation match the WHY (per-preset sticky column preference surviving reload AND tab switch, localStorage not URL)? Were plan deviations (the happy-dom Storage stub; the invariant-hardening fix adding dedup + required-`ticker`; the rejected override-repair follow-up) justified? The task notes a behaviour change: a tab switch now restores the stored override rather than reseeding from the preset — confirm that's actually what the code does.

STEP 4 — Summarise: state clearly whether the review PASSES, or list findings. Do not change status — just report the verdict and evidence. Note: `just check-all` is green (61 e2e pass) as of the latest commit; the branch is rebased onto current main.

Be honest and specific. If something is unclear or an AC lacks evidence, say so rather than rubber-stamping.

### Response

Clean working tree, and only the two relevant test files are in the branch diff. The other modified files in the parent's git status are in the main repo, not this worktree — not part of this task.

I have everything needed. Let me compile the verdict.

## Review Verdict: PASS

Task 083 is **complete** per its intent and all five acceptance criteria. The implementation matches the locked plan; deviations are justified and documented. Independent verification: 16 unit tests pass, 8 column-picker e2e specs pass (run myself in the worktree), working tree clean.

### Acceptance Criteria — All Pass (With Evidence)

**AC1 — Override survives reload.** PASS. e2e `"a column override survives a reload, with the modified marker"` (spec line 109): toggles Open on, reloads, asserts the Open columnheader visible, count `10/28`, and the `Default — modified` tab. Code path: lazy `useState` initialiser calls `resolveColumnOverride` (index.tsx:193), `onVisibleColumnsChange` persists each mutation (line 228).

**AC2 — Per-preset memory across tab switch.** PASS. e2e `"overrides are remembered per preset across a tab switch"` (line 130): customise Default (add Open) → switch to Returns (Open absent) → back to Default (Open restored + modified). The synchronous reseed block re-resolves from storage for the new preset (index.tsx:211-221). Unit test `"keys overrides per preset"` plus `"preserves other presets' overrides when writing one"` cover the keying.

**AC3 — Reset restores base AND clears storage.** PASS. e2e `"Reset clears the stored override so a later reload returns to base"` (line 150): toggle, Reset, then reload stays on base (`9/28`, no modified marker). `onReset` calls `clearColumnOverride` (index.tsx:235). Unit tests cover `clearColumnOverride` removal/isolation/no-op.

**AC4 — Stale stored field falls back gracefully.** PASS (unit-covered). `resolveColumnOverride` sanitises against the universe and falls back to base on empty/required-missing/equal-to-base. Five unit tests exercise this: drops unknown fields, de-duplicates, empty-after-filter → base, required-`ticker` missing → base, equal-to-base → base, plus corrupt-blob and non-array → base. No e2e for this (correctly — it's pure-function logic, well unit-tested).

**AC5 — Modified marker + Reset reflect restored set after reload.** PASS. The reload e2e (line 126) asserts the `Default — modified` tab post-reload; `isModified` is derived from the restored `visibleColumns` (index.tsx:223), so the marker and Reset-enabled state follow for free.

### Intent & Deviations

- **WHY met:** per-preset sticky column preference surviving reload AND tab switch via localStorage (`tad.columns`), not URL. Confirmed.
- **Behaviour change confirmed in code:** the reseed block (index.tsx:211-221) now calls `resolveColumnOverride` for the new preset rather than reseeding from `activePreset.columns` — a tab switch restores the stored override. This is the documented, intended change.
- **happy-dom Storage stub** (unit test): justified — happy-dom's `localStorage` has no working methods; the in-memory stub is deterministic and production guards (`typeof window` + try/catch) are unchanged. Sound.
- **Invariant-hardening (dedup + required-`ticker`):** `sanitiseColumns` de-duplicates and `resolveColumnOverride` requires all `required` fields. `LOCKED_COLUMN` was hoisted to `columns.ts` and reused in `ColumnsMenu` (replacing a local `LOCKED_FIELD`) and threaded as `requiredColumns`. Coherent, single-sourced.
- **Rejected override-repair follow-up:** justified — no code path produces a `ticker`-less/duplicate override, and the proposed repair would require a localStorage write inside the render-phase resolve (worse than fall-back-to-base).

### Notes (Non-Blocking)

- The universe passed to the resolver is `canonicalColumnOrder(PRESETS)` = the `everything` preset's 28 `CANONICAL_COLUMNS`. I verified every other preset's columns are a strict subset, so no legitimate field is ever silently dropped by `sanitiseColumns`. The `9/28` and other e2e count literals are correct for the committed presets.
- No `noqa`/architecture concerns; this is frontend-only, columns-only (TickerTable/sort/ColumnsMenu/ViewBar untouched as the plan required). The now-false "discarded on tab switch" comment was updated (index.tsx:154-161, 207-209).
- The three other test files in the caller's `git status` (TickerTable.test.tsx, tickers.spec.ts, views.spec.ts) are main-repo working-tree changes, **not** part of this branch — the worktree's tree is clean and the branch diff touches only the two relevant test files. Out of scope for this review.

No findings. The task can be shipped. agentId: a4eb59bb092eb1dc6 (use SendMessage with to: 'a4eb59bb092eb1dc6' to continue this agent) <usage>subagent_tokens: 73599 tool_uses: 21 duration_ms: 107847</usage>

---

<details><summary>Inner trace (subagent session agent-a4eb59bb092eb1dc6, depth 1)</summary>

## Main-Thread Message

Time: 2026-06-17T12:35:30.478Z

I'll start by reading the task file and the implemented code to build context.

---

## Bash Call

Time: 2026-06-17T12:35:31.793Z Description: Show commits and diff stat for the task branch

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git log --oneline main..HEAD && echo "---DIFFSTAT---" && git diff --stat main..HEAD
```

### Output

```text
21383dd Update column-picker e2e counts after Default preset shrank (task/083)
8e0868e Note rejected override-repair review follow-up (task/083)
961213c Enforce column-set invariants when restoring overrides (task/083)
7739850 Add task 083 implementation notes (task/083)
980fbf7 Persist column picker overrides per preset in ScreenerBody (task/083)
b0e2e9c Add per-preset column-override persistence module (task/083)
---DIFFSTAT---
 frontend/src/components/ColumnsMenu.tsx     |  20 ++--
 frontend/src/lib/columnOverrides.ts         | 121 ++++++++++++++++++++
 frontend/src/lib/columns.ts                 |   5 +
 frontend/src/routes/index.tsx               |  83 ++++++++++----
 frontend/tests/e2e/columns-picker.spec.ts   |  68 ++++++++++--
 frontend/tests/unit/columnOverrides.test.ts | 164 ++++++++++++++++++++++++++++
 tasks/083-persist-column-picker.md          |  50 ++++++++-
 7 files changed, 474 insertions(+), 37 deletions(-)
```

---

## Main-Thread Message

Time: 2026-06-17T12:35:34.157Z

Now let me read the implemented code files.

---

## Main-Thread Message

Time: 2026-06-17T12:35:38.377Z

Now the remaining files: LOCKED_COLUMN, ColumnsMenu, and the tests.

---

## Main-Thread Message

Time: 2026-06-17T12:35:42.889Z

Now let me check LOCKED_COLUMN, ColumnsMenu, and the supporting functions (isColumnSetModified, canonicalColumnOrder).

---

## Bash Call

Time: 2026-06-17T12:35:44.725Z Description: Show diffs for columns.ts and ColumnsMenu.tsx

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git diff main..HEAD -- frontend/src/lib/columns.ts frontend/src/components/ColumnsMenu.tsx
```

### Output

```text
diff --git a/frontend/src/components/ColumnsMenu.tsx b/frontend/src/components/ColumnsMenu.tsx
index 250faa5..31055c1 100644
--- a/frontend/src/components/ColumnsMenu.tsx
+++ b/frontend/src/components/ColumnsMenu.tsx
@@ -3,7 +3,13 @@ import { useId, useMemo, useRef, useState } from "react";

 import { Checkbox } from "@/components/ui/checkbox";
 import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
-import { COLUMNS, type GroupInfo, type Role, type TickerField } from "@/lib/columns";
+import {
+  COLUMNS,
+  type GroupInfo,
+  LOCKED_COLUMN,
+  type Role,
+  type TickerField,
+} from "@/lib/columns";
 import { cn } from "@/lib/utils";
 import { toggleColumnOff, toggleColumnOn, toggleGroup } from "@/lib/visibleColumns";

@@ -16,12 +22,8 @@ import { toggleColumnOff, toggleColumnOn, toggleGroup } from "@/lib/visibleColum
 //
 // Column universe + ordering = the canonical order (the `columns` prop, the
 // Everything preset in canonical order). Per-field metadata (label /
-// labelShort / role / group) comes from COLUMNS. Only Ticker is locked.
-
-// The one locked identity column — always shown, never toggleable. Every other
-// column (name, gics_sector, signals, gates) is freely toggleable: a role's
-// "always-on tier" is about default visibility, not a lock.
-const LOCKED_FIELD: TickerField = "ticker";
+// labelShort / role / group) comes from COLUMNS. Only Ticker is locked
+// (`LOCKED_COLUMN`).

 type Props = {
   /**
@@ -201,7 +203,7 @@ export function ColumnsMenu({
             // Count, tri-state, and bulk toggle act on the FULL group (allColumns)
             // — never the filtered subset — so a find never misreports the group
             // or shrinks what the header toggles.
-            const toggleable = allColumns.filter((f) => f !== LOCKED_FIELD);
+            const toggleable = allColumns.filter((f) => f !== LOCKED_COLUMN);
             const onCount = allColumns.filter((f) => visibleSet.has(f)).length;
             const toggleableOn = toggleable.filter((f) => visibleSet.has(f)).length;
             const allOn = toggleable.length > 0 && toggleableOn === toggleable.length;
@@ -247,7 +249,7 @@ export function ColumnsMenu({
                   const info = COLUMNS[field];
                   const isOn = visibleSet.has(field);
                   const role = roleLabel(info.role);
-                  if (field === LOCKED_FIELD) {
+                  if (field === LOCKED_COLUMN) {
                     return (
                       <div
                         key={field}
diff --git a/frontend/src/lib/columns.ts b/frontend/src/lib/columns.ts
index 63a28f4..16c59a7 100644
--- a/frontend/src/lib/columns.ts
+++ b/frontend/src/lib/columns.ts
@@ -30,6 +30,11 @@ type TickerSnapshot = components["schemas"]["TickerSnapshot"];
 // its definition).
 export type TickerField = keyof TickerSnapshot;

+// The one locked identity column — always shown, never toggleable in the picker,
+// and required in any restored column override. Every other column is freely
+// toggleable.
+export const LOCKED_COLUMN: TickerField = "ticker";
+
 // A feature's pipeline role. Identity columns (ticker/name/gics_sector) carry no
 // role — modelled as `null`. Defined here, not generated: it's a UI-origin tag,
 // not domain data on the wire.
```

---

## Main-Thread Message

Time: 2026-06-17T12:35:48.003Z

Now I have full context. Let me verify two things: that `canonicalColumnOrder(PRESETS)` indeed includes all valid fields (the universe), and confirm the e2e count literals match the committed presets. Let me check the views.ts and PRESETS definitions.

---

## Bash Call

Time: 2026-06-17T12:35:50.136Z Description: Inspect canonicalColumnOrder and preset ids

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -n "canonicalColumnOrder" frontend/src/lib/views.ts && echo "---DEFAULT preset columns count---" && grep -rn "id: \"default\"\|id: \"returns\"" frontend/src/lib/columns.ts
```

### Output

```text
88:export function canonicalColumnOrder(
---DEFAULT preset columns count---
frontend/src/lib/columns.ts:427:  { id: "returns", label: "Returns", bandShort: "Returns" },
frontend/src/lib/columns.ts:483:    id: "default",
frontend/src/lib/columns.ts:547:    id: "returns",
```

---

## Main-Thread Message

Time: 2026-06-17T12:36:00.249Z

Default has 9 columns (matches the `9/28` literal). The universe is the widest preset's columns. Let me confirm the canonical universe is 28 and that all preset columns are subsets of it (so `sanitiseColumns` against `canonicalOrder` won't drop legitimate fields from non-widest presets). This matters for AC4/correctness: if a preset (e.g. Default) has a column NOT in the widest preset, persisting that preset's override would silently drop it.

---

## Bash Call

Time: 2026-06-17T12:36:06.014Z Description: Verify all preset columns are subset of widest preset universe

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && cat > /tmp/check_universe.mjs << 'EOF'
import { readFileSync } from "fs";
const src = readFileSync("frontend/src/lib/columns.ts","utf8");
// crude: find PRESETS array region
const start = src.indexOf("export const PRESETS");
const region = src.slice(start);
// extract each preset block columns
const presetRe = /id:\s*"([^"]+)"[\s\S]*?columns:\s*\[([\s\S]*?)\]/g;
let m;
const presets = {};
while ((m = presetRe.exec(region))) {
  const id = m[1];
  const cols = [...m[2].matchAll(/"([^"]+)"/g)].map(x=>x[1]);
  if(!presets[id]) presets[id]=cols;
}
const lens = Object.entries(presets).map(([k,v])=>[k,v.length]);
console.log("preset lengths:", JSON.stringify(lens));
const widest = Object.entries(presets).sort((a,b)=>b[1].length-a[1].length)[0];
console.log("widest:", widest[0], widest[1].length);
const universe = new Set(presets[widest[0]]);
for(const [id,cols] of Object.entries(presets)){
  const missing = cols.filter(c=>!universe.has(c));
  if(missing.length) console.log("PRESET", id, "has fields NOT in universe:", missing);
}
console.log("universe size:", universe.size);
EOF
node /tmp/check_universe.mjs
```

### Output

```text
preset lengths: [["default",9],["reversal",10],["liquidity",5],["returns",7],["earnings",4]]
widest: reversal 10
PRESET default has fields NOT in universe: [
  'close',
  'ret_21d',
  'ret_252d',
  'volume_ratio',
  'is_abnormal_volume',
  'is_near_earnings'
]
PRESET liquidity has fields NOT in universe: [ 'volume', 'adv_20d_shares', 'volume_ratio', 'is_abnormal_volume' ]
PRESET returns has fields NOT in universe: [ 'ret_5d', 'ret_10d', 'ret_21d', 'ret_63d', 'ret_252d' ]
PRESET earnings has fields NOT in universe: [ 'last_earnings_date', 'next_earnings_date', 'is_near_earnings' ]
universe size: 10
```

---

## Main-Thread Message

Time: 2026-06-17T12:36:09.836Z

My crude regex picked up only the visible-preset `columns` arrays and got the "widest" wrong — the e2e says the universe is 28, so `widestPreset`/`canonicalColumnOrder` must derive from something larger than these 5 PRESETS columns. The regex likely missed an "Everything"/full preset. Let me look at how `widestPreset` works and find the full 28-column source.

---

## Bash Call

Time: 2026-06-17T12:36:12.171Z Description: Find widestPreset and the full-column preset source

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -n "widestPreset\|EVERYTHING\|everything\|allColumns\|canonicalColumnOrder\|PRESETS" frontend/src/lib/views.ts | head -40
```

### Output

```text
75:export function widestPreset(presets: readonly PresetView[]): PresetView | null {
88:export function canonicalColumnOrder(
91:  return widestPreset(presets)?.columns ?? [];
```

---

## Main-Thread Message

Time: 2026-06-17T12:36:16.063Z

So `canonicalColumnOrder` = the widest preset's `columns`, and the e2e asserts that's 28. My regex only matched 5 of the presets — there must be more PRESETS entries (including an "Everything" preset of 28 columns) that my regex missed. Let me list all preset ids and find the one with 28 columns.

---

## Bash Call

Time: 2026-06-17T12:36:16.736Z Description: List all preset ids

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -n "    id: \"" frontend/src/lib/columns.ts
```

### Output

```text
483:    id: "default",
500:    id: "reversal",
531:    id: "liquidity",
547:    id: "returns",
562:    id: "earnings",
569:    id: "everything",
```

---

## Main-Thread Message

Time: 2026-06-17T12:36:26.547Z

The "everything" preset uses `CANONICAL_COLUMNS` (the full 28). So the universe = `CANONICAL_COLUMNS`, and every other preset's columns are a subset of it. My earlier crude regex just didn't expand `CANONICAL_COLUMNS`. The universe correctly contains all preset columns — no silent drop concern. Let me confirm `CANONICAL_COLUMNS` length is 28 and that all preset columns are within it.

---

## Bash Call

Time: 2026-06-17T12:36:27.289Z Description: Find CANONICAL_COLUMNS definition

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && grep -n "CANONICAL_COLUMNS" frontend/src/lib/columns.ts | head
```

### Output

```text
439:const CANONICAL_COLUMNS: TickerField[] = [
571:    columns: CANONICAL_COLUMNS,
```

---

## Main-Thread Message

Time: 2026-06-17T12:36:33.331Z

28 columns confirmed (and `is_high_turnover` is the 28th). All preset columns are within this universe. Good — no silent-drop risk for legitimate fields.

Now let me run the unit tests and the e2e column-picker spec to confirm they actually pass (the task says check-all is green, but I'll verify the specific tests independently).

---

## Bash Call

Time: 2026-06-17T12:36:34.310Z Description: Run the columnOverrides unit tests

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run vitest run tests/unit/columnOverrides.test.ts 2>&1 | tail -30
```

### Output

```text
 RUN  v4.1.9 ~/github/.worktrees/tad/083-persist-column-picker/frontend


 Test Files  1 passed (1)
      Tests  16 passed (16)
   Start at  14:36:34
   Duration  421ms (transform 28ms, setup 54ms, import 21ms, tests 3ms, environment 202ms)
```

---

## Main-Thread Message

Time: 2026-06-17T12:36:37.244Z

16 unit tests pass. Now the e2e column-picker spec.

---

## Bash Call

Time: 2026-06-17T12:36:38.222Z Description: Run the columns-picker e2e spec

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run playwright test columns-picker.spec.ts 2>&1 | tail -25
```

### Output

```text
[WebServer] INFO:     127.0.0.1:60477 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60479 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60478 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  1 tests/e2e/columns-picker.spec.ts:48:1 › Reset restores the preset's columns and sort, clearing the modified marker (1.9s)
[WebServer] INFO:     127.0.0.1:60495 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60499 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60497 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60504 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60511 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60510 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  5 tests/e2e/columns-picker.spec.ts:97:1 › the picker closes on Escape (880ms)
[WebServer] INFO:     127.0.0.1:60516 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60515 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60518 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60524 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60527 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60528 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  7 tests/e2e/columns-picker.spec.ts:130:1 › overrides are remembered per preset across a tab switch (1.1s)
  ✓  6 tests/e2e/columns-picker.spec.ts:109:1 › a column override survives a reload, with the modified marker (1.1s)
[WebServer] INFO:     127.0.0.1:60535 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60537 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60539 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  8 tests/e2e/columns-picker.spec.ts:150:1 › Reset clears the stored override so a later reload returns to base (1.1s)

  8 passed (6.3s)
```

---

## Main-Thread Message

Time: 2026-06-17T12:36:48.525Z

All 8 e2e specs pass. Now let me check the other test files modified in the diff (TickerTable.test.tsx, tickers.spec.ts, views.spec.ts) to understand whether those changes are related to this task or unrelated leftovers — the parent's git status showed those as modified in the main tree, but I should check what's in the branch diff.

---

## Bash Call

Time: 2026-06-17T12:36:50.050Z Description: Check which test files are in the branch diff vs working tree

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git diff --stat main..HEAD -- frontend/tests/ && echo "===STATUS===" && git status --short
```

### Output

```text
 frontend/tests/e2e/columns-picker.spec.ts   |  68 ++++++++++--
 frontend/tests/unit/columnOverrides.test.ts | 164 ++++++++++++++++++++++++++++
 2 files changed, 225 insertions(+), 7 deletions(-)
===STATUS===
```

---

## Main-Thread Message

Time: 2026-06-17T12:37:15.531Z

Clean working tree, and only the two relevant test files are in the branch diff. The other modified files in the parent's git status are in the main repo, not this worktree — not part of this task.

I have everything needed. Let me compile the verdict.

## Review Verdict: PASS

Task 083 is **complete** per its intent and all five acceptance criteria. The implementation matches the locked plan; deviations are justified and documented. Independent verification: 16 unit tests pass, 8 column-picker e2e specs pass (run myself in the worktree), working tree clean.

### Acceptance Criteria — All Pass (With Evidence)

**AC1 — Override survives reload.** PASS. e2e `"a column override survives a reload, with the modified marker"` (spec line 109): toggles Open on, reloads, asserts the Open columnheader visible, count `10/28`, and the `Default — modified` tab. Code path: lazy `useState` initialiser calls `resolveColumnOverride` (index.tsx:193), `onVisibleColumnsChange` persists each mutation (line 228).

**AC2 — Per-preset memory across tab switch.** PASS. e2e `"overrides are remembered per preset across a tab switch"` (line 130): customise Default (add Open) → switch to Returns (Open absent) → back to Default (Open restored + modified). The synchronous reseed block re-resolves from storage for the new preset (index.tsx:211-221). Unit test `"keys overrides per preset"` plus `"preserves other presets' overrides when writing one"` cover the keying.

**AC3 — Reset restores base AND clears storage.** PASS. e2e `"Reset clears the stored override so a later reload returns to base"` (line 150): toggle, Reset, then reload stays on base (`9/28`, no modified marker). `onReset` calls `clearColumnOverride` (index.tsx:235). Unit tests cover `clearColumnOverride` removal/isolation/no-op.

**AC4 — Stale stored field falls back gracefully.** PASS (unit-covered). `resolveColumnOverride` sanitises against the universe and falls back to base on empty/required-missing/equal-to-base. Five unit tests exercise this: drops unknown fields, de-duplicates, empty-after-filter → base, required-`ticker` missing → base, equal-to-base → base, plus corrupt-blob and non-array → base. No e2e for this (correctly — it's pure-function logic, well unit-tested).

**AC5 — Modified marker + Reset reflect restored set after reload.** PASS. The reload e2e (line 126) asserts the `Default — modified` tab post-reload; `isModified` is derived from the restored `visibleColumns` (index.tsx:223), so the marker and Reset-enabled state follow for free.

### Intent & Deviations

- **WHY met:** per-preset sticky column preference surviving reload AND tab switch via localStorage (`tad.columns`), not URL. Confirmed.
- **Behaviour change confirmed in code:** the reseed block (index.tsx:211-221) now calls `resolveColumnOverride` for the new preset rather than reseeding from `activePreset.columns` — a tab switch restores the stored override. This is the documented, intended change.
- **happy-dom Storage stub** (unit test): justified — happy-dom's `localStorage` has no working methods; the in-memory stub is deterministic and production guards (`typeof window` + try/catch) are unchanged. Sound.
- **Invariant-hardening (dedup + required-`ticker`):** `sanitiseColumns` de-duplicates and `resolveColumnOverride` requires all `required` fields. `LOCKED_COLUMN` was hoisted to `columns.ts` and reused in `ColumnsMenu` (replacing a local `LOCKED_FIELD`) and threaded as `requiredColumns`. Coherent, single-sourced.
- **Rejected override-repair follow-up:** justified — no code path produces a `ticker`-less/duplicate override, and the proposed repair would require a localStorage write inside the render-phase resolve (worse than fall-back-to-base).

### Notes (Non-Blocking)

- The universe passed to the resolver is `canonicalColumnOrder(PRESETS)` = the `everything` preset's 28 `CANONICAL_COLUMNS`. I verified every other preset's columns are a strict subset, so no legitimate field is ever silently dropped by `sanitiseColumns`. The `9/28` and other e2e count literals are correct for the committed presets.
- No `noqa`/architecture concerns; this is frontend-only, columns-only (TickerTable/sort/ColumnsMenu/ViewBar untouched as the plan required). The now-false "discarded on tab switch" comment was updated (index.tsx:154-161, 207-209).
- The three other test files in the caller's `git status` (TickerTable.test.tsx, tickers.spec.ts, views.spec.ts) are main-repo working-tree changes, **not** part of this branch — the worktree's tree is clean and the branch diff touches only the two relevant test files. Out of scope for this review.

No findings. The task can be shipped.

---

</details>

## Main-Thread Message

Time: 2026-06-17T12:37:31.361Z

**Task review: PASS** — all five ACs mapped to specific passing tests, intent confirmed (per-preset sticky preference surviving reload + tab switch via localStorage), deviations justified. No findings.

Per full-mode Step 8.3, running a second independent review to confirm (nothing changed since the first pass, but the protocol asks for it).

---

## Subagent 7: Second Task Review 083 [General-Purpose]

Time: 2026-06-17T12:37:42.261Z

### Prompt

Run `/review-task` for TAD task 083 — independently verify the task is COMPLETE per its intent and acceptance criteria. This is a confirmation pass; a prior independent review passed. Be skeptical and look for anything it might have missed. Flag issues, do NOT fix them.

WORKTREE ROOT (cd here; all paths root here): ~/github/.worktrees/tad/083-persist-column-picker TASK FILE (read fully): tasks/083-persist-column-picker.md DIFF: `git -C ~/github/.worktrees/tad/083-persist-column-picker diff main..HEAD` (branch is rebased onto current main; `just check-all` is green, 61 e2e pass).

Follow `/review-task`:

1. Build context: read task + implemented code (`frontend/src/lib/columnOverrides.ts`, `frontend/src/routes/index.tsx`, `frontend/src/lib/columns.ts`, `frontend/src/components/ColumnsMenu.tsx`, `frontend/tests/unit/columnOverrides.test.ts`, `frontend/tests/e2e/columns-picker.spec.ts`).
2. Verify each of the 5 ACs (listed in the task file) as pass/fail/unclear — pass ONLY with specific evidence (a test exercising it or behaviour traced in code), not "looks right".
3. Verify intent (per-preset sticky column preference surviving reload AND tab switch, localStorage not URL) and that deviations (happy-dom Storage stub; dedup + required-ticker hardening; rejected override-repair follow-up) are justified.
4. Summarise: PASS, or list findings with evidence.

Focus your skepticism on edge cases a first pass might rubber-stamp: Does the synchronous reseed actually read storage for the NEW preset (not stale state)? Could the lazy useState initialiser read storage on every render (it must run once)? Is there any case where persisting an override and then reloading shows a DIFFERENT set than before reload (order drift)? Does `clearColumnOverride` on Reset actually remove the entry vs just emptying it? Are the e2e count literals (9/28 base, 10/28 +Open) correct for the committed presets?

Report PASS or specific findings. Be honest.

### Response

Typecheck clean. Now let me verify the AC5 "modified marker reflects restored set after reload" is genuinely traced. After reload, the lazy seed resolves the stored override → `visibleColumns` differs from `activePreset.columns` → `isModified` true → ViewBar shows "Default — modified" and Reset enabled. The e2e "a column override survives a reload, with the modified marker" asserts the `Default — modified` tab.

Let me do one final skeptical check on a subtle correctness issue: the **reseed during render writes no storage** (resolve is read-only — confirmed, `resolveColumnOverride` only calls `readMap`). And the lazy initialiser likewise read-only. So no render-phase side effects. Good — and this is exactly the rejection rationale for the override-repair follow-up.

One more: does `resolveColumnOverride` return a reference that could alias the stored array and get mutated later? It returns either `base` (the preset's `columns` array — a shared constant) or `sanitised` (a fresh array). The toggle helpers (`toggleColumnOn`/`Off`) all return fresh arrays via spread/splice/filter, never mutating in place. So returning the shared `base` reference is safe. Good.

Let me verify the rejected follow-up reasoning holds — that no code path produces a ticker-less override. The picker's locked-row branch renders ticker as a non-interactive `<div>` (no checkbox, no `handleToggle`), confirmed in ColumnsMenu lines 252-266. So ticker can never be toggled off. The rejection is sound.

All checks pass. Let me compile the verdict.

## Verdict: PASS

I independently verified task 083 (persist column-picker overrides per preset) against its intent and all 5 acceptance criteria. This is a genuine confirmation, not a rubber-stamp — I traced each skeptical edge case the prompt flagged and ran the tests myself.

### Acceptance Criteria — All PASS with Evidence

1. **Override survives reload** — Lazy `useState(() => resolveColumnOverride(...))` seeds from storage on mount. E2e "a column override survives a reload, with the modified marker" passes (toggles Open, reloads, asserts Open header + `10/28` + modified tab, no `view` URL param).
2. **Per-preset memory across tab switch** — Synchronous reseed block re-resolves storage for the NEW `activePreset.id`. E2e "overrides are remembered per preset across a tab switch" passes (Default+Open → Returns shows no Open → back to Default restores Open).
3. **Reset clears stored override** — `onReset` calls `clearColumnOverride`, which `delete`s the entry and `removeItem`s the key when the map empties (not just `{}`). E2e "Reset clears the stored override so a later reload returns to base" passes; unit tests confirm full key removal.
4. **Graceful fallback for stale/degenerate stored set** — `resolveColumnOverride` drops unknown fields (kept as partial override), de-dups, and returns base when empty / missing a required field / equal-to-base. 7 dedicated unit tests cover each branch.
5. **Modified marker/Reset reflect restored set** — `isModified = isColumnSetModified(visibleColumns, activePreset.columns)` reads true post-reload because the seed restored the override; asserted in the reload e2e.

### Skeptical Edge Cases — All Clear

- **Reseed reads new preset, not stale state**: `activePreset` is recomputed from the URL `view` each render, so on the reseed render `activePreset.id` is already the new id. Correct.
- **Lazy initialiser runs once**: function-form `useState`. Correct.
- **No order drift**: persist stores exact `next` (order preserved); resolve sanitises preserving stored order; toggle helpers emit canonical order. Round-trips identically.
- **Reset removes vs empties entry**: `removeItem` fires when map empties. Verified by unit test + e2e.
- **Count literals correct**: Default preset = 9 columns, canonical universe = 28 (counted), +Open = 10. Committed e2e `9/28` and `10/28` are correct.
- **No render-phase side effects**: `resolveColumnOverride` is read-only (validates the rejected override-repair follow-up's rationale).
- **Returned `base` reference safe**: toggle helpers never mutate in place, so sharing the preset `columns` constant is safe.
- **Required-field guard sound**: the picker locks `ticker` (non-interactive div, no toggle path), so no override can be ticker-less; the guard is purely defensive. The rejected repair follow-up is correctly out of scope.

### Tests Run (This Verification, Warm)

- `columnOverrides` unit: 16/16 pass.
- `columns-picker` e2e: 8/8 pass.
- `tsc --noEmit`: clean.
- Worktree clean; branch diff touches only the intended files (module, route, ColumnsMenu refactor, columns.ts `LOCKED_COLUMN` export, two test files, task/backlog/skill docs).

### Deviations — All Justified

- happy-dom `localStorage` stub in the unit test (env has no working Storage methods) — production `typeof window` + `try/catch` guards unchanged.
- Dedup + required-`ticker` hardening beyond the plan — defensive, single-homed in the module, well-tested.
- Override-repair rejection — sound (no path produces a malformed override; repair would need a render-phase write).

### Minor Findings (Non-Blocking, Do Not Fix)

- **Stale prose in task Implementation Notes**: the notes still cite `11/28`/`12/28` count literals, but commit `21383dd` ("Update column-picker e2e counts after Default preset shrank") corrected the committed e2e to `9/28`/`10/28`. The code is correct; only the task-file prose is out of date. Cosmetic.

No functional issues found. The implementation matches intent (localStorage not URL, per-preset, survives reload + tab switch) and all ACs are met. agentId: a1de4bcafe34ec6d5 (use SendMessage with to: 'a1de4bcafe34ec6d5' to continue this agent) <usage>subagent_tokens: 84750 tool_uses: 17 duration_ms: 116754</usage>

---

<details><summary>Inner trace (subagent session agent-a1de4bcafe34ec6d5, depth 1)</summary>

## Main-Thread Message

Time: 2026-06-17T12:37:44.418Z

I'll start by reading the task file and the implemented code to build context.

---

## Bash Call

Time: 2026-06-17T12:37:45.850Z Description: Show diff stat of branch vs main

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git diff main..HEAD --stat
```

### Output

```text
 .claude/skills/auto-task/SKILL.md           |   2 -
 .claude/skills/ship-task/SKILL.md           |   1 -
 CLAUDE.md                                   |  21 ----
 frontend/src/components/ColumnsMenu.tsx     |  20 ++--
 frontend/src/lib/columnOverrides.ts         | 121 ++++++++++++++++++++
 frontend/src/lib/columns.ts                 |   5 +
 frontend/src/routes/index.tsx               |  83 ++++++++++----
 frontend/tests/e2e/columns-picker.spec.ts   |  68 ++++++++++--
 frontend/tests/unit/columnOverrides.test.ts | 164 ++++++++++++++++++++++++++++
 tasks/083-persist-column-picker.md          |  50 ++++++++-
 tasks/_backlog.md                           |   2 -
 11 files changed, 474 insertions(+), 63 deletions(-)
```

---

## Main-Thread Message

Time: 2026-06-17T12:37:49.386Z

Let me read the implemented code files.

---

## Main-Thread Message

Time: 2026-06-17T12:37:54.764Z

Now let me read the remaining files: columns.ts, ColumnsMenu.tsx, the unit test, the e2e test, and supporting helpers.

---

## Main-Thread Message

Time: 2026-06-17T12:38:00.176Z

Now the e2e test and the visibleColumns helper.

---

## Main-Thread Message

Time: 2026-06-17T12:38:09.721Z

Now let me verify the e2e count literals. The task notes say `11/28` and `12/28` but the committed e2e test uses `9/28` and `10/28`. Let me verify the actual committed preset definitions and the canonical universe size.

The Default preset has these columns: ticker, close, ret_1d, ret_21d, ret_252d, ret5d_z, volume_ratio, is_abnormal_volume, is_near_earnings = **9 columns**.

CANONICAL_COLUMNS count: let me count — identity(3) + price_volume(3) + returns(6) + earnings(3) + sector_relative(5) + signals(2) + liquidity(3) + turnover(3) = 28. **Total = 28.** So `9/28` base, `10/28` with Open added. Correct.

Note: the task's Implementation Notes claim `11/28` and `12/28`, but the committed e2e uses `9/28` and `10/28`. That's a discrepancy between the prose note and the actual code. Let me verify what's actually committed matches the actual Default preset. The Default preset in `columns.ts` is 9 columns, so `9/28` is correct and the `11/28` in the notes is stale prose. Let me check git history to confirm the Default preset wasn't changed.

---

## Bash Call

Time: 2026-06-17T12:38:11.003Z Description: Check git log and columns.ts diff

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git log --oneline -5 && echo "---DIFF of columns.ts---" && git diff main..HEAD -- frontend/src/lib/columns.ts
```

### Output

```text
21383dd Update column-picker e2e counts after Default preset shrank (task/083)
8e0868e Note rejected override-repair review follow-up (task/083)
961213c Enforce column-set invariants when restoring overrides (task/083)
7739850 Add task 083 implementation notes (task/083)
980fbf7 Persist column picker overrides per preset in ScreenerBody (task/083)
---DIFF of columns.ts---
diff --git a/frontend/src/lib/columns.ts b/frontend/src/lib/columns.ts
index 63a28f4..16c59a7 100644
--- a/frontend/src/lib/columns.ts
+++ b/frontend/src/lib/columns.ts
@@ -30,6 +30,11 @@ type TickerSnapshot = components["schemas"]["TickerSnapshot"];
 // its definition).
 export type TickerField = keyof TickerSnapshot;

+// The one locked identity column — always shown, never toggleable in the picker,
+// and required in any restored column override. Every other column is freely
+// toggleable.
+export const LOCKED_COLUMN: TickerField = "ticker";
+
 // A feature's pipeline role. Identity columns (ticker/name/gics_sector) carry no
 // role — modelled as `null`. Defined here, not generated: it's a UI-origin tag,
 // not domain data on the wire.
```

---

## Main-Thread Message

Time: 2026-06-17T12:38:16.538Z

There's a commit `21383dd "Update column-picker e2e counts after Default preset shrank"` — this explains the `11/28`→`9/28` change. The Default preset shrank on main (it's in the rebase base), so the committed e2e counts were updated to `9/28`/`10/28` to match. The task's Implementation Notes prose (`11/28`/`12/28`) is stale relative to that fix but the actual code is correct. Good — this is a minor doc-staleness note, not a functional issue.

Now let me verify the key skeptical edge cases. First, the LOCKED_COLUMN diff — note the diff shows `LOCKED_COLUMN` was newly added in this branch but I should confirm `ColumnsMenu.tsx` already used it on main or it's part of this change.

---

## Bash Call

Time: 2026-06-17T12:38:17.343Z Description: Show ColumnsMenu diff

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git diff main..HEAD -- frontend/src/components/ColumnsMenu.tsx
```

### Output

```text
diff --git a/frontend/src/components/ColumnsMenu.tsx b/frontend/src/components/ColumnsMenu.tsx
index 250faa5..31055c1 100644
--- a/frontend/src/components/ColumnsMenu.tsx
+++ b/frontend/src/components/ColumnsMenu.tsx
@@ -3,7 +3,13 @@ import { useId, useMemo, useRef, useState } from "react";

 import { Checkbox } from "@/components/ui/checkbox";
 import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
-import { COLUMNS, type GroupInfo, type Role, type TickerField } from "@/lib/columns";
+import {
+  COLUMNS,
+  type GroupInfo,
+  LOCKED_COLUMN,
+  type Role,
+  type TickerField,
+} from "@/lib/columns";
 import { cn } from "@/lib/utils";
 import { toggleColumnOff, toggleColumnOn, toggleGroup } from "@/lib/visibleColumns";

@@ -16,12 +22,8 @@ import { toggleColumnOff, toggleColumnOn, toggleGroup } from "@/lib/visibleColum
 //
 // Column universe + ordering = the canonical order (the `columns` prop, the
 // Everything preset in canonical order). Per-field metadata (label /
-// labelShort / role / group) comes from COLUMNS. Only Ticker is locked.
-
-// The one locked identity column — always shown, never toggleable. Every other
-// column (name, gics_sector, signals, gates) is freely toggleable: a role's
-// "always-on tier" is about default visibility, not a lock.
-const LOCKED_FIELD: TickerField = "ticker";
+// labelShort / role / group) comes from COLUMNS. Only Ticker is locked
+// (`LOCKED_COLUMN`).

 type Props = {
   /**
@@ -201,7 +203,7 @@ export function ColumnsMenu({
             // Count, tri-state, and bulk toggle act on the FULL group (allColumns)
             // — never the filtered subset — so a find never misreports the group
             // or shrinks what the header toggles.
-            const toggleable = allColumns.filter((f) => f !== LOCKED_FIELD);
+            const toggleable = allColumns.filter((f) => f !== LOCKED_COLUMN);
             const onCount = allColumns.filter((f) => visibleSet.has(f)).length;
             const toggleableOn = toggleable.filter((f) => visibleSet.has(f)).length;
             const allOn = toggleable.length > 0 && toggleableOn === toggleable.length;
@@ -247,7 +249,7 @@ export function ColumnsMenu({
                   const info = COLUMNS[field];
                   const isOn = visibleSet.has(field);
                   const role = roleLabel(info.role);
-                  if (field === LOCKED_FIELD) {
+                  if (field === LOCKED_COLUMN) {
                     return (
                       <div
                         key={field}
```

---

## Main-Thread Message

Time: 2026-06-17T12:38:28.994Z

Good — `LOCKED_FIELD` was promoted to an exported `LOCKED_COLUMN` so `routes/index.tsx` can reference it for the `requiredColumns`. Clean refactor, single source of truth.

Now let me trace the skeptical edge cases carefully:

**1. Synchronous reseed reads storage for the NEW preset (not stale state):** In `routes/index.tsx`, the reseed block calls `resolveColumnOverride(activePreset.id, ...)`. Since `activePreset` is recomputed each render from the URL `view` param (`resolveActivePreset(PRESETS, view)`), when the view changes, `activePreset.id` is already the NEW preset's id on the render where `prevPresetId !== activePreset.id`. So it resolves storage for the new preset. Correct — not stale.

**2. Lazy useState initialiser runs once:** `useState(() => resolveColumnOverride(...))` — the function form runs only on mount. Correct.

**3. Order drift on reload:** `persistColumnOverride` stores the exact `next` array (sanitised, preserving order). `resolveColumnOverride` sanitises preserving stored order. The picker's toggle helpers produce canonical order. So persist→reload→resolve returns the same order. No drift.

**4. clearColumnOverride removes the entry:** Yes — `delete map[presetId]` then `writeMap`. And `writeMap` calls `removeItem` when the map becomes empty. So the key is fully removed, not left as `{}`. Verified by unit test "is a no-op when nothing is stored" and "removes a preset's stored override".

Let me check one subtle thing: the reseed condition. When a tab switch persists an override for the OLD preset and switches, then switches back — does the reseed correctly re-resolve? Let me also check: does the `onVisibleColumnsChange` persist with the correct `activePreset` at the time of the toggle? Let me verify there's no stale closure issue.

The `onVisibleColumnsChange` is a regular function recreated each render, closing over the current `activePreset`. Since it's passed fresh to `ColumnsMenu` each render, no stale closure. Correct.

Now let me verify `just check-all` is actually green and run the unit + e2e tests to confirm the claims.

---

## Bash Call

Time: 2026-06-17T12:38:30.052Z Description: Run columnOverrides unit tests

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bun run test:unit columnOverrides 2>&1 | tail -30
```

### Output

```text
error: Script not found "test:unit"
```

---

## Bash Call

Time: 2026-06-17T12:38:32.538Z Description: Show package.json scripts

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && cat package.json | grep -A30 '"scripts"'
```

### Output

```text
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest run",
    "test:watch": "vitest",
    "e2e": "playwright test",
    "check": "biome check && tsc --noEmit && vitest run",
    "postinstall": "openapi-typescript src/api/openapi.json -o src/api/schema.d.ts && tsr generate"
  },
  "devDependencies": {
    "@biomejs/biome": "^2.5.0",
    "@playwright/test": "^1.61.0",
    "@tailwindcss/vite": "^4.3.1",
    "@tanstack/router-cli": "^1.167.17",
    "@tanstack/router-plugin": "^1.168.18",
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.2",
    "@testing-library/user-event": "^14.6.1",
    "@types/node": "^25.9.2",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "@vitejs/plugin-react": "^6.0.2",
    "@vitest/ui": "^4.1.9",
    "happy-dom": "^20.10.3",
    "openapi-typescript": "^7.13.0",
    "shadcn": "^4.11.0",
    "typescript": "^6.0.3",
    "vite": "^8.0.16",
    "vitest": "^4.1.9"
  },
  "dependencies": {
```

---

## Bash Call

Time: 2026-06-17T12:38:35.267Z Description: Run columnOverrides unit tests

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bunx vitest run columnOverrides 2>&1 | tail -30
```

### Output

```text
 RUN  v4.1.9 ~/github/.worktrees/tad/083-persist-column-picker/frontend


 Test Files  1 passed (1)
      Tests  16 passed (16)
   Start at  14:38:35
   Duration  383ms (transform 26ms, setup 49ms, import 21ms, tests 4ms, environment 177ms)
```

---

## Main-Thread Message

Time: 2026-06-17T12:38:38.551Z

16 unit tests pass. Now the e2e suite for the columns picker.

---

## Bash Call

Time: 2026-06-17T12:38:39.593Z Description: Run columns-picker e2e tests

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bunx playwright test columns-picker 2>&1 | tail -25
```

### Output

```text
[WebServer] INFO:     127.0.0.1:60686 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60687 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60689 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  2 tests/e2e/columns-picker.spec.ts:48:1 › Reset restores the preset's columns and sort, clearing the modified marker (1.8s)
[WebServer] INFO:     127.0.0.1:60711 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60716 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60718 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60722 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60713 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60721 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  5 tests/e2e/columns-picker.spec.ts:97:1 › the picker closes on Escape (761ms)
[WebServer] INFO:     127.0.0.1:60724 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60726 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60728 - "GET /api/tickers HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60734 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60738 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60736 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  7 tests/e2e/columns-picker.spec.ts:130:1 › overrides are remembered per preset across a tab switch (1.1s)
  ✓  6 tests/e2e/columns-picker.spec.ts:109:1 › a column override survives a reload, with the modified marker (1.1s)
[WebServer] INFO:     127.0.0.1:60745 - "GET /api/status HTTP/1.1" 404 Not Found
[WebServer] INFO:     127.0.0.1:60746 - "GET /api/market HTTP/1.1" 200 OK
[WebServer] INFO:     127.0.0.1:60748 - "GET /api/tickers HTTP/1.1" 200 OK
  ✓  8 tests/e2e/columns-picker.spec.ts:150:1 › Reset clears the stored override so a later reload returns to base (1.1s)

  8 passed (6.1s)
```

---

## Main-Thread Message

Time: 2026-06-17T12:39:00.175Z

All 8 columns-picker e2e tests pass. Now let me verify each AC has direct test/code coverage and check the trickiest gaps.

**AC4 edge case**: "an empty or now-equal-to-preset result behaves as no override." The unit tests cover: empty after filtering → base, equal-to-base → base, unknown fields dropped, required field missing → base, dedup. Strong coverage. But the AC also says "unknown fields dropped" — i.e. a *partial* override that mixes valid + invalid fields should keep the valid ones (not fall fully back). The test "drops unknown fields, preserving stored order" confirms `["ticker","gone","open"]` → `["ticker","open"]` (kept as a valid override, not base).

Let me double-check one subtle interaction: when unknown fields are dropped and the remaining sanitised set happens to equal base, it correctly returns base. Covered logically by the `isColumnSetModified` check after sanitise.

Now, one thing worth probing: the `required` check. The Default base includes `ticker`. If a user persisted an override and then `ticker` somehow got dropped from a stored blob, resolve returns base. Good. But is there a scenario where the picker could persist a set WITHOUT ticker? The picker locks ticker (never toggleable), and `toggleColumnOff` is only wired to non-locked rows. So `ticker` always stays. The persist path stores picker output. So the required-field guard is purely defensive. Fine.

Let me verify the AC2 e2e (per-preset across tab switch) actually distinguishes per-preset memory — i.e. that Returns doesn't inherit Default's Open. The test switches to Returns and asserts Open has count 0, then back to Default and asserts Open visible. This confirms per-preset isolation and restore.

Let me check there are no other e2e tests in the broader suite that the Default-preset-shrink or persistence change might have broken (the task touched `views.spec.ts` and `tickers.spec.ts` on main per the git status — but those are in the main working tree, not this branch). Let me confirm the branch diff doesn't include unrelated test changes.

---

## Bash Call

Time: 2026-06-17T12:39:01.944Z Description: Check test file changes and worktree cleanliness

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && git diff main..HEAD --stat -- frontend/tests/ && echo "---" && git status --short
```

### Output

```text
 frontend/tests/e2e/columns-picker.spec.ts   |  68 ++++++++++--
 frontend/tests/unit/columnOverrides.test.ts | 164 ++++++++++++++++++++++++++++
 2 files changed, 225 insertions(+), 7 deletions(-)
---
```

---

## Main-Thread Message

Time: 2026-06-17T12:39:06.847Z

Clean worktree, only the columns-picker e2e and the new unit test changed. The `views.spec.ts`/`tickers.spec.ts`/`GroupBand.tsx` etc. modifications in the prompt's git status are uncommitted changes in the MAIN repo (unrelated to this task), not part of this branch.

Let me confirm the full `just check-all` claim by at least running the full unit + typecheck quickly (the heavy e2e I've already partially verified). Let me run the frontend `check` (biome + tsc + vitest).

---

## Bash Call

Time: 2026-06-17T12:39:07.655Z Description: Run TypeScript typecheck

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker/frontend && bunx tsc --noEmit 2>&1 | tail -10 && echo "TSC_EXIT=$?"
```

### Output

```text
TSC_EXIT=0
```

---

## Main-Thread Message

Time: 2026-06-17T12:39:38.919Z

Typecheck clean. Now let me verify the AC5 "modified marker reflects restored set after reload" is genuinely traced. After reload, the lazy seed resolves the stored override → `visibleColumns` differs from `activePreset.columns` → `isModified` true → ViewBar shows "Default — modified" and Reset enabled. The e2e "a column override survives a reload, with the modified marker" asserts the `Default — modified` tab.

Let me do one final skeptical check on a subtle correctness issue: the **reseed during render writes no storage** (resolve is read-only — confirmed, `resolveColumnOverride` only calls `readMap`). And the lazy initialiser likewise read-only. So no render-phase side effects. Good — and this is exactly the rejection rationale for the override-repair follow-up.

One more: does `resolveColumnOverride` return a reference that could alias the stored array and get mutated later? It returns either `base` (the preset's `columns` array — a shared constant) or `sanitised` (a fresh array). The toggle helpers (`toggleColumnOn`/`Off`) all return fresh arrays via spread/splice/filter, never mutating in place. So returning the shared `base` reference is safe. Good.

Let me verify the rejected follow-up reasoning holds — that no code path produces a ticker-less override. The picker's locked-row branch renders ticker as a non-interactive `<div>` (no checkbox, no `handleToggle`), confirmed in ColumnsMenu lines 252-266. So ticker can never be toggled off. The rejection is sound.

All checks pass. Let me compile the verdict.

## Verdict: PASS

I independently verified task 083 (persist column-picker overrides per preset) against its intent and all 5 acceptance criteria. This is a genuine confirmation, not a rubber-stamp — I traced each skeptical edge case the prompt flagged and ran the tests myself.

### Acceptance Criteria — All PASS with Evidence

1. **Override survives reload** — Lazy `useState(() => resolveColumnOverride(...))` seeds from storage on mount. E2e "a column override survives a reload, with the modified marker" passes (toggles Open, reloads, asserts Open header + `10/28` + modified tab, no `view` URL param).
2. **Per-preset memory across tab switch** — Synchronous reseed block re-resolves storage for the NEW `activePreset.id`. E2e "overrides are remembered per preset across a tab switch" passes (Default+Open → Returns shows no Open → back to Default restores Open).
3. **Reset clears stored override** — `onReset` calls `clearColumnOverride`, which `delete`s the entry and `removeItem`s the key when the map empties (not just `{}`). E2e "Reset clears the stored override so a later reload returns to base" passes; unit tests confirm full key removal.
4. **Graceful fallback for stale/degenerate stored set** — `resolveColumnOverride` drops unknown fields (kept as partial override), de-dups, and returns base when empty / missing a required field / equal-to-base. 7 dedicated unit tests cover each branch.
5. **Modified marker/Reset reflect restored set** — `isModified = isColumnSetModified(visibleColumns, activePreset.columns)` reads true post-reload because the seed restored the override; asserted in the reload e2e.

### Skeptical Edge Cases — All Clear

- **Reseed reads new preset, not stale state**: `activePreset` is recomputed from the URL `view` each render, so on the reseed render `activePreset.id` is already the new id. Correct.
- **Lazy initialiser runs once**: function-form `useState`. Correct.
- **No order drift**: persist stores exact `next` (order preserved); resolve sanitises preserving stored order; toggle helpers emit canonical order. Round-trips identically.
- **Reset removes vs empties entry**: `removeItem` fires when map empties. Verified by unit test + e2e.
- **Count literals correct**: Default preset = 9 columns, canonical universe = 28 (counted), +Open = 10. Committed e2e `9/28` and `10/28` are correct.
- **No render-phase side effects**: `resolveColumnOverride` is read-only (validates the rejected override-repair follow-up's rationale).
- **Returned `base` reference safe**: toggle helpers never mutate in place, so sharing the preset `columns` constant is safe.
- **Required-field guard sound**: the picker locks `ticker` (non-interactive div, no toggle path), so no override can be ticker-less; the guard is purely defensive. The rejected repair follow-up is correctly out of scope.

### Tests Run (This Verification, Warm)

- `columnOverrides` unit: 16/16 pass.
- `columns-picker` e2e: 8/8 pass.
- `tsc --noEmit`: clean.
- Worktree clean; branch diff touches only the intended files (module, route, ColumnsMenu refactor, columns.ts `LOCKED_COLUMN` export, two test files, task/backlog/skill docs).

### Deviations — All Justified

- happy-dom `localStorage` stub in the unit test (env has no working Storage methods) — production `typeof window` + `try/catch` guards unchanged.
- Dedup + required-`ticker` hardening beyond the plan — defensive, single-homed in the module, well-tested.
- Override-repair rejection — sound (no path produces a malformed override; repair would need a render-phase write).

### Minor Findings (Non-Blocking, Do Not Fix)

- **Stale prose in task Implementation Notes**: the notes still cite `11/28`/`12/28` count literals, but commit `21383dd` ("Update column-picker e2e counts after Default preset shrank") corrected the committed e2e to `9/28`/`10/28`. The code is correct; only the task-file prose is out of date. Cosmetic.

No functional issues found. The implementation matches intent (localStorage not URL, per-preset, survives reload + tab switch) and all ACs are met.

---

</details>

## Main-Thread Message

Time: 2026-06-17T12:39:46.562Z

Both task reviews **PASS**. The second flagged one cosmetic Nit: the task's Implementation Notes prose still cites the old `11/28`/`12/28` literals after the rebase corrected the e2e to `9/28`/`10/28`. That's a mechanical, certain fix worth making so the durable record is accurate.

---

## Main-Thread Message

Time: 2026-06-17T12:39:57.057Z

## Step 9: Wrap Up

Both reviews pass. Let me verify all work is committed, then capture the transcript and set status.

---

## Bash Call

Time: 2026-06-17T12:39:58.751Z Description: Commit note fix and show state

### Command

```text
cd ~/github/.worktrees/tad/083-persist-column-picker && just commit 'Correct e2e count literals in task notes after rebase (task/083)' tasks/083-persist-column-picker.md 2>&1 | tail -5; echo "=== status & log ==="; git status --short; echo "---"; git log --oneline main..HEAD
```

### Output

```text
Staged changes:
 tasks/083-persist-column-picker.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
[task/083-persist-column-picker a23dd11] Correct e2e count literals in task notes after rebase (task/083)
 1 file changed, 1 insertion(+), 1 deletion(-)
=== status & log ===
---
a23dd11 Correct e2e count literals in task notes after rebase (task/083)
21383dd Update column-picker e2e counts after Default preset shrank (task/083)
8e0868e Note rejected override-repair review follow-up (task/083)
961213c Enforce column-set invariants when restoring overrides (task/083)
7739850 Add task 083 implementation notes (task/083)
980fbf7 Persist column picker overrides per preset in ScreenerBody (task/083)
b0e2e9c Add per-preset column-override persistence module (task/083)
Shell cwd was reset to ~/github/tad
```

---
