# Designing Multi-Agent Research Systems: a Synthesis

**Status:** done — design rationale for /research skill (referenced at SKILL.md:144)

## Problem Anchor

How should a multi-agent research system be designed — decomposition, orchestration, review/convergence, and synthesis — to maximize comprehensiveness, depth, accuracy, and non-obvious insight discovery? What are the SOTA patterns, and what can be distilled into an incompressible Claude Code skill?

## Executive Summary

Seven parallel research agents investigated this question from orthogonal angles: ARIS implementation analysis, multi-agent systems survey (13 systems), AI debate/adversarial protocols, structured analytic techniques (ACH, Delphi, PRISMA), ensemble/aggregation patterns, prompt engineering for research quality, and cross-domain analogies (journalism, intelligence, law, medicine, superforecasting). This synthesis identifies what works, what doesn't, and what the adjacent fields know that AI researchers haven't adopted.

**The core finding**: the dominant quality lever is not prompt engineering or agent count — it is **architectural decisions** about decomposition, information flow, and convergence mechanics. Specifically: (1) token budget (retrieval volume and context available to agents) is the primary performance lever, (2) breadth through sub-question diversity dominates depth through iteration, (3) cooperative review beats adversarial debate, (4) structural debiasing (anonymization, pre-commitment, source independence tracking) matters more than instructional debiasing ("be critical"), and (5) the most impactful pattern missing from current systems is pre-commitment to resolution criteria before evidence collection.

A cross-cutting theme emerges: **pre-retrieval diversity is the load-bearing architectural pattern**. It appears as sub-question decomposition (§1.1), perspective injection (§1.6), and diverse search strategies (§1.2). Conversely, post-retrieval iteration shows diminishing returns (§2.2, §2.5) — the same principle viewed from the other side. The implication: invest effort in decomposition and search diversity upfront; keep review rounds minimal.

---

## 1. What Works: Evidence-Backed Patterns

### 1.1 Orchestrator-Worker with Parallel Sub-Questions

The dominant architecture across all successful systems. A lead agent decomposes the research question into orthogonal sub-questions, spawns parallel workers, and synthesizes results. Present in: Anthropic's internal system (90.2% improvement over single-agent), ARIS, Agent Laboratory, Virtual Lab, STORM.

The decomposition step is load-bearing. Anthropic found that detailed task descriptions for subagents are critical — clear objectives, output format specifications, and scope boundaries prevent agents from duplicating work. Vague instructions are the primary cause of redundancy (MAST FM-1.3: redundant step repetition accounts for 15.7% of all multi-agent failures).

**Optimal team size**: 3-7 agents. Benefits saturate due to correlated errors — ensemble selection research (arXiv:2602.08003) demonstrates an information-theoretic error floor: correlated failures from shared training data create diminishing returns that additional agents cannot overcome. DyLAN's Agent Importance Scoring showed similar saturation effects.

**Key design decision**: sub-question diversity, not prompt/persona diversity. Assigning different framings of the same question to the same model produces superficial variation but not genuine error independence (ensemble research, arXiv:2502.10858). Assigning genuinely different sub-questions — different search strategies, different source domains, different temporal focus — produces meaningfully decorrelated outputs.

## Sources: Anthropic Engineering Blog (2025), MAST arXiv:2503.13657, DyLAN arXiv:2310.02170, arXiv:2602.08003, arXiv:2502.10858

### 1.2 Breadth Before Depth

Breadth through prompt reformulation (85.1% accuracy) outperforms iterative depth refinement (83.3%) on research tasks (CISC 2025, arXiv:2502.10858). The mechanism: "deep iterative reasoning does not generate new knowledge — it progressively activates existing pre-trained knowledge." If the model doesn't have the knowledge, more reasoning loops don't help; retrieval is required.

The expand-then-squeeze search paradigm (arXiv:2508.05668) — generate many query variants across framings (mainstream, critic, adjacent-field, formal/informal terminology) → retrieve → distill to reasoning-critical facts — substantially outperforms single-query agents. The most valuable queries use the domain's native vocabulary (technical jargon, paper titles, author names, dataset names), not the user's original phrasing.

Anthropic's system confirms this: breadth-first search (broad queries → narrow) outperforms attempting comprehensive first-pass queries. On their internal BrowseComp web-browsing benchmark, token budget (the total volume of retrieval and context given to agents) was the primary performance lever — more tool calls and more retrieved context dominated prompt phrasing improvements. Note: this finding is from a web-browsing benchmark; the magnitude may differ for other research task types, but the directional finding (more retrieval > better prompts) is consistent with the broader evidence.

## Sources: CISC arXiv:2502.10858, arXiv:2508.05668, Anthropic Engineering Blog

### 1.3 Cooperative Review Over Adversarial Debate

ColMAD (2024) found that cooperative framing ("complement each other's missing points") achieves a 19% improvement over competitive debate on error detection tasks. The adversarial zero-sum structure causes "debate hacking": agents misinterpret task requirements, use overconfident tone to mislead judges, and focus on persuasion over truth.

Multi-agent debate underperforms on closed-answer benchmarks. An ICLR 2025 analysis found MAD frameworks fail to beat self-consistency across 9 benchmarks, primarily because those benchmarks "only require a single knowledge point," making debate "an inefficient resampling method." Specific failure modes:

- **Majority conformity**: when a majority gives the same answer (even incorrectly), minority agents conform
- **Same-model echo chambers**: debate degenerates to static exchange with no epistemic value
- **Correct-to-wrong reversals**: a significant fraction of initially correct answers become wrong after debate

**Caveat**: these findings are from multiple-choice and reasoning benchmarks. Debate may be more useful on open-ended research tasks where information is distributed across agents — the scalable oversight literature (Kenton et al., arXiv:2407.04622) shows debate's advantage is specifically in surfacing information the judge cannot independently access. The heterogeneity of models is essential — MoA (arXiv:2406.04692) consistently found heterogeneous model ensembles outperform homogeneous ones.

**What works instead of debate**: structured proposer-critic separation where the critic's role is to find gaps and missing evidence, not to argue against the conclusion. The critic produces specific, actionable feedback ("section 3 claims X without citation; check Y source"), not adversarial counterarguments.

## Sources: ColMAD arXiv:2510.20963, ICLR 2025 MAD Analysis, Kenton Et Al. arXiv:2407.04622, MoA arXiv:2406.04692

### 1.4 Chain of Verification (CoVe)

The most directly applicable anti-hallucination technique (Dhuliawala et al., ACL Findings 2024). Four-step loop: draft → plan verification questions → answer them in isolated contexts → revise. The isolation step is the mechanism: verification questions answered in a fresh context cannot confirm the prior draft. Results: list-QA precision 0.17 → 0.36, longform FactScore 55.9 → 71.4.

This maps directly onto a verification subagent role: after synthesis, spawn a verification agent that receives the draft and checks specific claims against independent retrieval, without access to the original evidence chain.

## Source: Dhuliawala Et Al., ACL Findings 2024, Aclanthology.org/2024.findings-Acl.212

### 1.5 Problem Anchor as Structured Document

ARIS's `research-refine` skill freezes a five-field "Problem Anchor" at the start: Bottom-line problem / Must-solve bottleneck / Non-goals / Constraints / Success condition. This is copied verbatim into every iteration round. The reviewer is explicitly instructed to call drift by name. Each refinement round requires an explicit "Anchor Check" and "Simplicity Check" before any changes.

The structured anchor prevents the most common failure mode in iterative research: scope drift. "Drift" is treated as a named first-class concept, not an implicit risk.

## Source: ARIS Research-refine/SKILL.md

### 1.6 Perspective Injection Before Retrieval

STORM's core insight: generate diverse perspectives *before* querying sources. Multiple perspective-bearing agents conduct separate interviews (retrieval sessions) rather than one undifferentiated search. This produces broader coverage than post-hoc diversity overlaid on a single retrieval pass.

Empirical result: 25% improvement in article organization, ~10% in coverage breadth versus retrieval-augmented baselines. The perspectives serve as natural sub-question generators — each perspective leads to different follow-up questions during retrieval.

## Source: STORM arXiv:2402.14207, Stanford

---

## 2. What Doesn't Work: Evidence Against Common Practices

### 2.1 Expert Persona Prompting

The most clearly debunked technique (Mollick et al., Wharton GAIL, December 2025). Six models × 25 trials × GPQA Diamond + MMLU-Pro: no expert persona reliably improved factual accuracy on any model. Domain-matched experts provided no advantage. Low-knowledge personas consistently degraded results.

**Replacement**: task-specific instructions about objective, format, and quality criteria — not "you are an expert in X."

## Source: Wharton GAIL, Gail.wharton.upenn.edu/research-and-Insights/playing-Pretend-Expert-Personas

### 2.2 Self-Refinement Without External Signal

EVOLVE (arXiv:2502.05605) directly challenges Self-Refine's conclusions: "LLMs show no clear evidence of inherent Self-Refinement and may even experience response quality degradation." The accuracy-correction paradox (arXiv:2601.00828): stronger, more accurate models are *worse* at self-correction — DeepSeek (94% accuracy) has only a 16.7% intrinsic correction rate vs. GPT-3.5 (66% accuracy) at 26.8%.

The mechanism: stronger models make fewer but deeper errors (setup/logic failures at 77% of DeepSeek errors) that resist self-correction without external grounding. Shallow errors (arithmetic) are self-correctable; deep errors (reasoning setup) are not. This is a stronger design constraint than "self-refinement doesn't work" — it means that when a capable model like Claude refines its own research output, it may *actively degrade* the output while appearing confident, because its errors are precisely the kind that resist internal detection.

EVOLVE's affirmative finding: models *can* develop self-refinement through iterative training (SFT + DPO with self-refinement loss). But at inference time, without such training, self-correction with external tool feedback (search engines, code interpreters) is the reliable path (CRITIC, arXiv:2305.11738).

**Implication for research skills**: review rounds must introduce new external signal (fresh retrieval, different model, tool output) — pure self-reflection is prohibited.

## Sources: EVOLVE arXiv:2502.05605, arXiv:2601.00828, CRITIC arXiv:2305.11738

### 2.3 Chain-of-Thought for Reasoning Models

For reasoning models (Claude 3.7+, o3-mini, Gemini 2.5 Flash), explicit CoT is marginally beneficial to harmful (Gemini 2.5 Flash: -3.3%) and adds 35-600% latency/tokens. Modern reasoning models do this internally.

## Source: Wharton GAIL, June 2025

### 2.4 Temperature for Diversity

Changes in temperature 0.0-1.0 have no statistically significant effect on problem-solving accuracy (EMNLP Findings 2024). Large models are temperature-resilient. Higher temperatures increase hallucination risk without meaningful diversity gains. Diversity should come from structure (different sub-questions, different source domains), not sampling parameters.

## Source: EMNLP Findings 2024, Aclanthology.org/2024.findings-Emnlp.432

### 2.5 Forcing Iteration Past Natural Convergence

MAD (Liang et al., 2023) found that forcing debates to continue past their natural stopping point degrades quality. The adaptive break — judge terminates when satisfied rather than at a fixed round count — is essential. DCI (2025) found structured deliberation underperforms on routine tasks by -0.60 points; the overhead is only justified for complex, non-routine decisions.

Working rule from converging evidence: **1-3 rounds is the practical range**. Most debates/reviews resolve in 1 round for simpler tasks. Beyond 3, cost exceeds benefit.

## Sources: MAD arXiv:2305.19118, DCI arXiv:2603.11781

---

## 3. The Sycophancy Problem

The default behavior of LLMs under iterative review is inappropriate convergence, not productive disagreement. This is a critical failure mode to design against — while MAST's data shows system design issues (redundant steps, reasoning-action inconsistency) are more frequent in aggregate, sycophancy is uniquely corrosive because it *looks like* the system working correctly (smooth convergence) while silently degrading output quality.

**Mechanisms**:

- RLHF optimization: human preference judgments favor agreement, and optimizing against these preferences likely reinforces sycophancy — though the causal chain is not fully established (Sharma et al., arXiv:2310.13548)
- Identity-based deference: agents defer to peers based on identity rather than argument quality (arXiv:2510.07517)
- Fallacious argument susceptibility: LLMs are simultaneously producers of and highly influenced by fallacious arguments; consensus emerges regardless of initial opinion distribution (arXiv:2502.19098)
- Mode collapse: when multiple agents share the same base model, anonymity alone doesn't prevent de facto groupthink — they share training-induced priors (Scalable Delphi, arXiv:2602.08889)

**Structural mitigations** (evidence-backed):

1. **Response anonymization**: removing agent identity markers reduces sycophantic deference (arXiv:2510.07517)
2. **Confidence signaling**: agents communicating explicit confidence scores reduce premature consensus by ~11% while improving correction cases by ~20% (ConfMAD, arXiv:2509.14034)
3. **Cooperative framing**: replacing adversarial "win" framing with "find what the other missed" eliminates debate hacking (ColMAD)
4. **Structural minority reports**: requiring dissenting views to be preserved in output rather than suppressed — DCI achieves 98% minority report production vs. ≤16% in baselines (arXiv:2603.11781)
5. **External signal in every round**: each review iteration must introduce new evidence (fresh retrieval, different model, tool output) — pure re-reasoning over the same context produces sycophantic drift

---

## 4. Convergence: When to Stop

**DCI convergence mechanics** (arXiv:2603.11781): DCI uses a structured convergent flow algorithm with three conditions: score dominance (leading option exceeds runner-up by a threshold), majority backing, and no unresolved blocking objections. If natural convergence doesn't occur within a maximum of 2 rounds, a forced-decision fallback applies (outranking → minimax regret → satisficing). DCI reports that roughly half of cases converge naturally; the rest require the fallback. Cost: ~62x single-agent token budget — the structured process only justifies its overhead on complex, non-routine decisions.

**ARIS convergence mechanics**:

- `auto-review-loop`: MAX_ROUNDS = 4, stop at score ≥ 6/10 or verdict contains "accept"/"sufficient"/"ready for submission"
- `research-refine`: MAX_ROUNDS = 5, SCORE_THRESHOLD = 9, three-way verdict (READY/REVISE/RETHINK), requires score ≥ 9 AND no drift AND no complexity bloat simultaneously

**Working synthesis for a research skill**: convergence = both reviewers identify no new substantive gaps or corrections. Hard cap at 3 rounds. Adaptive stopping (stop when converged, don't force more rounds). The convergence check is: "did this round produce actionable feedback that would change the document?" If no → stop.

---

## 5. What Adjacent Fields Know That AI Researchers Don't

The most underused pattern across seven fields — journalism, intelligence analysis, systematic reviews, superforecasting, adversarial collaboration, competitive intelligence, legal cross-examination:

### 5.1 Pre-Commitment to Resolution Criteria Before Evidence Collection

Every field that produces reliable truth-finding insists that the test be defined before results are seen. Law has rules of evidence. Cochrane has pre-registered protocols (PROSPERO). Adversarial collaboration has jointly designed tests. Superforecasters commit probabilities before outcomes.

**Current AI systems define success after retrieval**, which makes confirmation bias structurally inevitable. The fix: before any agent starts searching, the orchestrator commits the research question, inclusion criteria, and what evidence would change the conclusion.

### 5.2 Source Independence Tracking

Journalism's "two independent sources" rule requires that corroborating sources have no shared upstream origin. Two search results citing the same Reuters wire is not independent confirmation — it's echo. Current AI systems don't track source provenance. A lightweight source independence graph — tracking who cited whom and what common dataset underlies the claims — would catch false corroboration.

### 5.3 Grey Literature Sweep

Cochrane requires active pursuit of grey literature because publication bias means null-result studies are systematically absent from indexed sources. Studies with positive results are substantially more likely to be published (Dickersin, 1990, JAMA; Easterbrook et al., 1991, Lancet). An AI search limited to indexed, high-ranking content is biased by construction. A dedicated sub-agent targeting preprints, government reports, industry white papers, and minority-view outlets partially corrects this.

### 5.4 Key Assumptions Check

Intelligence analysis (ODNI Tradecraft Primer, 2009): before finalizing a conclusion, explicitly enumerate the 3-5 most load-bearing assumptions, assign each a confidence rating, and state "if this assumption is false, the conclusion changes as follows." This becomes part of the deliverable. Current AI research outputs bury assumptions in prose.

### 5.5 Pre-Mortem

Gary Klein (HBR, 2007): imagine the conclusion has already been reached and was badly wrong. Work backward to identify what could have caused that failure. Research on prospective hindsight (Mitchell et al., "Back to the Future: Temporal Perspective in the Explanation of Events," Journal of Behavioral Decision Making, 1989) found it increases correct failure identification by 30%. This is directly implementable as a synthesis step: after the draft, run a pre-mortem agent that assumes the main conclusions are wrong and explains why.

### 5.6 Calibrated Probability Over Verbal Hedges

Superforecasters assign explicit numerical probabilities and update incrementally (0.40 → 0.35, not "I'm less confident"). Their edge over intelligence analysts with classified access: 25-30% (Good Judgment Project). Current AI systems produce verbal hedges ("evidence suggests," "there is significant uncertainty") that are uncalibrated and unscoreable. Tagging claims with explicit confidence levels creates a scorable, auditable output.

### 5.7 Intra-Source Consistency Check

Legal cross-examination is most effective at exposing prior inconsistent statements, not at detecting deception through behavioral cues. Applied to research: a dedicated pass that checks whether a source's abstract matches its findings section, whether the conclusion follows from the stated methodology, and whether the author's current claim matches their prior published positions.

---

## 6. Multi-Agent Failure Modes (MAST Taxonomy)

The MAST taxonomy (arXiv:2503.13657, preprint, 2025) analyzed 1,600+ annotated traces across 7 MAS frameworks, identifying 14 failure modes in 3 categories. Most failures stem from poor system design, not model capability.

**Most relevant to research skills**:

| Failure Mode                     | Frequency | Mitigation                                                |
| -------------------------------- | --------- | --------------------------------------------------------- |
| Redundant step repetition        | 15.7%     | Detailed, non-overlapping sub-question specs              |
| Reasoning-action inconsistency   | 13.2%     | Structured output formats; separate reasoning from action |
| Failing to recognize completion  | 12.4%     | Explicit convergence criteria; hard iteration caps        |
| Disobeying task specifications   | 11.8%     | Tighter prompts; verification of output against spec      |
| Faulty verification logic        | 9.1%      | External verification (tool/retrieval) not self-check     |
| Absent/incomplete validation     | 8.2%      | Mandatory verification step before synthesis              |
| Task deviation/derailment        | 7.4%      | Problem Anchor copied into every round                    |
| Neglecting to seek clarification | 6.8%      | Explicit instruction to surface ambiguity                 |

---

## 7. ARIS-Specific Patterns Worth Capturing

### 7.1 Scoring Rubric (Research-Refine)

The only ARIS skill with a weighted rubric, sent verbatim to the reviewer:

| Dimension            | Weight |
| -------------------- | ------ |
| Problem Fidelity     | 15%    |
| Method Specificity   | 25%    |
| Contribution Quality | 25%    |
| Frontier Leverage    | 15%    |
| Feasibility          | 10%    |
| Validation Focus     | 5%     |
| Venue Readiness      | 5%     |

For dimensions scoring below 7: specific weakness, concrete fix, and priority (CRITICAL/IMPORTANT/MINOR). Also outputs Simplification Opportunities, Modernization Opportunities, and Drift Warning as structured fields.

### 7.2 Bidirectional Informativeness Filter

`idea-creator` applies an anti-filler criterion: "Not 'apply X to Y' unless the application reveals genuinely surprising insights." Ideas are filtered against "result wouldn't be interesting either way." This is the right filter for any research question — a great question is one where the answer matters regardless of direction.

### 7.3 Minimum Viable Fix per Weakness

The `auto-review-loop` prioritizes responses to reviewer concerns: metric additions > reframing > new experiments. This prevents over-engineering responses to feedback — the cheapest fix that addresses the weakness is preferred.

### 7.4 State Persistence for Crash Recovery

JSON state files (`REVIEW_STATE.json`) with current phase, scores, thread IDs, timestamps. If context compacts, the skill reads the state file and resumes. 24-hour staleness check prevents stale state from hijacking fresh runs. Fields: `{round, threadId, status, last_score, last_verdict, pending_experiments[], timestamp}`.

### 7.5 ARIS Gaps

1. No structured extraction schema (generic `| Paper | Venue | Method | Key Result |` table only)
2. No cross-session knowledge synthesis (each run is self-contained)
3. No reviewer calibration tracking (scores have no normalization across rounds)
4. No budget-aware strategy selection between depth and breadth
5. No meta-learning on recurring weaknesses across runs
6. No parallel multi-track research after filtering (everything converges to a single hypothesis)

---

## 8. Design Principles for an Incompressible Research Skill

Synthesizing across all seven research tracks, the minimal set of principles that cannot be removed without degrading quality:

1. **Decompose into orthogonal sub-questions, not personas.** Different agents get different questions, not different framings of the same question. Include at least one contrarian/adjacent track. This is the primary quality lever — invest effort here, not in iteration.

2. **Problem Anchor as immutable reference.** Frozen at the start, copied verbatim into every phase. Drift is a named concept that reviewers call out explicitly.

3. **Pre-commit resolution criteria before retrieval.** Before any agent starts searching, the orchestrator commits: what is the research question, what would a strong answer look like, and what evidence would change the conclusion. This is the most impactful pattern from adjacent fields (§5.1) — every discipline that produces reliable truth-finding (law, Cochrane, adversarial collaboration, superforecasting) insists the test be defined before results are seen.

4. **Breadth before depth.** Diverse search strategies across sub-questions. Each agent uses domain-native vocabulary, not just the user's original phrasing. Expand queries then squeeze findings.

5. **Synthesize, don't aggregate.** The orchestrator explicitly: (a) identifies points of agreement across agents and assesses how independent the agreement is (shared upstream sources = echo, not corroboration), (b) surfaces disagreements and explains why agents diverged, (c) looks for emergent patterns that no single agent identified — cross-domain analogies, implicit assumptions shared by all agents, gaps in the collective coverage. Contradictions are findings, not failures to be resolved.

6. **Review introduces external signal.** Every review round must bring new evidence (fresh retrieval, different perspective). Pure self-reflection is prohibited. Cooperative framing ("what's missing?"), not adversarial ("what's wrong?").

7. **Adaptive convergence with a hard cap.** Stop when both reviewers identify no new substantive gaps or corrections — the test is "did this round produce actionable feedback that would change the document?" The hard cap (3 rounds) is a safety net for non-convergence, not a target. Most reviews should converge in 1-2 rounds; reaching the cap signals a problem with the research, not a need for more rounds.

8. **Pre-mortem before delivery.** Assume the main conclusions are wrong — why might that be? Surface the 2-3 most plausible failure modes. State the key assumptions the conclusions depend on and what would change if each were false.

9. **Cite or flag.** Every factual claim has a source. If no source can be found, say so explicitly rather than fabricating. Unsupported claims are flagged, not silently stated.

10. **Let the model do the heavy lifting.** Specify the objective and quality criteria. Do not specify methodology, query formulation, or intermediate steps. Do not use persona prompting.

11. **Document what was not found.** Gaps, dead ends, and unresolvable questions are first-class outputs alongside findings.

---

## 9. Implications for the Skill Design

The research skill should:

- **Use the orchestrator-worker pattern** with 3-7 parallel sub-agents (model: sonnet for workers, the calling model for orchestration)
- **Decompose by sub-question**, not by persona. Include a contrarian/adjacent track
- **Present the decomposition before spawning** unless the user explicitly requested autonomy
- **Freeze a Problem Anchor** at the start (research question, verbatim, copied into every phase)
- **Pre-commit resolution criteria**: before spawning agents, state what a strong answer looks like and what evidence would change the conclusion — this prevents confirmation bias structurally
- **Each agent gets**: the Problem Anchor, its specific sub-question, search strategy guidance, instruction to cite sources and flag unsupported claims
- **Synthesize with explicit cross-agent analysis**: (a) map agreement and assess source independence (echo vs. corroboration), (b) surface and explain disagreements, (c) identify emergent patterns no single agent found, (d) assess evidence quality per claim
- **Run a pre-mortem** on the draft — assume conclusions are wrong, explain why, state key assumptions
- **Review with 2 independent reviewers** in parallel, each with a different lens (accuracy/gaps vs. synthesis quality/non-obvious angles)
- **Adaptive convergence**: stop when both reviewers find no new substantive feedback; hard cap at 3 rounds as safety net
- **Review rounds must introduce external signal** — fresh searches, not just re-reading
- **Output includes**: the Problem Anchor, references with URLs, gaps/uncertainties, key assumptions
- **Structure follows content**, not a rigid template

What the skill should NOT do:

- Use expert persona prompting
- Force adversarial debate between agents
- Iterate past convergence
- Specify how agents should search (let the model decide)
- Use temperature for diversity
- Self-refine without external signal

---

## References

### Multi-Agent Research Systems

- Anthropic: "How we built our multi-agent research system" — <https://www.anthropic.com/engineering/multi-agent-research-system>
- STORM (Stanford, NAACL 2024) — <https://arxiv.org/abs/2402.14207>
- Co-STORM (EMNLP 2024) — <https://arxiv.org/abs/2408.15232>
- AutoSurvey (NeurIPS 2024) — <https://arxiv.org/abs/2406.10252>
- Agentic AutoSurvey — <https://arxiv.org/abs/2509.18661>
- AI Scientist (Sakana AI) — <https://sakana.ai/ai-scientist/>
- AI Scientist v2 — <https://arxiv.org/abs/2504.08066>
- AI Scientist evaluation — <https://arxiv.org/abs/2502.14297>
- AgentReview (EMNLP 2024) — <https://arxiv.org/abs/2406.12708>
- ResearchAgent (NAACL 2025) — <https://arxiv.org/abs/2404.07738>
- Agent Laboratory — <https://arxiv.org/abs/2501.04227>
- AgentRxiv — <https://arxiv.org/abs/2503.18102>
- SciAgents (MIT) — <https://arxiv.org/abs/2409.05556>
- Virtual Lab (Stanford/Nature 2025) — <https://www.nature.com/articles/s41586-025-09442-9>
- CoScientist (Nature 2023) — <https://www.nature.com/articles/s41586-023-06792-0>

### Multi-Agent Failure Modes

- MAST Taxonomy (preprint, 2025) — <https://arxiv.org/abs/2503.13657>
- "Increasing Intelligence Can Worsen Collective Outcomes" — <https://arxiv.org/abs/2603.12129>

### Debate, Review, and Convergence

- AI Safety via Debate (Irving et al.) — <https://arxiv.org/abs/1805.00899>
- Doubly-Efficient Debate — <https://arxiv.org/abs/2311.14125>
- Scalable oversight with weak LLMs judging strong — <https://arxiv.org/abs/2407.04622>
- Multi-agent debate for factuality (Du et al.) — <https://arxiv.org/abs/2305.14325>
- MAD: Divergent thinking through debate (Liang et al.) — <https://arxiv.org/abs/2305.19118>
- ColMAD: Cooperative multi-agent debate — <https://arxiv.org/abs/2510.20963>
- "Can LLM Agents Really Debate?" — <https://arxiv.org/abs/2511.07784>
- ICLR 2025 MAD analysis — <https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/>
- DCI: Structured deliberation — <https://arxiv.org/abs/2603.11781>
- D3 Framework — <https://arxiv.org/abs/2410.04663>
- ECON: Bayesian Nash convergence — <https://arxiv.org/abs/2506.08292>

### Sycophancy and Bias

- Sycophancy in language models (Sharma et al.) — <https://arxiv.org/abs/2310.13548>
- DEBATE benchmark: LLM opinion convergence — <https://arxiv.org/abs/2510.25110>
- Identity bias in multi-agent debate — <https://arxiv.org/abs/2510.07517>
- Fallacious argument vulnerability — <https://arxiv.org/abs/2502.19098>
- ConfMAD: Confidence signaling — <https://arxiv.org/abs/2509.14034>
- Self-preference bias in LLMs — <https://arxiv.org/abs/2404.13076>
- LLM positivity bias in strategic analysis — <https://medium.com/@terrysweetser_90287/llm-positivity-bias-in-strategic-analysis>

### Self-Refinement

- Self-Refine (Madaan et al.) — <https://arxiv.org/abs/2303.17651>
- EVOLVE: Challenging Self-Refine — <https://arxiv.org/abs/2502.05605>
- Accuracy-Correction Paradox — <https://arxiv.org/abs/2601.00828>
- CRITIC: External tool feedback — <https://arxiv.org/abs/2305.11738>
- SCoRe: RL-based self-correction — <https://arxiv.org/abs/2409.12917>
- CorrectBench — <https://arxiv.org/abs/2510.16062>

### Ensemble and Aggregation

- Mixture-of-Agents (Together AI) — <https://arxiv.org/abs/2406.04692>
- Self-MoA revision — <https://arxiv.org/abs/2502.00674>
- LLM-Blender — <https://arxiv.org/abs/2306.02561>
- DyLAN — <https://arxiv.org/abs/2310.02170>
- LLM ensemble forecasting — <https://arxiv.org/abs/2402.19379>

### Prompt Engineering and Accuracy

- Chain-of-Verification (CoVe) — <https://aclanthology.org/2024.findings-acl.212/>
- Self-Consistency (CISC revision) — <https://aclanthology.org/2025.findings-acl.1030.pdf>
- Breadth vs. depth — <https://arxiv.org/html/2502.10858v1>
- Diverse search query formulation — <https://arxiv.org/html/2508.05668v3>
- Hybrid RAG citation accuracy — <https://arxiv.org/abs/2512.12117>
- Expert persona prompting debunked (Mollick) — <https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/>
- CoT for reasoning models (Mollick) — <https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/>
- Temperature vs. accuracy — <https://aclanthology.org/2024.findings-emnlp.432>
- Optimal specification level — <https://arxiv.org/abs/2505.13360>

### Structured Analytic Techniques

- Heuer, R. J. (1999). *Psychology of Intelligence Analysis*. CIA Center for the Study of Intelligence
- ACH empirical limitations (Dhami 2019) — <https://onlinelibrary.wiley.com/doi/full/10.1002/acp.3550>
- ODNI Tradecraft Primer (2009) — <https://www.stat.berkeley.edu/~aldous/157/Papers/Tradecraft%20Primer-apr09.pdf>
- Dalkey, N. & Helmer, O. (1963). "An Experimental Application of the Delphi Method." *Management Science* 9(3)
- Scalable Delphi (LLM agents) — <https://arxiv.org/html/2602.08889>
- HAH-Delphi (Human-AI Hybrid) — <https://arxiv.org/html/2508.09349v1>
- DelphiAgent fact verification — <https://www.sciencedirect.com/science/article/abs/pii/S0306457325001827>
- PRISMA 2020 Statement — <https://pmc.ncbi.nlm.nih.gov/articles/PMC8007028/>
- Pre-mortem (Klein, HBR 2007) — <https://hbr.org/2007/09/performing-a-project-premortem>
- Mitchell et al. (1989). "Back to the Future: Temporal Perspective in the Explanation of Events." *Journal of Behavioral Decision Making* 2(1)
- Tetlock, P. E. & Gardner, D. (2015). *Superforecasting: The Art and Science of Prediction*. Crown

### Adjacent Fields

- Story-Based Inquiry (journalism) — <https://www.storybasedinquiry.com/story-based-inquiry-method>
- Kahneman, D. (2003). "A Perspective on Judgment and Choice: Mapping Bounded Rationality." *American Psychologist* 58(9)
- Competitive Intelligence — <https://www.competitiveintelligencealliance.io/competitive-intelligence-complete-guide/>
- Pozner, L. S. & Dodd, R. J. (2004). *Cross-Examination: Science and Techniques*. LexisNexis
- Grey literature in systematic reviews — <https://pubmed.ncbi.nlm.nih.gov/28857505/>
- Dickersin, K. (1990). "The Existence of Publication Bias and Risk Factors for Its Occurrence." *JAMA* 263(10)
- Easterbrook, P. J. et al. (1991). "Publication Bias in Clinical Research." *Lancet* 337(8746)

### ARIS

- ARIS repository — <https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep>
- Key files: skills/{research-pipeline,auto-review-loop,research-review,research-refine,idea-discovery,research-lit,novelty-check,idea-creator,experiment-plan,dse-loop}/SKILL.md
