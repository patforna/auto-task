---
name: auto-task
description: TODO
---

# Auto Task

## Usage

`/auto-task <task> [further user instructions]`

## Goal

## Context

Workflow:

```
/create-task → /clarify-task → /plan-task → /impl-task → /code-review → /review-task → /ship-task
```

## Guidance (DO NOT IGNORE!)

<!-- Curate as we go along. -->

Internalise and follow these rules:

- Aim to complete all the steps with high-autonomy - assume there is no human available to help you complete the task. It there are questions, flags or surprises, use your own best judgement, make a note of it to show to the user when you're done and proceed. Only stop if you truly can't make progress without human intervention.
- Be resilient against failures. If anything fails or (worse) hangs - a tool call, a spawned process, a subagent, etc. - be pro-active and resourceful. Don't skip any steps or details because something failed. Keep trying. If necessary, investigate and fix or try alternative routes. Keep checking at 1-min intervals that subprocesses and subagents make progress and don't hang. If no progress for more than 10 mins, kill them aggressively and restart (don't skip).

## Prerequisite

- A well-defined task (typically created by a human) with status `ready-for-dev`.

## Protocol

## Step 1: Confirm

Find the task and output it's title and status.

## Step 2: Branch

Create a new branch `task/NNN-<slug>` (e.g. `task/029.09-add-sector-med-1d-return`)

Refuse to start if the working tree is dirty or the branch already exists.

## Step 3: Plan

Create an implementation plan using a mixture of (fresh) models:

    /sop /plan-task <task-path>

Unless there are major flags, write the plan to the task file.

## Step 4: Implement

Spawn a new opus sub-agent and run:

    /impl-task <task-path>

## Step 5: Review Code

In parallel:
- Run `/codex:review --background --base main`
- Run `/codex:adversarial-review --background --base main`
- Spawn a new opus sub-agent and run `/code-review main..HEAD`

When all review complete, spawn a new opus agent to `/synthesise` the responses using the following arguments:
- prompt: [derive from /code-review]
- perspective 1: findings produced by codex:review subagent
- perspective 2: findings produced by codex:adversarial-review subagent
- perspective 3: findings produced by opus `/code-review` subagent

## Step 6: Address Review Feedback (If Applicable)

In a new opus subagent:

**Triage:**
- Read the task - this is the original intent of the change.
- Read the synthesised code review findings from above
- For each finding, decide one of:

    - Would significantly change scope/goal -> Reject (cite the anchor)
    - False positive -> Reject (cite the specific code that disproves it and why)
    - Value of fix does not exceed cost (esp. complexity) of fix -> Reject (explain why)
    - Real issue but probably out of scope -> Reject (capture as follow up task)
    - Real issue that needs addressing -> Accept

    Render triage results as a table:

    | # | Finding (one line) | Disposition | Reason |
    |---|--------------------|-------------|--------|

**Fix:**
Apply accepted fixes, following `/impl-task`.

**Record:**
If and only if something should be recorded for posterity, amend the tasks `## Implementation notes` section accordingly.

## Step 7: Review Task

In a new opus subagent:
- Review the task is complete via `/review-task`
- If there are   # loop - feedback to impl-task agent

## Step 8: Wrap up

Make sure:
- all findings have been addressed (or deliberately been rejected)
- all changes have been committed

Then, update the task status by running `just task-status <task-file> ready-for-signoff`.

Output a summary of:
- the branch name
- what was achieved
- any learnings or gotchas that should be integrated back into the harness - only if truly load bearing.

## Step 9: Offer to ship

After the summary, ask the user (via `AskUserQuestion`) whether to run `/ship-task <task-file>` now. Do not invoke it without explicit approval in the current turn. If the user declines, stop here — the task is already at `ready-for-signoff` and shipping can happen later.