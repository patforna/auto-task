---
name: auto-task
description: use to drive a well-defined task end-to-end with minimal human input: plan, implement, review, ship.
---

# Auto Task

## Usage

`/auto-task <task> [further user instructions]`

## Goal

Drive a well-defined task end-to-end with minimal human input.

Stop only when human input is genuinely required (ship gate, irreducible ambiguity, etc.).

## Context

Workflow:

```
create-task → clarify-task → plan-task → impl-task → code-review → review-task → ship-task
                            └───────────────────────── auto-task ─────────────────────────┘
```

## Guidance (DO NOT IGNORE!)

<!-- Curate as we go along. -->

Internalise and follow these rules:

- Aim to complete all the steps with high-autonomy - assume there is no human available to help you complete the task. If there are questions, flags or surprises, use your own best judgement, make a note of it to show to the user when you're done and proceed. Only stop i) if the instructions in this file explicitly ask you to or ii) if you truly can't make progress without human intervention.
- Be resilient against failures. If anything fails or (worse) hangs - a tool call, a spawned process, a subagent, etc. - be proactive and resourceful. Don't skip any steps or details because something failed. Keep trying. If necessary, investigate and fix or try alternative routes. Keep checking at 1-min intervals that subprocesses and subagents make progress and don't hang. If no progress for more than 10 mins, kill them aggressively and restart (don't skip).
- When subagents produce user output (e.g. implementation plan, code review findings, etc.), make sure to re-output it in the main agent, so the user can actually see it.

## Prerequisite

- A well-defined task (typically created by a human) with status `ready-for-dev`.

## Protocol

## Step 1: Confirm

Find the task and output its title and status. Bonus points for using figlet =)

Update the current session name: `/rename task/NNN-<slug>`.

## Step 2: Worktree

Create a `task/NNN-<slug>` worktree under `~/github/.worktrees/tad/`:

    git worktree add -b task/NNN-<slug> ~/github/.worktrees/tad/NNN-<slug> main
    cd ~/github/.worktrees/tad/NNN-<slug>
    just worktree-init

Refuse to start if the branch already exists or the target worktree path is non-empty.

All subsequent steps run inside the worktree. Pass the absolute worktree path explicitly to every subagent — their Read/Edit/Write tools must root at the worktree path, not the primary worktree (see CLAUDE.md § Worktrees).

## Step 3: Plan

Create an implementation plan. Important: Invoke /sop inline / do not wrap it in a subagent.

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

Note: `/codex:review` and `/codex:adversarial-review` are plugin slash commands and cannot be model-invoked directly. To run one from inside auto-task, locate its definition under `~/.claude/plugins/cache/**/commands/<name>.md`, read the Bash invocation template inside, and run it via the Bash tool — substituting `${CLAUDE_PLUGIN_ROOT}` (a template placeholder, not a shell var!) with the resolved plugin root.

If Codex is unavailable (e.g. usage limit), fail loudly — do not substitute or skip.

When all reviews are complete, spawn a new opus agent to `/synthesise` the responses using the following arguments:
- prompt: [derive from /code-review]
- perspective 1: findings produced by codex:review subagent
- perspective 2: findings produced by codex:adversarial-review subagent
- perspective 3: findings produced by opus `/code-review` subagent

## Step 6: Address Review Feedback (If Applicable)

### 6.1: Triage

In a new opus subagent:

1. Read the task - this is the original intent of the change.
2. Read the synthesised code review findings from above.
3. For each finding, decide one of:

    - Would significantly change scope/goal -> Reject (cite the anchor)
    - False positive -> Reject (cite the specific code that disproves it and why)
    - Value of fix does not exceed cost (esp. complexity) of fix -> Reject (explain why)
    - Real issue but probably out of scope -> Reject (capture as follow up task)
    - Real issue that needs addressing -> Accept

    Note: do not ignore small issues or nits (e.g. typos, inconsistencies, style) **IF** they are trivial to fix - consider batching them up.

    Render triage results as a table:

    | # | Finding (one line) | Disposition | Reason |
    |---|--------------------|-------------|--------|

### 6.2: Fix

If any accepted findings remain, spawn a new opus subagent that fixes the issues following `/impl-task`.

If and only if something should be recorded for posterity, add it to the task's `## Implementation notes` section.

## Step 7: Review Task

1. Review: In a new opus subagent, review that the task is complete via `/review-task`.
2. Address Feedback: If the review returns findings, triage and address them as outlined in Step 6.
3. Second review: Repeat "1. Review". If still failing, stop here and flag it to the user. Do not proceed to Step 8.

## Step 8: Wrap up

### 8.1: Wrap up loose ends

Make sure that:

- all findings have been addressed (or have been rejected deliberately)
- all changes have been committed

### 8.2: Capture session transcript

    claude-replay --recurse-subagents "$CLAUDE_CODE_SESSION_ID" > .claude/skills/auto-task/_transcripts/<NNN-slug>.$CLAUDE_CODE_SESSION_ID.md

### 8.3: Update task and commit

Run `just task-status <task-file> ready-for-signoff` and commit (incl. transcript file).

### 8.4: Summarise

Output:

- what was achieved
- any learnings or gotchas that should be integrated back into the harness - only if truly load-bearing.
- a pointer to the session transcript

## Step 9: Ask user how to proceed

Offer the user the following options:

- Open the worktree in VS code
- Open the worktree in a new tmux pane
- Both of the above
- Run `/ship-task`

Do not proceed without explicit user approval. If the user declines, stop here.