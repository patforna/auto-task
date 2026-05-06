---
name: review-task
description: Verify a completed task against its specification in a fresh session. Typical workflow: /create-task → /clarify-task → /plan-task → /impl-task → /code-review → /review-task.
---

# Review Task

## Usage

`/review-task <task-path> [further user instructions]`

## Goal

Verify that a completed task satisfies its specification. This is a
verification pass, not a code quality review — the question is "did it do
what was asked?", not "is the code good?"

## Context

This skill is typically run as part of a larger workflow:

```
/create-task → /clarify-task → /plan-task → /impl-task → /code-review → /review-task
```

As steps (e.g. clarify, plan, impl, review) typically run in new sessions, it's imperative that the task file (stored in `docs/tasks`) plus repo state carry everything the next agent needs.

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

If the verdict is **PASS** — run `just task-status <task-file> done` (updates
frontmatter and epic table). Commit the status update.

If the verdict is **FAIL** — list the specific gaps. The human decides
whether to re-run `/impl-task` with the findings, adjust the task, or accept
as-is. Status stays `wip`.

## What this skill does NOT do

- Code quality review (design, style, conventions) — use `/cross-pollinate-code-review`
- Run linters or type checkers — `just check` handles that
- Suggest improvements beyond the task scope
- Rewrite code or fix issues (flag them; let the human decide)
