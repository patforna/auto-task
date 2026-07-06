# Consolidated Research Synthesis

Condenses the research corpus in this directory (Mar–Jun 2026) into the actionable claims that shaped auto-task's skills, re-validated against the field as of 2026-07-03. Per-doc originals are provenance; when they disagree with this file, this file wins.

Reading rule for the whole corpus: **mechanisms are live, numbers are dead.** Every hard benchmark figure, model ID, tool version, and time/size anchor should be treated as expired (coding time-horizons now double in under 3 months). The July 2026 validation pass found no mechanism overturned — movement is softened anchors plus richer vendor tooling.

## Task Creation / Sizing

## (Task-Sizing, Bdd-for-Agentic-Task-Specs, Agile-Samurai)

- Size tasks for cheap verification, not worker capacity; never encode time anchors — they stale as models improve. **Validated 2026-07: the "3+ files = coherence cliff" and "~30-min sweet spot" numbers are stale (Opus 4.5/4.8-class models handle far larger scopes); the mechanism holds.**
- Files-touched is the strongest difficulty predictor; AC-count is a split smell test, not a hard rule.
- Concrete examples over abstract rules: if two agents could build different things from an AC, add an example. Specify observable behaviour, not mechanism or paths.
- Orientation beats execution — agents fail more during setup than implementation; self-contained specs are the highest-leverage input.
- Non-functional "fast/safe" items are constraints, not stories; testability is near-non-negotiable.
- **Field note 2026-07:** Spec-Driven Development (spec as source of truth, EARS-style ACs — Spec Kit, Kiro, etc.) is now the dominant industry frame. This corpus is compatible but pre-SDD in vocabulary.

## Planning

## (Implementation-Planning, Dialectic-Planning, Dialectic-Convergence)

- Plan = behaviour-verification list; every step pairs a behaviour with a verify check.
- Nervousness Heuristic: include only what you'd worry about; name existing code to reuse; never pre-commit new class/file names.
- Two-phase prompting: open during planning, precise during execution; fresh context for implementation.
- Plan review is the highest-leverage checkpoint (~30:1 payback). Auto-task deliberately trades this human gate for autonomy, moving the human gate to ship.
- Diversity beats detail in plan generation; every convergence round must inject external signal — pure self-reflection is net-negative. Cap rounds at ~3–5; most value lands in 2–3. **Validated 2026-07 with a caveat: diversity survives as the lever, but "must be different foundation models" softens to "inject diversity via model, seed, or context — matched to workload"; context isolation is the load-bearing part.**

## Implementation / TDD

## (Impl-Task-Skill-Research, Tdd-in-the-Agentic-Engineering-Era, Kent-Beck, Tdd-by-Example, Testing-Tools, Architecture-Testing-Tools)

- TDD is the control mechanism, non-negotiable where silent corruption is possible (wrong numbers, not errors); red→green→refactor inline with Fake-It/Triangulate/Obvious.
- Commit at green per plan step; force a refactor checkpoint after every green — AI only inhales complexity, it never exhales unprompted. **Alignment gap: the tdd skill has refactor-at-green only as optional cadence, not a mandatory logged step.**
- Pure-wiring steps skip TDD; apply by criticality. Two-attempt fix rule, then backtrack to last green.
- Keep the impl skill lean (~150 lines); overspecification reduces success while raising cost.
- **Open decision:** tdd-agentic-era argued for a subagent-isolated Red phase (test author ≠ implementer); impl-task-skill-research bet single-context with the pre-approved plan as substitute. The skills adopted single-context, yet their own guidance admits the failure mode ("AI-written tests often mirror what the code does"). The 2026 evidence (cross-context review, arXiv 2603.12123) favours revisiting — e.g. isolate Red for quant-critical modules only.
- Tooling settled: pytest-cov branch mode + pytest-randomly + Hypothesis on critical modules; skip mutmut/Codecov/pandera; custom architecture test over import-linter/tach.

## Code Review / Triage

## (Code-Review-Literature-and-Sota, Triage-Findings-Literature-and-Sota, Codex-Review-Internals; Supersedes the 2026-03-13 Code-Review Doc)

- Reviewer ≠ generator is the most robust finding. **Validated 2026-07 and sharpened: context isolation is the core mechanism (same-model critique in a fresh context recovers most of the benefit — arXiv 2603.12123); cross-model is a secondary diversity lever.** Same-context self-review degrades to convention-checking.
- Defects are only ~15% of review value; priority runs contract/design → correctness/security → tests → perf → docs → style (style fully automated, never a comment).
- The explicit do-NOT-flag list is the highest-leverage prompt element; piping raw SAST output in produces the worst F1.
- Naive multi-agent fan-out underperforms a single strong prompt + verify pass. **Validated 2026-07 (arXiv 2604.02460, equal-compute); carve-out: independent non-coordinating specialist reviewers (security/perf/contract) are the exception.**
- Triage is a router, not deliberation: deterministic drops → autofix bypass → ship-gate with traced dispositions. Never auto-reject Critical/Major; suppression must be visible. Calibrate via per-project memory — the 80-confidence gate is inherited and uncalibrated (still true of review-code as implemented).
- codex-review-internals is pinned to codex 0.129.0; the CLI is now well past that (0.142.x, permission profiles, GPT-5.5 default) — re-verify before relying on its baked prompts/schema.

## Design Review

## (Agentic-Design-Review-Sota)

- Deterministic assertions gate; AI/vision output is triage, not pass/fail. Measure, don't eyeball; check token fidelity at the source; drive real inputs; name the e2e assertion for any unguarded invariant. Skip pixel-VRT and Figma integration for a solo token-based stack.

## Repo Health

## (Repo-Health-Skill-Research)

- Health output is a report, not an alert; hard-cap 3–5 findings; cross-check against real code (hallucination risk is material); prioritise hotspot = complexity × change-frequency; start with ~3 fitness functions, "three strikes → encode a rule".

## Memory / Knowledge

## (Agentic-Memory-Knowledge-Mgmt, Agentic-Memory-Final-Proposal — Both Concluded "Don't Build It")

- Files-first memory, human approves every write, provenance and decay as first-class, tiered context loading; vector search only past ~500–1000 items. **Validated 2026-07 and vendor-vindicated: Claude Code's memory and Anthropic's Managed-Agents Memory + "Dreams" consolidation implement exactly this shape (never auto-commit).**

## Skills Design / Meta

## (Reusable-Claude-Skills, Skill-Improvements-Proposal, Sdlc-Tools-Landscape, Practitioner Surveys)

- Two-tier placement: methodology skills global, tooling-coupled skills project-local; project-specific behaviour lives in consuming-repo bindings, never in skill bodies.
- The three load-bearing SDLC ideas from the tool survey: fresh context per task, scoped context injection, multi-model plan diversity. ACI principle: "no output = success".
- Commit conventions: keep plain imperative style; Conventional Commits rejected as YAGNI.

## Research Methodology

## (Agentic-Research-Design, Aris-Deep-Dive, Autonomous-Literature-Research, Karpathy-Autoresearch)

- Pre-retrieval diversity is the lever: orthogonal sub-questions, 3–7 agents, domain-native vocabulary; pre-commit resolution criteria before searching; external signal every review round, hard cap ~3.
- Freeze the problem anchor verbatim; cross-model adversarial review + crash-resilient state enable long unattended runs.
- LLM proposes structural changes; classic optimisers sweep parameters — don't burn LLM budget on enumerable search.

## Supersessions and Resolved Contradictions

- The May 2026 code-review docs supersede the 2026-03-13 one (correctness ≈15% of review value, not 40%; fan-out caution added).
- dialectic-convergence refines dialectic-planning: context isolation is the stronger mechanism; model diversity helps only at comparable model quality.
- ARIS's adversarial review framing loses to agentic-research-design's cooperative "what's missing" framing (later doc wins).
- agentic-memory-final-proposal superseded knowledge-mgmt; both then rejected in favour of built-in auto-memory.
- Still open: subagent-isolated Red phase (see Implementation above); AC-always vs AC-optional-when-deliverable-named.
