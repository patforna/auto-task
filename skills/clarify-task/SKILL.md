---
name: clarify-task
description: Surface ambiguities, implicit assumptions, and missing definitions in a task before planning begins. Workflow: /define-task → /clarify-task → /plan-task → /impl-task → /review-task.
---

# Clarify Task

## Usage

`/clarify-task <task-path>`

## Goal

Identify and resolve the subtle gaps a task can carry even when it passes the basic planability gate: blank or underspecified definitions, ambiguous semantics, implicit assumptions that would be silently resolved wrong, missing edge cases.

This is a dialogue, not a gate. The output is a task that a planning agent can execute without silently filling in the wrong interpretation.

## Workflow context

```
/define-task  →  /clarify-task (this skill)  →  /plan-task  →  /impl-task  →  /review-task
```

## Step 1: Read the task and the code it touches

Read the task file. Then read the relevant code — not to plan, but to ground your questions in what actually exists. Generic questions ("can you clarify?") are useless. Grounded questions ("the arrow on `next_earnings_date` is blank — is that the next date strictly after `date`, or the nearest in either direction?") are useful.

For **research tasks** (`type: research`), read the question or hypothesis instead of code, and focus on scope and deliverable ambiguity rather than API/behavioural gaps.

## Step 2: Surface questions

Look for:

- **Blank or incomplete definitions** — fields left with `->` but no value, descriptions that trail off or reference behaviour without specifying it
- **Semantic ambiguities** — terms that could mean two different things ("days" = calendar or trading?), conditions with multiple valid readings, column names whose semantics aren't pinned down
- **Implicit assumptions** — things you'd have to assume to implement correctly that aren't stated (how to treat missing data, which direction a check looks, what null means vs. a sentinel)
- **Edge cases the ACs don't cover** — cases that would force a decision during implementation but aren't addressed (boundary values, asymmetric conditions, fallback behaviour)

Present questions as a numbered list. Each question should:
- Name the specific text, field, or AC it refers to
- State the ambiguity or gap concisely
- Offer concrete options where applicable ("calendar days or trading days?" not "can you clarify?")

**Wait for the user to answer before proceeding.**

## Step 3: State remaining assumptions

After receiving answers, identify any non-obvious assumptions you're still making — things that are now resolved enough to implement, but where you've made a choice the user may not have explicitly considered.

State each one: what you're assuming and why (what would happen if you assumed the alternative). Keep it short — this is a confirmation, not a new round of questions.

**Wait for the user to confirm or correct before proceeding.**

## Step 4: Update the task

Apply all clarifications and confirmed assumptions to the task file:

- Fill in blank or incomplete definitions
- Replace vague language with the agreed-upon specifics
- Remove notes that were open questions and are now resolved — don't leave them as stale "look into" items
- Remove or inline any assumptions that are now settled

Edit only what was clarified — don't rephrase, reformat, or improve surrounding prose. The task should now be complete enough for `/plan-task` to produce verifiable steps without having to resolve ambiguity.
