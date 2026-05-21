---
name: clarify-task
description: Use this skill to resolve ambiguities, clarify vague criteria and make implicit assumptions explicit. Invoked at the end of /create-task and the start of /plan-task. Typical workflow: create-task → clarify-task → plan-task → impl-task → code-review → review-task → ship-task.
---

# Clarify Task

## Usage

`/clarify-task <task-path> [further user instructions]`

## Goal

Ensure the task is clear enough so that two reasonable agents - with access to the task content and repo only - would neither complete the task in a meaningfully different way nor disagree on whether the task is done.

## Context

This skill is typically run as part of a larger workflow:

```text
create-task → clarify-task → plan-task → impl-task → code-review → review-task → ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (stored in `tasks/`) plus repo state carry everything the next agent needs.

## Step 1: Understand the task

- Read the task and explore the relevant parts of the codebase to make sure you fully understand what the task is about and ground your questions.
- If you detect ambiguity, vagueness or implicit assumptions, do another round of deeper exploration and try to resolve.

## Step 2: Identify issues

If after completing Step 1 you conclude that two reasonable agents - with access to the task content and repo only - would either complete the task in a meaningfully different way or disagree on whether the task is done, flag it to the user.

Triggers (non-exhaustive):

- Motivation missing - task says *what* but not *why*.
- Incomplete content - trailing-off sentences, TODOs, TBDs, "should we...?", etc.
- Acceptance criteria weak - vague, untestable, or missing boundary/edge cases (see `/create-task` § Acceptance criteria).
- Unclear scope - a criterion two reasonable agents would read differently.
- Semantic ambiguity - same term, field, column, etc. meaning different things (e.g. "days" = calendar or trading?).
- Implicit assumptions - things the implementer must assume that aren't stated.

## Step 3: Surface and clarify issues with user

If anything from the previous step needs clarification, flag it to the user and wait for the user to answer.

Make sure that each feedback item:

- Has a number for reference.
- States the issue clearly and succinctly.
- Proposes a recommended answer with one-line reasoning, and names the alternative if (and only if) applicable/reasonable - to make it easy for a user to confirm or override.

If there are no substantial issues to surface or none left, reply with a short one-liner saying that the task seems clear.

## Step 4: Update the task

Integrate the feedback from Step 3 into the task file.

When editing the task file:

- Strictly follow the `/create-task` skill's "Guidance" section and "Step 3: Write the task".
- Do not make any edits beyond what's strictly necessary to integrate the feedback (exception: fixing obvious typos - please do without asking).

## Step 5: Verify

Spawn a sub-agent to re-run Steps 1–2 on the updated task and report any remaining issues. If new issues surface, address them via Steps 3–4. Cap at 3 rounds.

## Step 6: Mark ready

Finally, update the task status by running `just task-status <task-file> ready-for-dev`.

```text
```
