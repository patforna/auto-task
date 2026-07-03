# Dialectic and Adversarial Approaches to AI Planning

Research conducted 2026-03-13. Investigates whether multi-agent debate, critic agents, and adversarial review improve plan quality for agentic workflows.

---

## The Core Question

Does having a critic — whether a separate model, same-model self-critique, or structured adversarial process — produce better plans than single-pass generation? And if so, which architecture works best?

---

## Multi-Agent Debate (MAD): Current Evidence

### The ICML/ICLR Findings

The most rigorous evaluation is "Should we be going MAD?" (Smit et al., ICML 2024). Key findings:

- **MAD does not reliably outperform simpler baselines** like self-consistency and chain-of-thought ensembling in its default configuration.
- **MAD is hyperparameter-sensitive.** Multi-Persona debate, initially one of the worst protocols, improved ~15% on USMLE when "agreement intensity" (how much agents should agree with each other) was tuned.
- **Heterogeneous agents help.** Combining different foundation models showed more promising improvement than multiple instances of the same model (ICLR Blogposts 2025).

### The ICML 2024 Factuality Paper

Du et al. ("Improving Factuality and Reasoning in Language Models through Multiagent Debate", ICML 2024) showed multi-agent debate reduces factual hallucinations and improves mathematical reasoning. The mechanism: agents are forced to respond to specific critiques rather than just regenerating.

### Practical Implication

MAD works, but it is not a free lunch. The gains come from **diversity of perspective** (different models, different prompts, different roles), not from debate mechanics per se. Running the same model three times with the same prompt and having them "debate" adds cost without proportional benefit.

---

## Self-Critique: the Uncomfortable Evidence

### The Huang Et Al. Result (ICLR 2024)

"Large Language Models Cannot Self-Correct Reasoning Yet" — the landmark paper:

- Asking GPT-4 to review and correct its own reasoning answers **consistently decreased accuracy**. The model changed correct answers to wrong ones more often than it fixed errors.
- Without external feedback, self-correction is unreliable. The model lacks a ground-truth signal to distinguish good from bad reasoning.

### The TACL Survey (2024)

"When Can LLMs Actually Correct Their Own Mistakes?" (Kamoi et al., TACL 2024) synthesises the field. Conditions for successful self-correction:

| Condition                            | Self-correction works? | Notes                                      |
| ------------------------------------ | ---------------------- | ------------------------------------------ |
| No external feedback (intrinsic)     | Rarely                 | Often degrades performance                 |
| With external tool verification      | Yes                    | Tools are the linchpin (CRITIC paper)      |
| With explicit error pointing         | Yes                    | LLMs can fix errors when told what's wrong |
| With external knowledge (RAG)        | Yes                    | Grounds critique in facts                  |
| With a different, stronger model     | Yes                    | Cross-model critique is more reliable      |
| With RL training for self-correction | Yes                    | Google's SCoRe (ICLR 2025)                 |

### The Intrinsic Self-Critique Counterpoint

"Enhancing LLM Planning Capabilities through Intrinsic Self-Critique" (arXiv 2512.24103, Dec 2025) showed strong gains **without** external verifiers:

- Gemini 1.5 Pro: 49.8% → 89.3% on Blocksworld (3-5 blocks)
- Claude 3.5 Sonnet: 68% → 89.5% on Blocksworld (3-5 blocks)

The key difference from Huang et al.: this used **iterative few-shot self-critique** with structured prompting, not naive "check your answer." The critique was scaffolded with examples of what good critique looks like.

### Synthesis: Does the Critic Need to Be a Different Model?

The evidence suggests a spectrum:

1. **Naive same-model self-critique** ("check your answer") — harmful or neutral. The model lacks signal to distinguish correct from incorrect.

2. **Structured same-model self-critique** (scaffolded with examples, specific critique dimensions, iterative) — can work well, especially for planning where the failure mode is missing considerations rather than logical errors.

3. **Same-model with external tools** (code execution, web search, formal verifier) — works. The tools provide the ground-truth signal the model lacks.

4. **Cross-model critique** (different model reviews) — works, and adds genuine diversity of architectural bias. Different models have different blind spots.

For **planning** specifically (vs. reasoning or factual QA), self-critique is more viable because plan quality is about coverage and coherence, not logical/mathematical correctness. A model can more reliably identify "you didn't consider X" than "your arithmetic is wrong."

---

## Generate-and-Select Vs. Critique-and-Revise

Two fundamentally different strategies:

### Generate-and-Select (Diversity-First)

Generate N independent candidates, then pick the best one.

- **How:** Sample multiple completions (high temperature or different prompts), evaluate each, select winner.
- **Strengths:** Explores the solution space broadly. PlanSearch (ICLR 2025) showed plan diversity beats plan detail — generating diverse plans then selecting outperformed iterating on a single plan.
- **Weaknesses:** No synthesis. If Plan A has the right architecture and Plan B has the right edge-case handling, selection can only pick one.
- **Best for:** When the problem has a single "right" approach that might be missed, and you need coverage of the solution space.

### Critique-and-Revise (Iterative Refinement)

Generate one candidate, critique it, revise based on critique, repeat.

- **How:** SELF-REFINE (Madaan et al., 2023) — alternate FEEDBACK and REFINE steps. The model critiques its own output, then generates an improved version.
- **Strengths:** Can **synthesize** — combining good elements from different perspectives into a novel superior plan. Analogous to human revision, not just voting.
- **Weaknesses:** Susceptible to the self-correction trap (Huang et al.) — the model may "correct" good elements into bad ones without external signal.
- **Best for:** When the plan needs refinement of a basically-correct approach rather than a fundamentally different one.

### The Hybrid: Generate Diverse, Then Synthesize

The most promising approach in the literature combines both:

1. Generate N diverse plans (different models, prompts, or personas)
2. Rather than selecting one winner, **synthesize** a new plan that takes the best elements from each
3. Optionally, critique the synthesis

This matches the PlanSearch finding (diversity > detail) while avoiding the limitation of pure selection (no synthesis).

**This is essentially what the current plan-task Dialectic mode does:** three models generate plans independently, then agreements/disagreements/gaps are identified and synthesized.

---

## Red-Teaming Plans Before Execution

### The Pre-Mortem Pattern

Borrowed from project management (Gary Klein): before executing, assume the plan failed and work backward to identify why. Applied to agent plans:

> "Assume this plan was executed by a capable agent and the result was wrong. What went wrong?"

This reframes critique from "find problems" (which triggers sycophancy) to "explain the failure" (which triggers causal reasoning — a different cognitive mode).

### Adversarial Roles in Multi-Agent Systems

PeerGuard (2025) applies cross-agent auditing where agents must justify conclusions before action. The pattern: separate the **proposer** from the **auditor**, giving the auditor an explicit mandate to find problems.

The key insight from debate research: simply asking an agent to "review" produces weak critique. Giving it an explicit **adversarial role** ("your job is to find the fatal flaw") produces stronger critique. Agreement intensity tuning (from the MAD paper) confirms this — agents default to too much agreement.

### OWASP and Red-Teaming Frameworks

OWASP's Gen AI Red Teaming Guide (Jan 2025) and Top 10 for Agentic Applications (Dec 2025) focus on safety/security red-teaming rather than plan quality. But the methodology transfers: structured adversarial evaluation with specific attack categories is more effective than open-ended "find problems."

For plan red-teaming, structured categories might be:

- **Missing preconditions** — what does the plan assume exists that might not?
- **Ordering violations** — what happens if step N fails? Does step N+1 still make sense?
- **Scope creep vectors** — where might the implementing agent go beyond scope?
- **Verification gaps** — which steps lack concrete checks?
- **Integration risks** — what could break in code the plan doesn't touch?

---

## Society of Mind: the Broader Architecture

Minsky's Society of Mind (1986) proposed intelligence as the interaction of many simple agents, none of which is intelligent alone. The modern LLM incarnation:

### Current Implementations

- **AutoGen** (Microsoft, 2024) — 200K+ downloads in 5 months; chains LLM agents with different roles and tools.
- **CrewAI** — role-based multi-agent workflows with explicit delegation.
- **MetaGPT** — agents follow "standard operating procedures" and structured workflows (closer to software engineering than open debate).
- **Sibyl** — "jury" of agents that refine answers, outperforming single-agent chain-of-thought on challenging QA.

### What Works in Practice

The most effective multi-agent architectures for planning are **not** free-form debate. They are **structured role differentiation**:

| Pattern             | Example                                                 |
| ------------------- | ------------------------------------------------------- |
| Proposer + Critic   | One agent plans, another finds flaws                    |
| Specialist ensemble | Each agent brings domain expertise (security, perf, UX) |
| Architect + Editor  | Aider's pattern — one designs, one implements           |
| Devil's Advocate    | One agent explicitly argues against the proposed plan   |

Free-form debate between identical agents tends to converge on consensus (sycophancy) rather than surfacing genuine disagreements. Structured roles with explicit mandates produce better outcomes.

---

## Practical Recommendations for Plan-Task

### What the Evidence Supports

1. **The current Dialectic mode is well-designed.** Three different models generating plans independently, then synthesizing, aligns with PlanSearch's finding that diversity > detail. Using different foundation models (not just different prompts to the same model) provides genuine architectural diversity.

2. **Add a structured critique pass.** After synthesis, a targeted critique using the pre-mortem framing ("assume this failed — why?") and structured categories (missing preconditions, ordering violations, scope creep vectors, verification gaps) would catch issues that agreement-driven synthesis misses.

3. **Self-critique can work for plans** if scaffolded. Planning critique is about coverage and coherence ("did you consider X?"), not logical correctness ("is your math right?"). This is the domain where self-critique is most viable.

4. **The pre-mortem reframe matters.** "What could go wrong?" produces better critique than "review this plan" because it triggers causal reasoning rather than agreement-seeking.

5. **Agreement intensity should be low for critics.** The MAD research shows agents default to too much agreement. An explicit adversarial mandate improves critique quality.

### What the Evidence Does Not Support

1. **Free-form debate between identical agents.** Running the same model three times and having them argue produces heat, not light.

2. **Naive self-correction.** "Check your plan" without structure, examples, or specific critique dimensions is neutral-to-harmful.

3. **Unlimited iteration.** Diminishing returns set in quickly. 1-2 critique rounds capture most value; further rounds tend toward convergence rather than improvement.

---

## Open Questions

- **Cost-benefit at task scale.** The Dialectic mode is ~3x cost. Is the improvement worth it for typical plan-task invocations, or only for genuinely ambiguous multi-approach tasks? The current "recommend and wait for go" gate handles this.

- **Structured critique vs. full Dialectic.** For tasks where the approach is clear but the plan might miss edge cases, is a single-model structured critique pass (cheaper) as effective as full 3-model Dialectic?

- **Critique scaffolding.** What does the optimal critique prompt look like? The research suggests specific dimensions (pre-mortem categories) outperform open-ended "find problems," but the optimal set for implementation plans is not established.

---

## Sources

### Multi-Agent Debate

- Du et al. — "Improving Factuality and Reasoning in Language Models through Multiagent Debate" (ICML 2024) — [project page](https://composable-models.github.io/llm_debate/)
- Smit et al. — "Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs" (ICML 2024) — [proceedings](https://proceedings.mlr.press/v235/smit24a.html)
- ICLR Blogposts 2025 — "Multi-LLM-Agents Debate: Performance, Efficiency, and Scaling Challenges" — [blog](https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/)
- ECON — "From Debate to Equilibrium: Belief-Driven Multi-Agent LLM Reasoning via Bayesian Nash Equilibrium" (ICML 2025) — [GitHub](https://github.com/tmlr-group/ECON)

### Self-Critique and Self-Correction

- Huang et al. — "Large Language Models Cannot Self-Correct Reasoning Yet" (ICLR 2024) — [paper](https://arxiv.org/abs/2310.01798)
- Kamoi et al. — "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs" (TACL 2024) — [paper](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177)
- Gou et al. — "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing" (ICLR 2024) — [paper](https://arxiv.org/abs/2305.11738)
- "Enhancing LLM Planning Capabilities through Intrinsic Self-Critique" (arXiv Dec 2025) — [paper](https://arxiv.org/abs/2512.24103)
- Madaan et al. — "SELF-REFINE: Iterative Refinement with Self-Feedback" (NeurIPS 2023) — [paper](https://openreview.net/pdf?id=S37hOerQLB)
- Google — "Training Language Models to Self-Correct via Reinforcement Learning" (SCoRe, ICLR 2025) — [paper](https://arxiv.org/pdf/2409.12917)

### Planning Approaches

- PlanSearch — "Planning in Natural Language" (ICLR 2025) — diversity > detail
- Yao et al. — "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" (NeurIPS 2023) — [paper](https://arxiv.org/abs/2305.10601)
- LATS — Language Agent Tree Search — combines reflection, evaluation, and MCTS

### Multi-Agent Architectures

- AutoGen (Microsoft) — multi-agent conversation framework
- MetaGPT — SOP-driven multi-agent collaboration
- PeerGuard (2025) — cross-agent auditing and mutual reasoning
- Sibyl — jury-of-agents for answer refinement

### Red-Teaming and Adversarial Review

- OWASP — Gen AI Red Teaming Guide (Jan 2025); Top 10 for Agentic Applications (Dec 2025)
- NIST — AI Risk Management Framework; ARIA red teaming exercises (2024)
- Gary Klein — "Performing a Project Premortem" (HBR 2007)

### Prior TAD Research

- `docs/research/2026-03-13-implementation-planning-for-agents.md`
