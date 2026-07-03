# Task Sizing & Granularity for Agentic Workflows

Research into how tasks should be sized when the implementer is an AI agent, not a human engineer. Conducted to pressure-test the define-task skill's sizing guidance.

Date: 2026-03-13

---

## Motivation

The define-task skill had lightweight sizing guidance: "roughly 1–2 days of human engineering effort; more than ~10 acceptance criteria is a signal to split." The concern: "1–2 days of human effort" may not be the right mental model when the implementer is an AI agent — agent failure modes around task size are fundamentally different from human ones.

## Method

5-agent parallel research, each investigating a different angle, followed by synthesis and pressure testing against 3 scenarios (trivial bug fix, medium feature, large cross-cutting refactor).

---

## Agent 1: Human Sizing Literature

### INVEST Criteria — What Transfers

| Letter      | Principle                   | Agent relevance |
| ----------- | --------------------------- | --------------- |
| Independent | No blocking dependencies    | Critical        |
| Negotiable  | Solution open to discussion | Irrelevant      |
| Valuable    | Delivers user value         | Transfers       |
| Estimatable | Team can size it            | Irrelevant      |
| Small       | Completable in days         | Transfers       |
| Testable    | Clear acceptance criteria   | Critical        |

I, S, T are load-bearing for agents. N and E solve human coordination problems that don't exist.

### Key Principles That Transfer

- **Thin vertical slices** — each increment is independently testable, committable, shippable. Directly applicable.
- **Right-size for the verification loop, not the worker's capacity.** Agents don't have fixed capacity — they have a reliability curve that degrades with size. Size to how cheaply the result can be verified.
- **SPLIT patterns** (Richard Lawrence) — business rules, workflow steps, simple/complex, data variations, spike before implementation. Transfer almost entirely.
- **Reinertsen's batch size economics** — agent transaction costs are very low (no standup, no handoff), so optimal batch size is very small.
- **Yesterday's weather** — don't estimate; measure throughput and use historical data to forecast.

### What Doesn't Transfer

- Story points / relative estimation — team calibration tool, irrelevant for solo agent.
- Planning Poker — value was shared understanding among humans.
- Negotiability — no human negotiation loop.

### Sources

- Bill Wake — INVEST criteria (2003)
- Richard Lawrence — Story Splitting Flowchart
- Don Reinertsen — Principles of Product Development Flow
- DORA — Working in Small Batches
- Vasco Duarte / Woody Zuill — NoEstimates

---

## Agent 2: Agent Failure Modes Around Size

### The Headline Numbers

- **SWE-bench → SWE-bench Pro:** Top models drop from 70%+ to ~23%. A 3x collapse moving from single-file scoped bugs to multi-file long-horizon tasks.
- **FeatureBench (ICLR 2026):** Claude 4.5 Opus drops from 74% to **11%** on multi-file feature work.
- **73% of task failures** are cascading errors from a single root cause (arXiv 2509.25370).

### Failure Mode Taxonomy

| Mode                        | Onset                             | Nature      | Mitigable?        |
| --------------------------- | --------------------------------- | ----------- | ----------------- |
| Context rot                 | Gradual from ~50K tokens          | Slope       | Partially         |
| Error compounding           | Any multi-step task               | Exponential | Yes (gates)       |
| Intent drift                | After ~20 consecutive tool calls  | Gradual     | Yes (specs)       |
| Coherence loss (multi-file) | 3+ files touched                  | Cliff       | Partially         |
| Scope creep                 | Any size, damage scales with size | Persistent  | Yes (constraints) |
| Lost thread                 | ~50K tokens, worse at 100K        | Gradual     | Partially         |
| Verification gap            | Scales with change size           | Linear      | Partially         |

### Key Findings

- **Cascading errors are the dominant failure mode.** A single wrong assumption in step 2 of a 10-step task makes steps 3–10 wrong. At 90% per-step accuracy, a 10-step task has 35% full success probability.
- **The fix is decomposition + specs, not mid-task correction.** Cognition (Devin): "sending more messages to correct a veering agent is more likely a sign that the task's inherent complexity exceeds the agent's capabilities."
- **Context rot is structural.** All 18 frontier models tested (Chroma Research 2025) show degradation at every context length increment, not just near limits. "Lost in the middle" effect confirmed.
- **Fresh context for subtasks** is Anthropic's own recommendation — eliminates accumulated bias.

### Sources

- SWE-bench Pro (arXiv 2509.16941)
- Chroma Research — Context Rot (2025)
- AgentDebug — Where LLM Agents Fail (arXiv 2509.25370)
- Cognition — Devin 2025 Performance Review
- METR — Developer Productivity Study (2025-07)
- Microsoft — Failure Modes in Agentic AI Systems

---

## Agent 3: Agent-Specific Sizing Dimensions

### The Quantitative Foundation

- **METR 50%-task-completion horizon:** ~1 hour human-equivalent for Claude 3.7 Sonnet. Doubling every ~7 months.
- **Toby Ord half-life model:** Doubling task duration roughly squares failure probability. Updated Feb 2026: agents actually have a **declining hazard rate** (Weibull model) — more likely to fail during orientation than execution. Agents that survive the setup phase do better than the naive model predicts.
- **Practical sweet spot:** ~30 minutes human-equivalent (METR). Every agent tested showed performance degradation past 35 minutes.
- **Cascading edit failures:** 23.4% of agent failures (Microsoft taxonomy).

### Dimensions That Matter More for Agents

| Dimension                   | Evidence                                                                                                 |
| --------------------------- | -------------------------------------------------------------------------------------------------------- |
| Files touched               | Primary predictor. Multi-file 3% of easy, 56% of hard SWE-bench tasks.                                   |
| Cross-module coordination   | Distinct from file count. Even Opus-class fails on semantic correctness in multi-file edits.             |
| Context load (relevance)    | ETH Zurich/DeepMind: LLM-generated AGENTS.md *reduces* success by 2–3%. More context ≠ better.           |
| State accumulation          | Each step is independent failure point per Ord model.                                                    |
| Ambiguity in ACs            | Binary multiplier. Ambig-SWE: models can't distinguish well-specified from under-specified instructions. |
| Novelty vs pattern-matching | Steepest performance dropoff on novel architectural decisions (RE-Bench).                                |

### Dimensions That Matter Less for Agents

Fatigue, context switching cost (but context *window* limits matter), communication overhead, motivation, learning curve (but no cross-session retention).

### The Key Insight

The hard part is **orientation, not execution.** Ord's Weibull finding means self-contained task specs that enable fast orientation are the highest-leverage intervention.

### Sources

- Toby Ord — Half-Life for AI Agent Success Rates (2025, updated Feb 2026)
- METR — Measuring AI Ability to Complete Long Tasks (2025)
- METR — Task-Completion Time Horizons
- SWE-bench Pro (arXiv 2509.16941)
- FeatureBench (ICLR 2026, arXiv 2602.10975)
- Ambig-SWE (arXiv 2502.13069)
- ETH Zurich / DeepMind — Evaluating AGENTS.md
- RE-Bench (METR)
- Microsoft — Failure Modes in Agentic AI Systems

---

## Agent 4: Decomposition Patterns for Agents

### Classical Patterns Evaluated

| Pattern              | Agent verdict                                                                                            |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| Thin vertical slices | Good default when codebase has clear layer interfaces.                                                   |
| Horizontal layers    | **Surprisingly good for agents.** No silo problem — each session starts fresh. Containment is a feature. |
| Interface-first      | **Best pattern for multi-agent work.** Interface IS the coordination mechanism.                          |
| Walking skeleton     | **Excellent.** Concrete scaffolding for subsequent sessions.                                             |
| By business rule     | Clean — maximally independent subtasks with isolated ACs.                                                |
| By workflow step     | Natural for sequential processes; define intermediate formats upfront.                                   |
| By data variation    | Self-contained subtasks per input type.                                                                  |

### When Decomposition Helps Agents

- Reduced context window pressure (each session loads only what it needs)
- Clearer verification (small tasks loop until tests pass)
- Parallelism (worktrees enable 3–5 concurrent agents)
- Fault isolation (bad output on one subtask doesn't lose others)

### When Decomposition Hurts Agents

- Coordination overhead (Anthropic + OpenAI: "decision-making overhead often exceeds benefits of splitting into multiple agents")
- Loss of holistic understanding (integration bugs — "10 devs who never talked to each other")
- Redundant context loading across sessions
- Artificial seams in naturally cohesive work

### Minimum Viable Task

- **Too small:** rename variable, fix typo. Overhead exceeds value.
- **Sweet spot:** Read 2–5 files, change 1–3 files, verify with 1–5 checks. 3–7 acceptance criteria.
- **Too large:** >10 files in working memory, or context degrades before completion.

### The Integration Problem

Who ensures pieces fit together?

1. Type system as contract enforcer
2. Integration test task after component tasks
3. Review agent reading all diffs
4. Merge-then-test cadence (each worktree merges, CI catches failures)

### Sources

- Anthropic — Building Effective Agents
- Addy Osmani — LLM Coding Workflow (2026)
- incident.io — Shipping Faster with Claude Code and Git Worktrees
- OpenAI — Practical Guide to Building Agents
- InfoQ — Working with Code Assistants: Skeleton Architecture

---

## Agent 5: Acceptance Criteria Count as Sizing Proxy

### AC Count Vs Complexity — Weak Correlation

3 complex ACs can be harder than 15 simple ones. AC count conflates breadth with depth. It's a signal, not a measure.

### Alternative Proxies Ranked

| Proxy                    | Measurability | Correlation with agent difficulty |
| ------------------------ | ------------- | --------------------------------- |
| Files likely touched     | High          | Strong                            |
| Files needed for context | Medium        | Strong                            |
| Distinct test scenarios  | High          | Moderate-Strong                   |
| Behavioural boundaries   | Medium        | Moderate                          |
| Output line estimate     | Medium        | Strong (>300 lines = error spike) |

### The Goldilocks Zone

| Range    | Signal                                                        |
| -------- | ------------------------------------------------------------- |
| 1–2 ACs  | Too vague or trivially small                                  |
| 3–7 ACs  | Sweet spot — enough specificity, fits in context              |
| 8–12 ACs | Amber zone — check file count and context radius before split |
| 13+ ACs  | Almost certainly should split                                 |

### Recommendation

Multi-signal heuristic beats single threshold. AC count is valuable because it's available early, but should be triangulated with files touched and context radius. The ~10 threshold is well-calibrated as a smell test (confirmed independently across multiple practitioner sources), but it's a smell test that triggers deeper analysis, not a hard rule.

**Goodhart's Law risk:** If AC count becomes the target, defining agents will write fewer, fatter ACs to dodge the threshold.

### Sources

- Toby Ord — Half-Life model (2025, updated 2026)
- METR — Long Tasks (2025)
- Scrum.org — AC count best practices
- Agile Learning Labs — Splitting by AC
- CodeScene — Agentic AI Coding Patterns

---

## Synthesis

### Where All 5 Perspectives Converge

1. **Files touched is the strongest predictor** of agent difficulty — stronger than time estimates, AC count, or lines of code. SWE-bench Pro: 3x collapse at multi-file boundary. FeatureBench: 74% → 11%.

2. **Decomposition has exponential payoff** for agents (METR/Ord half-life model), vs roughly linear for humans.

3. **Right-size for verification, not capacity.** The question isn't "can the agent do this?" but "can the result be verified cheaply?"

4. **Orientation > execution.** Ord's Weibull finding: agents fail more during setup than execution. Self-contained task specs are the highest-leverage intervention.

5. **Ambiguity is a binary multiplier.** Either the agent can verify its own work or it can't.

6. **AC count is a valid but insufficient proxy.** Multi-signal triangulation (ACs + files touched + context radius) is clearly better.

### The Size Debate

| Source                  | Recommended size                    |
| ----------------------- | ----------------------------------- |
| METR empirical optimal  | ~30 min human-equivalent            |
| Cognition (Devin)       | 4–8 hours junior engineer           |
| Previous skill guidance | 1–2 days senior engineer            |
| Reinertsen theory       | As small as transaction costs allow |

The 30-minute finding is from early-2025 models; the horizon doubles every ~7 months. With excellent specs (which the skill aims to produce), agents can handle larger tasks. The right answer is model-dependent and will shift — which argues against a time-based anchor entirely.

### Decision

Replace the single "1–2 days + ~10 ACs" heuristic with a multi-signal split check plus where-to-cut patterns. Drop the time-based anchor (goes stale). Add a lower bound to prevent over-splitting.

---

## Pressure Test Results

| Scenario                            | Split signals fired | Guidance verdict               | Correct? |
| ----------------------------------- | ------------------: | ------------------------------ | -------- |
| Trivial bug fix (1 file, 2 ACs)     |                   0 | Don't split                    | Yes      |
| Medium feature (4 files, 7 ACs)     |                   1 | Borderline, proceed as one     | Yes      |
| Large refactor (8–12 files, 14 ACs) |                   3 | Split — walking skeleton first | Yes      |

The walking-skeleton pattern covered the refactoring scenario well. Minor gap: no explicit "by dependency cluster" pattern for refactors, but walking skeleton plus the existing patterns were sufficient.

---

## Validity Window

This research is based on models and benchmarks available as of March 2026. Key assumptions that may shift:

- METR's 50% horizon doubles every ~7 months → re-evaluate sizing thresholds when new METR data publishes
- FeatureBench 11% resolve rate for multi-file work → track whether this improves with newer models
- Toby Ord's Weibull/declining-hazard finding → may change with architectural improvements (longer context, better planning)
- The "files touched" cliff at 3+ → may soften as models improve at multi-file coordination

**Re-validate by:** September 2026 or when next-generation models (post Claude 4.5 Opus) show benchmark results.
