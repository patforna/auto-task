---
name: impl-task
description: Implement a task — pick it up, implement it, summarise, codify learnings.
---

# Implement Task

Pick up a written task and execute its implementation plan. Write a summary
when done and codify any learnings.

**Usage:** `/impl-task <task-path>`

The argument is a path to a task file.
If the intent is ambiguous, ask.

## Workflow context

This is the second phase of the `/write-task` → `/impl-task` workflow:

```
Explore & discuss → /write-task → commit task → new session → /impl-task → commit code + summary
```

The task was written during an exploration session that had all the "why"
context. This session starts fresh — the task is self-contained, carrying
everything needed to implement without the original exploration context.

## Step 1: Read and Understand

1. **Read the task** and locate the `#### Implementation plan`.
2. If no plan exists, stop and tell the user to run `/write-task` first.
3. **If the task has an `epic:` field** in its frontmatter, read the epic file
   for strategic context (goal, ordering, dependencies, kill criteria).
4. **Read CLAUDE.md** and any files referenced by the task.
5. **Read the acceptance criteria** — these are your success conditions.
6. Confirm you understand the plan — no silent assumptions.

## Step 2: Implement

Follow the plan step by step. For each step:

- Use TDD style (test first, then implement) unless the step is pure wiring.
- Run the verification check after each step.
- If you deviate from the plan, update the plan in the task to reflect reality.

After all steps pass, run the full check:

```bash
just check
```

## Step 3: Commit

- `git pull --rebase` first.
- Commit with a message referencing the task.
- Do NOT push — wait for explicit approval.

## Step 4: Summarise

Write a summary directly into the task, below the implementation plan:

```markdown
#### Summary

[What was actually built. Note any deviations from the plan.]

Commits: [short hashes]
```

Keep it concise — one paragraph is usually enough. The plan + summary together
tell the full story; no need to repeat what the plan already says.

Commit the task update.

## Step 5: Codify Learnings

If the implementation surfaced anything worth preserving beyond this task:

- **Domain insight or gotcha** → `docs/knowledge.md`
- **Design decision with rationale** → `docs/decisions.md`
- **New rule or convention** → `CLAUDE.md`

Reference the addition in the summary (e.g., "added rolling-window guard to CLAUDE.md").

If nothing was surprising, skip this step.

## Step 6: Update Status

- Set `status: done` in the task's frontmatter.
- **If the task belongs to an epic**, update the task's status in the epic's
  task index table. If all tasks in the epic are now done, set the epic's
  status to `done` too.

## Anti-Patterns

- Implementing without reading the plan and acceptance criteria first
- Writing the summary before implementation is complete
- Summarising what the code does instead of what changed and why
- Codifying learnings that are obvious or already documented
- Deviating from the plan without updating it in the task
