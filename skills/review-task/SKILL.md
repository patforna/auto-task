---
name: review-task
description: Verify a completed task against its specification in a fresh session. Invoke when the user requests it.
---

# Review Task

## Usage

`/review-task <task-path> [further user instructions]`

## Goal

Verify that a completed task satisfies its specification. This is a
verification pass, not a code quality review — the question is "did it do
what was asked?", not "is the code good?"

## Context

Phase 4 in the task workflow:

1. Explore & define (`/define-task`)
2. Plan (`/plan-task`)
3. Implement (`/impl-task`)
4. **Verify (`/review-task`) — this skill**

This skill MUST run in a **fresh session** — not the session that implemented
the task. Self-review is empirically unreliable due to confirmation bias and
anchoring. The implementing agent will miss issues that a fresh reviewer
catches. As the task file is self-contained, no implementation context is
needed.

## Step 1: Orient

Read the task file. Identify:
- Description (the *why*)
- Acceptance criteria (the *what*)
- Implementation plan (the *how*, including any deviations noted)
- Summary (what was actually built)
- Notes (constraints, gotchas, pointers)

Read the code the task touched — the diff, the tests, neighbouring files for
context. Read CLAUDE.md for project rules.

## Step 2: Verify each AC

For each acceptance criterion, determine: **pass**, **fail**, or **unclear**.

A criterion passes when you can point to **specific evidence** — a test that
exercises it, observable behaviour in the code, or output from running it.
"The code looks like it would work" is not evidence; a passing test is.

Run `just check` to confirm the test suite passes.

If you need to run specific tests or commands to verify an AC, do so. Cite
the evidence.

## Step 3: Check for gaps

Beyond individual ACs:

- **Intent alignment** — Does the implementation match the *why* in the
  description? An agent can satisfy every criterion but miss the intent.
- **Plan deviations** — Were deviations documented in the summary? Are they
  justified?
- **Completeness** — Are there ACs that were partially implemented, silently
  skipped, or interpreted in a surprising way?
- **Summary accuracy** — Does the task summary reflect what was actually
  built?

## Step 4: Verdict

Present findings structured as:

```
## Review: [task title]

### Verdict: PASS | FAIL

### AC verification

| # | Criterion (short)        | Status  | Evidence                    |
|---|--------------------------|---------|------------------------------|
| 1 | [abbreviated AC]         | pass    | [test name / observation]    |
| 2 | [abbreviated AC]         | fail    | [what's missing]             |

### Gaps (if any)

- [Intent misalignment, plan deviation, or completeness issue]
```

If the verdict is **PASS** — the task is ready for human sign-off.

If the verdict is **FAIL** — list the specific gaps. The human decides
whether to re-run `/impl-task` with the findings, adjust the task, or accept
as-is.

## What this skill does NOT do

- Code quality review (design, style, conventions) — use `/code-review`
- Run linters or type checkers — `just check` handles that
- Suggest improvements beyond the task scope
- Rewrite code or fix issues (flag them; let the human decide)
