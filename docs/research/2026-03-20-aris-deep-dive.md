# ARIS Deep Dive

**Status:** done — core patterns adopted into /research, /review-loop, /cross-pollinate skills; finance-specific integration plan (§5) parked in ideas backlog

Deep analysis of [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) (Auto-Research-In-Sleep, 2.7k stars) — a collection of plain-Markdown skill files for autonomous ML research with Claude Code. Conducted by reading every skill file, MCP server, and tool in the repo.

## 1. Architecture & Mechanics

### How It Works

ARIS is a **methodology, not a platform** — zero dependencies, zero lock-in. Every skill is a single `SKILL.md` file with YAML frontmatter. No code to install, no database, no Docker. Skills are invoked as slash commands and chain together via file-based state.

Four workflows compose into a full research pipeline:

| Workflow                | Skill                | What It Does                                                                                                                 |
| ----------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 1 — Idea Discovery      | `/idea-discovery`    | Literature survey → brainstorm 8-12 ideas → novelty check → GPU pilots → rank → refine top idea → plan experiments           |
| 1.5 — Experiment Bridge | `/experiment-bridge` | Parse experiment plan → implement code → cross-model code review → sanity check → deploy to GPU → collect results            |
| 2 — Auto Review Loop    | `/auto-review-loop`  | External LLM reviews paper → identifies weaknesses → Claude fixes & runs experiments → repeat until score ≥ 6/10 or 4 rounds |
| 3 — Paper Writing       | `/paper-writing`     | Narrative report → outline → figures → LaTeX → PDF → 2-round auto-improvement                                                |

`/research-pipeline` chains all four end-to-end. The design is "sleep and wake up to results" — launch stages 1-2 in the evening, start 3-4 before bed.

### Cross-Model Adversarial Review

The core architectural insight. Two LLMs with distinct roles:

- **Executor** (Claude Code): fast, fluid — writes code, deploys experiments, rewrites papers
- **Reviewer** (GPT-5.4 via Codex MCP): slower, rigorous — probes weaknesses the executor didn't anticipate

Rationale: self-play (one model reviewing itself) falls into local minima. Cross-model review is adversarial — the biggest gain is going from 1 model to 2, not from 2 to N. The reviewer gets **no tools** — it only sees the prompt context prepared by the executor.

Invocation: `mcp__codex__codex` for initial review, `mcp__codex__codex-reply` for follow-up in the same thread (maintains conversation context via `threadId`). Always uses `model_reasoning_effort: "xhigh"`.

Three MCP server variants support different reviewer backends:

- `claude-review` — uses Claude Code CLI as reviewer (for Codex-as-executor setups)
- `llm-chat` — generic OpenAI-compatible API adapter (DeepSeek, MiniMax, Kimi, GLM, etc.)
- `minimax-chat` — dedicated MiniMax adapter

### State Persistence

All state lives in project files (JSON + Markdown):

| File                                | Purpose                                                                  |
| ----------------------------------- | ------------------------------------------------------------------------ |
| `REVIEW_STATE.json`                 | Auto-review loop progress (round, scores, threadId, pending experiments) |
| `AUTO_REVIEW.md`                    | Cumulative review log with verbatim responses                            |
| `IDEA_REPORT.md`                    | Ranked ideas with pilot results                                          |
| `refine-logs/FINAL_PROPOSAL.md`     | Refined method proposal                                                  |
| `refine-logs/EXPERIMENT_PLAN.md`    | Experiment roadmap                                                       |
| `refine-logs/EXPERIMENT_TRACKER.md` | Experiment status tracking                                               |
| `PAPER_PLAN.md`                     | Paper outline + claims-evidence matrix                                   |
| `GRANT_STATE.json`                  | Grant proposal crash recovery state                                      |
| `DSE_STATE.json`                    | Design space exploration crash recovery                                  |

If Claude Code's context window fills up and auto-compacts, the workflow reads the state file and resumes — no human intervention needed. 24-hour staleness check prevents stale state from hijacking fresh runs.

### Auto-Review Loop ("Ralph Loops")

The iterative review mechanism that gives ARIS its name:

1. External LLM (GPT-5.4 xhigh) reviews the current state as a NeurIPS/ICML reviewer
2. Parses score, verdict, action items; saves full raw response verbatim
3. Optional human checkpoint (present score + weaknesses, wait for approval)
4. Claude implements fixes — prioritizes cheap/high-impact: metric additions > reframing > new experiments
5. Waits for experiment results if needed
6. Documents round, writes state file
7. Resubmits for review. Repeat until score ≥ 6/10 or MAX_ROUNDS (4)

Safety: experiments >4 GPU-hours are skipped (flagged for manual follow-up). Explicit rule: "Do NOT hide weaknesses to game a positive score." Real-world result: 5/10 → 7.5/10 over 4 rounds, running 20+ GPU experiments autonomously overnight.

### Autonomous Multi-Session Execution

- **State files** for resumption across sessions and context compaction
- **Permission auto-allow**: `.claude/settings.local.json` pre-approves MCP tools and Write/Edit to avoid permission prompts overnight
- **Screen sessions**: GPU experiments run in `screen` on remote servers, monitored asynchronously
- **Async review jobs**: `claude-review` MCP server supports `review_start` + `review_status` polling for long reviews

### Skill File Format

Standard Claude Code skill format — YAML frontmatter (`name`, `description`) followed by Markdown body. No custom schema beyond what Claude Code natively supports. Skills invoke each other via `/skill-name` syntax. Parameters pass down the call chain via `-- key: value` inline overrides.

## 2. Skill Inventory

### Core Research Pipeline (Domain-Agnostic)

| Skill                      | Purpose                                                                       | Reusable for Tad?    |
| -------------------------- | ----------------------------------------------------------------------------- | -------------------- |
| `research-pipeline`        | End-to-end orchestrator (idea discovery → implementation → review → paper)    | Adapt                |
| `research-lit`             | Multi-source literature search (Zotero → Obsidian → local PDFs → web → arXiv) | **Direct reuse**     |
| `idea-creator`             | Brainstorm 8-12 ideas, filter by feasibility, run GPU pilots, rank            | Adapt                |
| `idea-discovery`           | Workflow 1 orchestrator (lit → ideas → novelty → review → refine)             | Adapt                |
| `novelty-check`            | Verify research idea hasn't been published (multi-source + cross-model)       | **Direct reuse**     |
| `research-review`          | Deep critical review via external LLM as NeurIPS/ICML reviewer                | Adapt                |
| `research-refine`          | Iterative proposal refinement with Problem Anchor and cross-model review      | Adapt                |
| `research-refine-pipeline` | Chains research-refine + experiment-plan                                      | Skip                 |
| `experiment-plan`          | Turn proposal into claim-driven experiment roadmap                            | Adapt                |
| `experiment-bridge`        | Implement experiment code, cross-model code review, deploy                    | Skip (no GPUs)       |
| `run-experiment`           | Deploy ML experiments on local/remote GPU                                     | Skip (no GPUs)       |
| `monitor-experiment`       | Monitor running experiments, collect results                                  | Skip (no GPUs)       |
| `analyze-results`          | Analyze experiment results, generate comparison tables                        | Adapt                |
| `auto-review-loop`         | Multi-round adversarial review loop (score ≥ 6/10 or 4 rounds)                | **Pattern to steal** |
| `auto-review-loop-llm`     | Same but with any OpenAI-compatible API                                       | **Pattern to steal** |
| `arxiv`                    | Search, download, summarize arXiv papers                                      | **Direct reuse**     |
| `comm-lit-review`          | Communications-domain literature review (IEEE venues)                         | Fork for finance     |
| `formula-derivation`       | Derive and verify research formulas                                           | Skip                 |
| `dse-loop`                 | Design space exploration (parameter sweep with crash recovery)                | **Pattern to steal** |

### Paper Production (Domain-Agnostic, Not Needed for Tad)

| Skill                         | Purpose                                                       |
| ----------------------------- | ------------------------------------------------------------- |
| `paper-plan`                  | Generate paper outline from narrative report                  |
| `paper-write`                 | Draft LaTeX paper section-by-section                          |
| `paper-writing`               | Orchestrator (plan → figures → write → compile → improve)     |
| `paper-figure`                | Generate matplotlib/seaborn plots and LaTeX tables            |
| `paper-illustration`          | AI-generated architecture diagrams (Claude → Gemini pipeline) |
| `paper-compile`               | Compile LaTeX with auto error fixing                          |
| `paper-poster`                | Generate conference poster (LaTeX + PPTX + SVG)               |
| `paper-slides`                | Generate presentation slides with speaker notes               |
| `auto-paper-improvement-loop` | 2-round writing quality improvement                           |
| `proof-writer`                | Rigorous mathematical proofs                                  |
| `mermaid-diagram`             | Generate Mermaid diagrams with visual review                  |

### Utility / Domain-Specific

| Skill                  | Purpose                                           |
| ---------------------- | ------------------------------------------------- |
| `grant-proposal`       | Draft grant proposals (8+ funding agencies)       |
| `idea-discovery-robot` | Robotics-specific fork of idea-discovery          |
| `feishu-notify`        | Feishu/Lark notifications (Chinese messaging app) |
| `pixel-art`            | Pixel art SVG illustrations                       |

### MCP Servers

| Server          | Purpose                                                                   |
| --------------- | ------------------------------------------------------------------------- |
| `claude-review` | Bridge: Codex executor ↔ Claude CLI reviewer (async job support)          |
| `llm-chat`      | Generic OpenAI-compatible API adapter for any reviewer LLM                |
| `minimax-chat`  | Dedicated MiniMax API adapter                                             |
| `feishu-bridge` | HTTP server for bidirectional Feishu messaging (not MCP, standalone HTTP) |

### Tools

| Tool                                        | Purpose                                                     |
| ------------------------------------------- | ----------------------------------------------------------- |
| `arxiv_fetch.py`                            | CLI helper: search arXiv API, download PDFs                 |
| `generate_codex_claude_review_overrides.py` | Code generator: rewrite Codex skills to use Claude reviewer |

## 3. Patterns to Steal

### 3.1 Problem Anchor / Invariant Object

Several skills freeze a core constraint at the start and carry it through every iteration to prevent drift. `research-refine` freezes a "Problem Anchor" (immutable problem statement copied verbatim into every round). `formula-derivation` selects an "invariant object" (the single quantity organizing the derivation). `experiment-plan` freezes claims.

**For Tad**: Every research hypothesis should have a frozen "hypothesis anchor" — the specific testable claim that doesn't drift through iterative refinement. E.g., "5-day reversal signal conditioned on VIX regime produces >1.5 Sharpe in S&P 500 2010-2024."

### 3.2 Cross-Model Adversarial Review

Claude does the work, a second model critiques. Always at maximum reasoning effort. Thread persistence enables multi-round dialogue. The reviewer gets no tools — only prepared context.

**For Tad**: Use this for strategy hypothesis review. Claude generates the hypothesis + backtest, a second model plays devil's advocate (data mining bias? survivorship? regime sensitivity? capacity?). Tad doesn't need the Codex MCP — can use Claude's native agent teams with different model tiers (Opus generates, Sonnet critiques, or vice versa).

### 3.3 Score-Gated Acceptance Loops

Skills iterate until a quality threshold is met (auto-review-loop: score ≥ 6/10, paper-illustration: score ≥ 9/10, mermaid-diagram: score ≥ 9/10). Each uses structured scoring rubrics where specific failures cap the maximum score.

**For Tad**: Research outputs (literature syntheses, strategy hypotheses, backtest analyses) could use a similar quality gate — generate, score against criteria, revise until acceptable. Scoring criteria for a strategy hypothesis: statistical significance, economic rationale, regime robustness, data snooping risk, capacity.

### 3.4 Crash-Resilient State Files

Long-running skills write JSON state files (`REVIEW_STATE.json`, `GRANT_STATE.json`, `DSE_STATE.json`) with current phase, scores, thread IDs, timestamps. If context compacts, the skill reads the state file and resumes. 24-hour staleness check prevents stale state from hijacking fresh runs.

**For Tad**: Any multi-step research workflow (lit survey → hypothesis generation → backtest → analysis) should persist state to a JSON file so it survives context compaction. This is the key enabler for overnight autonomous runs.

### 3.5 Budget-Constrained Autonomy

Explicit compute budgets (PILOT_MAX_HOURS=2, MAX_TOTAL_GPU_HOURS=8, TIMEOUT), patience counters, and maximum iteration caps prevent runaway resource consumption. Experiments >4 GPU-hours are skipped and flagged.

**For Tad**: Not GPU-hours, but API-call budgets and wall-clock timeouts. A literature survey shouldn't make 500 web searches. A backtest loop shouldn't run for 8 hours. Define explicit caps.

### 3.6 Graceful Degradation

Skills check for optional integrations (Zotero MCP, Obsidian MCP, W&B, Feishu, `arxiv_fetch.py`) and silently skip if unavailable. Zero-impact guarantee — every skill works with zero config.

**For Tad**: Skills should check for optional MCP servers (ScholarMCP, arxiv-mcp-server, Exa) and fall back to WebSearch if unavailable. The happy path uses specialized tools; the fallback path still works.

### 3.7 Checkpoint Gates (AUTO_PROCEED)

Human-in-the-loop checkpoints at key decision points, controlled by a constant. When true, auto-selects the best option; when false, waits for user input. Each checkpoint presents a summary and options (approve / override / skip / stop).

**For Tad**: Default to AUTO_PROCEED=false for strategy decisions (committing capital is irreversible). For pure research (literature review, hypothesis generation), AUTO_PROCEED=true is fine.

### 3.8 Kill Early, Document Dead Ends

Eliminated ideas, failed pilots, and negative results are documented as valuable outputs. "Dead ends are just as valuable as successes." The `novelty-check` skill has three verdicts: PROCEED / PROCEED WITH CAUTION / ABANDON.

**For Tad**: Critical for quant research. A strategy that doesn't work is valuable information — it narrows the search space. Document why it failed, what was tested, what the data showed.

### 3.9 Domain Specialization via Fork

`idea-discovery-robot` is a domain-specific fork of `idea-discovery` with robotics constraints overlaid. `comm-lit-review` forks `research-lit` with communications venue tiering. Both preserve the base structure while adding domain-specific filtering, grouping, and evaluation criteria.

**For Tad**: Fork `research-lit` into a finance-specific variant with venue tiering (Journal of Finance, RFS, JFE, JFQA as Tier A; working papers from top-20 finance departments as Tier B; SSRN/arXiv q-fin as Tier C), domain-specific grouping axes (by factor family, holding period, universe, regime), and finance-specific synthesis patterns.

### 3.10 Large File Handling Fallback

Every writing-heavy skill includes: "If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`)." This is a practical workaround for Claude Code's file size limits.

**For Tad**: Already handled by our skill system, but good to have as an explicit rule in writing-heavy skills.

## 4. Applicability to Tad

### Mapping ARIS to Tad's Needs

| ARIS Capability                     | Tad Need                                | Fit        | Notes                                                       |
| ----------------------------------- | --------------------------------------- | ---------- | ----------------------------------------------------------- |
| Literature search (`research-lit`)  | Literature review for strategy research | **Direct** | Fork with finance venues, add SSRN/NBER search              |
| Idea brainstorming (`idea-creator`) | Strategy hypothesis generation          | **Adapt**  | Replace "research idea" framing with "strategy hypothesis"  |
| Novelty check                       | Prior art check for strategies          | **Direct** | Check if strategy is already well-known/crowded             |
| Cross-model review                  | Strategy review / red-teaming           | **Direct** | Devil's advocate for data mining, regime, capacity concerns |
| Auto-review loop                    | Iterative strategy refinement           | **Adapt**  | Score = backtest quality metrics, not paper score           |
| Experiment plan → run → analyze     | Backtest plan → run → analyze           | **Adapt**  | Replace GPU experiments with backtest runs                  |
| Problem Anchor                      | Hypothesis anchor                       | **Direct** | Prevents drift during iterative refinement                  |
| State persistence                   | Crash-resilient research sessions       | **Direct** | Same pattern, different state fields                        |
| Paper production pipeline           | N/A                                     | **Skip**   | Not publishing papers                                       |
| Grant proposal                      | N/A                                     | **Skip**   |                                                             |
| GPU deployment                      | N/A                                     | **Skip**   | Tad runs backtests locally, not on GPU clusters             |

### What's Missing from ARIS for Quant Finance

1. **Backtest integration**: ARIS runs ML experiments on GPUs. Tad needs to run backtests with its own pipeline (`just run`, Polars-based analysis). The experiment-plan/run/analyze chain needs to be replaced with a backtest-plan/run/analyze chain.

2. **Data snooping awareness**: ARIS doesn't worry about data mining bias — it's doing ML research. Quant finance research needs explicit guards: out-of-sample testing, multiple testing corrections, holdout periods, sensitivity to start/end dates.

3. **Finance-specific evaluation criteria**: ARIS scores research novelty and methodological rigor. Tad needs: Sharpe ratio, max drawdown, capacity, turnover, transaction costs, regime sensitivity, correlation with known factors.

4. **Market microstructure awareness**: Execution feasibility, slippage, market impact — none of which exist in ARIS.

5. **Point-in-time data discipline**: No concept of look-ahead bias, survivorship bias, or point-in-time data in ARIS.

6. **Structured extraction schema**: ARIS extracts research ideas. Tad needs structured strategy extraction: signal definition, universe, holding period, reported Sharpe, conditioning variables, decay profile, data period (per the schema in the autonomous literature research doc).

### What Can Be Adopted as-Is

- `research-lit` base structure (multi-source search with graceful degradation)
- `novelty-check` workflow (multi-source + cross-model verification)
- `arxiv` skill (search/download/summarize)
- State persistence pattern (JSON state files with staleness check)
- Problem Anchor pattern
- Cross-model adversarial review pattern
- Score-gated acceptance loops
- Graceful degradation pattern
- Checkpoint gate pattern (AUTO_PROCEED)

### What Needs Adaptation

- Idea generation → strategy hypothesis generation (different framing, different evaluation criteria)
- Auto-review loop → strategy review loop (score = backtest metrics, not paper score)
- Experiment plan → backtest plan (different execution model)
- Domain-specific venue tiering for finance literature
- Finance-specific evaluation rubrics

## 5. Integration Plan

### Coexistence with Tad's Existing Skills

Tad has 12 skills in three groups:

- **Knowledge lenses** (5): `/tdd`, `/goos`, `/ddd`, `/software-design`, `/clean-code`
- **Task lifecycle** (5): `/define-task` → `/plan-task` → `/impl-task` → `/review-task` (+ `/create-task`)
- **Code health** (2): `/code-review`, `/kaizen`

ARIS-inspired research skills are a **new fourth group** that complements the existing system. They don't replace or conflict with any existing skills. The task lifecycle skills manage implementation work; research skills manage discovery work. They connect at the boundary: a research skill produces a finding, the user promotes it to a task via `/define-task`.

### Proposed Skill List for Tad's Research System

Ordered by implementation priority. Each skill is a single `SKILL.md` file — maximally incompressible, no unnecessary abstraction.

#### Phase 1 — Foundation (Immediate Value)

| Skill         | Responsibility                                                                                                                                                                                         | Key ARIS Source                                          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------- |
| `/lit-search` | Search for papers/articles across sources (arXiv, SSRN, Semantic Scholar, web). Download PDFs. Finance venue tiering. Graceful degradation (MCP servers → WebSearch fallback).                         | `research-lit`, `arxiv`, `comm-lit-review`               |
| `/lit-ingest` | Read a paper/article and extract structured data per the extraction schema (signal definition, universe, holding period, Sharpe, conditioning variables, etc.). Append to `docs/literature/_index.md`. | New (extraction schema from autonomous-lit-research doc) |

These two skills alone enable the core research loop: find papers, extract structured knowledge. Everything else builds on top.

#### Phase 2 — Autonomous Research

| Skill             | Responsibility                                                                                                                                                                                                        | Key ARIS Source                                    |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `/lit-survey`     | Multi-agent survey on a topic. Orchestrates: `/lit-search` across multiple query formulations → `/lit-ingest` for each paper → synthesis document. Problem Anchor pattern (frozen research question).                 | `idea-discovery`, `research-pipeline`              |
| `/lit-hypothesis` | Given literature findings, generate testable strategy hypotheses. Cross-model adversarial review (generate with one model, red-team with another for data mining, regime, capacity concerns). Score-gated acceptance. | `idea-creator`, `novelty-check`, `research-review` |

#### Phase 3 — Backtest-Driven Research (When Backtest Pipeline Is Mature)

| Skill               | Responsibility                                                                                                                                                                                     | Key ARIS Source                       |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `/lit-gap-analysis` | Cross-reference literature findings against Tad's implemented strategies. Identify gaps, validate assumptions, flag regime risks.                                                                  | `analyze-results`                     |
| `/strategy-review`  | Iterative strategy refinement loop. Score against finance-specific criteria (Sharpe, drawdown, capacity, data snooping risk). Cross-model devil's advocate. Loop until quality gate or max rounds. | `auto-review-loop`, `research-refine` |

#### Not Proposed (YAGNI)

- No paper production skills (not publishing)
- No GPU deployment skills (backtests are local)
- No grant proposal skills
- No notification skills (solo dev, no Feishu)
- No separate novelty-check skill (fold into `/lit-hypothesis` — one less skill to maintain)
- No orchestrator skill chaining everything end-to-end (premature — run skills manually until the workflow stabilizes, then consider automation)

### Design Principles for Tad Research Skills

Derived from ARIS patterns, filtered through Tad's CLAUDE.md principles:

1. **File-based state**: Research state lives in `docs/literature/` and `docs/research/`. No databases. JSON state files for crash recovery in long-running workflows.
2. **Problem Anchor**: Every research workflow freezes its core question at the start. The anchor is copied verbatim into every iteration.
3. **Graceful degradation**: Check for MCP servers, fall back to WebSearch. Skills work with zero config.
4. **Score-gated quality**: Research outputs must pass quality criteria before being accepted. Criteria are domain-specific (not paper scores — strategy evaluation metrics).
5. **Dead ends are outputs**: Failed hypotheses and negative findings are documented, not discarded.
6. **KISS**: Start with `/lit-search` and `/lit-ingest`. Add skills only when the previous ones are working and the need is clear. ARIS has 30+ skills because it serves a community with diverse needs. Tad is one person.
7. **No overnight autonomy yet**: ARIS's overnight autonomous execution is powerful but risky for a solo dev. Start with human-in-the-loop (AUTO_PROCEED=false at decision points). Move to autonomous execution only after the workflows are proven reliable.

### ARIS Patterns to Codify in CLAUDE.md (Not Skills)

Some ARIS patterns belong in project-level instructions rather than individual skills:

- **Extraction schema**: The per-paper extraction schema (signal definition, universe, holding period, etc.) belongs in CLAUDE.md or a reference file, not embedded in a skill.
- **Finance venue tiering**: A reference file (like ARIS's `venue-tiering.md`) listing finance journal/conference tiers, searchable by skills that need it.
- **Data snooping checklist**: A reference checklist for evaluating strategy hypotheses (out-of-sample? holdout period? multiple testing? regime sensitivity?), loadable by any skill that evaluates strategies.

## Sources

All analysis based on direct reading of the [ARIS repository](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) at commit HEAD as of 2026-03-20. Key files referenced:

- Core pipeline: `skills/{research-pipeline,research-lit,idea-creator,idea-discovery,novelty-check,research-review,research-refine,experiment-plan,experiment-bridge,run-experiment,monitor-experiment,analyze-results,auto-review-loop}/SKILL.md`
- Paper production: `skills/{paper-plan,paper-write,paper-writing,paper-figure,paper-illustration,paper-compile,paper-poster,paper-slides,auto-paper-improvement-loop,proof-writer}/SKILL.md`
- Domain forks: `skills/{comm-lit-review,idea-discovery-robot,dse-loop}/SKILL.md`
- Cross-model review: `skills/skills-codex-claude-review/{README,auto-review-loop,research-review,paper-write}/SKILL.md`
- MCP servers: `mcp-servers/{claude-review,llm-chat,minimax-chat,feishu-bridge}/server.py`
- Tools: `tools/{arxiv_fetch,generate_codex_claude_review_overrides}.py`
- Docs: `README.md`, `docs/{CODEX_CLAUDE_REVIEW_GUIDE,LLM_API_MIX_MATCH_GUIDE,NARRATIVE_REPORT_EXAMPLE,CURSOR_ADAPTATION}.md`
