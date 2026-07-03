---
name: create-task
description: Use this skill to crystallise and scope an ongoing conversation into a well-defined task, capturing user intent at a high level. Typical workflow: create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task.
---

# Create Task

## Usage

`/at:create-task [further user instructions]`

## Goal

Crystallise and scope an ongoing conversation into a well-defined task, capturing user intent at a high level.

## Context

This skill is typically run as part of a larger workflow:

```text
create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file plus repo state carry everything the next agent needs.

## Task Store and Project Bindings

This plugin ships an opinionated default task convention: markdown task files in a `tasks/` directory at the repo root, managed by the agent with plain file I/O — no extra tooling required.

Projects override the defaults via **bindings** — plain-markdown files the agent reads, not machine-parsed config:

- `.claude/auto-task.config.md` — project bindings, committed, shared by everyone working in the repo.
- `.claude/auto-task.config.local.md` — personal overrides, gitignored; wins over the project file on conflict.

Precedence: plugin defaults ← project bindings ← local bindings. **If either file exists, read it before proceeding.** Recognised sections (all optional): Task Store, Verification, Worktrees, Review, Design Review, Models, Conventions, Transcript Capture, Feedback Snapshots — the plugin's `examples/auto-task.config.md` is a copy-paste template with each section's default spelled out.

## Guidance (DO NOT IGNORE!)

<!-- Curate as we go along. -->

These rules govern both how you gather intent and write the task. Internalise and follow them throughout.

- Be maximally succinct. Capture the user's intent with the fewest words that remove ambiguity. Task content length obviously follows complexity but don't pad.
- When a task has an authoritative attachment (design brief, spec, report), don't restate its content. Only capture decisions or information that's additional to the attachment.
- Don't spell out what a capable agent infers from the repo - established conventions (e.g. fail-fast), the single obvious mechanism for a change, enum values readable from a table. Test per line: would two reasonable agents build the same thing without it?
- Use plain English. Write like a human agile BA/PM writing a user story, not like a technical writer or AI producing a spec.
- Prefer short sentences and bullet points over paragraphs.
- Minimise use of backticks, emphasis, file paths, symbol names, and code mechanics - exact names and details get resolved in later stages.
- Read code to understand, not to transcribe. Read enough to describe the task accurately.
- Match scope exactly. For example: don't bundle "review X, then fix it". A review task ends at the review report; a fix task ends at the fix.
- Avoid AI-slop at all costs - both verbosity and language like "categorised by theme and priority", "promote into guardrails", "earned their keep".

## Step 1: Understand User Intent

1. Review the current conversation to identify the user's main goal and, if applicable, the agreed approach, constraints, decisions made or important insights discovered during the conversation.

    **If there is no substantial content** or the user specifically asked to **create a placeholder task**, just create the task file (see "Step 2") and delete any templated content below the title. If there was some content worth capturing, capture it as a short sentence or a few bullet points in the task. If it's unclear what the title should be, ask the user - if possible with a few recommended options for the user to select from. After creating the file, you're done.

    **Otherwise** check existing tasks, commits, code, docs, decisions, etc. to find out if there is prior art that relates or answers potentially open questions.

2. If you are unsure about the user's intent or find yourself making implicit assumptions, **stop and ask focused questions** - ideally with recommended options and one-line reasoning for the user to select from. Don't hallucinate or invent specificity.

## Step 2: Create Task File

Create the task file — by default at `tasks/{NNN}-{slug}.md` in the repo, where `{NNN}` is the next task number (max existing + 1, zero-padded to 3 digits) and `{slug}` is a short kebab-case form of the title. If the project bindings define a create-task command, use that instead. Use the table below to decide on type:

| Type       | Meaning                                     |
| ---------- | ------------------------------------------- |
| `feat`     | Product increment, new capability (Default) |
| `design`   | Visual/UI work from a design-system brief   |
| `tech`     | Refactor, cleanup, architecture             |
| `bug`      | Something broken                            |
| `research` | Research a topic or issue                   |
| `other`    | Anything else                               |

The file looks like this:

```markdown
---
title: {display_title}
date: {today}
status: new
type: {task_type}
---

## {Display_title}

TODO: Add description

### Acceptance Criteria

TODO: Add ACs

### Notes

TODO: Add notes
```

**Task states:** the frontmatter `status` progresses `new` → `ready-for-dev` (end of clarify) → `in-dev` (start of impl) → `ready-for-signoff` (end of task review) → `done` (ship). Off-ramp states: `rejected` (investigated and declined), `later` (consciously postponed).

**Attachments:** if the task comes with supporting material (a design brief, reference artifact, screenshot, sample data), put it in `tasks/attachments/{NNN}/` (next to the task files) and reference it from the task file — don't drop it as a top-level sibling.

**Committing:** commit task-file changes following the repo's commit conventions, with the task-link suffix appended to the subject (default `(task/{NNN})`; bindings § Conventions can change or drop it). If the bindings route tasks to a separate repo or provide commit recipes, follow those — task-file commits then land there, never in the code repo.

## Step 3: Write the Task

**Crystallise** the information you gathered in Step 1 and fill it into the task file sections - "Description", "Acceptance criteria", "Notes".

### Description

Describe **what** will be different after this change. Prefer a single sentence; use up to three only when genuinely justifiable. Add **why** only if it isn't obvious from the what — one clause, not a paragraph. Never narrate how the conversation arrived here ("two things came out of the discussion…", "we then realised…") — the next agent needs the decision, not the backstory.

Save the rest for the "Acceptance criteria" or "Notes" sections.

#### Examples

```markdown
# Show Ticker Data in Frontend

This task is about sending a tracerbullet through the system and surfacing some real ohlvc for a hardcoded ticker.
```

```markdown
# Get Upcoming Earnings Dates

Currently, earnings dates are only loaded up to "today".

This task is about fetching upcoming earnings dates so that we, for example, can determine if we're close to an upcoming earnings date.
```

### Acceptance Criteria

Add (just) enough ACs so that two reasonable agents would:

- agree they capture the user's intent;
- **not** build meaningfully different things;
- agree on whether the task is done.

Ensure each AC has the following properties:

- Focused on Behaviour - describes what the system does, not how it's coded. Outside-in, caller's perspective.
- Specific - names concrete inputs, outputs, or thresholds (e.g. "stocks with <20 days of history are excluded"). If necessary, anchor with a concrete example, input/output, before/after or scenario to make the intent undeniable.
- Testable - pass/fail is mechanical (a test, CLI output, observable state). No "robust", "clean", "handles edge cases".
- Boundary-aware - covers **non-obvious** edge cases that matter for correctness and an implementing agent might not discover through exploration alone (empty input, nulls, asymmetric conditions)
- Non-redundant - does not restate what implicitly applies to all tasks ("follows conventions", "tests pass", "build is green", etc.)

**Two exceptions** to the behaviour-level default:

- When structure IS the deliverable (e.g. refactoring), structural criteria are OK (e.g. "no references to compute() functions remain");
- When a formula or algorithm defines correctness, include it as specification (e.g. "sigma2_t = (1 - lambda) *r_t^2 + lambda* sigma2_{t-1}").

#### Examples

```markdown
# Get Upcoming Earnings Dates

## Acceptance Criteria

- After running `load`, the earnings-dates parquet contains existing past data + n weeks of future data.
- If future data changes (move, add, delete) and we re-run `load`, the future data in parquet reflects the latest state correctly.
- Historical rows (earnings_date <= today) are unaffected by the refresh logic.
- ...
```

```markdown
# Show Ticker Data in Frontend

## Acceptance Criteria

- When navigating to the frontend, I see a table, with a header and content like below:

  | Ticker | Close | 5d Return |
  | ------ | ----- | --------- |
  | NVDA   | $180  | 6%        |
  | TSLA   | $340  | −8%       |

- Content is delivered from backend API (close from ohlvc data, 5d return from features data)
- ...
```

**Note:** If the task description already identifies the deliverable unambiguously (e.g. "Remove the signals package and all references to it"), skip and remove the section from the task file.

### Notes

Add anything else of importance from the conversation that's not yet captured and an agent couldn't discover easily by exploring the repo.

This could include but is not limited to:

- Non-obvious insights, learnings or discoveries;
- Decisions, constraints, guidance on approach, system design, technology, implementation, etc.;
- Alternatives considered;
- etc.

Use bullet points and short sentences. If in doubt whether a note is inferable from the repo, leave it out — only keep what a capable agent couldn't discover by exploring. Clarify will surface anything load-bearing that's actually missing.

#### Examples

```markdown
# Get Upcoming Earnings Dates

## Notes

- Note that upcoming earnings dates might shift and/or new earnings dates might be added as we get closer to them.
- The easiest solution is probably to discard and re-fetch all future earnings dates whenever we're loading earnings dates as a simple/pragmatic solution for stale data issues.
- ...
```

```markdown
# Show Ticker Data in Frontend

## Notes

- This is the first task that pulls real data from the backend api. Let's slow down and be extra thoughtful in making sure we put the right patterns (code, schema, endpoints, tests, etc.) in place as future work will build on this.
- We will hardcode tickers for now (i.e. NVDA, TSLA)
- ...
```

**Note:** If there are no notes, delete the section from the task file.

## Step 4: Decompose (Only If Required)

Consider splitting the task if any of these are true:

- More than ~10 ACs
- ACs cluster into distinct themes or touch unrelated subsystems
- ACs imply a natural sequential ordering

When splitting, consider doing so along these seams:

- Walking skeleton/tracerbullet. Ship end-to-end skeleton as first task. Then add meat to the bones in subsequent tasks;
- By increase in fidelity/complexity. Ship happy path as first task. Then further iterations or increments as separate subsequent tasks;
- By natural sequential ordering. A can be shipped fully before B;
- By business rule. Each rule/variant gets its own task with isolated ACs. Good for complex rules;
- By workflow step. Each step in a multi-step flow ships independently (e.g. load → validate → persist → notify);
- By data variation. One input type/source first, others later (e.g. tickers, input sources, features, etc.);
- Functional, then non-functional - make it work, then make it fast / observable / resilient;
- etc.

**Important:**

- Don't "over-split" as decomposition incurs overhead.
- Decide whether split tasks should be bundled into an epic (i.e. a high-level task that aggregates a number of closely related sub-tasks) or split into separate standalone tasks.
- If you think a task should be split, **ALWAYS CHECK WITH THE USER FIRST** - present your rationale and proposal and **wait for approval**.

If the decision is to split into standalone tasks, simply create the standalone tasks by following steps 2 and 3.

If the decision is to split into an epic and sub-tasks, follow the steps outlined in "Appendix: Creating Epics".

## Step 5: Tighten

Run one succinctness pass before clarifying. Spawn a subagent that reads the task - and any attachment - the way the implementing agent will, with full repo access. Ask it to flag every line a capable agent wouldn't need:

- Inferable from the repo - established conventions, the single obvious mechanism, values readable from a table → cut.
- Restating an attachment the task already points at → cut.
- Load-bearing - a decision two reasonable agents would otherwise make differently → keep, or pin it with one line if it's currently only implied.
- The Description's account of how the conversation evolved is never load-bearing → cut to the compressed why.

The subagent returns proposed cuts with a one-line reason each. Apply every cut unless you can state, in one line, the specific decision two reasonable agents would otherwise make differently. "Useful context" / "helps a human reader" is not such a reason — the audience is the implementing agent, with full repo access. Bias toward cutting; keeping is the exception you justify. Run it once - don't loop.

If you decomposed into multiple tasks, run the pass on each.

## Step 6: Clarify

Run `/at:clarify-task <task-path>` in a subagent to validate whether the task would be clear to a new agent. If not, address the feedback and keep repeating until no major gaps are left.

If clarifying an epic, make sure that the epic task and all sub-tasks are clarified.

## Step 7: User Review

Present the task(s) to the user for review. The user will provide feedback if applicable and initiate next steps.

## Step 8: Offer a Feedback Snapshot (Only If Bound)

Skip this step unless the project bindings define a feedback-snapshot location. If they do, **offer** (per task, never auto-create) to snapshot the post-clarify file there as `YYYY-MM-DD-<task-slug>-before.md` — kept out of the repo so it doesn't travel with the skill.

## Appendix: Creating Epics

An epic is simply a high-level task that aggregates a number of sub-tasks.

To create an epic, follow the instructions for creating a standalone task. Drop the `Acceptance criteria` section and instead add a `Tasks` section to the end. Example:

```markdown
## Tasks

| #   | Task                      | File                     | Status |
| --- | ------------------------- | ------------------------ | ------ |
| 01  | Implement Reversal Signal | 012.01-signal.md         | new    |
| 02  | Filters and Gates         | 012.02-filters-gates.md  | new    |
| 03  | Remove SL/TP              | 012.03-remove-sltp.md    | new    |
| 04  | Multi-Day Holding         | 012.04-multi-day-hold.md | new    |
```

### Epic Sub-Tasks

Epic sub-tasks are like standalone tasks, except their file name is slightly different to keep them lexicographically close to the epic task.

To create an epic sub-task file, follow the instructions for creating a standalone task, but use the following file format: `<EpicNbr>.<NN><task slug>.md` (e.g. `012.03-remove-sltp.md`). The numbers of the tasks belonging to the epic are zero-padded (`01`, `02`, ... `10`, `11`). Example:

```text
015-reversal-eval.md        ← epic
015.01-cli-knobs.md         ← task 1
015.02-pnl-concentration.md ← task 2
```

**Important**: When creating an epic sub-task, **update the epic's tasks table** so that it includes the new sub-task and status.
