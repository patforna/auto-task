---
name: review-task
description: Verify that a task has been completed according to its intent and criteria. Typical workflow: /create-task → /clarify-task → /plan-task → /impl-task → /code-review → /review-task → /ship-task.
---

# Review Task

## Usage

`/review-task <task-path> [further user instructions]`

## Goal

Verify that a task has been completed according to its intent and criteria.

## Context

This skill is typically run as part of a larger workflow:

```
/create-task → /clarify-task → /plan-task → /impl-task → /code-review → /review-task → /ship-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (stored in `/tasks`) plus repo state carry everything the next agent needs.

## Guidance (DO NOT IGNORE!)

<!-- Curate as we go along. -->

These rules govern how to perform the review. Internalise and follow them throughout.

- Flag issues — do not attempt to fix them; let the user decide.

## Step 1: Build context

Read the task and the code that was implemented. Ensure you fully understand the task's intent, criteria and what was implemented.

## Step 2: Verify ACs

For each acceptance criterion, determine: **pass**, **fail**, or **unclear**.

A criterion passes when you can point to **specific evidence** — for example, a test that exercises it, observable behaviour in the code, or output from running it. "The code looks like it would work" is not evidence; a passing test is.

## Step 3: Verify intent

In addition to checking ACs:

- Check that the implementation truly matches the *why* in the description. It's easy to meet every AC but miss the intent.
- If there were deviations from the plan, check that they are justified.

## Step 4: Summarise

Say whether the review passed or, if not, present a summary of your findings and wait for user input.

## Step 5: Wrap up

Once there are no findings left, or the user has asked you to proceed, rembmer to update the task status by running `just task-status <task-file> ready-for-signoff`.
