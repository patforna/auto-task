---
name: impl-task
description: Implement a task — pick it up, execute the plan using TDD, summarise. Workflow: /define-task → /plan-task → /impl-task → /review-task.
---

# Implement Task

## Usage

`/impl-task <task-path>`

The argument is a path to a task file.
If the intent is ambiguous, ask.

## Goal

Pick up a planned task and execute it using test-driven development.
Commit after each step. Write a summary when done and codify any learnings.

## Workflow context

```
/define-task  →  /plan-task  →  /impl-task (this skill)  →  /review-task
```

Each step runs in a new session. The task file carries everything the next
agent needs — it is the handoff between sessions.

## Step 1: Orient

1. **Read the task** and locate the `## Implementation plan`.
   If no plan exists, stop and tell the user to run `/plan-task` first.
2. If the task has an `epic:` field, read the epic for strategic context.
3. **Read CLAUDE.md** — every rule is a constraint on your implementation.
4. Read files referenced by the task and the code each plan step will touch.
   Load per step as you go — don't read the entire codebase upfront.
5. **Read the acceptance criteria** — these are your success conditions.
6. Set status to wip: `just task-status <task-file> wip` (updates frontmatter and epic table).
7. Confirm you understand the plan. If anything is ambiguous, ask before coding.

## Step 2: Implement (per plan step)

Work through the plan step by step. Each step names a behaviour to verify —
that behaviour is your first test.

### The TDD cycle

For each step that has testable behaviour:

**Red** — Write a small failing test for the behaviour the step names. Run it.
Confirm it fails.

**Green** — Make it pass. Choose your strategy by confidence:

| Strategy               | When                    | How                                                     |
|:-----------------------|:------------------------|:--------------------------------------------------------|
| **Obvious Implementation** | Confident, clear logic  | Write the real code directly. If unexpected red, back down. |
| **Fake It**            | Uncertain or complex    | Return a constant, then replace with real logic as duplication surfaces. |
| **Triangulation**      | Unsure how to generalise | Write a second test demanding different output, then generalise. |

Run the relevant test(s) after every Red and Green step — not the full suite.

**Refactor** — Remove duplication introduced by getting to green. This includes
duplication between test and production code. AI tends to only add complexity
(inhale) — you must actively simplify (exhale) after each green. This is not
optional tidying; it is load-bearing for your ability to continue working.

Repeat the cycle until the plan step's behaviour is fully covered. A step may
need multiple TDD cycles (one per test case).

### Pure wiring steps

If a step is pure wiring with no testable behaviour (e.g., adding a CLI flag
that delegates to an existing function): implement directly. No test needed.

### Verify and commit (per plan step)

After all TDD cycles for a step are green and refactored (or for wiring steps,
after implementation):

1. **Verify** — `just check` (full suite + lint + typecheck + format).
2. **Commit** — `just commit "<step description> (refs <task>)" <changed-files>`.
   Do NOT push.

### When things go wrong

- **Test fails after implementation**: Try to fix. If stuck after 2 attempts,
  revert to last green state and take a smaller step.
- **Plan step seems wrong**: Update the plan in the task file, note the
  deviation, continue.
- **Scope creep discovered**: Stop. Note what was found. Flag to user.
  Do not silently fix unrelated issues.
- **`just check` fails on unrelated code**: Flag to user rather than fixing
  silently — it may be someone else's in-progress work.

### Step size

Smaller steps when uncertain, surprised, or in unfamiliar territory. Bigger
steps when confident. An unexpected red means shift down to smaller steps.
An unexpected green means review your test — it may be wrong. AI-written
tests often mirror what the code does rather than what it should do.

For complex logic (especially quant code), consult the TDD reference below
for the full Beck-style pattern catalog (Child Test, Triangulation, Value
Objects, etc.).

## Step 3: Final verification

After all plan steps pass:

1. Run `just check` one final time.
2. Review the full diff: `git diff` from first implementation commit to HEAD.
3. **Scope check** — does the diff touch only what the plan requires? Flag
   anything unexpected.
4. **AC check** — for each acceptance criterion, verify it is demonstrably met
   (by a test, by observable output, or by code inspection). If an AC is not
   met, go back and implement it.
5. **Hygiene check** — no debug prints, no TODO comments you introduced, no
   commented-out code, no unrelated formatting changes.

This is NOT a comprehensive code review (that's `/cross-pollinate-code-review`'s job and
`/review-task` in a fresh session). This is a quick scope-and-hygiene pass.

## Step 4: Summarise and codify

Write a summary directly into the task, below the implementation plan:

```markdown
#### Summary

[What was actually built. Note any deviations from the plan.]

Commits: [short hashes]
```

Keep it concise — one paragraph is usually enough. The plan + summary together
tell the full story; no need to repeat what the plan already says.

If the implementation surfaced something worth preserving, codify it in the
right place and reference it from the summary:

- **Domain surprise** → `docs/knowledge.md`
- **Design decision with rationale** → `docs/decisions.md`
- **New rule or convention** → `CLAUDE.md`
- **Plan deviated** — note the deviation type in the summary so future
  planning improves.

If nothing was surprising, skip the codification — just write the summary.

Commit the task update.

Status note: `/review-task` sets `status: done` via `just task-status` after verification passes.
This skill sets `wip` at the start (Step 1) — don't set `done` here.

## Anti-Patterns

- Implementing without reading the plan and acceptance criteria first.
- Writing all code then all tests (test-after). Write the test FIRST.
- Skipping the refactor step — complexity accumulates and stalls progress.
- One big commit at the end instead of per-step commits.
- Silently fixing unrelated issues found during implementation.
- Writing the summary before implementation is complete.
- Summarising what the code does instead of what changed and why.
- Deviating from the plan without updating it in the task.
- Reading the entire codebase upfront — load files as each step needs them.

## TDD Reference (Beck-style)

!`sed '1,/^---$/d' .claude/skills/tdd/SKILL.md`
