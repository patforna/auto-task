---
name: auto-task
description: use to drive a well-defined task end-to-end with minimal human input: plan, implement, review, ship.
---

# Auto Task

## Usage

`/at:auto-task <task> [--lite] [further user instructions]`

## Modes

- **Full** — default.
- **Lite (`--lite`)** — only when the user explicitly passes the flag. Single-pass planning (Step 3), a single reviewer (Step 5), and a single task review (Step 8). Worktree, implementation, design review, and wrap-up are unchanged.

## Goal

Drive a well-defined task end-to-end with minimal human input.

Stop only when human input is genuinely required (ship gate, irreducible ambiguity, etc.).

## Context

Workflow:

    create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task
                                └───────────────────────── auto-task ─────────────────────────┘

Task files live in the project's task store — `tasks/` in the repo by default. Project bindings can override this and every other default below: verification command, worktree location and init, standing review context, design-review serve command, model choices, commit conventions, transcript capture. Bindings live in `.claude/auto-task.config.md` (project, committed) and `.claude/auto-task.config.local.md` (personal overrides — win on conflict); see `/at:create-task` § Task Store and Project Bindings. **Read them first if they exist.** Pass their paths to every subagent you spawn so they read them too.

`main` throughout this skill means the repo's default branch — substitute yours (e.g. `master`) if it differs.

## Guidance (DO NOT IGNORE!)

<!-- Curate as we go along. -->

Internalise and follow these rules:

- Aim to complete all the steps with high-autonomy - assume there is no human available to help you complete the task. If there are questions, flags or surprises, use your own best judgement, make a note of it to show to the user when you're done and proceed. Only stop i) if the instructions in this file explicitly ask you to or ii) if you truly can't make progress without human intervention.
- Be resilient against failures. If anything fails or (worse) hangs - a tool call, a spawned process, a subagent, etc. - be proactive and resourceful. Don't skip any steps or details because something failed. Keep trying. If necessary, investigate and fix or try alternative routes. Keep checking at 1-min intervals that subprocesses and subagents make progress and don't hang. If no progress for more than 10 mins, kill them aggressively and restart (don't skip).
- When subagents produce user output (e.g. implementation plan, code review findings, etc.), make sure to re-output it in the main agent, so the user can actually see it.
- Use raw `git worktree add` for worktrees — NOT the harness `EnterWorktree` tool. Reason: the worktree must live at a persistent, predictable path that Step 9/10 hands off to the user's editor/tmux; an opaque harness temp path breaks that handoff.
- In unattended auto-task, a task at `status: new` that clearly went through `/at:create-task` (locked decisions + acceptance criteria present) may be treated as ready-for-dev — proceed and note the missed status bump in the final report. Don't stall on the status field alone.

## Prerequisite

- A well-defined task (typically created by a human) with status `ready-for-dev`.

## Protocol

## Step 1: Confirm

Find the task and output its title and status. Bonus points for using figlet =)

## Step 2: Worktree

Create a `task/NNN-<slug>` worktree. Default location is a sibling of the repo, `../<repo>.worktrees/NNN-<slug>`; the bindings may pin a different path:

    git worktree add -b task/NNN-<slug> <worktree-path> main
    cd <worktree-path>

Then initialise it: run the bindings' worktree-init command if defined; otherwise install the project's dependencies (a fresh worktree shares no installed deps with the primary) and copy over any gitignored files the app needs to run locally (e.g. `.env` — check `.env.example` and similar templates against the primary checkout).

Refuse to start if the branch already exists or the target worktree path is non-empty.

All subsequent steps run inside the worktree. Pass the absolute worktree path explicitly to every subagent — their Read/Edit/Write tools must root at the worktree path, not the primary worktree.

With the default in-repo task store, the task file is inside the worktree — pass `<task-path>` to subagents rooted at the worktree, and task-file edits (plan, status bumps) ride the task branch. If the bindings route tasks to a separate repo, the task file is **not** in the worktree: pass its absolute external path, and task-file edits commit there, independent of the worktree branch.

## Step 3: Plan

Create an implementation plan. Important: Invoke /at:panel inline / do not wrap it in a subagent. Panel line-up per bindings § Models (default: strongest available Claude model + Codex).

    /at:synthesize /at:panel /at:plan-task <task-path>

In `--lite` mode, skip the panel and synthesis — run `/at:plan-task <task-path>` directly (still inline, not in a subagent).

Unless there are major flags, write the plan to the task file.

## Step 4: Implement

Spawn a new sub-agent (implementer model per bindings § Models; default: the strongest available model) and run:

    /at:impl-task <task-path>

## Step 5: Review Code

In `--lite` mode: spawn a single sub-agent to run `/at:review-code main..HEAD`, skip the adversarial pass and the synthesis step, and carry its findings straight into Step 7. The rest of this step applies to full mode only.

In parallel:

- Spawn a new sub-agent and run `/at:review-code main..HEAD`
- Run an **independent adversarial review** of the same range. Reviewer per bindings § Models; default: if the `codex` plugin is installed, use `/codex:adversarial-review --background --base main`; if it is not installed, spawn a second independent review subagent (fresh context, adversarial framing) and note the degradation in the final report. If the bindings define standing review context, append it verbatim to the reviewer's focus text.

Note: `/codex:...` are plugin slash commands and cannot be model-invoked directly. To run one from inside auto-task, locate its definition under `~/.claude/plugins/cache/**/commands/<name>.md`, read the Bash invocation template inside, and run it via the Bash tool — substituting `${CLAUDE_PLUGIN_ROOT}` (a template placeholder, not a shell var!) with the resolved plugin root.

If Codex is installed but unavailable (e.g. usage limit), fail loudly — do not substitute or skip.

When all reviews are complete, spawn a new agent to `/at:synthesize` the responses using the following arguments:

- prompt: [derive from /at:review-code]
- perspective 1: findings produced by the `/at:review-code` subagent
- perspective 2: findings produced by the adversarial reviewer

Synthesiser: keep each finding's `Autofix:` line exact when deduping — it's the routing token the Step 7.1 autofix fast-lane keys on, not prose.

## Step 6: Review Design (UI Changes Only)

Skip unless the change alters rendered output (layout, spacing, colour, typography, interaction states).

Run `/at:review-design <task-path>` **execute on the main thread** — do not wrap it in a subagent: it boots the app (per the bindings' design-review serve command) and drives the chrome-devtools MCP with real input, which a subagent can't do reliably. It is flag-only and emits findings in `/at:review-code`'s format. Navigate to the URL the serve command prints — don't assume a fixed port.

Re-output its findings in the main agent so the user can see them, and carry them into Step 7 alongside the code review findings.

## Step 7: Address Review Feedback (If Applicable)

### 7.1: Triage

In a new subagent:

1. Read the task — this is the original intent of the change.
2. Read the synthesised code review findings from above, plus any design findings from Step 6.
3. Findings carrying an `Autofix:` line **and severity Minor or Nit** skip the triage table entirely and go straight to the Step 7.2 fix (scoped to changed files only). If an autofix *class* recurs across reviews, flag it to be fixed at the root instead of re-fixing it.
4. For each remaining finding, decide one of — every row carries a one-line cited reason (the evidence, not just the verdict):

   - Real issue that needs addressing -> Accept (cite what it breaks / why it's worth fixing)
   - Real issue but probably out of scope -> Reject (capture as a follow-up note in the task's `## Implementation notes`)
   - Value of fix does not exceed cost (esp. complexity) of fix -> Reject (explain why)
   - False positive -> Reject (cite the specific code that disproves it)
   - Would significantly change scope/goal -> Reject (cite the anchor)
   - Premise excluded by the project's standing review context (bindings) — e.g. harm requires a deployment surface the project explicitly lacks — and the finding names no present-tense local bug -> Reject (cite the context)
   - Recommends restoring behaviour an Acceptance Criterion or locked decision deliberately removed -> Reject (cite the AC/decision)

   Discriminator for the standing-context bullet: gate on the impact *mechanism*, not keywords — keep any finding whose harm mechanism the project actually has.

Never auto-reject a Critical or Major finding. If the instinct is to reject one, surface it in the Step 10 decisions report instead and let the human decide.

Render triage results as a table:

| #   | Finding (one line) | Disposition | Reason |
| --- | ------------------ | ----------- | ------ |

### 7.2: Fix

If any findings were accepted (step 4) or routed to the autofix fast-lane (step 3), spawn a new subagent that fixes them following `/at:impl-task`. Review the fix with a single adversarial reviewer scoped to the fix commits (codex `/codex:adversarial-review --base <pre-fix-sha>` when installed, else a fresh review subagent) and address feedback as outlined in Step 5 and 7, respectively.

In `--lite` mode, review the fix with a single subagent reviewer, consistent with Step 5. Skip the fix-review entirely when every accepted fix is trivial/mechanical (Minor/Nit, no logic change) — the verification command plus the Step 8 task review cover those.

## Step 8: Review Task

0. Sync: rebase the worktree branch onto latest main (`git -C "$primary" pull --rebase origin main` — resolve `$primary` as in `/at:ship-task`; skip if no remote — then `git rebase main` from the worktree; on conflicts resolve guided by the task/plan, then re-run the verification command) — surfaces integration drift here instead of at ship time.
1. Review: In a new subagent, review that the task is complete via `/at:review-task`.
2. Address Feedback: If the review returns findings, triage and address them as outlined in Step 7.
3. Second review: Repeat "1. Review". If still failing, stop here and flag it to the user. Do not proceed to Step 9.

In `--lite` mode, run steps 1–2 once and skip the second review (step 3).

## Step 9: Wrap Up

### 9.1: Wrap up Loose Ends

Make sure that:

- all findings have been addressed (or have been rejected deliberately)
- all changes have been committed

### 9.2: Capture Session Transcript (Only If Bound)

Skip unless the project bindings define a transcript-capture command and destination. If they do, run it and keep the transcript out of the repo (diff and grep noise).

### 9.3: Update Task and Commit

Set the task status to `ready-for-signoff` and commit it (frontmatter edit with a `(task/NNN)` subject by default; the bindings' task-status command if defined — with an external task store the bump commits there, not in the worktree).

### 9.4: Summarise

Output:

- what was achieved
- any learnings or gotchas that should be integrated back into the harness - only if truly load-bearing.
- a pointer to the session transcript (if captured)

## Step 10: Ask User How to Proceed

First, surface a short prose summary of the triage decisions so the human can review the critical bits before shipping — a report, not a gate: how many findings were fixed, which were rejected and why, which were deferred, and — called out explicitly — any Critical/Major findings surfaced for a human call rather than auto-actioned.

Then offer the user the following options:

- Open the worktree in their editor (e.g. VS Code)
- Open the worktree in a new tmux pane
- Both of the above
- Run `/at:ship-task`

Do not proceed without explicit user approval. If the user declines, stop here.
