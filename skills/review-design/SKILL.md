---
name: review-design
description: Use to review a design / UI change against its intent — measure the live app instead of eyeballing, and flag deviations. Read-only; produces findings, applies no fixes. Sibling of /review-code.
---

# Review Design

## Usage

`/review-design [the change + its design intent]`

## Goal

Verify a design / UI change matches the intended design, objectively. Read-only: surface findings, never fix. Skip entirely for changes that don't alter rendered output.

## Method

Serve the app on deterministic fixture data and drive it via the chrome-devtools MCP:

    just serve test   # api :8100 / vite :5273 on the test fixtures → http://localhost:5273/?theme=light

Fixed fixtures give stable, machine-independent measurements (real data drifts between runs).

1. **Measure, Don't Eyeball.** Read DOM geometry / computed styles (`getBoundingClientRect`, colour, contrast) and compare to the spec — objective numbers beat impressions.
2. **Confirm the Gestalt** with a screenshot against the design reference.
3. **Exercise Interaction States** (hover / focus / open) with *real* input (real key/click events) — synthetic dispatch hides state-dependent bugs.
4. **Check for Unguarded Invariants** — load-bearing geometry / colour with no e2e assertion.

## Output

Findings only — no edits. Match `/review-code`'s format so downstream triage consumes code and design findings uniformly:

- Severity: Critical / Major / Minor / Nit
- One-line finding + cited evidence (the measured number vs the spec, or the screenshot deviation)
- For an unguarded invariant: name the e2e assertion to add — the fix happens downstream, not here

No autofix lane: design findings aren't mechanically certain, so every one goes through full triage.
