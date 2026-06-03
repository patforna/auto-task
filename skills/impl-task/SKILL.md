---
name: impl-task
description: Implement a task by executing its implementation plan. Typical workflow: create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task.
---

# Implement Task

## Usage

`/impl-task <task-path> [further user instructions]`

## Goal

Implement a task by executing its implementation plan.

## Context

This skill is typically run as part of a larger workflow:

```text
create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (stored in `tasks/`) plus repo state carry everything the next agent needs.

## Guidance (DO NOT IGNORE!)

<!-- Curate as we go along. -->

These rules govern how to execute the implementation. Internalise and follow them throughout.

- Commit early and often.
- Include `(task/NNN)` in the commit.
- Look for and internalise existing style, patterns, conventions. Don't deviate unless the plan explicitly asks for it.
- Maintain the testing pyramid. Test at the lowest possible level. Few, mostly happy-path tests at the top of the pyramid (e2e, component).
- Do not use I/O, randomness, or real date/time in unit tests.
- Take small steps when uncertain, surprised, or in unfamiliar territory; bigger steps when confident. An unexpected red means shift down to smaller steps. An unexpected green means review your test with fresh eyes — there are probably gaps.

## Step 1: Task Readiness

If the task does not contain an `Implementation plan` section (usually set by `/plan-task`), stop, flag it to the user and ask how to proceed.

Otherwise, update the task status by running `just task-status <task-file> in-dev`.

## Step 2: Build Context

Read the task and the code the implementation plan will touch. If in doubt, err on the side of reading too much. Ensure you fully understand the task, implementation plan and current state of the codebase before proceeding.

## Step 3: Implement

Work through the implementation plan step by step. Re-read the implementation plan so it's fresh in your context before proceeding to the next step.

Fully read, internalise and use `/tdd` to drive implementation. Do not write or modify production code without a failing test.

### When Things Go Wrong

- If an implementation plan step seems wrong or missing, try to resolve the issue and note it down in `Implementation notes` (see below).
- If tests keep failing after 3 implementation attempts, revert to the last green state and take a smaller step.
- If the build fails on unrelated changes, flag it to the user. Don't fix silently — it may be someone else's work in progress.

## Step 4: Self-Review

After completing all planned steps, review `git diff` from your first commit to HEAD:

- Does the diff touch only what the plan requires? If not, resolve.
- Verify that each AC is demonstrably met. If not, resolve.
- Ensure there are no unwanted leftovers that you introduced (e.g. debug prints, TODO comments, commented-out or obsolete code, etc.).

## Step 5: Wrap Up

Add an `## Implementation notes` section to the end of the task file, noting anything worth flagging or preserving — in plain English. For example:

- Any deviations from the plan.
- Any surprises encountered during implementation.
- Any learnings worth codifying (incl. how).
- Any non-obvious assumptions that were made implicitly.
- Any non-obvious follow-up work not yet captured.
- etc.

Commit the task update.

## Step 6: Integrate Feedback

Wait for the user to provide feedback. Once provided, address it, commit, respond.
