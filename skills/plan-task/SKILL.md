---
name: plan-task
description: Turn a defined task into a sequenced implementation plan ready for handoff. Invoke when the user requests it.
---

# Plan Task

## Usage

`/plan-task <task-path> [optional further instructions]`

## Goal

Turn a defined task into an implementation plan that closes the decision space without doing the work.

The task definition says **what** to build and **why**. The plan says **how to verify it's built** — sequenced into steps that each prove a behaviour. The implementing agent starts in a fresh session with only the task file and the repo. The plan must be self-contained.

## Context

Phase 2 in the task workflow:

1. Explore & define (`/define-task`) — captures intent, ACs, notes
2. **Plan (`/plan-task`) — sequences the implementation (this skill)**
3. Implement (`/impl-task`) — executes in a fresh session

## What belongs in a plan

**The nervousness heuristic:** Remove the plan. Give the implementing agent just the task definition. What would you be nervous about? Those things — and only those things — belong in the plan.

Things you'd be nervous about:
- The agent extending the wrong module (name the right one)
- An existing utility the agent should reuse but wouldn't find easily (point to it)
- Non-obvious ordering between steps (sequence them)
- A constraint on approach that affects correctness (state it)

## What doesn't belong

- Pseudocode — if it reads like "code written in English", it's too detailed
- Names for new files, classes, or functions — let the agent decide from the codebase
- Implementation details derivable from reading the code
- Anything already in CLAUDE.md (testing, conventions, style)
- Universal truths ("write tests", "handle errors", "follow patterns")

## Step 1: Orient

Read the task. Read the code it will touch — at minimum the modules named in the ACs or description. Understand the current structure before deciding what to change.

If the task has an `epic:` field, read the epic for ordering and dependency context.

**Gate:** If you can confidently sequence the implementation from the ACs alone — the approach is obvious, the files are few, no tricky ordering — tell the user. The task may be simple enough to skip planning and go straight to `/impl-task`.

## Step 2: Design the plan

Sequence the work into steps. Each step names a **concrete behaviour to verify**, not an implementation instruction.

Properties of a good step:
- **Verifiable** — has a concrete check (a test, a CLI command, expected output)
- **Independent** — can fail without invalidating subsequent steps where possible
- **Behaviour-level** — describes what the system does, not how the code is structured

Sequencing strategy:
- Walking skeleton or happy path first — thinnest end-to-end path
- Then edge cases and variations
- Structural changes (refactoring) before behavioural changes when both are needed

For non-obvious approaches, briefly state why this approach over alternatives. Don't justify every decision — only where a reasonable agent might choose differently.

Add **non-goals** when scope creep is likely — name things the agent might do that it shouldn't.

### Plan format

Write the plan as a new section in the task file:

```markdown
## Implementation plan

### Approach

[One paragraph: strategy and why. For non-obvious choices, name the alternative
considered and why rejected. Omit for straightforward tasks.]

### Non-goals

- [Things the agent might do but shouldn't. Omit section if no scope creep risk.]

### Steps

1. [Behaviour to verify] → verify: [concrete check]
2. [Behaviour to verify] → verify: [concrete check]
3. [Behaviour to verify] → verify: [concrete check]
```

### Self-check

Before presenting:
1. **Nervousness test** — remove the plan, read only the ACs. Anything make you nervous? Is it addressed?
2. **Pseudocode test** — does any step describe *how* to write code? Relax it.
3. **Length test** — can the user review this in under 5 minutes? Shorten.

## Step 3: Review

Present the plan to the user. After approval, write the plan into the task file and commit.
