---
name: clarify-task
description: Use this skill to resolve ambiguities, vague criteria, over-specification, and make implicit assumptions explicit before planning the task in more detail. Invoked at the end of /create-task and the start of /plan-task. Typical workflow: /create-task → /clarify-task → /plan-task → /impl-task → /code-review → /review-task.
---

# Clarify Task

## Usage

`/clarify-task <task>`

## Goal

Resolve ambiguity, vague criteria, over-specification, implicit assumptions before planning the task in more detail.

This is both a gate and a dialogue with the user. The output is a task that a planning agent can execute without silently filling in the wrong interpretation.

## Context

This skill is typically run as part of a larger workflow:

```
/create-task → /clarify-task → /plan-task → /impl-task → /code-review → /review-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (stored in `docs/tasks`) plus repo state carry everything the next agent needs.

## Step 0: Short-circuit

Skip silently when any of these hold:

- **Placeholder task** — `TODO:` markers from the create-task template still present, minimal content, or the user explicitly created it as a placeholder. Nothing substantive to clarify yet.
- **Epic task** — has a sub-task table, not ACs. Clarify the sub-tasks individually, not the epic.
- **Already clarified in this session** — the user confirms clarify has just run and nothing has changed since.

If the task is so under-specified that you can't form grounded questions at all, stop and suggest running `/create-task <task-path>` to flesh it out before trying to clarify.

## Step 1: Read the task and the code it touches

Read the task file. Then read the code it names — not to plan, but to ground questions in what actually exists. Generic questions ("can you clarify?") are useless; grounded ones ("`next_earnings_date` is blank — calendar or trading days?") are useful.

**Research tasks (`type: research`)** — read the question or hypothesis rather than code. A research task is clarified when it has a clear question, a defined deliverable, and a scope boundary. Don't require falsifiable behavioural ACs.

## Step 2: Surface issues

Scan for each category below and surface anything that fires:

- **Blank or stub content** — `->` stubs, trailing-off descriptions, embedded `TBD`, question marks in ACs, "should we...?", "have a think", "need to decide". Conversation artefacts that will silently become wrong decisions.
- **Judgement-word ACs** — "works correctly", "handles edge cases", "robust", "clean", "appropriate", "acceptable". Each needs replacing with a concrete observable — inputs, outputs, or behaviour.
- **Missing why** — task says *what* but not *why*. Without the motivation, the planning agent fills the gap with an assumption that changes tradeoffs.
- **Scope forks** — a criterion a reasonable agent could read two ways and build meaningfully different things from. Quote the text and describe the fork: "this could mean X or Y — which?"
- **Semantic ambiguity** — same term meaning two things across the task ("days" = calendar or trading?), field or column semantics that aren't pinned down.
- **Implicit assumptions** — things the implementer must assume that aren't stated: missing-data handling, direction of checks, null vs. sentinel, boundary inclusivity.
- **Edge cases ACs don't cover** — boundary values, asymmetric conditions, fallback behaviour that would force a runtime decision but isn't addressed.
- **Over-specification** — criteria that dictate implementation choices without affecting observable behaviour. Flag for relaxation so the implementer can find better paths. Two exceptions stand: when structure *is* the deliverable (refactoring), and when a formula defines correctness.

Present what fires as a numbered list, grouped by AC or section. Each entry:

- Names the specific text, field, or AC it refers to
- States the gap concisely
- Proposes a recommended answer with one-line reasoning, and names the alternative ("calendar days — earnings calendars are published as calendar dates; trading days would need market-calendar lookups"). The user can confirm with a "yes" or override — much faster than picking from an open-ended menu.

**If nothing substantial fires, exit silently.** Don't announce a passing check.

**Wait for the user to answer before proceeding.** The user may dismiss individual items — that's fine; the downstream skill has its own invocation of this check.

## Step 3: State remaining assumptions

After the user answers, name any non-obvious assumptions you're still making — things now resolved enough to implement, but where you've chosen an interpretation the user may not have explicitly considered.

State each: what you're assuming, what the alternative would produce. Keep it short — this is a confirmation, not a new round.

If you are genuinely uncertain that the criteria still capture the user's intent, say so rather than papering over.

**Wait for the user to confirm or correct before proceeding.**

## Step 4: Update the task

Apply clarifications and confirmed assumptions to the task file:

- Fill in blank or incomplete definitions.
- Replace vague language with the agreed specifics.
- Relax over-specified criteria so they describe behaviour, not mechanism.
- Remove resolved questions, TODOs, and "look into" notes — don't leave them as stale breadcrumbs.
- Inline assumptions that are now settled.

Edit only what was clarified — don't rephrase, reformat, or improve surrounding prose. The task should now be complete enough for `/plan-task` to produce verifiable steps without having to resolve ambiguity.
