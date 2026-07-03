# Code Review: Literature and SOTA — Pre-Agentic Era Through May 2026

Research date: 2026-05-16. Method: 10 parallel research agents (4 pre-agentic, 4 agentic-SOTA, 1 cross-era taxonomy, 1 internal prior-work scan), synthesised, then two review rounds with independent reviewers and fresh external verification. The per-agent working findings and the round-by-round review-disposition log were intermediate scratch and have been deleted; the Review Process section below is the self-contained record.

---

## Problem Anchor (Verbatim)

> "What do the literature (academia), the software craftsmanship/open-source community, and big-tech/strong-engineering-culture companies say about how to do code reviews — covering (a) why review, (b) what to focus on, (c) how/process, (d) when/how often, (e) types of review — first in the pre-agentic-AI era, then how this has changed in the agentic-AI era with the current SOTA as of May 2026 (last ~2 years, big labs, proven agent review skills/marketplaces, thought leaders). Synthesise into actionable guidance suitable for writing a sharp, general-purpose agent-executed 'code-review' SKILL, including an evidence-based recommendation on which review mode(s) such a skill should drive."

### Resolution Criteria (Pre-Committed, Before Results Seen)

A strong answer must: (1) separate *stated rationale* from *empirically measured outcome* for "why review"; (2) give a priority-ordered "what to focus on" taxonomy with provenance, not a flat checklist; (3) distinguish review *types* and *cadences* with fit conditions; (4) treat vendor benchmarks as marketing until independently replicated; (5) deliver a falsifiable review-mode recommendation with trade-offs; (6) grade every load-bearing claim by evidence strength and flag what is single-source or unverifiable. Evidence that would change the conclusion: a credible independent benchmark showing AI review >60% precision *and* recall; a replication showing same-context self-review matches fresh-context; or strong evidence that mandatory PR review *causally* (not correlationally) reduces production defects.

---

## Thesis

**The pre-agentic era and the agentic era reach the same division of labour from opposite directions.** Pre-agentic empirical research found only ~15% of review comments concern defects; review's durable value is design integrity and knowledge transfer. The agentic era now drives the same split structurally: linters + AI absorb the bulk mechanical/defect-pattern volume, and humans concentrate on design, architecture, and judgement. Every structural recommendation in this document falls out of that convergence and out of one corollary it forces: **the reviewer must be separated from the generator.**

## Executive Synthesis — the Load-Bearing Findings

Strength key: **▰▰▰** robust (independent replication / large primary data) · **▰▰** moderate (single strong study or convergent practice) · **▰** weak (vendor-run, anecdotal, or unverified single source).

| #   | Finding                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Strength                   |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| 1   | **Defect detection is not the primary value of review.** ~15% of comments concern defects; the rest is evolvability, design, comprehension, knowledge transfer. Replicated across Microsoft (Bacchelli & Bird 2013; Czerwonka 2015), Google (Sadowski 2018), industrial+student (Mäntylä & Lassenius 2009: 75% of found defects are evolvability-class).                                                                                                                                                      | ▰▰▰                        |
| 2   | **Review quality collapses with size.** 200–400 LOC sweet spot; quality drops sharply >400 LOC and >~500 LOC/h; Google's lived practice (~24 LOC median, 70% reviewed <24h) shows small-batch is achievable. Canonical numbers trace to one observational study (SmartBear/Cisco) — direction robust, magnitude soft.                                                                                                                                                                                         | ▰▰                         |
| 3   | **Style/formatting must be 100% automated, never reviewed.** Universal across Morling's Pyramid, Google eng-practices, Microsoft playbook, every 2025–26 AI tool. The automatable fraction is *inferred* at ~60–80% (Czerwonka: ~50% maintainability + ~15% style), not directly measured.                                                                                                                                                                                                                    | ▰▰▰ (the 60–80% figure: ▰) |
| 4   | **Priority order is settled:** API/contract & design → correctness/logic/security/concurrency → tests → performance/dependencies → docs/naming → style (automate). Fix-cost and blast-radius set the rank.                                                                                                                                                                                                                                                                                                    | ▰▰▰                        |
| 5   | **Severity-tiered, selective gating beats pass/fail.** 3–4 levels; gate policy "no Critical/Major in correctness, security, or data-safety at merge." Conventional Comments / `nit:` is the dominant *convention* (widely adopted; not empirically validated against plain comments).                                                                                                                                                                                                                         | ▰▰▰ (CC efficacy: ▰)       |
| 6   | **Same-context self-review by the generating model is structurally unreliable.** Intrinsic self-correction degrades accuracy (Huang et al., ICLR 2024); adversarial framing reaches 88% success vs an autonomous same-context agent. Fresh/separate context is the minimum viable fix. Independently established by (a) academic self-correction theory, (b) a dedicated controlled experiment (CCR, arXiv:2603.12123), and (c) the deliberate PR-first, separate-context architecture of every major vendor. | ▰▰▰                        |
| 7   | **The agentic SOTA architecture has converged:** PR/diff-first, a fleet of disjoint-scope specialist agents, a verification/judge pass before posting, severity gating, repo-context files, structured per-finding output, phased advisory→gating rollout.                                                                                                                                                                                                                                                    | ▰▰▰                        |
| 8   | **The "do NOT flag" list is the highest-leverage *prompt element*** — convergent practitioner architecture (Cloudflare, Anthropic, multiple skills) plus indirect empirical support: piping uncontrolled positive signal (raw SAST) into the model produced the *worst* F1 (4.87%) on SWR-Bench.                                                                                                                                                                                                              | ▰▰                         |
| 9   | **AI review accuracy is modest in absolute terms.** ~19–22% F1 on the most rigorous independent academic benchmark (SWR-Bench, 1k PRs); ~51% F1 best-in-class on the only credible independent real-PR benchmark (Martian, 200k+ PRs). Vendor self-benchmarks (44–82%) collapse under independent re-evaluation (Greptile 82%→45%). → AI review is a **high-recall first-pass signal requiring human validation**, not a gate replacement.                                                                    | ▰▰                         |
| 10  | **Evidence-backed signal boosters:** multi-run self-aggregation (+44% F1, +119% recall, precision stable), single best-match (top-1) RAG (more retrieval *hurts*), problem/PR-description injection, severity gating, two-pass verify-before-post, reasoning-trained models. **Proven non-helpers:** persona prompting (Mollick et al. 2025), raw SAST piped into the LLM, LLM-generated context files, intrinsic self-correction.                                                                            | ▰▰                         |
| 11  | **AI-generated code shifts the review target:** ~12% more review rounds, lower suggestion-adoption, higher rejection, more convention misses (arXiv:2603.15911, 278k conversations); higher defect density (vendor: ~1.7×). This is the *dominant* use case for an agent-executed skill.                                                                                                                                                                                                                      | ▰▰ (density: ▰)            |
| 12  | **Mandatory PR review is simultaneously over-applied and under-enforced.** ~65% of PRs are comment-free; yet AI volume has strained the pipeline (DORA 2025: throughput up, delivery instability up). Resolution: risk-stratified review + automated-gates-first + AI as a signal-raising first pass + humans on design/judgement.                                                                                                                                                                            | ▰▰                         |

---

## Part 1 — the Pre-Agentic Era

### 1.1 Why Review (Stated Rationale Vs Measured Outcome)

The most replicated, most ignored finding: the *reason teams adopt* review (catch bugs) is not its *primary measurable output*.

- Bacchelli & Bird (ICSE 2013, Microsoft, multi-method, ~570 comments): reviews deliver knowledge transfer, team awareness, alternative solutions more than defect detection. **▰▰▰**
- Czerwonka et al. (ICSE 2015, "Code Reviews Do Not Find Bugs"): ~15% of comments flag a possible defect; ~50% address maintainability. **▰▰▰**
- Mäntylä & Lassenius (IEEE TSE 2009): 75% of defects found are *evolvability*, 25% functional. **▰▰**
- Sadowski et al. (ICSE-SEIP 2018, Google, 9M reviews): goals ranked education → norm-maintenance → gatekeeping → accident prevention → design tracing; 97% satisfaction. **▰▰▰**
- Boehm 1:10:100 cost curve is the economic rationale, but the data is 1970s waterfall; agile multipliers are nearer 1:4. Direction sound, multiplier unreliable. **▰▰**
- Unreviewed commits ~2× likelier to introduce defects (McIntosh 2016; 2024 MCR survey) — but Ebert et al. (2020, Bayesian replication) found the effect *indirect* (mediated by prior-defect history, module age), not clean causation. **Contested.**

Skill implication: frame review value as **design integrity + correctness + knowledge capture**, not "bug hunting"; expect most output to be improvement-class, with correctness defects the highest-severity minority.

### 1.2 What to Focus on — Taxonomy and Priority Order

Converged across Google eng-practices, Morling's Code Review Pyramid (2022), Greiler's checklist, the Augment 40-question checklist, the SWE-at-Google book:

| Priority | Dimension                          | What to check                                                                               | Leave to tooling?                                                  |
| -------- | ---------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 1        | API & contract semantics           | interface completeness, backward compatibility, versioning — hardest to reverse             | No                                                                 |
| 1        | Design & architecture              | fit with codebase, coupling, SRP, no over-engineering                                       | No                                                                 |
| 1        | Correctness & logic                | boundary conditions, null/index safety, time/tz, invalid-state transitions, idempotency     | Partial (type-checkers)                                            |
| 1        | Concurrency                        | races, deadlocks, shared-state synchronisation                                              | No (weak static detection)                                         |
| 1        | Security                           | injection, XSS/CSRF/SSRF, broken access control, crypto misuse, unsafe deser., supply chain | Partial (SAST/dep-scan flag; humans verify business-context authz) |
| 2        | Error handling                     | failure-path consistency, no leaky errors, logging completeness                             | Partial                                                            |
| 2        | Tests                              | happy/edge/failure coverage, test validity, right test type                                 | CI runs; adequacy is human                                         |
| 2        | Implementation semantics           | N+1, unbounded collections, blocking I/O, algorithmic complexity                            | Profilers flag; humans judge trade-offs                            |
| 2–3      | Performance / non-functionals      | resource cleanup, memory bounds, contention — hot paths only                                | Profilers/APM                                                      |
| 2–3      | Dependencies / supply chain        | CVEs, necessity, licence, transitive impact, SBOM diff                                      | Dep-scanners; human owns necessity/licence                         |
| 3        | Documentation                      | comments explain *why*; public API docs current                                             | Linters flag presence; human judges quality                        |
| 3        | Naming / readability / consistency | clear, convention-consistent, understandable without extra context                          | Partial (linters catch casing)                                     |
| 4 / 0    | Style & formatting                 | **fully offload — never a review comment**                                                  | Yes                                                                |

Empirical anchor: Bacchelli & Bird's ~15%-are-defects result *is* the motivation for both the priority order and the offload principle — reviewers historically spend attention where it matters least.

### 1.3 How — Process Mechanics

- **Size discipline is the single biggest quality lever.** SmartBear/Cisco: 200–400 LOC / 60–90 min / <500 LOC/h; >450 LOC/h → below-average defect density in 87% of reviews. Bosu et al. (1.5M comments, **▰▰▰**): useful-comment rate falls as files-per-change rises — a robust, independent corroboration of the size effect. Meta enforces smallness architecturally (stacked diffs); Google culturally (~24 LOC median).
- **Coverage over cognitive ordering (agent-relevant).** The human guidance ("read intent → central files → periphery") is a *cognitive-fatigue* heuristic that does not transfer to an agent. The agent equivalent: cover every changed file in the diff (read it or explicitly justify skipping it); recover intent from the PR description and tests before judging.
- **Standard of approval:** approve when the change *improves overall code health* — don't hold for perfection (Google). Counter-voice: Yelp — never approve what you are not confident in. Reconcilable: approve if no regression; mark residual concerns non-blocking.
- **Author duties:** self-review the diff in the reviewer's view first; one logical thing per PR; separate refactor from behaviour change; *why*-first description; CI green before review; respond to every comment.
- **Reviewer count:** Google routinely 1 (75% of reviews) by design + strong ownership/readability gates; Microsoft/AWS 2+. "2 is optimal" (Sauer et al.) predates MCR, was not independently verified, is folk-cited. Practical convergence: 1–2 substantive reviewers.

### 1.4 When / How Often

- **Latency is an organisational variable, not a property of review.** Google median <4h (max one business day); Microsoft ~24h; Meta P50 hours / P75 ~a day with P75 correlated to dissatisfaction. Slow review degrades quality and throughput.
- **Cadence taxonomy:** per-commit (mechanical/CI), per-PR pre-merge (industry default), post-merge async (senior/high-trust + strong automation), time-boxed sweep (systemic drift), release-gate (regulated), event-triggered (incident/CVE). Conceptually complementary — sweeps can catch architectural drift and accumulated AI-debt that per-PR review misses structurally — **but no published cadence norm or effectiveness data exists as of May 2026** (a real decision the skill author must make without an evidence anchor; see Open Questions).

### 1.5 Types of Review

| Type                         | When                                                         | Strength                                                                                                      | Weakness                                                       |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Formal Fagan inspection      | safety-critical / regulated                                  | highest detection (80–90%, **IBM-era synchronous multi-day; not transferable to MCR**)                        | very expensive, synchronous, doesn't scale                     |
| Over-the-shoulder            | ad-hoc, co-located, onboarding                               | zero setup, strong knowledge transfer                                                                         | author paces; not auditable; poor remote                       |
| Pair programming             | XP teams, complex/novel code                                 | continuous in-the-moment review; ~15% fewer post-release defects *(student-origin study; effect size varies)* | ~15% time overhead; no durable artefact; not async/distributed |
| Tool-assisted async PR (MCR) | default since ~2010                                          | scalable, async, CI-integrated, durable thread                                                                | LGTM rubber-stamping; latency; degrades >400 LOC               |
| CI / pre-commit gate         | every commit                                                 | deterministic, near-zero latency, shift-left                                                                  | misses logic/design; SAST ~76% false positives                 |
| Post-commit / post-merge     | senior, high-trust, TBD-adjacent                             | no blocking latency                                                                                           | needs trust + automation; revert cost                          |
| Security review              | high-risk paths, threat-model changes                        | catches what general review misses (~1% of comments are security)                                             | needs specialist time                                          |
| Architecture / ADR review    | before significant implementation                            | cheapest place to catch design error                                                                          | needs upfront discipline                                       |
| Spec/plan review (emerging)  | before implementation; spec-first workflows (Spec Kit, Kiro) | catches intent errors when cheapest; pairs with agentic codegen                                               | aspirational; requires spec-first discipline most teams lack   |
| Codebase sweep / audit       | release, M&A, post-incident, periodic                        | catches accumulated/systemic debt                                                                             | expensive, infrequent, findings go stale; no cadence norm      |

### 1.6 the Contrarian Case (Steelmanned) and Its Resolution

**Against mandatory pre-merge review:** rubber-stamping is endemic (~65% comment-free; Chromium issued an internal anti-rubber-stamp plea); latency is a compounding throughput tax; review catches mostly *evolvability* defects while logic/race/supply-chain bugs slip through regardless; diminishing returns past the first reviewer; risky files get *less* scrutiny than clean ones (Qt, 11,736 reviews); pairing/TBD+CI may dominate for capable teams; AI volume has strained the human pipeline empirically.

**Rebuttal:** rubber-stamping and latency are execution failures (large PRs, poor routing), fixable structurally. Knowledge transfer and shared ownership are durable benefits no tool replicates. Unreviewed commits remain ~2× as defect-prone. Pairing doesn't generalise to distributed/OSS/high-volume; "Ship" without review means *no human ever saw it*. The correct response to AI volume is to *augment* with AI first-pass + tighten discipline, not abandon review.

**Resolution:** not "always vs never" but **risk-stratified** (the Thesis applied to process): automated gate for everything; human/AI review concentrated on high-risk/high-complexity change with small PRs and fast turnaround; lighter flows for low-risk.

---

## Part 2 — the Agentic Era SOTA (May 2026)

### 2.1 the Accuracy Reality (And the Benchmark-Independence Problem)

Every vendor publishing a benchmark wins it. Decisive demonstration: Greptile scored *itself* 82% on its own 5-repo set; an independent party re-scored the **same repositories at 45%** (DeepSource).

- **SWR-Bench** (academic, 1,000 manually-verified real PRs, Sep 2025): best-in-class F1 **~19–22%**; most approaches precision <10%. **▰▰▰**
- **Martian** (independent, 200k+ real PRs, researcher-led, OSS methodology, Jan–Feb 2026): best-in-class F1 **~51%** (CodeRabbit). Closest to a neutral standard; even so surfaced via a vendor blog. **▰▰**
- Vendor benchmarks (Greptile 82%, Qodo 60%, Augment 59%, Propel 64%) and Factory's base-model run are single-author, OOB-config, OSS-repo, unreplicated. **▰**
- No product reaches **>60% precision and >60% recall simultaneously on independent data** as of May 2026. The precision/recall trade-off is unsolved.

Carried forward: all benchmarks use out-of-the-box config on public repos; tuned performance with REVIEW.md/custom rules on private monorepos is **unmeasured** — plausibly higher, by an unknown margin. Named 2026-era model identifiers in vendor benchmarks (e.g. GPT-5.2, Opus 4.6) are single-source and unverified — do not rely on them as named examples in the skill.

### 2.2 Failure Modes

| Failure mode                                                                                                                                                                                                                                                                                                                       | Evidence                                   | Strength |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | -------- |
| Intrinsic self-correction degrades accuracy (flips correct→wrong more than wrong→correct without external signal)                                                                                                                                                                                                                  | Huang et al., ICLR 2024; widely replicated | ▰▰▰      |
| Confirmation bias under framing — *two distinct results*: (a) iterative LLM-assisted framing attack succeeded **88%** vs Claude Code in autonomous same-context mode; (b) a separate strong "bug-free" framing template collapsed GPT-4o-mini vuln detection by **93.5pp** (97.2%→3.6%); Claude Opus 4.5 most robust (4.9pp, n.s.) | 250 CVE/patch study, Apr 2026              | ▰▰▰      |
| Self-bias — models favour their own generations in self-refinement                                                                                                                                                                                                                                                                 | multiple sycophancy studies 2024–25        | ▰▰       |
| Non-determinism persists at temperature 0 (BF16 non-associativity)                                                                                                                                                                                                                                                                 | arXiv 2502.20747; ACM 2024                 | ▰▰       |
| Context-isolation blindness — file-in-isolation misses cross-service breakage                                                                                                                                                                                                                                                      | 450k-file test (single vendor)             | ▰        |
| False-positive noise — uncontrolled tools emit a "firehose" developers learn to ignore                                                                                                                                                                                                                                             | Cloudflare; Qodo survey                    | ▰▰       |
| Adoption gap — AI suggestions adopted 16.6% vs human 56.5%; >50% of unadopted AI suggestions incorrect (28.7%) or mis-fixed (24%); adopted AI suggestions raise cyclomatic complexity ~10–30× more than human ones                                                                                                                 | arXiv 2603.15911, 278k conversations       | ▰▰▰      |

### 2.3 What Measurably Improves Signal — and What Doesn't

**Improves (evidence-backed):**

- **Multi-run self-aggregation** — n=10 same-model passes, surface findings appearing in ≥2: +43.7% F1, +118.8% recall, precision stable (SWR-Bench). Biggest model-agnostic lever; n=3–5 practical band.
- **Top-1 RAG** — exactly one semantically-similar past diff+review pair lifts human-rated usefulness ~12–15% → ~45–55%; **top-3/top-5 degrade it** (conflicting exemplars).
- **Problem/PR-description injection** — materially improves correctness classification.
- **Severity gating before posting** — trade recall for precision; empirically the right trade for developer trust.
- **Two-pass verify-before-post** — every finding must carry a concrete file:line + plausible causal chain or it is dropped.
- **Reasoning-trained models** — +77% F1 at equal parameter count.
- **Metadata redaction for security review** — strip author commit messages/PR text so framing can't bias the model.

**Does not help / actively hurts (proven):**

- Persona prompting — no accuracy gain across 6 models/2 benchmarks; low-knowledge personas hurt (Mollick et al., Dec 2025). *Use task instructions, not roles.*
- Raw static-analysis output piped into the LLM — worst F1 (4.87%); noise drowns signal. (This is the strongest indirect evidence that the do-not-flag/noise-suppression layer is load-bearing.)
- LLM-generated repo-context files — −3% performance, +20% cost. Human-authored minimal context files help (~+4%).
- Intrinsic self-correction in the same context.
- Naive multi-agent fan-out — CR-Agent (multi-agent) *underperformed* a single sophisticated prompt (PR-Review) on SWR-Bench. Decomposition helps **only** with disjoint hypotheses + a dedup/verify pass; parallel copies of the same prompt do not.

### 2.4 the Converged Architecture

Reference implementations: Anthropic's `code-review` plugin (4 parallel agents, 0–100 confidence, gate at 80, per-issue validation, skip draft/closed), Anthropic's managed Cloud Code Review, and Cloudflare's production system (coordinator + ≤7 domain sub-reviewers, structured XML findings, judge-pass dedupe, risk-tiered models; **131,246 reviews / 48,095 MRs in 30 days, median 3m39s, $1.19/review, 0.6% override** — first-party single-org **▰▰**). Caveats: the **$1.19 figure rests on an 85.7% token-cache hit rate** (a fresh deployment pays several × that until cache warms); the **0.6% override rate measures willingness to invoke break-glass, not the false-positive rate** of the review.

Convergent structural elements (across Anthropic, Cloudflare, Qt, Qodo, strongest community skills) — these are *patterns*, not mandates; the practical default is a single prompt + verify pass (see Implications #9), with the rest adopted as scale/risk warrants:

1. **Diff/PR-first input** with selective context injection (not whole-codebase dumps).
2. **Disjoint-scope specialist agents** + a coordinator (a security agent isn't distracted by naming). *But see §2.3 — start from a single well-structured prompt + verify pass; fan out only for known high-risk domains.*
3. **A verification/judge pass** filtering candidates before posting — the primary false-positive control.
4. **Explicit "do NOT flag" list** — pre-existing issues, linter/type/test-owned items, correct-but-odd code, pedantic nits, framework-handled errors. The highest-leverage prompt element.
5. **Confidence threshold** (~80, inherited not derived) with a below-threshold calibration bucket.
6. **Repo-context files** (CLAUDE.md / REVIEW.md / AGENTS.md), human-authored, minimal; REVIEW.md can redefine severity per repo, cap nit volume, set skip rules, enforce re-review convergence.
7. **Structured per-finding schema:** severity · file:line · issue · why · concrete fix; machine-readable tally for CI gating.
8. **Reviewer ≠ fixer** — read-only; emit a `fix_prompt`, don't apply it (reviewer-as-fixer anchors and drifts scores across passes).
9. **Progressive disclosure** — core SKILL.md tight (<~500 lines); references load on demand.
10. **Phased rollout** — advisory → measure FP on 25–50 PRs → tune → then gate. No day-one hard-block.
11. **Risk-tiered model/scope** — light path for trivial diffs; full review for large or security-sensitive paths regardless of size.

*Provenance caveat (echo discipline):* the Anthropic plugin, Cloud service, and SKILL-authoring guidance share one design team — treat Anthropic-specific details (confidence=80, exact label names) as **single-design-team, not independently validated**. The *patterns* are independently corroborated by Cloudflare's coordinator judge-pass, the nishilbhave anchoring-bias finding, and the SWR-Bench raw-SAST result; the specific constants are not.

Anti-patterns: monolithic single-pass; no negative-constraint list; flagging pre-existing/linter-covered issues; reviewer-as-fixer; over-long SKILL/REVIEW files; running on draft/closed PRs; re-reviewing style each push; menu of approaches instead of one default + escape hatch.

### 2.5 Reviewing AI-Generated Code — the Dominant Use Case

For an agent-executed skill in 2026 the code under review is itself usually agent-authored. The largest independent study (arXiv:2603.15911 — **web-verified**: 278,790 conversations, 300 OSS projects, **▰▰▰**) establishes concrete, actionable differences vs human-written code:

- Human reviewers exchange **11.8% more rounds** reviewing AI-generated code.
- AI-suggestion adoption is **16.6% vs 56.5%** for human suggestions; **>50% of unadopted AI suggestions are incorrect or replaced by a different fix**.
- Adopted AI suggestions inflate code size and cyclomatic complexity **far more** (~10–30×) than human ones.
- AI review comments are **>7× longer per line** and **>95% focused on code-improvement/defect-detection**, while humans add understanding, testing, and knowledge-transfer.
- Vendor data (CodeRabbit, **▰**): AI-generated code ~1.7× defect density (directional only).

Actionable consequences (promoted into the Implications list): when the diff is agent-authored, (a) intensify correctness/security scrutiny; (b) explicitly check **convention-conformance and abstraction-duplication** (re-inventing existing utilities is a characteristic AI failure); (c) bias toward **smaller review units**; (d) keep comments terse — the model's own verbosity is a measured anti-pattern; (e) treat AI suggestions as candidates, not authority (low adoption, high incorrectness).

### 2.6 SOTA Workflow Integration and the Human/agent Division of Labour

Converged: separate generator from reviewer; severity tiers with selective merge-blocking; specialist agents > generalists *with the §2.3 caveat*; humans move upstream (specs, REVIEW.md/AGENTS.md, architecture, final merge authority) and stop line-by-line; context files are mandatory infrastructure; PR cadence not per-commit for the heavy LLM pass; non-blocking-first rollout.

Contested / thin evidence: how hard to gate (Cloudflare blocks on critical; Anthropic Cloud stays neutral); multi-round convergence loops (Zylos: 3–11 rounds → 3–5× more bugs, n=3 **▰**); pre-commit agent review at team scale (no enterprise case study); spec-driven review as primary gate (aspirational); codebase-sweep cadence (no published norm); whether the reviewer should know code is AI-generated.

---

## The Review-Mode Decision (Answer to the Deferred Question)

Deliberately left to the research; the evidence is decisive.

**Default mode: PR / branch / diff review in a fresh, separate agent context, triggered on PR-open or explicit request.**

Rationale, by evidential weight:

1. **Intrinsic self-correction degrades accuracy** (Huang et al., ICLR 2024, ▰▰▰): the same model in the same context shares the exact probability mass that produced the error.
2. **Framing/confirmation bias** against same-context agents (Apr 2026 CVE study, ▰▰▰): an iterative LLM-assisted framing attack succeeded 88% against Claude Code in autonomous mode, and 100% (17/17 CVEs) for the template-attack variant.
3. **Industry convergence is unanimous and deliberate** — Anthropic, Google, GitHub, CodeRabbit, Greptile are all PR-first, separate-context, multi-agent.
4. **A dedicated controlled experiment** (CCR, arXiv:2603.12123 — web-verified independent paper, **not** a TAD artefact): fresh-session review F1 **28.6%** vs same-session **24.6%** (p=0.008), and repeated same-session did *not* beat single-pass (p=0.11, ruling out repetition). Single controlled study, n=30 mixed artefacts (code/docs/scripts), no replication → **▰▰**, corroborating not decisive.
5. **Fresh context unlocks multi-run aggregation** (+44% F1), only practical as a separate lightweight invocation.

**Secondary, opt-in: a lightweight pre-commit gate that runs deterministic tools (lint, types, tests, complexity) — explicitly NOT same-context LLM semantic self-review.** If a pre-commit LLM pass is wanted it must use a *fresh invocation* and stay scoped to convention/pattern conformance against CLAUDE.md, never open-ended correctness judgement of just-written code.

**In-session invocation (the common reality):** a general-purpose skill will often be invoked right after implementation, before a PR exists. The skill must not silently perform same-context semantic self-review. It should detect the absence of a diff target (no base branch/PR ref supplied) and then: warn that same-context self-review is structurally limited; run a *downgraded scope* — convention and CLAUDE.md/project-rule conformance plus the do-NOT-flag filter, advisory-only, no open correctness/security judgement, no severity gate required; and recommend creating a branch/PR and re-invoking as fresh-context diff review for the full semantic pass.

**Configurable, not both-mandatory.** Two mandatory LLM stages double latency/cost for sub-linear gain. PR/diff + fresh-context is the default and the only mandatory LLM pass.

| Dimension             | PR/branch (fresh ctx)                                                    | Same-context self-review                 |
| --------------------- | ------------------------------------------------------------------------ | ---------------------------------------- |
| Self-bias             | low                                                                      | high                                     |
| Framing vulnerability | low                                                                      | high                                     |
| Recall                | boosted by multi-run aggregation                                         | cannot improve without external signal   |
| Latency               | async when CI-triggered, sync when user-invoked; never blocks the commit | blocks commit                            |
| Human-visible         | yes (PR)                                                                 | no                                       |
| Operational maturity  | industry-proven                                                          | no production-scale precedent            |
| Right job             | semantic correctness, security, logic, design                            | deterministic structural/style gate only |

---

## Cross-Era Synthesis

### Independent Agreement Vs Echo

| Cluster                                                                  | Verdict                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Review's durable value is design + knowledge transfer, not bug-finding" | **Independent** — Microsoft CodeFlow data, Google 9M-review study, industrial+student defect taxonomy: three corpora, no shared upstream → high confidence                                                                               |
| "Separate reviewer from generator"                                       | **Independent** — ICLR self-correction theory, the CCR controlled experiment, vendor production architecture: three streams → high confidence                                                                                            |
| Priority order + style-offload                                           | **Convergent practice** — Google policy, Morling model, every AI tool                                                                                                                                                                    |
| "200–400 LOC / <500 LOC/h"                                               | **Echo** — nearly all trace to the single SmartBear/Cisco observational study; direction robust, exact figure one lineage. (Independent corroboration of the *direction* only: Bosu et al. 1.5M comments)                                |
| "~15% of comments are defects"                                           | **Echo** — Bacchelli & Bird / Czerwonka, re-cited everywhere; direction robust, exact % one lineage                                                                                                                                      |
| "AI code ~1.7× defect-dense"                                             | **Echo, single vendor** (CodeRabbit) — directional only                                                                                                                                                                                  |
| Verify-before-post · do-not-flag · REVIEW.md customisation               | **Echo within Anthropic** (plugin / Cloud / SKILL guidance share a design team). Independent corroboration of the *patterns*: Cloudflare judge-pass + nishilbhave anchoring + SWR-Bench SAST. Treat Anthropic-specific constants as weak |

### Disagreements and Why They Diverge

| Question                                       | Camp A                                  | Camp B                                           | Assessment                                                                                                                                                 |
| ---------------------------------------------- | --------------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reviewers per change                           | Google: 1 (by design + ownership gates) | Microsoft/AWS: 2+                                | Context-dependent; "2 optimal" is unverified folklore                                                                                                      |
| Does review causally cut post-release defects? | McIntosh 2016: associated               | Ebert 2020: indirect only                        | Causality unproven; both credible                                                                                                                          |
| Mandatory PR gate vs pairing/TBD/Ship-Show-Ask | Google/GitLab/Palantir/Yelp             | Fowler/Beck/trunk-based                          | Industry converged on PRs; elite XP teams legitimately differ; unsettled                                                                                   |
| Does codebase-RAG materially lift recall?      | a6/Greptile: 82% vs 44% diff-only       | a5: that 82% → 45% independently                 | RAG plausibly helps cross-cutting recall; magnitude vendor-inflated/unproven. Stance: diff-first for precision, targeted retrieval for cross-file concerns |
| Specialist multi-agent vs single strong prompt | Cloudflare/Anthropic/Qt: fleet wins     | SWR-Bench: multi-agent < single PR-Review prompt | Decomposition wins **only** with disjoint scope + verify pass; don't over-commit to fan-out                                                                |
| Gate vs advise                                 | Cloudflare blocks on critical           | Anthropic Cloud stays neutral                    | Depends on FP tolerance, trust, legal risk                                                                                                                 |

### Emergent Patterns

1. **The 15% is the design spec.** The historically-deplored "only ~15% of comments are defects" is, in the agentic era, the brief: automate/AI-absorb the bulk; reserve humans for the judgement-bound residue. The old weakness defines the new division of labour.
2. **Size limits survive for a new reason.** A human cognitive-fatigue ceiling persists because interaction-effect density and long-context degradation rise with diff size — same rule, different mechanism.
3. **"The author would fix it if they knew"** (the Codex reviewer system prompt's filter, surfaced from `2026-05-12-codex-review-internals.md`) operationalises Bacchelli & Bird's "useful comment". Intuitively right, **not independently studied** — a hypothesis, not a proven technique.
4. **Convergence loops cut both ways.** Multi-round review finds 3–5× more bugs *or* entrenches a wrong answer (~83% confidence by round 3 in free-form debate). Safe form: *new external signal each round*; pure re-reflection is net-negative — exactly TAD's existing `review-loop` doctrine, independently corroborated (CCR's SR2 result; arXiv:2603.16244 "More Rounds, More Noise").

### Claim-Strength Ledger (Load-Bearing Numbers)

| Claim                                                     | Source lineage                                                                                                             | Strength              |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| ~15% of comments are defects                              | Bacchelli&Bird 2013 / Czerwonka 2015 (primary)                                                                             | ▰▰▰                   |
| 200–400 LOC / <500 LOC/h                                  | SmartBear/Cisco single observational study                                                                                 | ▰▰                    |
| Intrinsic self-correction degrades accuracy               | Huang et al. ICLR 2024 + replications                                                                                      | ▰▰▰                   |
| Framing attack 88% vs same-context agent                  | Apr 2026 CVE study (250 pairs)                                                                                             | ▰▰▰                   |
| Multi-run aggregation +44% F1                             | SWR-Bench (controlled)                                                                                                     | ▰▰▰                   |
| Best independent real-PR F1 ~51%                          | Martian, 200k+ PRs                                                                                                         | ▰▰                    |
| Best academic F1 ~19–22%                                  | SWR-Bench, 1k PRs                                                                                                          | ▰▰▰                   |
| Reviewing AI code: +11.8% rounds, 16.6% vs 56.5% adoption | arXiv:2603.15911, 278k conv. (web-verified)                                                                                | ▰▰▰                   |
| CCR fresh 28.6% vs same-session 24.6% F1                  | arXiv:2603.12123 (web-verified, single controlled study, n=30 mixed)                                                       | ▰▰                    |
| Cloudflare 131k reviews / $1.19 / 0.6% override           | Cloudflare blog (first-party, single-org; cost cache-dependent)                                                            | ▰▰                    |
| AI code 1.7× defect density                               | CodeRabbit vendor analysis                                                                                                 | ▰                     |
| DORA 2025: throughput↑, instability↑                      | DORA 2025 primary (web-verified). Precise +51%/+441%/+242% deltas are from a secondary (Faros.ai) summary, not the primary | ▰▰ primary / ▰ deltas |

---

## Pre-Mortem — Assume the Main Conclusions Are Wrong

- **If "fresh-context PR review" is wrong:** would require intrinsic self-correction to work for code (contra ICLR 2024) or same-context to match fresh-context. CCR magnitude is single-study, small-n, mixed-artefact; may not replicate — but the *direction* is independently supported by anchoring, sycophancy, framing, and CCR's repetition control. **Depend on the direction, not the number.**
- **If "AI review is low-accuracy first-pass" is wrong:** benchmarks use OOB config on OSS repos; tuned REVIEW.md performance on real monorepos is unmeasured and plausibly higher. The qualitative conclusions (require human validation, suppress noise, gate on severity) hold regardless.
- **If "specialist multi-agent beats single prompt" is wrong:** SWR-Bench already shows the counter-case (multi-agent < single sophisticated prompt). The Implications list is calibrated accordingly — **start with one well-structured prompt + verify pass; fan out to specialists only for known high-risk domains (security, concurrency)**. Heavy fan-out is an option, not dogma.
- **Fragile assumption:** several May-2026 SOTA data points (Cloudflare/HubSpot operational figures, some 2026 arXiv IDs, vendor model names) are single-source and sub-agent-reported. CCR and 2603.15911 were web-verified this round; the rest are not. The skill must not hard-depend on any single such number.

---

## Implications for a General-Purpose Code-Review SKILL

Ordered by leverage — this is the brief for the skill author.

1. **Default to PR/diff review in a fresh context.** Detect invocation context by checking for a diff target (base branch / PR ref / explicit range); absent one, the skill is in-session. In-session: warn that same-context self-review is structurally limited, run the *downgraded scope* (convention + CLAUDE.md/project-rule conformance + the do-NOT-flag filter; advisory-only; no open correctness/security judgement; severity tiers optional), and recommend branch→PR→re-invoke for the full semantic pass. Pre-commit = deterministic tools only; never same-context LLM correctness.
2. **The "do NOT flag" list is the spine.** Pre-existing issues; anything a linter/type-checker/test owns; correct-but-unusual code; pedantic nits; speculative/no-file:line concerns; style. Governs signal more than the positive checklist.
3. **Priority-ordered focus, not a flat checklist:** correctness/logic & API/design & security/concurrency first; tests; then perf/deps; docs/naming low; style never.
4. **Severity tiers + selective gate:** Critical/Major (correctness, security, data-safety) block; Minor advisory; nit/info collapsible. Severity-labelled comments (Conventional-Comments-style is a widely-adopted convention, not empirically validated — use it for clarity, don't oversell it).
5. **Verify-before-post:** every finding needs file:line + a concrete failure mechanism, or drop it. Confidence threshold (~80) with a below-threshold calibration bucket.
6. **Scope + context discipline:** review the diff; cover (read or justify skipping) every changed file; pull **exactly one** semantically-similar past diff+review pair (top-1 — top-k degrades); expand surrounding code only at interface boundaries for cross-file concerns; never load the whole codebase; never auto-generate codebase summaries to feed itself.
7. **Reviewer ≠ fixer:** read-only; emit a copy-pasteable fix instruction, don't apply it.
8. **Structured output:** severity · file:line · issue · why · fix; machine-readable tally for CI.
9. **Architecture default:** one well-structured prompt + a verification pass. Fan out to disjoint-scope specialist agents only for known high-risk domains (security, concurrency) — naive parallelism loses (SWR-Bench).
10. **Power-ups, off by default:** multi-run aggregation (n=3–5, surface ≥2-pass findings) for recall; reasoning model; metadata redaction for security passes; new external signal each iteration if looping; cross-model only when models are comparably capable (else Self-MoA).
11. **No persona prompting.** Task instructions only (Mollick et al.).
12. **Treat AI-generated diffs as the default and review them harder:** intensify correctness/security; explicitly check convention-conformance and abstraction-duplication; prefer smaller units; keep comments terse; treat AI suggestions as candidates not authority (16.6% adoption, >50% of unadopted are wrong).
13. **Cost is a first-class constraint.** Default to one pass + verify on a tiered model (light for trivial diffs, strong for large/security paths); make multi-run/multi-agent opt-in. State the expected cost envelope; don't make the expensive path mandatory.
14. **Keep it tight.** Nervousness heuristic: every line must prevent a specific failure the agent would otherwise hit; over-specified skills measurably degrade performance.

### TAD-Specific Appendix (General Core Stays Portable)

TAD's review must never duplicate `just check-all` (ruff, pyright, architecture tests, pytest, openapi-drift, frontend-check/e2e). Top domain concern is **silent corruption** (guarded division → `None` not `NaN`; `pl.when(x>0)` / `numerator/denom if denom>0 else None`). Workflow position: `impl-task → code-review → review-task → ship-task` (review assumes correctness plausible; verifies quality, not ACs). Findings route to GitHub issues (`review`/`kaizen` labels), not the backlog. File-by-file coverage discipline is a hard-won rule (commit `e4f88a3`). Two-tier CI already exists: per-commit `claude-code-review.yml` + weekly `claude-kaizen.yml`; `cross-pollinate-code-review` is the local multi-model variant. The general skill should stay portable; a short appendix carries these.

---

## Open Questions and What Was Not Found

1. CCR (arXiv:2603.12123): exists and is independent (web-verified) but is a single controlled study of n=30 mixed artefacts (code/docs/scripts; n per the paper via web verification, not re-derived from this corpus) with no replication, not code-review-on-real-PRs specifically. Direction safe; magnitude hypothesis-grade.
2. Optimal confidence threshold (0.8 inherited from the Anthropic plugin, not derived); P0–P3 vs HIGH/MED/LOW for filtering — untested.
3. Self-MoA vs multi-model when both models are frontier-tier (bears on whether Claude+Codex cross-review still pays) — unresolved.
4. Real-world tuned AI-review precision/recall with REVIEW.md on private monorepos — entirely unmeasured.
5. Minimum effective `n` for multi-run aggregation (3 vs 10) — unknown, cost-sensitive.
6. Sweep/periodic-review cadence — **no published norm or effectiveness data**; the skill author must choose without an evidence anchor.
7. No fully independent non-vendor benchmark comparing ≥3 tools on the same real bugs beyond Martian; some 2026 arXiv IDs, vendor operational numbers, and 2026-era model names are single-source and not cross-verified here (CCR and 2603.15911 were verified this round).
8. No empirical study isolating same- vs separate-session self-review with accuracy as the dependent variable *on real code review* (CCR is the closest; mixed artefacts).

---

## References

Pre-agentic — academic:

- Fagan, M. (1976). Design and Code Inspections. IBM Systems Journal 15(3). <https://dl.acm.org/doi/10.1147/sj.153.0182>
- Bacchelli & Bird (2013). Expectations, Outcomes, and Challenges of Modern Code Review. ICSE. <https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/>
- Rigby & Bird (2013). Convergent Contemporary Software Peer Review Practices. ESEC/FSE. <https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/rigby2013convergent.pdf>
- Czerwonka, Greiler & Tilford (2015). Code Reviews Do Not Find Bugs. ICSE. <https://www.microsoft.com/en-us/research/publication/code-reviews-do-not-find-bugs-how-the-current-code-review-best-practice-slows-us-down/>
- Mäntylä & Lassenius (2009). What Types of Defects Are Really Discovered in Code Reviews? IEEE TSE 35(3). <https://www.semanticscholar.org/paper/65e184940d7bd3538c9e59d11da1782d573bae02>
- Bosu, Greiler & Bird (2015). Characteristics of Useful Code Reviews. MSR. <https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/>
- Sadowski et al. (2018). Modern Code Review: A Case Study at Google. ICSE-SEIP. <https://research.google/pubs/pub47025/>
- McIntosh et al. (2016). Impact of MCR Practices on Software Quality. EMSE 21. <https://link.springer.com/article/10.1007/s10664-015-9381-9>
- Ebert et al. (2020). Do Code Review Measures Explain Post-Release Defects? EMSE 25(5). <https://arxiv.org/abs/2005.09217>
- Paul & Turzo (2021). Why Security Defects Go Unnoticed during Code Reviews. <https://ar5iv.labs.arxiv.org/html/2102.06909>
- Votta (1993). Does Every Inspection Need a Meeting? ACM SIGSOFT. <https://dl.acm.org/doi/10.1145/167049.167070>
- A Roadmap for Modern Code Review (survey, 327 papers). 2024. <https://arxiv.org/html/2405.18216v2>

Pre-agentic — big tech & community:

- Google eng-practices. <https://google.github.io/eng-practices/>
- Software Engineering at Google, ch.3/9/19. <https://abseil.io/resources/swe-book/html/ch09.html>
- Microsoft Engineering Playbook — Code Reviews. <https://microsoft.github.io/code-with-engineering-playbook/code-reviews/>
- CodeFlow (CACM 2019). <https://cacm.acm.org/magazines/2019/2/234350-codeflow/fulltext>
- Meta — Improving code review time. 2022. <https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/>
- Meta stacked diffs. <https://newsletter.pragmaticengineer.com/p/stacked-diffs-and-tooling-at-meta>
- AWS Well-Architected SEC11-BP04. <https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_appsec_manual_code_reviews.html>
- LinkedIn — Scaling Collective Code Ownership. 2018. <https://www.linkedin.com/blog/engineering/developer-experience-productivity/scaling-collective-code-ownership-with-code-reviews>
- Conventional Comments. <https://conventionalcomments.org/>
- Morling — Code Review Pyramid. 2022. <https://www.morling.dev/blog/the-code-review-pyramid/>
- Lynch — How to Do Code Reviews Like a Human. 2017. <https://mtlynch.io/human-code-reviews-1/>
- Wilsenach — Ship/Show/Ask. 2021. <https://martinfowler.com/articles/ship-show-ask.html>
- Fowler — Pull Request. 2022. <https://martinfowler.com/bliki/PullRequest.html>
- Beck — Thinking About Code Review. 2023. <https://tidyfirst.substack.com/p/thinking-about-code-review>
- thoughtbot guides — Code Review. <https://github.com/thoughtbot/guides/blob/main/code-review/README.md>
- Atwood — Ten Commandments of Egoless Programming (Weinberg 1971). <https://blog.codinghorror.com/the-ten-commandments-of-egoless-programming/>
- SmartBear/Cisco — Best Kept Secrets of Peer Code Review. 2011. <https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/>
- Greiler — 30 Best Practices; Checklist. <https://www.michaelagreiler.com/code-review-best-practices/>
- Orosz — Good vs Better Code Reviews. 2018. <https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/>
- OWASP Secure Code Review Cheat Sheet. <https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html>
- DORA 2025 — State of AI-Assisted Software Development. <https://dora.dev/research/2025/dora-report/> · <https://cloud.google.com/resources/content/2025-dora-ai-assisted-software-development-report>

Agentic era — labs, products, studies, skills:

- Anthropic — code-review plugin. <https://github.com/anthropics/claude-code/blob/main/plugins/code-review/commands/code-review.md>
- Anthropic — Cloud Code Review docs. <https://code.claude.com/docs/en/code-review>
- Anthropic — Skill authoring best practices. <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>
- Anthropic — Automate security reviews with Claude Code. 2025. <https://claude.com/blog/automate-security-reviews-with-claude-code>
- Cloudflare — AI Code Review at scale. 2026. <https://blog.cloudflare.com/ai-code-review/>
- GitHub — Copilot code review GA. 2025. <https://github.blog/changelog/2025-04-04-copilot-code-review-now-generally-available/>
- OpenAI Codex — GitHub code reviews. <https://developers.openai.com/codex/use-cases/github-code-reviews>
- Google — Gemini Code Assist review. <https://developers.google.com/gemini-code-assist/docs/review-repo-code>
- Google Research — Resolving Code Review Comments with ML. ICSE-SEIP 2024. <https://research.google/pubs/resolving-code-review-comments-with-machine-learning/>
- Cursor — Building Bugbot. <https://cursor.com/blog/building-bugbot>
- CodeRabbit — Martian benchmark write-up. 2026. <https://www.coderabbit.ai/blog/coderabbit-tops-martian-code-review-benchmark>
- Martian — code-review-benchmark. <https://github.com/withmartian/code-review-benchmark>
- Greptile — Benchmarks. 2025. <https://www.greptile.com/benchmarks>
- DeepSource — AI code review benchmarks (independence critique). <https://deepsource.com/blog/ai-code-review-benchmarks>
- Qodo — Real-world benchmark for AI code review. 2026. <https://www.qodo.ai/blog/how-we-built-a-real-world-benchmark-for-ai-code-review/>
- Factory.ai — Code review benchmark (13 base models). 2026. <https://factory.ai/news/code-review-benchmark>
- SWR-Bench — automated code review eval (1k PRs). 2025. <https://arxiv.org/html/2509.01494v1>
- Huang et al. — LLMs Cannot Self-Correct Reasoning Yet. ICLR 2024. <https://proceedings.iclr.cc/paper_files/paper/2024/file/8b4add8b0aa8749d80a34ca5d941c355-Paper-Conference.pdf>
- CCR — Cross-Context Review: Improving LLM Output Quality by Separating Production and Review Sessions. arXiv:2603.12123, Mar 2026. <https://arxiv.org/abs/2603.12123>
- More Rounds, More Noise: Why Multi-Turn Review Fails to Improve Cross-Context Verification. arXiv:2603.16244, 2026. <https://arxiv.org/abs/2603.16244>
- Mollick et al. — Persona prompting and accuracy. 2025. <https://arxiv.org/abs/2512.05858>
- Confirmation bias in LLM-assisted security review (250 CVE pairs). 2026. <https://arxiv.org/html/2603.18740v2>
- Human–AI Synergy in Agentic Code Review (278k conversations). arXiv:2603.15911, 2026. <https://arxiv.org/abs/2603.15911>
- Evaluating LLMs for Code Review. 2025. <https://arxiv.org/html/2505.20206v1>
- When More Retrieval Hurts (top-1 vs top-k RAG for review). 2025. <https://arxiv.org/abs/2511.05302>
- LLM non-determinism at temperature 0. 2025. <https://arxiv.org/abs/2502.20747>
- baz-scm/awesome-reviewers (470+ prompts from 1,000+ repos). <https://github.com/baz-scm/awesome-reviewers>
- awesome-skills/code-review-skill. <https://github.com/awesome-skills/code-review-skill>
- Community-skill catalogue (16 artefacts: Anthropic plugin/Cloud, Cloudflare, baz-scm/awesome-reviewers, awesome-skills/code-review-skill, et al.) — sourced during research; working file not retained

Internal prior work (this repo):

- docs/research/2026-03-13-code-review-for-agentic-workflows.md
- docs/research/2026-05-12-codex-review-internals.md
- docs/research/2026-03-20-dialectic-convergence-skill-research.md
- .claude/skills/{cross-pollinate-code-review,review-loop,review-task,kaizen}/SKILL.md
- .github/workflows/{claude-code-review,claude-kaizen}.yml

Per-claim evidence, strength ratings, and "searched but not found" notes were captured in the intermediate per-agent findings files (10 agents), now deleted; the load-bearing claims, sources, and strength grades are carried in the synthesis above.

---

## Review Process

Two review rounds, two independent reviewers each, fresh external signal per round (round 1: web-verified CCR / arXiv:2603.15911 / DORA 2025 primary; round 2: two fresh reviewers vs the revised doc + disposition log). Round 1: 26 findings, all accepted (one corrected by fresh evidence — CCR is a genuine independent paper, not a TAD self-citation). Round 2: 8 findings, 7 accepted (two-sentence actionability/precision fixes), 1 rejected (protocol-mandated References section). rev3-rigor independently declared convergence; **converged at round 2**. (The detailed round-by-round disposition log was intermediate scratch and has been deleted; this summary is the retained record.)
