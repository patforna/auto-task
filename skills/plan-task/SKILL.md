---
name: plan-task
description: Turn a defined task into a sequenced implementation plan ready for handoff. Workflow: /define-task → /plan-task → /impl-task → /review-task.
---

# Plan Task

## Usage

`/plan-task <task-path> [further user instructions]`

## Goal

Turn a defined task into an implementation plan that closes the decision space without doing the work.

The task definition says **what** to build and **why**. The plan says **how to verify it's built** — sequenced into steps that each prove a behaviour. The implementing agent starts in a fresh session with only the task file and the repo. The plan must be self-contained.

## Workflow context

```
/define-task  →  /plan-task (this skill)  →  /impl-task  →  /review-task
```

Each step runs in a new session. The task file carries everything the next
agent needs — it is the handoff between sessions.

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

## Step 1: Clarify

Run `/clarify-task <task-path>` to surface and resolve ambiguities before planning. Skip if the user confirms it was already run in this session.

## Step 2: Readiness check

Read the task. Before exploring the code, verify the task is plannable. Agents cannot detect when they're working from ambiguous specs — they silently resolve ambiguity, usually wrong. This gate prevents that.

**Skip this gate for epics** (they have sub-task tables, not ACs — plan the sub-tasks instead).

For **research** tasks (`type: research`), apply a lighter check: require a clear question or hypothesis, a defined deliverable, and a scope boundary. Don't require falsifiable behavioural ACs.

For all other tasks, check:

1. **Acceptance criteria exist** — not TODOs, placeholders, or "have a think"-style prompts. The create-task template uses `TODO: Add ACs` — if that's still there, the task isn't defined.
2. **Rationale is present** — the task explains *why* (motivation/problem), not just *what*. Without the why, you'll fill the gap with a reasonable but possibly wrong assumption.
3. **Criteria are falsifiable** — no vague language: "works correctly", "handles edge cases", "is robust", "clean", "acceptable". Each criterion has an unambiguous pass/fail.
4. **No unresolved questions** — no embedded "should we...?", "TBD", "TODO", "have a think", "need to decide". These are conversation artifacts that should have been resolved in `/define-task`.

If any check fails, **stop**. Do not plan around ambiguity — it compounds downstream. Present:
- Which checks failed, with the specific text that triggered each.
- Clarifying questions where possible — grounded in the code, not generic ("do you want X excluded from ranking, or just flagged?" rather than "can you clarify?").
- Suggest running `/define-task <task-path>` to flesh out the task, or let the user fix inline.

## Step 3: Orient and recommend

Read the code the task will touch — at minimum the modules named in the ACs or description. Understand the current structure before deciding what to change.

If the task belongs to an epic, read the epic for ordering and dependency context.

**Recommend an approach:**

- **Skip planning** — the approach is obvious, files are few, no tricky ordering. Go straight to `/impl-task`.
- **Single model** — straightforward task with a clear approach.
- **Dialectic** — multiple valid approaches, cross-cutting concerns, or novel architecture. Plan diversity surfaces blind spots a single model misses (PlanSearch: diversity beats detail).

Show the recommendation and wait for the user's go.

## Step 4: Design the plan

### Single model

Design the plan directly — sequence the work into steps, each naming a **concrete behaviour to verify**. After drafting, run one pre-mortem pass: "Assume an agent followed this plan and the task failed. What went wrong?" Revise if it surfaces anything structural.

### Dialectic

The goal is **perspective diversity** — genuinely different plans, not N variations of the same idea. Different models have different architectural biases, so multi-model generation is the mechanism.

**Generate 3 plans in parallel** — one per frontier model:

**Opus** — background agent:
> Read the task at {task_path} and the code it touches. Read CLAUDE.md.
> Produce an implementation plan (not code): approach with rationale,
> sequenced steps with verification checks, non-goals.
> Write to /tmp/{slug}-plan-opus.md

**Codex** — headless via bash:
```bash
codex exec --full-auto "Read the task at {task_path} and the code it touches. Read CLAUDE.md. Produce an implementation plan (not code): approach with rationale, sequenced steps with verification checks, non-goals. Write to /tmp/{slug}-plan-codex.md"
```

**Gemini** — headless via bash:
```bash
gemini exec "Read the task at {task_path} and the code it touches. Read CLAUDE.md. Produce an implementation plan (not code): approach with rationale, sequenced steps with verification checks, non-goals. Write to /tmp/{slug}-plan-gemini.md"
```

If a model isn't available, stop and tell the user before proceeding.

**Synthesize, don't select.** Read all 3 plans. Compare:
- **Agreements** — high confidence; take directly
- **Disagreements** — the interesting decisions; for each, state which is stronger and why
- **Gaps** — things none of the plans caught

Write a single synthesized plan — don't pick a winner and discard the rest. Carry rejected approaches from the disagreements into the plan's "Alternatives considered" section so the implementing agent doesn't rediscover and pursue them.

**Iterative refinement.** Critique the synthesized plan, revise, repeat until convergence. Each round uses a different lens to avoid re-running the same check:

1. **Pre-mortem** — "Assume an agent followed this plan and the task failed. What went wrong?" (missing preconditions, ordering dependencies, merge contradictions)
2. **Verification audit** — for each step, can the check actually be run? Does it prove the behaviour it claims to?
3. **Scope and blast radius** — what might the agent touch that it shouldn't? What scope creep vectors exist?
4. **Fresh read** — read the plan cold as if you'd never seen the task. Is it self-contained? Would a capable agent in a fresh session know what to do?

**Convergence signal:** stop when a round produces only cosmetic changes (wording, formatting) rather than structural ones (new steps, reordering, changed approach). Typically 2-4 rounds. If still finding structural issues after round 4, flag to the user — the task may need re-scoping.

### Properties of a good step

- **Verifiable** — has a concrete check (a test, a CLI command, expected output)
- **Independent** — can fail without invalidating subsequent steps where possible
- **Behaviour-level** — describes what the system does, not how the code is structured

### Sequencing strategy

- Walking skeleton or happy path first — thinnest end-to-end path
- Then edge cases and variations
- Structural changes (refactoring) before behavioural changes when both are needed

Add **non-goals** when scope creep is likely — name things the agent might do that it shouldn't.

### Plan format

Write the plan as a new section in the task file. Lead with a **short-form summary** — one bullet per step, each one line, so a reader can get the shape of the plan in 30 seconds before diving into step detail.

```markdown
## Implementation plan

### Summary

1. [Step 1 title] — [one-line hook]
2. [Step 2 title] — [one-line hook]
3. [Step 3 title] — [one-line hook]
   ...

### Approach

[One paragraph: strategy and why. Omit for straightforward tasks.]

### Alternatives considered

- [Rejected approach] — [why rejected. Omit section if no plausible alternative.]

### Non-goals

- [Things the agent might do but shouldn't. Omit section if no scope creep risk.]

### Steps

1. [Behaviour to verify] → verify: [concrete check]
2. [Behaviour to verify] → verify: [concrete check]
3. [Behaviour to verify] → verify: [concrete check]
```

Keep summary bullets and step numbers in lockstep — bullet N matches step N.

### Self-check

Before presenting:
1. **Nervousness test** — remove the plan, read only the ACs. Anything make you nervous? Is it addressed?
2. **Pseudocode test** — does any step describe *how* to write code? Relax it.
3. **Length test** — can the user review this in under 5 minutes? Shorten.

## Step 5: Review

Print the **Summary** section verbatim to the console so the user gets the shape of the plan without opening the task file. Then wait for approval. After approval, commit.
