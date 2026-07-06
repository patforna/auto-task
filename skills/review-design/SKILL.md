---
name: review-design
description: Use to review a design / UI change against its specification. Read-only; produces findings, applies no fixes.
---

# Review Design

## Usage

`/at:review-design [the change + its design intent]`

## Prerequisite

Requires chrome-devtools MCP. If not available, do not proceed and fail loudly.

## Goal

Verify a design / UI change matches the specified design.

## Guidance (DO NOT IGNORE!)

- Skip entirely for changes that don't alter rendered output.
- Read-only: surface findings, never fix.

## Step 1: Start the App

Start the app on deterministic fixture data and drive it via the chrome-devtools MCP.

The serve command comes from the project config (`.claude/auto-task.config.md`, design-review section) — e.g. a recipe that serves test fixtures. If no such entry exists, look for an obvious fixture-backed dev-server; if none, fail loudly — do not review against live/non-deterministic data.

Prefer a serve command that binds free ports (so parallel sessions don't collide) and navigate to the URL it prints — don't assume a fixed port.

## Step 2: Verify

1. **Measure, Don't Eyeball.** Read DOM geometry / computed styles (`getBoundingClientRect`, colour, contrast) and compare to the spec.
2. **Check Token Fidelity.** Read the diff, not just the render — flag hardcoded literals where a token was specified (e.g. `#3B82F6` instead of `var(--color-primary)` or a `bg-primary` utility). Computed styles collapse the token name, so this is a source-level check.
3. **Confirm the Gestalt** with a screenshot against the design reference. Save the frames — one per state×theme the change actually touches, plus open interaction states (tooltip/popover) — under `.design-review/<task-or-slug>/` (ensure it's gitignored) so the human can review them without re-booting the app. The chrome-devtools screenshot tool only writes within the repo workspace root, so save there even when reviewing a worktree (not under the worktree path).
4. **Exercise Interaction States** (hover / focus / open) with *real* input (real key/click events) — synthetic dispatch hides state-dependent bugs. Also cover the data / UI states the design defines (disabled / error / empty / loading), driven via the fixtures.
5. **Check for Unguarded Invariants** — load-bearing geometry / colour with no e2e assertion.

## Step 3: Output

Findings only — no edits. Match `/at:review-code`'s format so downstream triage consumes code and design findings uniformly:

- Severity: Critical / Major / Minor / Nit
- One-line finding + cited evidence (the measured number vs the spec, or the screenshot deviation)
- For an unguarded invariant: name the e2e assertion to add — the fix happens downstream, not here
- Reference the saved screenshot paths (Step 2.3) so the reader can open the frames alongside the findings

No autofix lane: design findings aren't mechanically certain, so every one goes through full triage.
