# Proposal: Four Improvements to the TAD Skill System

**Status:** done — implemented in 9e197e0 (2026-04-09)

Cross-pollinated proposal. Three independent reviewers (feasibility, completeness, simplicity) validated and refined this — synthesis at the end.

---

## The Four Problems (All Validated as Real)

1. **No state persistence**: `/research` loses all agent work if a session crashes mid-synthesis.
2. **No scope calibration**: A simple factual question gets the same 7-agent + review loop treatment as deep strategic analysis.
3. **Invisible review quality**: `/review-loop` says "log rejected findings" but has no structure. Findings silently disappear or get sycophantically accepted.
4. **Context pressure drift**: Critical instructions (Problem Anchor, cite-or-flag) stated once at session start. Long-running sessions forget them.

---

## Implementation Plan: One at a Time

All three reviewers converged on: **implement sequentially, validate with real runs before layering the next**. Batching all four creates a confounding problem — if research quality changes, you won't know which improvement caused it.

### Phase 1: Scope Calibration

**Why first**: Highest waste prevented. A simple question running the full protocol wastes 20-30 minutes. This is the most impactful change.

**Change to `/research` Step 1** — add after Problem Anchor formulation:

> Assess complexity. For simple factual lookups, propose 1-2 agents and no review loop. For standard multi-source questions, 3-5 agents and 1 review round. For deep strategic questions, the full protocol. Present this assessment with the plan — the user can override.

No tier table, no hardcoded agent counts. The agent uses judgment; the user approval gate (already in Step 1) catches miscalibration. The vocabulary Light/Standard/Deep is useful shorthand but not a formal specification.

**Safeguards**:

- **Never skip the user gate for Light**, even if it seems obvious. A 5-second confirmation costs nothing; a shallow answer to a hidden-depth question costs a re-run. (Feasibility reviewer flagged this — "rubber-stamp gate" risk.)
- **Escalation**: If a Light-tier agent returns conflicting evidence or signals hidden complexity, escalate to Standard with user confirmation rather than delivering a shallow answer. (Completeness reviewer identified this gap.)

**Validate**: Run 5-10 research tasks spanning simple→complex. Check: Does the agent calibrate reasonably? Does the user override frequently? Do Light results miss important nuance?

---

### Phase 2: Problem Anchor Re-Statement

**Why second**: Cheap (one sentence added per phase transition), guards all subsequent improvements against their own failure mode (long skill runs drifting from protocol).

**Change to `/research`** — add to Steps 3, 4, and 5:

> Re-read the Problem Anchor and resolution criteria before starting this step.

That's it. One sentence each. No Protocol Reminder template, no rule re-statement block. The Problem Anchor is the valuable core — re-stating rules that are already in the active instructions is cargo cult (all three reviewers converged on this).

**Change to `/review-loop`** — add at the top of each review round:

> Re-state the Problem Anchor before reviewing.

**Change to `/impl-task`** — add between TDD steps:

> Re-read the current plan step and its verification criteria before proceeding.

**Platform limitation** (noted by completeness reviewer): This is a mitigation, not a guarantee. True context-compaction hooks (like Yegge's PreCompact) require platform support that doesn't exist in Claude Code today. Phase-transition re-statement is the pragmatic ceiling.

**Validate**: In 3-5 long research runs, check whether the Problem Anchor actually appears in model output at phase transitions. If the model ignores the instruction under pressure, the mechanism isn't working.

---

### Phase 3: Pushback Log

**Why third**: Makes review quality visible. Creates the observability needed to evaluate whether scope calibration tiers are well-tuned.

**Change to `/review-loop`** — replace the free-form "log rejected findings" instruction with:

> Record each reviewer finding and its disposition in a markdown table:
>
> | #   | Reviewer claim | Response | Outcome |
> | --- | -------------- | -------- | ------- |
>
> Outcome is `accepted` or `rejected` with a one-line reason. For rejections, the existing categories apply: the finding is factually wrong (evidence), would drift from the Problem Anchor (drift), or costs more than it's worth (disproportionate).
>
> Include the table as a "## Review Process" section in the final artifact.

No formal taxonomy with capitalised labels. The three rejection categories already exist in the skill (Step 3, lines 47-55) — they stay as vocabulary in the reason column, not as an enum.

**Edge cases** (completeness reviewer): When a finding is partially accepted, split into two rows. When a finding is valid but already addressed, record as "accepted: already present, no change needed." Keep it pragmatic.

**For `/research`**: The review process table flows into the research document as an appendix. For Deep-tier research with multiple rounds, consider writing the review log to a separate `{slug}-review-log.md` rather than bloating the main document (feasibility reviewer flagged appendix length).

**Validate**: After 3-5 review loops, check: Does the table actually get produced? Is it useful for understanding review quality? Do rejections have real reasons or boilerplate?

---

### Phase 4: State Persistence

**Why last**: Most complex. Benefits from scope calibration (Light-tier runs don't need persistence) and Problem Anchor re-statement (the file I/O instructions themselves are prone to drift in long sessions).

**Design — file-presence as implicit state** (simplicity reviewer's proposal, which also resolves the feasibility reviewer's "second code path" concern):

Each agent writes its output to `docs/research/wip/{slug}/{agent-name}.md` as it completes. No `state.json`. No phase tracking. The presence of files *is* the state:

- No `wip/{slug}/` directory → not started
- Some `{agent-name}.md` files → researching (some agents completed)
- All expected agent files present → ready to synthesise
- Final document in `docs/research/` → done

**Resumption**: On invocation, if `wip/{slug}/` exists, list the files, present what's there, and ask the user:

- **Resume**: Skip completed agents (those with output files), re-dispatch the rest
- **Synthesise now**: Use what's available, skip missing agents
- **Restart**: Delete the wip directory and start fresh

This avoids: slug-matching fragility (the user picks from existing wip directories), JSON state staleness (no second source of truth), and the "second code path" problem (resume is just "skip agents that have files").

**Cleanup**: On successful delivery, delete `wip/{slug}/`.

**Scope**: `/research` only. `/kaizen` and `/cross-pollinate-code-review` are shorter-running. If the pattern proves useful, extract as a convention to CLAUDE.md later.

**Validate**: Deliberately interrupt a research session mid-agent-completion. Resume. Check: Are completed agent outputs preserved? Does synthesis use them correctly?

---

## Future Applicability (Not in Scope, Noted for Reference)

These patterns apply to other multi-agent skills but implementation is deferred until validated in `/research`:

| Skill                                      | State persistence |   Scope calibration   |         Pushback log          |    Anchor re-statement    |
| ------------------------------------------ | :---------------: | :-------------------: | :---------------------------: | :-----------------------: |
| `/kaizen` (8 subagents)                    |        Yes        | Yes (focused vs full) |              N/A              | Yes (reconciliation step) |
| `/cross-pollinate` (2-3 models)            |    No (short)     |          No           | Yes (contradiction decisions) |   Yes (synthesis step)    |
| `/cross-pollinate-code-review` (iterative) |    No (short)     |          No           |  Yes (critique disposition)   |  Yes (convergence check)  |
| `/plan-task` (dialectic, 3 models)         |    No (short)     |          No           | Yes (disagreement resolution) |  Yes (refinement rounds)  |

**Cross-cutting extraction**: After Phase 4, if the patterns are stable, extract to CLAUDE.md as conventions:

- "Long-running skills: re-state the Problem Anchor at each phase transition"
- "Review skills: record finding dispositions in a markdown table"
- "Multi-agent skills: persist agent outputs to `wip/{slug}/` for crash recovery"

---

## Cross-Pollination Process

**Reviewers**: Three independent Claude agents, fresh context, different mandates (feasibility, completeness, simplicity). Codex dispatch attempted but failed (model not supported with ChatGPT account).

**Where all three agreed**: All four problems are real. State persistence is highest risk. Pushback log is lowest risk. Light tier needs safeguards. User approval gate must not be bypassed.

**Key simplifications from synthesis**:

- State persistence: Dropped `state.json` (all three flagged over-engineering risk; simplicity reviewer proposed file-presence alternative that resolves feasibility reviewer's "second code path" concern)
- Scope calibration: Replaced tier table with prose guidance (simplicity reviewer; the agent uses judgment regardless)
- Pushback taxonomy: Dropped formal 5-category enum (simplicity reviewer; existing rejection vocabulary is sufficient)
- Protocol Reminder: Reduced to Problem Anchor re-statement (all three converged; full template is cargo cult)
- Implementation order: Flipped to scope calibration first (simplicity reviewer; highest waste prevented), validated by completeness reviewer noting improvements 1 and 2 are independent

**Unresolved tension**: Feasibility reviewer noted that adding all 4 improvements increases skill instruction length, which *increases* context pressure — the exact problem Improvement 4 tries to solve. Resolution: keep changes minimal (the simplified versions above are ~50% less text than the originals) and implement one at a time so skill length grows gradually.
