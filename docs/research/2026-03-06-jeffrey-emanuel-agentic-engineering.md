# Jeffrey Emanuel — Agentic Engineering Research

**Date:** 2026-03-06 **Source:** <https://jeffreyemanuel.com/> **Focus:** Agentic engineering theses and how they relate to TAD's `/impl` workflow

---

## Who He Is

- Math degree (Reed College), ~13 years as long/short equity analyst at major hedge funds (Millennium, Balyasny, Scoggin, etc.)
- Now Founder/CEO of Lumera Network (Cosmos L1), but primary activity is AI automation consulting for PE/hedge funds and building agentic tooling
- 90+ open-source repos, 16K+ GitHub stars (`github.com/Dicklesworthstone`), 29K followers on X (`@doodlestein`)
- Creator of the "Agentic Coding Tooling Flywheel" — 14 interconnected tools for multi-agent coordination
- Gained attention when his 12K-word "Short Case for Nvidia" essay went viral during the DeepSeek disruption (Jan 2025)

---

## Key Theses

### 1. The Overprompting Trap — "Get Out of the Model's Way"

His central mental model for working with LLMs:

- **Planning phase -> stay open.** Give high-level goals and purpose. Minimize constraints. The model's strategic ability exceeds human direction once objectives are clear.
- **Execution phase -> be precise.** Break the plan into ultra-specific tasks so implementing agents can focus narrowly, "like a short-order cook in a diner."
- **The chef analogy:** Hiring a world-class chef then constraining every ingredient is like "a ninja acrobat dancing around laser beams" — technically compliant, artistically compromised.

**Core claim:** Every word in a prompt consumes attention and narrows solution space. Over-constraining during planning degrades quality.

### 2. Separate Cognition Across Phases

From his Claude Code article on complex refactors:

- Have two different models (e.g., Opus + GPT) independently generate refactoring plans
- Run dialectical refinement: each critiques the other's plan, repeat 2-3 rounds until convergence
- Execute in a fresh session referencing the finalized plan — never let context compaction corrupt it
- If stuck, switch models — the competitor picks up using documented progress

**Core claim:** Planning and execution are different cognitive tasks. Mixing them wastes capability. Token expenditure on planning is an investment, not waste.

### 3. Multi-Model Dialectics Beat Single-Model Monologues

His LLM Coding Tournament pits 4 models against each other across 5+ rounds:

- Round 0: independent solutions. Rounds 1-5: each reviews all prior solutions and synthesizes
- Cross-pollination breaks local optima. Collective output consistently exceeds any individual model
- Generalizes beyond code to medical diagnostics, legal drafting, financial modeling

### 4. The Future Is Agent Fleets — the "Agentic Coding Flywheel"

14 interconnected open-source tools for multi-agent coordination:

| Tool                        | Purpose                                               |
| :-------------------------- | :---------------------------------------------------- |
| MCP Agent Mail (1.6K stars) | "Gmail for agents" — threaded messaging + file leases |
| Beads Viewer (1.2K stars)   | DAG-based task visualization with dependency planning |
| CASS                        | Unified search across 11+ agent session formats       |
| CASS Memory System          | Three-layer memory: procedural, episodic, semantic    |
| Destructive Command Guard   | Blocks `rm -rf`, `git reset --hard`, etc.             |
| Simultaneous Launch Button  | Two-person cryptographic approval for dangerous ops   |
| Agentic Flywheel Setup (1K) | One-command VPS bootstrap: 3 agents + 30 tools        |

**Flywheel concept:** Each tool amplifies the others. The premise is coordinated agent fleets, not solo agents.

### 5. Safety Is an External Problem

- Internal safety mechanisms are fragile — trivially disabled
- Solution: external governance modeled on criminal justice — a "Congress of Helper Models" monitors the primary agent
- Practical implementations: Destructive Command Guard, Simultaneous Launch Button, ACIP prompt injection framework

### 6. Compress Context, Don't Cram It

Consistently advocates pre-processing information into optimized formats before feeding to models. Cramming raw data degrades performance even when it fits. For brownfield codebases: compress into interface specs, omit implementation details.

### 7. AI as Co-Researcher, Not Just Tool

His "11 Ways to Break the Transformer" article: asked a model how to improve attention, it generated an 11-framework research agenda spanning Lie groups, tropical geometry, etc. — then wrote JAX kernels to validate. The human's role shifts to curation and direction-setting.

---

## Cross-Cutting Pattern

Almost everything reduces to one principle: **the bottleneck is no longer capability — it's orchestration.** Returns come from:

1. Knowing when to constrain vs. when to liberate the model
2. Coordinating multiple models/agents with shared memory and communication
3. Building external safety infrastructure rather than relying on internal alignment
4. Compressing and structuring context before analysis

His hedge fund background is visible: the multi-model dialectic mirrors investment committees (independent analysis -> structured debate -> convergence). External safety mirrors how funds manage trader risk — not by trusting self-limits, but via independent risk teams with kill switches.

---

## Relevance to TAD's `/impl` Skill

### What We Already Cover

| Emanuel's Pattern                        | TAD Workflow                          |
| :--------------------------------------- | :------------------------------------ |
| Separate planning from execution         | `/write-story` -> `/play-story` split |
| Divergent multi-model generation         | `/impl` Phase 1 (Opus + Codex)        |
| Comparative review + hybrid spec         | `/impl` Phase 2                       |
| Synthesis from hybrid spec               | `/impl` Phase 3                       |
| Fresh session to avoid context pollution | `/play-story` starts fresh            |

### Gaps Identified

## 1. No Dialectical Planning Phase (High Value)

`/impl` goes: understand spec -> both models implement -> compare code -> synthesize. Emanuel's insight: have models plan independently first, critique each other's plans, converge, *then* implement.

Proposed Phase 0.5 between Step 0 and Phase 1:

1. Both models read spec and produce an implementation approach (module structure, signatures, edge case strategy, test plan — not code)
2. Orchestrator compares approaches, writes a converged plan
3. Both models in Phase 1 implement from converged plan (not directly from spec)

Cost: one extra round of model calls. Payoff: implementations start from stronger plan, Phase 2 review is tighter because differences are genuine design disagreements rather than spec interpretation drift.

**2. Overprompting in `/write-story` specs (small, principled)**

`/write-story` includes an `#### Implementation plan` with concrete steps. Good for `/play-story` (single agent, needs guidance), but constrains `/impl`'s divergent models before they've thought independently.

Fix: add to `/impl` Step 0 that when a spec has an implementation plan, treat it as **context, not constraint** — both models should deviate if they find a better approach.

### What to Skip

- Multi-round tournaments (5+ rounds): `/impl`'s 3 phases capture 80% of value
- External safety congress: overkill for solo dev; `just check` + TDD is right level

---

## Reading List

**Must read:**

- "The Overprompting Trap" — <https://jeffreyemanuel.com/writing/overprompting>

**Skim-worthy:**

- "Making Complex Code Changes with Claude Code" — <https://jeffreyemanuel.com/writing/making_complex_code_changes_with_cc>

---

## Full Article Index (For Reference)

| Title                                                                  | URL                                                       | Category              |
| :--------------------------------------------------------------------- | :-------------------------------------------------------- | :-------------------- |
| The Overprompting Trap                                                 | /writing/overprompting                                    | AI & Prompting        |
| My Favorite Statistical Measure: Hoeffding's D                         | /writing/hoeffdings_d_explainer                           | Statistics            |
| Factor Risk Models and the Hedge Fund Business                         | /writing/barra-factor-model                               | Investing             |
| Building a Brain, Not a Calculator: Bio-Inspired Nanochat Architecture | /writing/bio_inspired_architecture                        | Frontier Research     |
| 11 Ways to Break the Transformer                                       | /writing/model_guided_math                                | Frontier Research     |
| Lamport's Bakery Algorithm                                             | /writing/bakery_algorithm                                 | Algorithms            |
| LLM Introspective Compression                                          | /writing/llm_introspective_compression                    | AI Research           |
| Multi-Round LLM Coding Tournament                                      | /writing/llm_multi_round_coding_tournament                | AI Research           |
| Making Complex Code Changes with Claude Code                           | /writing/making_complex_code_changes_with_cc              | Dev Workflow          |
| RaptorQ: The Black Magic of Liquid Data                                | /writing/raptorq                                          | Algorithms            |
| Protecting Against AI Prompt Injection                                 | /writing/protecting_against_prompt_injection              | Security              |
| Dr. GPT: Empowering Your Healthcare Decisions                          | /writing/dr_gpt_empowering_your_healthcare_with_ai        | Healthcare & AI       |
| TaxGPT: Using AI for Tax Prep                                          | /writing/tax_gpt_using_ai_for_tax_prep                    | Utility               |
| The Incredible Magic of CMA-ES                                         | /writing/cmaes_explainer                                  | Algorithms            |
| Engineering the Mindmap Generator                                      | /writing/making_of_the_mindmap_generator                  | Software Architecture |
| PPP Loan Fraud: A Data Science Detective Story                         | /writing/ppp_loan_fraud_analysis                          | Data Science          |
| The Short Case for Nvidia Stock                                        | /writing/the_short_case_for_nvda                          | Markets & AI          |
| The Most Impressive Prediction of All Time                             | /writing/the_most_impressive_prediction_of_all_time       | History & Science     |
| Building the Python Backend for YTO                                    | /writing/what_i_learned_making_the_python_backend_for_yto | Engineering           |
| Some Thoughts on AI Alignment                                          | /writing/some_thoughts_on_ai_alignment                    | AI Safety             |
| The Lessons of Hermann Grassmann                                       | /writing/hermann_grassmann_nature_of_abstractions         | History of Math       |
