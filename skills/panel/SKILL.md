---
name: panel
description: Use to get independent perspectives on a topic from multiple models (opus + codex). Use with /synthesize to merge.
---

# Panel

## Precondition

Must be run from main thread (reason: subagents can't spawn other subagents)

## Usage

`/panel <prompt>`

Prompt is mandatory — if missing, fail loudly; don't infer.

## Goal

Get independent perspectives on a topic from multiple models (opus + codex).

## Step 1: Expand Skill References

If the prompt invokes a skill (explicit `/name` only — not bare names in prose/diagrams), inline its `SKILL.md`, clearly fenced, after the instruction. Recurse into `/name` invocations found inside, but inline each skill at most once — never re-expand one already present (terminates; prevents cycles and bloat).

Example: `/panel please /plan-task 054 but don't write to the task file.`

Expanded prompt:

""" Please /plan-task 054 but don't write to the task file.

Skill references: === BEGIN plan-task SKILL.md === [full content of ~/github/tad/.claude/skills/plan-task/SKILL.md] === END plan-task SKILL.md === """

## Step 2: Append Anti-Sycophancy Block

Append the block below to the prompt:

> Answer directly and honestly. Do not hedge or soften to be agreeable. If your honest answer differs substantively from what the prompt seems to expect, give that one.

## Step 3: Dispatch

Spawn a Codex (via `codex:codex-rescue`) and an Opus subagent in parallel and pass through the prompt.

If Codex is unavailable (e.g. usage limit), fail loudly — do not substitute or skip.

Write the responses to `/tmp/panel-<timestamp>-<slot>.md`.

## Step 4: Deliver

Present both responses verbatim, each directly attributed to its model (Codex / Opus), including the paths to the raw responses.

Do not synthesise, reconcile, or edit.
