---
name: plan-task
description: Write an implementation plan for a well-defined task. Typical workflow: create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task.
---

# Plan Task

## Usage

`/at:plan-task <task-path> [further user instructions]`

## Goal

Given a well-defined task (the "why" and "what"), write an implementation plan (the "how") that closes the decision space for an implementing agent.

## Context

This skill is typically run as part of a larger workflow:

```text
create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (stored in the `tad-tasks` repo at `~/github/tad-tasks/`) plus repo state carry everything the next agent needs.

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

If the task's status is not `ready-for-dev` (usually set at the end of `/at:clarify-task`), flag it to the user and ask how to proceed.

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

Re-read the Guidance section (incl. Anti-Patterns). For each step in the plan, ask whether it violates the Guidance. If it does and there's no strong reason for doing so, re-work the plan once.

<!-- Note: According to research, additional self-reflection loops without external signal degrades quality more often than it helps -->

## Step 5: Present

Present the plan to the user.

## Step 6: Write Plan to Task (Optional)

If the user instructed you to do so, write the Implementation Plan section to the task file.
