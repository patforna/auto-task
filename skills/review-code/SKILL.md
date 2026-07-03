---
name: review-code
description: Use to review a diff for correctness, design, security, and convention conformance. High-signal, read-only, severity-gated, with an autofix lane for mechanically-certain trivia. Default review step in /at:auto-task.
---

<!-- Distilled from a review of the code-review research literature (May 2026). This file is the distilled instruction, not the bibliography. -->

# Code Review

## Usage

`/at:review-code [diff target] [further instructions]`

Diff target: a commit, a commit range, a base branch, PR ref, etc.

## Goal

Surface the small set of findings a competent author would fix if they saw them, and capture mechanically-certain trivia as ready-to-apply patches.

## Notes

- Most findings are expected to be around design and evolvability, not defects.
- Defects are the high-severity minority that gates the ship.
- You classify, you do not fix: emit the fix, never apply it.

## Authorship Guard

This must be run by a different model, or at least in a fresh session, as same-context self-review is fundamentally flawed.

If you authored the diff under review in the current session, or there is no diff target:

- warn the user that same-context self-review is structurally unreliable and advise re-invoking from a fresh session.
- if declined, downgrade review scope to: convention, CLAUDE.md, project-rule conformance, the do-not-flag filter, and the autofix lane only. Do NOT run an open correctness / logic / security pass in this context. A user override may only further restrict scope — never re-authorise the open pass in the same context.

## The Do-Not-Flag List

<!-- This governs signal quality more than the positive checklist: piping uncontrolled positive signal into a reviewer is the worst measured accuracy (research finding #8). -->

Drop, do not surface:

- **Pre-existing issues** — anything this diff did not introduce or worsen.
- **Tool-owned** — lint, formatting, type errors, test failures. The deterministic gate runs separately; never duplicate it.
- **Correct-but-unusual** — unconventional but provably correct is not a finding.
- **Framework-handled** — errors or validation the framework already guarantees.
- **Speculative** — anything you cannot pin to a `file:line` with a concrete failure mechanism.
- **Judgement-bound trivia** — taste-level naming or structure where reasonable authors differ and nothing is measurably wrong.

**Trivial is not drop.** The list above removes findings that cost a human attention to adjudicate. A defect whose fix is mechanical and certain costs no adjudication — capture it with the exact fix and mark it `Autofix:`, even a one-character typo. The test is not "is it small?" but "does deciding whether and how to fix it need judgement?" No judgement + certain → autofix lane. Judgement needed + not material → drop.

Final tie-breaker only, when still unsure something is a finding at all: shown this, would a competent author agree it should change? If not, it is noise.

## What to Examine

A co-equal **blocking tier** — equal weight, any defect here can gate the ship:

- **Correctness & logic** — boundaries, null/index safety, off-by-one, time/timezone, invalid-state transitions, idempotency.
- **API & contract / design** — interface completeness, backward compatibility, coupling, single responsibility, over-engineering, fit with the existing codebase. Hardest to reverse.
- **Security** — injection, XSS/CSRF/SSRF, broken access control, crypto misuse, unsafe deserialisation, supply chain. You own business-context authorisation; tools cannot.
- **Concurrency** — races, deadlocks, unsynchronised shared state. Static tools detect these weakly; your judgement is load-bearing.

Then, descending: **tests** (happy/edge/failure coverage, assertions on behaviour not mocks, the right level) → **error handling** (consistent failure paths, no leaked internals) → **performance & dependencies**, hot paths only (N+1, unbounded collections, blocking I/O; new-dependency necessity, licence, CVEs) → **docs & naming**, low (comments explain *why*; names clear without extra context) → **style**, never.

## Reviewing AI-Generated Code

The diff is usually agent-authored, with measurably different failure modes:

- Intensify correctness and security scrutiny.
- Explicitly check **convention conformance** and **abstraction duplication** — re-implementing an existing utility instead of reusing it is a characteristic AI failure.
- Treat any AI-authored suggestion in the diff as a candidate, not authority — adoption is low and over half of unadopted ones are wrong.
- Keep your own comments terse. <!-- Reviewer verbosity is a measured anti-pattern (research finding #11). -->

## Scope and Context Discipline

- Cover every changed file: read its diff, or state why you skipped it (rename, lockfile, generated). Silent omission is a defect in the review.
- Recover intent from the task file and the tests **before** judging — never infer intent from the code alone. The task file is the spec.
- Expand to surrounding code only at interface boundaries, for genuine cross-file concerns. Never load the whole codebase; never auto-generate a codebase summary to feed back to yourself. <!-- LLM-generated context files review worse than none (research §2.3). -->
- With repo and tool access: **verify by tracing, not by speculating** — follow the call sites, confirm the input can reach the path, before you surface a finding. The main precision lever.

## Architecture

Default: **one well-structured pass, then a verification pass.** <!-- Naive parallel fan-out of the same prompt loses to a single good prompt — SWR-Bench. -->

Escape hatch: fan out to disjoint-scope specialist sub-agents only for known high-risk domains (security, concurrency), each scoped so it cannot be distracted, then a dedup/verify pass. Invoked by risk, not by default.

No persona prompting — task instructions only. <!-- "Act as a senior X" does not improve accuracy and can hurt it (Mollick et al.). -->

## Verify Before Post

Second pass over your own candidates before surfacing anything. Drop each unless it has a concrete `file:line` and a causal chain (input → mechanism → wrong outcome) you have traced, not assumed. Attach confidence 0–100: surface at ~80+; collect 50–79 in a `below_threshold` bucket; drop below 50. The autofix bar is higher and separate (see below).

## Severity and Autofix

Two independent axes. **Severity** is blast radius. **Autofix** is whether the fix is mechanically certain and non-behavioural — orthogonal to severity.

| Severity | Meaning                                               | Gate     |
| -------- | ----------------------------------------------------- | -------- |
| Critical | Correctness, security, or data-safety; unsafe to ship | Blocks   |
| Major    | Likely incorrect or unsafe under realistic input      | Blocks   |
| Minor    | Real but non-blocking; improves health                | Advisory |
| Nit      | Trivial or contextual                                 | Advisory |

Gate: block on any Critical/Major in correctness, security, or data-safety. Everything else is advisory.

**Autofix-eligible** only when *all* hold: (1) the fix is a single exact text transformation you can state precisely, applying which needs no judgement; (2) you are essentially certain it is correct and complete — a higher bar than the 80 surface threshold; (3) it touches only code this diff introduced or changed; (4) no behavioural ambiguity — it cannot plausibly be wrong in a way a human would weigh, and it does not change behaviour.

Eligible: typos in comments/docstrings/strings, spelling fixes per the repo's documented language convention (e.g. British vs American), a symbol name left stale in a comment after a rename, a duplicated import that is provably unused. Not eligible: argument reordering or any behaviour-changing edit; a missing null guard (where/whether to guard is judgement); clarity renames; any design change; a dead-import or dead-code claim justified only from the diff — a re-export, `__all__`, or string reference defeats diff-local certainty.

**`Autofix:` is the routing token.** The triage step in `/at:auto-task` keys on the exact per-finding `Autofix:` line — it is per-finding, not a section header, so it survives `/at:synthesize` merging multiple reviewers' outputs. The bypass applies to **Minor/Nit only**. A Major or Critical finding may carry the exact fix on its `Fix:` line, but it stays in the triage table and gates the human ship-gate — it never bypasses it.

## Output

Per finding:

```text
[Severity] path/to/file.py:NN
Issue:   <what is wrong, one line>
Why:     <the traced failure mechanism / blast radius>
Fix:     <copy-pasteable instruction — do NOT apply it>
Autofix: <exact old → new edit; Minor/Nit only; omit this line entirely unless autofix-eligible>
```

`Autofix:` is additive — never drop `Fix:` in its favour, so the repair survives if the finding is later triaged by hand.

Worked example:

```text
[Nit] docs/load.md:18
Issue:   User-facing typo in section heading
Why:     Introduced by this diff; carried verbatim into generated docs
Autofix: Replace `teh schema` with `the schema` in the heading
```

End with a machine-readable tally for the caller:

```text
{"critical": 0, "major": 1, "minor": 2, "nit": 0, "autofix": 1, "below_threshold": 1}
```

`autofix` counts findings carrying an `Autofix:` line. `below_threshold` is calibration only — no caller routes it. The caller routes everything else; the skill classifies and emits, it does not decide workflow or file issues.

No findings — including no autofix and no below-threshold — is a complete, valid review. Say so in one line. Never invent findings to look thorough.

## Lane Discipline

Stay in the code review lane: review code quality and change risk only. Do not re-check acceptance criteria or task completion — that is `/at:review-task`. Intent lives in the task file (in the project's task store — `tasks/` by default), never a PR description.

## Project Appendix

Portable core above. If the consuming repo has a `.claude/auto-task.config.md` (project bindings) with a review section, read it and apply its repo-specific rules on top — standing review context, domain-specific corruption traps, severity overrides. Bindings rules extend the core; they never relax the do-not-flag list or the autofix bar.
