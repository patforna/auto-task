# Dialectic Cross-Pollination and Convergence Loops for Agentic Skills

**Status:** done — findings adopted into /cross-pollinate, /review-loop, and /research skills

Research synthesis on multi-model dialectic patterns and iterative convergence mechanisms, to inform the design of reusable agentic skills.

Date: 2026-03-20

---

## Research Question

How should we design agentic skills for (1) multi-model cross-pollination (dialectic) and (2) iterative review-until-convergence loops? Should these be one skill or two? What are the load-bearing design decisions, and what should be left to the model?

---

## 1. The Case for Cross-Model Review

### 1.1 Context Separation Is the Primary Mechanism

The strongest recent evidence comes from **Cross-Context Review (CCR)** (Song et al., March 2026), which tested four review conditions across 150 injected errors:

| Condition                            | F1 Score |
| :----------------------------------- | :------- |
| Cross-context review (fresh session) | 28.6%    |
| Same-session self-review             | 24.6%    |
| Repeated same-session review         | 21.7%    |
| Context-aware subagent review        | 23.8%    |

The key finding: repeated same-session review (21.7%) degrades F1 compared to single same-session review (24.6%). Cross-context review in a fresh session (28.6%) substantially outperforms both. The benefit comes from context separation -- production context creates anchoring bias and confirmation loops. For code artifacts specifically: +4.7 F1 points over same-session baseline.

Source: [arXiv:2603.12123](https://arxiv.org/abs/2603.12123)

### 1.2 Model Diversity Helps — with Caveats

**A-HMAD** (Nov 2025) achieves 4-6% absolute accuracy gains and 30%+ factual error reduction using heterogeneous model combinations.

Source: [Springer](https://link.springer.com/article/10.1007/s44443-025-00353-3)

However, **Rethinking Mixture-of-Agents** (Li et al., Feb 2025) delivers the critical caveat: Self-MoA (sampling the single best model multiple times) outperforms multi-model MoA by 6.6% on AlpacaEval. Quality effects are **1.4-3.2x stronger** than diversity effects (regression coefficients from Table 4: 1.39x MMLU, 1.66x MATH, 3.20x CRUX). Multi-model mixing only helps when models are of *comparable quality* with *different specializations*.

Source: [arXiv:2502.00674](https://arxiv.org/abs/2502.00674)

**Synthesis:** Don't mix weak models with strong ones. The gain from cross-model review comes from (1) context separation (always valuable) and (2) uncorrelated failure modes (valuable when models are comparably capable). Using a frontier model + a weak model is worse than two calls to the frontier model.

### 1.3 the Biggest Gain Is 1→2 Models

Multiple sources point to the 1→2 gain being the largest, though for different reasons:

- ARIS (anecdotal, not a controlled study): "the biggest gain is going from 1 model to 2, not from 2 to N"
- Block AI ablation (controlled): without adversarial coach feedback, 4 rounds of solo iteration produced non-functional code — the gain here is from **role differentiation** (coach vs player), not model diversity per se
- Aider architect-editor: two-role pattern sets SOTA at 14x less cost — again, **role separation** (architect reasons, editor implements) rather than model diversity
- Zylos Research (informal benchmarks): multi-model review catches 3-5x more bugs than single-pass

**Important distinction**: the 1→2 gain comes from two separable mechanisms: (a) context separation and role differentiation (fresh eyes + explicit adversarial mandate), and (b) model diversity (different training data → uncorrelated failure modes). Both contribute, but the evidence for (a) is stronger than for (b). Even two calls to the same model in fresh contexts outperforms one call (CCR paper).

Source: [ARIS GitHub](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep), [Block AI](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf), [Aider](https://aider.chat/2024/09/26/architect.html)

### 1.4 When Cross-Model Review Adds Value

| Scenario                                  | Cross-model benefit | Reasoning                                                                 |
| :---------------------------------------- | :------------------ | :------------------------------------------------------------------------ |
| Code review for bugs                      | **High**            | Uncorrelated failure modes across architectures                           |
| Planning and design                       | **High**            | Different blind spots for coverage and approach                           |
| Security-sensitive changes                | **High**            | Different attack surface awareness                                        |
| Straightforward reasoning / single answer | **Low**             | Self-consistency (same model, multiple samples) is cheaper and comparable |
| Frontier model on standard tasks          | **Low**             | Self-MoA dominates                                                        |

Source: [Zylos Research](https://zylos.ai/research/2026-02-17-multi-model-ai-code-review)

---

## 2. Structured Roles Beat Free-Form Debate

### 2.1 MAD Doesn't Reliably Outperform Simpler Methods

"Should we be going MAD?" (Smit et al., ICML 2024): multi-agent debate does not reliably outperform self-consistency or CoT ensembling in default configurations. ICLR 2025 Blogpost evaluation reinforced this across five MAD frameworks and nine benchmarks.

Sources: [ICML proceedings](https://proceedings.mlr.press/v235/smit24a.html), [ICLR 2025](https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/)

### 2.2 LLMs Entrench Rather Than Converge Through Debate

"When Two LLMs Debate, Both Think They'll Win" (May 2025): 60 three-round debates among ten frontier models. Average initial confidence 72.9% (should be 50%), escalating to 83% by final round. In 61.7% of debates, both sides simultaneously claimed >75% win probability.

Source: [arXiv:2505.19184](https://arxiv.org/abs/2505.19184)

### 2.3 What Works Instead: Structured Role Differentiation

| Pattern              | Description                                    | Evidence                                               |
| :------------------- | :--------------------------------------------- | :----------------------------------------------------- |
| Generator + Reviewer | One creates, one critiques in fresh context    | CCR paper: context separation is the key mechanism     |
| Architect + Editor   | One reasons about the solution, one implements | Aider: SOTA results, 14x cost reduction                |
| Coach + Player       | Iterative adversarial refinement               | Block AI: ablation proves coach is essential           |
| Proposer + Auditor   | Explicit adversarial mandate                   | PeerGuard: explicit mandate produces stronger critique |

### 2.4 the Sycophancy Problem

Agents default to agreement. "Peacemaker or Troublemaker" (2025) found sycophancy is a core failure mode that collapses debates into premature consensus. Mixing peacemaker and troublemaker roles -- maintaining adversarial tension -- produces optimal outcomes in decentralized settings.

Source: [arXiv:2509.23055](https://arxiv.org/abs/2509.23055)

**Mitigation patterns:**

- Explicit adversarial mandate: "Your job is to find the fatal flaw" (PeerGuard)
- Anti-sycophancy instruction: "Be BRUTALLY honest" and "Do NOT hide weaknesses to game a positive score" (ARIS)
- Low agreement intensity for critic roles (Smit et al.)
- Pre-mortem reframe: "Assume this failed -- explain why" triggers causal reasoning, not agreement-seeking
- Evidence-based pushback protocol: reviewee pushes back only with local evidence, not position-based ("I disagree")

---

## 3. Convergence Mechanisms

### 3.1 Self-Correction Without External Signal Degrades Quality

This is the single strongest finding across the literature:

- Huang et al. (ICLR 2024): "after self-correction, the accuracies of all models drop across all benchmarks." The model changes correct answers to incorrect ones more often than it fixes errors.
- Kamoi et al. (TACL 2024): "No prior work demonstrates successful self-correction with feedback from prompted LLMs" for general tasks.
- Multi-agent debate improvement is better explained by self-consistency (majority voting) than genuine self-correction (Huang et al.).

Sources: [arXiv:2310.01798](https://arxiv.org/abs/2310.01798), [TACL](https://arxiv.org/abs/2406.01297)

**Implication:** Every iteration in a convergence loop must introduce **external signal** -- a different model's perspective, tool execution results, new retrieved evidence, or structured verification. Pure self-reflection is net negative.

### 3.2 How Many Rounds Add Value?

The evidence converges on **2-3 rounds** for substantive improvement:

| Source                              | Finding                                                                               |
| :---------------------------------- | :------------------------------------------------------------------------------------ |
| Multi-Agent Annotation (2512.00047) | Steepest improvement R0→R1; plateau after round 4                                     |
| Multi-Agent Reflexion               | Caps at 2: "nearly all meaningful disagreements arise within the first two exchanges" |
| Huang et al.                        | Debate degrades from round 1 (83.2%) to round 2 (83.0%) on GSM8K                      |
| ARIS                                | 4 rounds achieves 5/10→7.5/10                                                         |
| Zylos Research                      | 60-70% of bugs found in first half of review rounds; exponential decay                |
| Hegelian Dialectic (2501.14917)     | Most innovation in early iterations; diminishing returns quickly                      |

**Distinction:** Pure re-evaluation converges by round 2. Implementation loops where each round produces new experimental data (fix the code → rerun tests → re-review) justify 4-5 rounds because each round introduces fresh external signal.

### 3.3 Practical Convergence Criteria

**Tier 1 -- Strong evidence, use these:**

| Mechanism                        | Implementation                                                                       | Evidence                        |
| :------------------------------- | :----------------------------------------------------------------------------------- | :------------------------------ |
| Hard cap                         | `MAX_ROUNDS = 5` (user's stated preference)                                          | All production systems use caps |
| External signal per round        | Each round must introduce new information (different model, tool output, new search) | Huang et al., Kamoi et al.      |
| No-new-feedback convergence      | If reviewers identify no new substantive critique → stop early                       | Multi-Agent Reflexion, ARIS     |
| Cross-model review               | Reviewer must be a different model than generator                                    | ARIS, A-HMAD, CCR               |
| Problem Anchor + Drift Detection | Freeze original question; reject feedback that changes it                            | ARIS research-refine            |

**Tier 2 -- Reasonable evidence:**

| Mechanism               | Implementation                                                   | Evidence                          |
| :---------------------- | :--------------------------------------------------------------- | :-------------------------------- |
| Score-gated acceptance  | Structured rubric with threshold (e.g., ≥6/10 on all dimensions) | ARIS (5/10→7.5/10 achieved)       |
| Patience counter        | Stop after N rounds without score improvement                    | ARIS dse-loop, ML training        |
| Structured pushback log | Executor records rejected feedback with reasoning                | ARIS research-refine              |
| Conjunctive criteria    | All quality gates must pass, not just overall score              | ARIS (score + verdict + no drift) |

### 3.4 the Convergence Formula

Convergence = **no new substantive feedback** + **no drift from anchor** + **hard cap not exceeded**.

This conjunction is more robust than any single criterion. A rising score with drift from the original question is worse than a flat score that stays on target. A "no feedback" signal from a sycophantic reviewer is not genuine convergence.

---

## 4. Cross-Examination and Pushback

### 4.1 the Pushback Protocol

ARIS's `research-refine` skill implements structured pushback:

| Round | Reviewer Said | Author Response | Outcome |
| :---- | :------------ | :-------------- | :------ |

Plus explicit sections:

- **Anchor Check**: "Reviewer suggestions rejected as drift: [list]"
- **Simplicity Check**: "Reviewer suggestions rejected as unnecessary complexity: [list]"

This forces explicit reasoning about **why** feedback is rejected, preventing both over-compliance (sycophancy) and silent dismissal.

### 4.2 When Pushback Helps Vs Hurts

Pushback is valuable when:

- Reviewer lacks local context the executor has (design intent, constraints)
- Finding is based on a misread
- Severity is overstated

Pushback degrades quality when:

- Executor is defending its own output from consistency bias
- Pushback is position-based ("I disagree") rather than evidence-based ("the code at line 42 handles this case because...")
- It creates debate loops that consume the iteration budget

### 4.3 Disagreement Resolution

When two reviewers disagree:

1. **Both cite specific evidence** → surface both views, let orchestrator assess evidence quality
2. **One cites evidence, one doesn't** → defer to the evidence-backed view
3. **Neither cites evidence** → flag as genuine uncertainty
4. **Don't force consensus** → unresolved disagreements are findings, not failures

Source: AgentAuditor (Feb 2026) proposes Anti-Consensus Preference Optimization -- training the adjudicator on majority-failure cases. Sometimes the dissenter is right. ([arXiv:2602.09341](https://arxiv.org/abs/2602.09341))

---

## 5. Practical Multi-Model Orchestration

### 5.1 Available CLIs

| CLI            | Invocation (non-interactive)              | Key flags                             |
| :------------- | :---------------------------------------- | :------------------------------------ |
| Claude Code    | `claude -p "prompt" --output-format json` | `--model`, `--allowedTools`           |
| Codex          | `codex exec "prompt" -o /tmp/out.txt`     | `--model`, `--full-auto`, `--sandbox` |
| Gemini         | `gemini -p "prompt" --output-format text` | `-m`, `--yolo`, `--sandbox`           |
| Vibe (Mistral) | `vibe --prompt "request" --output text`   | `--max-turns`, `--max-price`          |

### 5.2 Cost per Review Round (March 2026)

A typical review round (~5K input tokens of context + review prompt, ~2K output tokens):

| Model             | Cost per round |
| :---------------- | :------------- |
| Claude Opus 4.6   | ~$0.075        |
| Claude Sonnet 4.6 | ~$0.045        |
| GPT-5.2           | ~$0.037        |
| Gemini 2.5 Pro    | ~$0.026        |
| Gemini 2.5 Flash  | ~$0.007        |

A full dialectic review (1 generation + 2 independent reviews + 3 convergence rounds) costs roughly **$0.15-0.50** based on these estimates. Not meaningfully expensive.

### 5.3 Model Strengths by Review Type

| Review Type                | Best Model       | Evidence                                        |
| :------------------------- | :--------------- | :---------------------------------------------- |
| Multi-file architecture    | Claude Opus 4.6  | ~80.8% SWE-bench Verified                       |
| Terminal/build/CI issues   | GPT-5.3-Codex    | 77.3% Terminal-Bench 2.0, ~12 points above Opus |
| Novel/ambiguous reasoning  | Gemini 3.1 Pro   | 77.1% ARC-AGI-2                                 |
| Cost-efficient bulk review | Gemini 2.5 Flash | ~85% of Pro quality at lower cost               |

### 5.4 Automated Model Selection

The orchestrator can decide how many models to use based on pre-LLM heuristics on the input:

| Signal                | How to detect                        | Escalation trigger     |
| :-------------------- | :----------------------------------- | :--------------------- |
| Size/complexity       | Line count, file count, module count | >200 lines or >5 files |
| Security sensitivity  | Path patterns (auth/, crypto/, etc.) | Any match              |
| Domain criticality    | Configurable patterns                | Project-specific       |
| User explicit request | Skill invocation with flag           | Always honored         |

This is cheap (pure file analysis, no LLM calls) and can be tuned over time. No off-the-shelf tool implements this exactly -- it's a gap to fill.

### 5.5 Graceful Degradation

Priority cascade:

1. Try primary external model (Codex)
2. If unavailable, try secondary (Gemini)
3. If both unavailable, fall back to single-model with context-separated review (spawn a subagent)
4. Never fail because an external model is down

---

## 6. What Exists Already

### 6.1 Closest Implementations to What We Want

| Tool                           | Pattern                                          | Convergence                                    | Multi-model |
| :----------------------------- | :----------------------------------------------- | :--------------------------------------------- | :---------- |
| alecnielsen/adversarial-review | 4-phase adversarial debate loop (Claude + Codex) | Multi-round with synthesis                     | Yes         |
| charlieyou/cerberus            | 3-model consensus gating                         | Auto-iterate until consensus, configurable cap | Yes (3)     |
| CRTXAI/CRTX                    | Arbiter + escalation tiers                       | Rejection triggers fix cycle                   | Yes         |
| amazedsaint/clocoloop          | Claude implements, Codex reviews, loop           | Iterate until Codex approves                   | Yes         |
| hamelsmu/claude-review-loop    | Stop hook forces Codex review                    | Loop until review passes                       | Yes         |
| heavy3-ai/code-audit           | 3-model council + consensus counting             | Agreement-based, not iterative                 | Yes (3)     |
| josescasanova/k-review         | 6 parallel passes + majority voting              | Voting, not iterative                          | Yes (3)     |
| karpathy/llm-council           | Multi-LLM panel + chairman synthesis             | Single-pass, not iterative                     | Yes         |

### 6.2 What's Unique About Our Approach

None of the existing tools combine ALL of:

1. Generic (not code-review-specific) — applicable to any artifact
2. Cross-model dialectic with automated model selection
3. Structured convergence loop with Problem Anchor and drift detection
4. Evidence-based pushback protocol
5. Composable as a pattern within other skills

Most existing tools are hardcoded for code review. A generic dialectic+convergence skill that works for plans, research, code, and any other artifact is novel.

---

## 7. Skill Design Principles

### 7.1 Incompressibility

From Anthropic's own guidance: "Default assumption: Claude is already very smart. Only add context Claude doesn't already have. Challenge each piece of information: 'Does Claude really need this explanation?'"

Source: Anthropic's skill authoring best practices documentation (the core principle is well-established across multiple Anthropic guides, even if the exact URL has shifted).

Every instruction must pass: **"If I remove this line, would the output quality measurably degrade?"**

### 7.2 What to Prescribe Vs Flex

**Prescribe** (load-bearing):

- Context separation: fresh context for each reviewer
- External signal requirement: each round must introduce new information
- Comparable model quality: don't mix weak models with strong (Rethinking MoA: quality dominates diversity 1.4-3.2x)
- Problem Anchor: freeze the goal, detect drift
- Convergence criteria: no-new-feedback + no-drift + hard cap
- Anti-sycophancy: explicit adversarial mandate for reviewers
- Evidence-based pushback only: cite specific evidence, not just disagree
- Graceful degradation: fallback cascade when models unavailable
- Hard cap: maximum iteration count

**Flex** (let the model decide):

- Which specific models to use (the model is better at assessing what's available and appropriate than a rigid heuristic)
- How many models (tell the model "use more models for complex or critical work" and let it assess)
- Specific review prompts and critique dimensions
- How to synthesize (the model is better at this than any template)
- Output format and structure

### 7.3 One Skill or Two?

**Arguments for ONE skill:**

- The convergence loop without external signal is dangerous (Huang et al.) — so convergence needs cross-model review
- The dialectic without iteration is what /plan-task already does
- The combination is the novel, load-bearing pattern
- One context load, no coordination overhead
- Every existing implementation (ARIS, Cerberus, adversarial-review) combines them

**Arguments for TWO skills:**

- Composability: the convergence loop can use external signal from sources other than a second model (tool execution, test results, search results, human feedback) — making it independently useful
- Single responsibility: existing skills already use these patterns separately — /plan-task uses cross-pollination without convergence, /research uses convergence loops without cross-pollination
- The existing skills can compose the new primitives: /plan-task's dialectic mode → invoke /cross-pollinate; /research's review loop → invoke /converge

**Recommendation: TWO skills**, because:

1. **Tool-verified convergence is a valid standalone pattern.** The convergence loop can get external signal from tool execution (run tests, run linters, run backtests), not just from a second model. This is the centerpiece justification — a `/converge` skill that iterates on code with test execution as the external signal is useful and safe.
2. **Cross-pollination without iteration is useful.** Get 3 perspectives and synthesize once — this is what /plan-task's dialectic mode already does. A standalone skill makes this reusable.
3. **Existing skills already use these patterns separately.** /plan-task has dialectic generation (cross-pollination). /research has a review loop (convergence). Making these explicit primitives enables cleaner composition.
4. Each skill stays under 500 lines.
5. **Important safety note:** A standalone `/converge` skill MUST prescribe that each round introduces external signal. The skill description should warn against pure self-reflection loops.

### 7.4 Naming

- **`/cross-pollinate`** — emphasizes the diversity mechanism, not the debate mechanics. "Dialectic" implies thesis-antithesis-synthesis, which is one pattern but not the only one. "Cross-pollinate" captures the broader idea: get diverse perspectives and synthesize the best elements.
- **`/review-loop`** — more specific than `/converge` (which could mean many things in a data pipeline codebase). Action-oriented, describes what it does.

### 7.5 Orchestrator Bias

The orchestrator (the main Claude session) is both the synthesizer and potentially one of the reviewers. This creates anchoring bias — if the orchestrator produced the initial output and also evaluates reviews, it may favor its own perspective (D3 measured self-enhancement bias at 24.6% for single-judge evaluation).

**Mitigation:** The convergence check should ideally happen in a fresh context (spawn a subagent to evaluate whether convergence criteria are met). At minimum, the orchestrator should evaluate findings against the explicit rubric, not "gut feel" — D3 shows this reduces positional swap bias from ~20% to ~4%.

### 7.6 Semantic Compression Risk

The multi-agent annotation paper (2512.00047) found that over multiple rounds, agents compress information — they lose nuance and edge cases as they converge on shared understanding. Surface-level similarity (cosine similarity rising) masks semantic compression (intrinsic dimensionality dropping).

**Mitigation:** The convergence loop should maintain a "notable but rejected" findings log — information that was considered but intentionally set aside, so it doesn't silently disappear through compression. The Problem Anchor prevents drift on the question, but this log prevents drift on the answer's nuance.

### 7.7 Coexistence with Existing Skills

| Existing Skill      | Relationship to New Skills                                                                                                                             | Migration                                                                                                                                           |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/dialectic-review` | Uses both patterns (cross-model review + convergence loop), but is code-review-specific                                                                | Keep as-is. Its specificity (Codex command mapping, /code-review output format) is its strength.                                                    |
| `/plan-task`        | Step 3 Dialectic mode is cross-pollination (3 models generate plans + synthesis). Iterative refinement is convergence.                                 | Could reference /cross-pollinate as the mechanism, but the tight integration with plan format means keeping the logic inline is cleaner.            |
| `/research`         | Steps 4-5 are a convergence loop (two reviewers → address feedback → re-review → cap at 3). Step 2 is parallel research (a form of cross-pollination). | Same — the research-specific review rubric and agent team pattern are tightly integrated. Reference the new skills as methodology, not invocations. |

**Conclusion:** The new skills are **reference patterns** that existing skills can draw from, AND **standalone invocable workflows** for ad-hoc use. They don't replace existing skills — they provide the generalized methodology that existing skills have already domain-specialized.

---

## 8. Key Design Decisions for the Skills

### 8.1 `/cross-pollinate`

**Input:** Any target (file, document, question, plan, code) + optional instructions.

**Core pattern:** Independent generation/review by multiple models → synthesis.

**Load-bearing decisions (4 — minimum viable):**

1. **Context separation is mandatory** — each model works in a fresh, independent context
2. **Independence before synthesis** — no model sees another's output until synthesis phase
3. **Comparable model quality** — don't pair a frontier model with a significantly weaker one
4. **Graceful degradation** — cascade through available models; never fail because one is unavailable

**What to flex:** Which specific models, how many models (more for complex/critical work), how to decompose the task for each, whether to synthesize or select, output format.

### 8.2 `/review-loop`

**Input:** Any artifact to iterate on + goal (Problem Anchor) + optional review criteria.

**Core pattern:** Review → address feedback (with pushback) → check convergence → repeat.

**Load-bearing decisions (5 — minimum viable):**

1. **External signal per round** — each review must come from a source independent of the generator (different model, tool output, new evidence). Pure self-reflection is explicitly prohibited.
2. **Problem Anchor** — freeze the goal, carry verbatim, detect and reject drift
3. **Convergence check** — stop when: no new substantive feedback AND no drift AND hard cap reached (default 5)
4. **Adversarial mandate** — reviewers must find flaws, not confirm quality
5. **Evidence-based pushback** — the author can reject feedback, but must cite specific evidence

**What to flex:** Specific review dimensions, which model(s) for review, how to address feedback, output format, notable-but-rejected findings log.

---

## 9. Anti-Patterns

| Anti-Pattern                              | Why It Fails                                             | Alternative                                      |
| :---------------------------------------- | :------------------------------------------------------- | :----------------------------------------------- |
| Same-model self-review without tools      | Degrades quality (Huang et al., ICLR 2024)               | Cross-model or tool-verified review              |
| Free-form debate between identical agents | Entrenchment, not convergence (CMU overconfidence paper) | Structured roles with adversarial mandate        |
| Forcing consensus                         | Suppresses valid minority findings                       | Surface disagreements; don't require agreement   |
| Mixing weak models with strong            | Quality dominates diversity 1.4-3.2x (Rethinking MoA)    | Use comparably capable models only               |
| Unlimited rounds                          | Diminishing returns after round 2-3; models entrench     | Hard cap + no-new-feedback early exit            |
| Score-only convergence                    | Scores aren't calibrated across rounds or reviewers      | Conjunctive criteria (score + no-drift + no-new) |
| Position-based pushback                   | "I disagree" without evidence degrades quality           | Evidence-based pushback only                     |
| Reviewing in same session as production   | Anchoring bias; worse than not reviewing (CCR paper)     | Fresh context for every review                   |

---

## References

### Multi-Model Review and Debate

- [Cross-Context Review](https://arxiv.org/abs/2603.12123) — Song et al., March 2026. Context separation > model diversity.
- [Should we be going MAD?](https://proceedings.mlr.press/v235/smit24a.html) — Smit et al., ICML 2024.
- [ICLR 2025 MAD Analysis](https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/) — Self-consistency beats debate.
- [A-HMAD](https://link.springer.com/article/10.1007/s44443-025-00353-3) — Heterogeneous multi-agent debate.
- [Rethinking MoA](https://arxiv.org/abs/2502.00674) — Self-MoA > multi-model MoA; quality > diversity.
- [When Two LLMs Debate](https://arxiv.org/abs/2505.19184) — Overconfidence escalation in debates.
- [Peacemaker or Troublemaker](https://arxiv.org/abs/2509.23055) — Sycophancy as core failure mode.
- [When Disagreements Elicit Robustness](https://arxiv.org/abs/2502.15153) — Disagreement safe for code tasks.
- [Free-MAD](https://arxiv.org/abs/2509.11035) — Anti-conformity + trajectory scoring.
- [ECON](https://arxiv.org/abs/2506.08292) — Bayesian Nash Equilibrium for multi-LLM.
- [Can LLM Agents Really Debate?](https://arxiv.org/abs/2511.07784) — Majority pressure suppresses correction.
- [Adversarial Cooperation in Code Synthesis](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf) — Block AI. Coach-player essential.

### Self-Correction and Convergence

- [LLMs Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) — Huang et al., ICLR 2024.
- [When Can LLMs Correct Their Mistakes?](https://arxiv.org/abs/2406.01297) — Kamoi et al., TACL 2024.
- [SELF-REFINE](https://arxiv.org/abs/2303.17651) — Madaan et al., NeurIPS 2023.
- [SCoRe](https://arxiv.org/abs/2409.12917) — Google, ICLR 2025. RL-trained self-correction.
- [Emergent Convergence](https://arxiv.org/abs/2512.00047) — Semantic compression over rounds.
- [Multi-Agent Reflexion](https://arxiv.org/abs/2512.20845) — 2-round cap, consensus check.
- [Hegelian Dialectic for LLMs](https://arxiv.org/abs/2501.14917) — Innovation front-loaded.
- [Scaling Agent Systems](https://arxiv.org/abs/2512.08296) — Google/MIT. Multi-agent helps parallel tasks, hurts sequential.

### Adversarial Collaboration

- [Kahneman's Adversarial Collaboration](https://www.edge.org/adversarial-collaboration-daniel-kahneman) — Original framework.
- [AgentAuditor](https://arxiv.org/abs/2602.09341) — Anti-consensus preference optimization.
- [D3: Debate, Deliberate, Decide](https://arxiv.org/abs/2410.04663) — Anonymized adversarial debate.
- [ConsensAgent](https://aclanthology.org/2025.findings-acl.1141/) — ACL 2025. Dynamic sycophancy mitigation.
- [SYCOPHANCY.md](https://sycophancy.md/) — Open-spec anti-sycophancy protocol.

### Deep Research Tools

- [Anthropic Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) — 90.2% improvement.
- [OpenAI Deep Research](https://openai.com/index/introducing-deep-research/) — RL-trained convergence.
- [LangChain Open Deep Research](https://github.com/langchain-ai/open_deep_research) — Max 3 reflection cycles.
- [Stanford STORM](https://storm-project.stanford.edu/research/storm/) — Multi-perspective conversations.
- [FutureHouse Robin](https://arxiv.org/abs/2505.13400) — Lab-in-the-loop convergence.

### Existing Implementations

- [adversarial-review](https://github.com/alecnielsen/adversarial-review) — Claude + Codex debate loop.
- [cerberus](https://github.com/charlieyou/cerberus) — 3-model consensus gating.
- [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) — Cross-model adversarial review loops.
- [Aider architect-editor](https://aider.chat/2024/09/26/architect.html) — Two-model SOTA pattern.
- [Claude Octopus](https://github.com/nyldn/claude-octopus) — Multi-tentacled orchestrator.

### Skill Design

- [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Incompressibility, progressive disclosure.
- [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Evaluator-optimizer pattern.
- [Emanuel: The Overprompting Trap](https://jeffreyemanuel.com/writing/overprompting) — Every constraint narrows solution space.
- [Agent Skills Standard](https://agentskills.io/specification) — Cross-agent skill format.
- [Emanuel: LLM Coding Tournament](https://github.com/Dicklesworthstone/llm_multi_round_coding_tournament) — Multi-model cross-pollination.

### Practitioner Resources

- [Zylos: Multi-Model AI Code Review](https://zylos.ai/research/2026-02-17-multi-model-ai-code-review) — Exponential decay convergence curve.
- [SmartScope: Claude Code x Codex Review Loop](https://smartscope.blog/en/blog/claude-code-codex-review-loop-automation-2026/) — Three maturity levels.
- [Aseem Shrey: Claude and Codex Argue](https://aseemshrey.in/blog/claude-codex-iterative-plan-review/) — 14 issues in 3 rounds.
- [CIA Tradecraft Primer](https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf) — Pre-mortem, ACH, red teaming.
