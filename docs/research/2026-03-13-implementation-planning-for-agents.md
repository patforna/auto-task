# Implementation Planning for AI Agents

Consolidated research conducted 2026-03-13 via six parallel agents, each investigating a different angle. Informed the design of the `plan-task` skill.

---

## The Core Question

When an AI agent implements a well-defined task, what should the implementation plan look like? The answer depends on three variables: task complexity (how many files, how much ambiguity), model capability (which shifts constantly), and context management (fresh session vs accumulated).

The plan sits between two artifacts:

- **Task definition** (input) — what to build and why, with falsifiable ACs
- **Implementation** (output) — the actual code changes

The plan's job: **close the decision space without doing the work.**

---

## Where All Six Perspectives Converge

### 1. Plans as Behaviour Verification Lists, Not Implementation Checklists

Every tradition converges on this. TDD's test list IS the plan (Beck). BDD says specify observable behaviour, not mechanism (North, Keogh). Google design docs explain *why this approach*, not *how to write the code*. Emanuel says over-constraining during execution degrades output quality.

The inversion is subtle but load-bearing:

| Implementation checklist             | Behaviour verification list               |
| ------------------------------------ | ----------------------------------------- |
| "Create `GatedBacktestRun` class"    | "`backtest` CLI accepts a `--gate` flag"  |
| "Add validation to `parse_config()`" | "Invalid config raises with message X"    |
| "Refactor `run()` into two methods"  | "No `_compute_*` methods remain on `Run`" |

The behaviour is the requirement; the approach is flexible. An implementing agent that finds a better approach can deviate from the "how" as long as the behaviour is verified.

### 2. The Nervousness Heuristic

The single most actionable calibration tool that emerged from the research:

> Remove the plan. Give the agent just the task definition. What would you be nervous about? Those things — and only those things — belong in the plan.

What you'd be nervous about:

- The agent choosing the wrong module to extend
- The agent not knowing about an existing utility it should reuse
- The agent creating a new abstraction when it should modify an existing one
- A step requiring awareness of a non-obvious ordering constraint

What you wouldn't be nervous about:

- Whether the agent can write a for loop
- Whether the agent will choose reasonable variable names
- Whether the agent will discover obvious functions by reading the code

### 3. Verification per Step Is the Highest-Leverage Element

The most consistent finding across all sources:

- Anthropic: "the single highest-leverage thing you can do"
- Cognition: "tell Devin how to test or check its own work"
- METR: agents that verify progress avoid the 200K token plateau
- Plan-and-Act research: dynamic replanning improved success by 10.31%
- Beck's plan.md: every test is a verification gate

Plans without verification steps are wish lists. Plans with verification steps are feedback loops.

### 4. Fresh Eyes for Implementation

Emanuel, Anthropic, and METR converge: implementation should start from a clean context with only the plan and relevant source files. The exploration history (dead ends, rejected approaches) actively degrades implementation quality by biasing activation states. Anthropic: "start a fresh session to execute."

This makes plans MORE important, not less — the plan must be self-contained enough for a fresh agent to execute without the planning conversation.

### 5. Non-Goals Prevent Scope Creep

Google's design docs, Spotify's Honk agent experience (LLM judge vetoes ~25% of changes for going beyond scope), and the BDD research all converge: agents scope-creep because nothing said "don't." Explicit non-goals are the preventative.

### 6. Name Existing Code; Don't Name New Code

From the failure modes research: pointing the agent to existing code is helpful ("extend `BacktestRun.run()` to accept a `gate` parameter"). Pre- committing to new abstractions is harmful ("create `GatedBacktestRun`") because it locks in decisions before the implementing agent reads the codebase.

BDD's principle: specify behaviour, not mechanism — unless the mechanism IS the spec (refactoring tasks, formula-defined correctness).

---

## Traditional SE Traditions: What Transfers

### XP — Kent Beck

**Core insight:** Planning is a dialogue, not a document. The plan is a test list — a prioritised backlog of behaviours to implement.

Beck's direct AI experience (BPlusTree3 project): TDD is a "superpower" for agents. The `plan.md` pattern: a list of tests, each worked through with red-green-refactor, human watching and intervening with specific guidance when needed. Never mix refactoring and feature work in the same commit.

Skills deprecated vs amplified:

| Worth $0                  | 1000x leverage                |
| ------------------------- | ----------------------------- |
| Language syntax expertise | Vision and strategy           |
| API knowledge             | Task breakdown and sequencing |
| Boilerplate generation    | Feedback loop design          |
| Framework familiarity     | Knowing what to verify        |

### TDD

The test list IS the plan. The "red" step is a micro-decision about what to build next. Outside-in TDD (London school) is more relevant to agentic planning than classicist — it starts from user-visible behaviour and drills inward, matching the define-task → plan-task → impl-task flow.

### DDD — Eric Evans

The biggest planning failures are linguistic. Ubiquitous language prevents translation errors between spec and code. Bounded contexts are natural task boundaries. Strategic design (where to draw boundaries) matters more than tactical design (entities, value objects) for planning.

Minimum viable version: use the codebase's existing vocabulary in plans. If you find yourself using a term that doesn't appear in the code, that's either a missing abstraction or a misunderstanding.

### Martin Fowler — Evolutionary Design

Design is not a phase; it's an ongoing activity. The Design Stamina Hypothesis: good design pays for itself in weeks, not months. Refactoring is not cleanup; it's the primary mechanism by which design evolves. Separate structural changes from behavioural changes — exactly what Beck prescribes for agents.

### Google Design Docs

Non-goals are more valuable than goals. Alternatives-considered proves you've thought. The purpose is surfacing disagreements cheaply, not writing an implementation manual.

For agent plans: state the approach, state what you're NOT doing, name one alternative you considered and why you rejected it. Three sentences, not three pages.

### Thoughtworks / Lean

Walking skeleton first — thinnest end-to-end implementation touching all architectural components. Thin vertical slices — each increment is independently testable. Last responsible moment — defer reversible decisions until you have better information.

---

## Agentic Engineering: What the Evidence Shows

### Empirical Findings

| Finding                                                | Source                    |
| ------------------------------------------------------ | ------------------------- |
| Planning before coding improves Pass@1 by 11-25%       | Self-Planning (ACM TOSEM) |
| Plan diversity > plan detail                           | PlanSearch (ICLR 2025)    |
| Agent success drops 3x at multi-file boundary          | SWE-bench Pro             |
| 73% of failures cascade from single root cause         | AgentDebug (arXiv)        |
| 90% per-step accuracy → 35% success on 10 steps        | Cascading error model     |
| Dynamic replanning beats static plans by 10.31%        | Plan-and-Act (arXiv)      |
| Context rot at every length increment, not just limits | Chroma Research           |
| Agents fail more during orientation than execution     | Ord Weibull model (2026)  |
| METR 50% horizon doubles every ~7 months               | METR (2025)               |
| More context can REDUCE success rates                  | ETH Zurich / DeepMind     |

### The Overprompting Trap (Emanuel)

Over-constraining during planning degrades quality. Every word in a prompt consumes attention and narrows the solution space. The two-phase strategy:

| Phase     | Mode    | Provide                             | Withhold                  |
| --------- | ------- | ----------------------------------- | ------------------------- |
| Planning  | Open    | High-level goals, purpose, outcomes | Implementation details    |
| Execution | Precise | Detailed steps, interfaces, checks  | Exploration, alternatives |

"Models are now smart enough that, once they understand the high-level goals, they can do a better job planning than you can." Provide purpose and constraints — not how to achieve them. Save precision for execution.

### Plans as Compressed Context (Emanuel)

A plan document IS a compression of the exploration phase. It should contain decisions and rationale, not the process of arriving at them. Cramming raw data degrades performance even when it fits in context. Compressed, high-signal context outperforms exhaustive specification.

### Dialectic / Critique Pass (Emanuel)

Even without multiple models, the principle applies: generate a plan, then critique it from a fresh perspective. "What would a skeptical senior engineer say is wrong with this plan?" Catches structural problems before they propagate.

---

## Plan Failure Modes

### Over-Planning

| Anti-pattern                    | Why it fails                                      |
| ------------------------------- | ------------------------------------------------- |
| Plans as pseudocode             | Moves effort without reducing risk                |
| Pre-committing file/class names | Locks in decisions before reading the codebase    |
| BDUF                            | Speculative; economics favour deferred decisions  |
| Analysis paralysis              | Cost of perfecting spec > cost of agent iteration |

### Under-Planning

| Anti-pattern                 | Why it fails                                        |
| ---------------------------- | --------------------------------------------------- |
| Silent assumption resolution | Agent picks an interpretation without flagging it   |
| Missing non-goals            | Agent scope-creeps (Spotify: 25% of changes vetoed) |
| No verification steps        | Agent can't detect if it's on track                 |
| Under-specifying the "what"  | Catastrophic (unlike under-specifying the "how")    |

### The Calibration Checklist

Before approving a plan:

1. **Nervousness test** — remove the plan, read only the task. What are you nervous about? Is each concern addressed?
2. **Pseudocode test** — does any step describe *how* to write code rather than *what* to achieve? Too detailed.
3. **Ambiguity test** — could two agents make different architectural decisions? Too vague on what matters.
4. **Verification test** — does each step have a concrete check?
5. **Coupling test** — if step 3 fails, does the plan still make sense from step 4? Over-coupled.
6. **Length test** — can a human review this in under 5 minutes? Too long.

---

## Plan Review as Highest-Leverage Checkpoint

Plan review is the human's highest-leverage checkpoint because:

1. **Cheaper than code review.** A plan is 10-30 lines; the code may be 200-500.
2. **Catches highest-impact errors.** Wrong architectural decisions, missing non-goals, ambiguous criteria — visible in the plan, invisible in the code.
3. **Last chance before cascade.** After the agent starts, correcting course means discarding work. Mid-course correction rarely works for tasks beyond the agent's capability (Cognition).
4. **Fagan inspection evidence.** 30:1 payback ratio for every hour invested in design review (IBM, NASA/JPL data).

---

## Plan Format Comparison

Every major tool — Claude Code, Cursor, Codex CLI, Devin, Aider — produces free-form markdown. No standard schema exists. Structure comes from prompting.

The minimum viable plan that consistently appears across effective tools:

```text
## Goal
One sentence: what and why.

## Steps
1. [Behaviour] → verify: [check]
2. [Behaviour] → verify: [check]
3. [Behaviour] → verify: [check]

## Constraints
- Don't touch X
- Preserve Y
```

For complex tasks, add: approach rationale, non-goals, key files to read.

---

## The XP/BDD/TDD/DDD Stack for Agentic Planning

```text
DDD strategic patterns  →  WHERE to cut tasks (bounded contexts, aggregates)
BDD outside-in          →  WHAT to verify (observable behaviour)
TDD test list           →  HOW to sequence (simplest first, compound later)
XP thin slices          →  HOW BIG (independently shippable)
XP walking skeleton     →  WHAT FIRST (thinnest end-to-end path)
```

Maps to the TAD workflow:

```text
define-task  →  DDD (where to cut) + BDD (what to verify)
plan-task    →  TDD (sequencing) + XP (sizing, skeleton first)
impl-task    →  XP red-green-refactor cycle
```

---

## Solo Dev Implications

### Irreducible Planning Core

After stripping team coordination overhead:

1. **Clarify intent** — the task file carries both Card and Conversation (BDD)
2. **Separate what from how** — ACs are rock-solid; approach is flexible
3. **Decompose into verifiable increments** — exponential payoff for agents
4. **Verification criteria** — "single highest-leverage thing" (Anthropic)
5. **Context preparation** — which files, patterns, domain terms

### Thoughtworks + Google Synthesis

| Google design doc section | TAD equivalent            | Notes                            |
| ------------------------- | ------------------------- | -------------------------------- |
| Context and scope         | Description (why + what)  | Already in define-task           |
| Goals                     | Acceptance criteria       | Already in define-task           |
| Non-goals                 | Plan non-goals            | Optional, for non-obvious scope  |
| The design                | Implementation plan steps | plan-task output                 |
| Alternatives considered   | Approach rationale        | Optional, for non-obvious choice |

Non-goals and alternatives-considered are optional — overhead for small tasks, valuable for non-obvious approaches.

### Build for the Next LLM

| Timeless                   | Shifts with models     |
| -------------------------- | ---------------------- |
| Intent (why)               | Step granularity       |
| Acceptance criteria (what) | File-level hints       |
| Verification criteria      | Pattern references     |
| Domain vocabulary          | Edge case detail level |
| Decomposition              | Size thresholds        |
| Context curation           |                        |

The task definition is the durable artifact. The implementation plan is the ephemeral one — it gets thinner as models get more capable.

### Minimum Instruction Set for the Skill

The irreducible plan-task instructions:

1. Read the task and the code it touches (orientation before action)
2. Produce steps that can each be verified independently (cascading error prevention)
3. Show the plan to the user (human-in-the-loop gate)
4. Persist the plan (commit to git)

Everything else is either already in CLAUDE.md, inferable by capable models, or model-dependent detail that should shrink over time.

---

## Sources

### Traditional SE

- Kent Beck — TDD By Example; Tidy First? (Substack); BPlusTree3 (GitHub); Pragmatic Engineer interview (2025)
- Martin Fowler — "Is Design Dead?"; Design Stamina Hypothesis; "Context Engineering for Coding Agents"
- Eric Evans — Domain-Driven Design; Bounded Context (Fowler bliki)
- Alistair Cockburn — Walking Skeleton (97 Things)
- Mary & Tom Poppendieck — Lean Software Development; Last Responsible Moment
- Google — "Design Docs at Google" (Malte Ubl); SWE Book Ch. 10

### Agentic Engineering

- Anthropic — "Building Effective Agents"; Claude Code Best Practices
- Jeffrey Emanuel — "The Overprompting Trap"; "Making Complex Code Changes with Claude Code"; "Multi-Round LLM Coding Tournament" (jeffreyemanuel.com)
- Harper Reed — "My LLM Codegen Workflow ATM" (harper.blog, 2025)
- Simon Willison — "Using LLMs for Code" (simonwillison.net, 2025)
- Peter Steinberger — "Just Talk To It"; "My AI Dev Workflow" (steipete.me)

### Research

- METR — "Measuring AI Ability to Complete Long Tasks" (2025)
- Toby Ord — Half-Life model for AI Agent Success Rates (2025, updated 2026)
- Wang et al. — "Plan-and-Solve Prompting" (arXiv 2305.04091)
- PlanSearch — "Planning in Natural Language" (arXiv 2409.03733, ICLR 2025)
- Self-Planning Code Generation (ACM TOSEM 2024)
- Chroma Research — Context Rot (2025)
- AgentDebug — "Where LLM Agents Fail" (arXiv 2509.25370)
- Ambig-SWE (arXiv 2502.13069)
- Plan-and-Act (arXiv 2503.09572)
- SWE-bench Pro (arXiv 2509.16941)
- Spotify Engineering — "Background Coding Agents" Parts 2-3 (2025)
- Aider — Architect/Editor mode benchmarks (aider.chat)
- GitHub Spec Kit (github.com/github/spec-kit)
- Boehm & Basili — "Software Defect Reduction Top 10" (IEEE 2001)
- Fagan — "Design and Code Inspections" (IBM 1976)
- CHI 2025 — Plan-Then-Execute user study (ACM DL)

### Prior TAD Research

- `docs/research/2026-03-13-bdd-for-agentic-task-specs.md`
- `docs/research/2026-03-13-task-sizing-for-agents.md`
- `docs/research/2026-03-06-jeffrey-emanuel-agentic-engineering.md`
- `docs/research/2026-03-06-agentic-setups.md`
- `docs/research/2026-03-06-beads-yegge.md`
