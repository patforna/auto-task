# AI-Assisted SDLC Tools Landscape: 30-Tool Survey

Date: 2026-03-16

Research into 30 tools spanning spec-driven development frameworks, autonomous coding agents, AI IDEs, and multi-agent orchestration systems — evaluated against our current Claude Code + custom skills setup.

---

## Executive Summary

The AI-assisted development tooling space has exploded into a crowded landscape of 30+ tools, yet they all converge on the same fundamental workflow: **spec → plan → tasks → implement → verify**. The differentiation is in execution mechanics, not philosophy. After thorough research, the finding is that our current setup is structurally sound and already captures the load-bearing ideas. A small number of specific techniques from specific tools are worth adopting; the tools themselves are not.

**Three ideas that are genuinely load-bearing:**

1. **Fresh context per task** (Ralph Loop / GSD) — restart the agent for each task rather than accumulating state in one long session
2. **Structured context injection** (Agent OS / Kiro) — break CLAUDE.md into granular, scopeable files loaded contextually rather than all-at-once
3. **Multi-model plan diversity** (already in our dialectic planning) — the one technique that multiple independent tools converged on as a genuine quality multiplier

**Everything else is either already covered by our skills, adds overhead that exceeds its benefit for a solo dev, or solves coordination problems we don't have.**

---

## Tool Categories

### Category 1: Spec-Driven Development Frameworks

These tools formalise the "write a spec before coding" discipline into structured workflows with file artifacts.

| Tool        | Stars | Core Idea                                   | Solo Dev Fit                                                         |
| ----------- | ----: | ------------------------------------------- | -------------------------------------------------------------------- |
| Spec Kit    |   77k | Constitution → Spec → Plan → Tasks → Code   | Low — 10x slower than iterative prompting per Scott Logic benchmarks |
| OpenSpec    |   31k | Change-folder model (proposal/design/tasks) | Low — our skills cover the same phases with tighter integration      |
| BMAD Method |   41k | Multi-agent roles (PM/Architect/Dev)        | Low — team coordination overhead without a team                      |
| cc-sdd      |  2.9k | Kiro-style requirements → design → tasks    | Medium — EARS format requirements are interesting                    |
| SpecFlow    |    71 | Quality gates + multi-agent voting review   | Low — early stage, Claude Code-only, web-stack focused               |
| Agent OS    |  4.1k | Standards discovery + injection             | Medium — granular standards files are worth borrowing                |

**Key findings:**

- **Spec Kit** (GitHub, 77k stars) is the most widely known but independently benchmarked as 10x slower than iterative prompting for the same output quality (Scott Logic). Generated 2,577 lines of markdown to implement 689 lines of code. The Martin Fowler analysis found "AI agents frequently ignore instructions or generate duplicates" despite specs.

- **BMAD** (41k stars) simulates a full agile team with 21 agent personas. For a solo dev, you are simultaneously PM, Architect, Scrum Master, and Developer — running through all roles adds ceremony without coordination benefit.

- **cc-sdd** (2.9k stars) introduces **EARS-format requirements** (Easy Approach to Requirements Syntax: "WHEN trigger THEN response"). This structured format has empirical evidence of improving AI generation accuracy. One user reported 71 files with "virtually no rework."

- **Agent OS v3** (4.1k stars) deliberately removed orchestration, focusing purely on the context layer. Its `/discover-standards` command analyses your codebase and generates granular standards files. The insight: break your conventions into scopeable files rather than one monolithic prompt.

- **All SDD frameworks share a critical weakness:** spec update when requirements change mid-implementation. Spec Kit's Issue #1191 documents this; it's a known gap across the category.

**Convergent pattern:** every framework independently converged on "constitution/CLAUDE.md" as a persistent project rules file. We already have this.

---

### Category 2: Planning & Orchestration Systems

These tools focus on task decomposition, dependency tracking, and execution sequencing.

| Tool          |  Stars | Core Idea                                    | Solo Dev Fit                                                      |
| ------------- | -----: | -------------------------------------------- | ----------------------------------------------------------------- |
| Taskmaster AI |    26k | PRD → dependency-aware task graph            | Medium — `next` command is genuinely useful                       |
| GSD           |    23k | Fresh context per task + wave execution      | Medium — context isolation pattern is worth adopting              |
| Ralph Loop    | varies | Bash loop restarts agent per task (TDD gate) | Medium — fresh-context principle already captured by our workflow |

**Key findings:**

- **Taskmaster AI** (26k stars) is an MCP server with 36 tools that parses a PRD into a dependency DAG. The `next` command returns the highest-priority task with all dependencies satisfied. The `update-tasks --from=N` command rewrites only future tasks when implementation diverges. The 36-tool default payload costs ~21k tokens per request (configurable down to ~5k in core mode).

- **GSD v2** (23k stars) is the most execution-focused framework. Its core insight: **each task runs in a fresh context window** with only relevant files pre-loaded. This avoids "context rot" — the degradation of LLM output quality over long sessions. Tasks are grouped into dependency waves for parallel execution.

- **Ralph Loop** is a ~300 line bash script that restarts the agent for each task. TDD is the gate: the agent cannot commit until tests pass. Anthropic ships a first-party plugin. The core insight (fresh context per iteration) is architecturally sound; the full loop infrastructure is optional.

**The fresh-context principle** is the highest-signal finding in this category. Long sessions accumulate stale context that degrades output. Restarting the agent per task with only the relevant files loaded is a mechanical fix.

---

### Category 3: Autonomous Coding Agents

These are complete agent systems that take an issue or objective and produce code autonomously.

| Tool          | Stars | Core Idea                                      | Solo Dev Fit                                |
| ------------- | ----: | ---------------------------------------------- | ------------------------------------------- |
| OpenHands     |   69k | CodeAct: agent writes Python to control itself | Low — overlaps with Claude Code             |
| SWE-Agent     |   19k | Agent-Computer Interface (ACI)                 | Low — ideas worth knowing, tool redundant   |
| Devika        |   20k | Open-source Devin clone                        | Skip — effectively abandoned                |
| AutoDev       |  4.4k | Seven SDLC-phase agents                        | Low — Chinese community, immature           |
| Sweep AI      |     - | JetBrains PSI-based code agent                 | Low — pivoted from GitHub bot to IDE plugin |
| AutoCodeRover |  3.1k | AST-aware search + fault localisation          | Low — ideas worth knowing                   |

**Key findings:**

- **OpenHands** (69k stars, ICLR 2025) uses **CodeAct** — the agent writes executable Python as its action rather than JSON tool calls. This gives more flexibility for multi-step tool composition. SWE-bench score: 77.6%.

- **SWE-Agent** (19k stars, NeurIPS 2024) introduced the **Agent-Computer Interface (ACI)** principle: interfaces designed for LM agents matter as much as prompt engineering. Specific techniques: limit output verbosity, give explicit "no output = success" feedback, validate state eagerly (linter on every edit). The team subsequently showed that **100 lines of Python (mini-SWE-agent) matches the full system's performance** — elaborate scaffolding is unnecessary.

- **AutoCodeRover** (3.1k stars, ISSTA 2024) combines AST-aware code search with spectrum-based fault localisation: it uses test coverage data from failing vs. passing tests to score which lines are statistically most likely faulty before patching. Under $0.70 per issue.

- **Devika** (20k stars) is effectively abandoned — 138 open issues with no maintainer response, unpatched security vulnerabilities.

**The transferable insight** from this category is the ACI principle: when building tools or skills for agents, the interface design matters as much as the prompt. Limit verbosity, give explicit success feedback, validate eagerly.

---

### Category 4: AI IDEs

These are full IDE products with built-in AI agents and planning workflows.

| Tool             | Users | Core Idea                          | Solo Dev Fit                   |
| ---------------- | ----: | ---------------------------------- | ------------------------------ |
| Kiro (AWS)       |  beta | EARS-format specs + steering files | Medium — ideas worth borrowing |
| Windsurf/Cascade |   1M+ | Flow awareness + persistent memory | Low — IDE-specific advantages  |
| Cursor Plan Mode | large | Think-then-implement separation    | Low — our /plan-task does this |

**Key findings:**

- **Kiro** (AWS, beta) is the most structured: every feature flows through `requirements.md` (EARS format) → `design.md` → `tasks.md`, all committed to `.kiro/specs/`. **Steering files** (`.kiro/steering/`) use four loading modes: `Always`, `FileMatch` (only for matching file patterns), `Auto` (AI decides), `Manual` (invoked with `#name`). This granular scoping is more sophisticated than a single CLAUDE.md. **Agent Hooks** fire on file save, agent turn completion, etc. — enabling automatic test runs without manual prompting.

- **Windsurf** (1M+ users) has **flow awareness** — continuous real-time tracking of editor state (files opened, manual edits, terminal output). The **Memories** system auto-captures cross-session context during conversations. The docs acknowledge that memories are convenient but unreliable: "For knowledge you want Cascade to reliably reuse, write it as a Rule." **Planning Mode** runs two concurrent timelines: immediate actions + long-term plan, with the plan updating automatically.

- **Cursor Plan Mode** confirmed the "alignment ceremony" framing: the value is not the plan document itself but the forcing function of clear thinking. Plans that live in the IDE's home directory (not the repo) are a design weakness; our task files in the repo are structurally better.

**Transferable ideas:**

- Kiro's **steering file scoping** (load different instructions for different file types) is worth emulating — granular CLAUDE.md fragments loaded contextually
- Kiro's **event-driven hooks** (run tests on file save, auto-fix lint errors) could be approximated with `watchexec` in a CLI workflow
- Windsurf's **dual-timeline planning** (immediate action + persistent plan) is a useful mental model even without the IDE

---

### Category 5: Multi-Agent Frameworks

These are general-purpose frameworks for building multi-agent systems.

| Tool      | Stars | Core Idea                            | Solo Dev Fit                                     |
| --------- | ----: | ------------------------------------ | ------------------------------------------------ |
| LangGraph |  90k+ | Graph-based stateful agent workflows | Low — overkill for CLI workflows                 |
| CrewAI    |   46k | Role-based AI teams                  | Low — prompt engineering with orchestration glue |
| AutoGen   |   56k | Conversational multi-agent reasoning | Low — Microsoft deprecated active development    |

**Key findings:**

- All three frameworks add complexity for capabilities Claude Code's native sub-agent spawning already provides. They become relevant when building agentic **products** (not personal workflows) or when needing durable cross-session state.

- **AutoGen's MagenticOne** has the most sophisticated planning: an Orchestrator maintains a Task Ledger (facts, plan) and Progress Ledger (self-reflection), running an outer loop (replan when stuck) and inner loop (delegate subtasks). The ledger pattern is worth knowing as a mental model.

- **CrewAI** has a multi-agent **voting** pattern for code review — three agents at different temperatures, k=2 voting. Spec-Flow (SpecFlow) adopted this pattern.

- All three are **redundant** for a solo dev using Claude Code with sub-agents. The one scenario where they add value is scheduled autonomous pipelines that need to survive process crashes and resume from checkpoints — Dagu already covers this for our workflows.

---

### Category 6: Experimental / Research

These are academic or early-stage systems with novel ideas.

| Tool               | Stars | Core Idea                         | Solo Dev Fit                      |
| ------------------ | ----: | --------------------------------- | --------------------------------- |
| EvoGit             |  1.2k | Evolutionary code via Git graph   | Skip — research, not tooling      |
| EnvX               |     - | Repos as autonomous agents        | Skip — research, 52% success rate |
| Constitutional SDD |     - | Security rules embedded in specs  | Medium — principle worth adopting |
| Beads              |   19k | Dependency-aware agent task store | Low — Dolt overhead for solo dev  |

**Key findings:**

- **EvoGit** uses Git commits as the coordination medium between agents (stigmergic coordination). Novel idea but purely experimental.

- **Constitutional SDD** (arXiv, Jan 2026) embeds security rules in a machine-readable constitution with CWE references, enforcement levels, and implementation patterns. Result: 73% reduction in CWE violations. The **selective injection** of 3-5 relevant principles per generation task (not the entire document) is a practical context-management technique. The meta- insight: enforce quality at the point of generation, not at review time.

- **Beads** (19k stars, v0.61 released today) has matured significantly. The `PreCompact` hook auto-syncs before Claude compacts context. `--claim-next` atomically closes current and claims next task. Formulas/Molecules provide reusable workflow templates. For a solo dev, the Dolt dependency remains heavyweight — but the `bd prime` + `PreCompact` hook pattern for context injection is well-designed.

---

### Category 7: Context & Skill Management

| Tool        | Funding   | Core Idea                               | Solo Dev Fit                              |
| ----------- | --------- | --------------------------------------- | ----------------------------------------- |
| Tessl       | VC-backed | Package manager for agent skills        | Low — solving organisational distribution |
| Superpowers | MIT/OSS   | Claude Code plugin with TDD enforcement | Medium — most similar to our setup        |

**Key findings:**

- **Tessl** (tessl.io, founded by Snyk's Guy Podjarny) is a **skills registry** — npm for agent context. The original description ("spec-as-source") is inaccurate; it's actually a package manager for structured context that makes agents more reliable. The **Task Evals** concept is notable: measure whether a skill actually changes agent behavior empirically, don't just assume.

- **Superpowers** (87k stars) is the most-starred Claude Code plugin. Enforces brainstorm → spec → micro-task pipeline with TDD. Subagent dispatch per task, two-stage code review per task. Structurally very similar to our skills but packaged as a single installable plugin.

---

## Convergent Patterns Across All 30 Tools

These patterns appeared independently in 3+ tools:

| Pattern                                   | Tools                                               | We Have It?                         |
| ----------------------------------------- | --------------------------------------------------- | ----------------------------------- |
| Spec/plan before code                     | All 30                                              | Yes — define-task + plan-task       |
| Project constitution / rules file         | Spec Kit, BMAD, Kiro, CSDD, Agent OS, our CLAUDE.md | Yes                                 |
| Task decomposition with dependencies      | Taskmaster, GSD, Beads, Kiro, cc-sdd                | Partially — tasks but no formal DAG |
| Fresh context per task                    | GSD, Ralph Loop, SWE-Agent, Superpowers             | No — we accumulate in one session   |
| TDD as quality gate                       | Ralph Loop, Superpowers, Spec-Flow, our tddv2       | Yes                                 |
| Multi-model plan diversity                | Our dialectic planning, Spec-Flow voting            | Yes                                 |
| Archive completed work as decision record | OpenSpec, our task files                            | Partially                           |
| Structured requirements format (EARS)     | Kiro, cc-sdd                                        | No                                  |
| Granular, scopeable context files         | Kiro steering, Agent OS standards, Windsurf rules   | No — single CLAUDE.md               |
| Security rules at generation time         | Constitutional SDD                                  | No                                  |
| Context injection hooks (session start)   | Beads bd prime, Agent OS inject-standards           | No                                  |

---

## Comparison with Our Current Setup

### What Our Setup Already Does Well

Our define → plan → implement → review workflow with custom Claude Code skills is structurally isomorphic to what every tool in this survey implements. The specific advantages:

1. **Native Claude Code skills** — tighter integration than injected slash commands (OpenSpec, cc-sdd) or external frameworks (Spec Kit, BMAD)
2. **Dialectic multi-model planning** — our plan-task skill already uses the technique that multiple tools (Spec-Flow's voting, BMAD's multi-role) converge on
3. **Automated CI code review** — daily workflow with commit-range tracking; no other surveyed tool has equivalent CI integration for a solo dev
4. **TDD skill** — Beck-style strict TDD with red/green/refactor; matches Ralph Loop's quality gate and Superpowers' enforcement
5. **Task files as persistent artifacts** — versioned, self-contained, committed; better than Cursor's home-directory plans or Windsurf's ephemeral planning mode
6. **CLAUDE.md as source of truth** — already implements the "constitution" pattern from Spec Kit, BMAD, and CSDD

### What Our Setup Is Missing

Based on the survey, these are the genuine gaps — things multiple independent tools converge on that we don't have:

1. **Fresh context per task during implementation.** GSD and Ralph Loop both restart the agent for each task. Our impl-task skill runs in one session, accumulating context. For multi-step implementations, this causes quality degradation as the session lengthens.

2. **Granular, scopeable context files.** Kiro's steering files (with FileMatch/Auto loading modes) and Agent OS's standards discovery are structurally better than a single CLAUDE.md that grows monotonically. As CLAUDE.md grows past ~200 lines, only a fraction is relevant to any given task.

3. **Context injection at session boundaries.** Beads' `bd prime` (SessionStart hook) and `PreCompact` hook inject task state at the right moment. We have no equivalent — every session starts with whatever CLAUDE.md provides plus whatever the user remembers to mention.

---

## Recommendations

Applying the "incompressible, aimed at the next model" filter: only suggest changes that are truly load-bearing or game-changing.

### 1. Fresh Context per Task (From GSD / Ralph Loop)

**What:** When `/impl-task` has multiple steps, each step should ideally run in a fresh agent session (or at minimum, a fresh sub-agent) with only the task file and relevant source files loaded.

**Why it's load-bearing:** Context degradation is the single most consistently cited failure mode across the entire survey. GSD, Ralph Loop, SWE-Agent, and Superpowers all independently converge on this solution. Mini-SWE-agent showed that a simple loop with fresh context matches elaborate scaffolding.

**How it could work:** The impl-task skill could spawn each plan step as a sub-agent (using Claude Code's Agent tool with worktree isolation), rather than executing all steps in the main session. Each sub-agent reads the task file, implements one step, commits, exits. The main session orchestrates.

**Caveat:** This adds token cost (each sub-agent re-reads context). Worth it for tasks with 5+ steps; overkill for 2-3 step tasks.

### 2. Granular Context Files (From Kiro / Agent OS)

**What:** Break CLAUDE.md into scopeable fragments — e.g., `.claude/context/quant-patterns.md`, `.claude/context/git-rules.md`, `.claude/context/testing.md` — with metadata indicating when each should be loaded.

**Why it's load-bearing:** As the project matures, CLAUDE.md will grow. Kiro and Agent OS both show that granular, conditionally-loaded context keeps the signal-to-noise ratio high. The current "load everything always" approach works at ~100 lines but won't at ~500.

**How it could work:** This is mostly a future concern. CLAUDE.md is currently ~95 lines and well-curated. The right time to split is when it crosses ~200 lines or when you notice the agent citing irrelevant rules.

**Caveat:** Premature splitting adds indirection without benefit. Flag for later, don't do now.

### 3. Nothing Else Clears the Bar

The remaining gaps (EARS-format requirements, security constitution, task dependency DAG, context injection hooks) are individually interesting but don't clear the "incompressible / game-changing" threshold:

- **EARS format** improves requirements clarity but our define-task skill already enforces "specific, falsifiable, behaviour-level" criteria — the substance is the same, EARS is just notation
- **Security constitution** is load-bearing for regulated industries but not for a quant research codebase
- **Task dependency DAG** (Taskmaster, Beads) solves a coordination problem that matters at 10+ parallel tasks; at our scale, sequential task ordering in a plan file is sufficient
- **Session-start hooks** for context injection would be nice but Claude Code's auto-memory + CLAUDE.md already serve this purpose adequately

---

## Tool-by-Tool Reference

### Spec Frameworks

**Spec Kit** (github/spec-kit, 77k stars, Apache 2.0). GitHub's official SDD toolkit. Constitution → Specify → Plan → Tasks → Implement. Agent-agnostic (20+ tools). Independently benchmarked as 10x slower than iterative prompting. Markdown bloat: 2,577 lines of docs for 689 lines of code. No clean spec update path (Issue #1191). v0.1.4, 537 open issues.

**OpenSpec** (Fission-AI/OpenSpec, 31k stars, MIT). Lightweight alternative. Change-folder model with proposal/design/tasks artifacts committed to repo. Brownfield-friendly, iterative. Process flow not enforced — AI sometimes skips approval gates. No code-first path. Context bloat from 10 injected skills.

**BMAD Method** (bmad-code-org/BMAD-METHOD, 41k stars, open source). Enterprise SDD with 21 agent personas across 4 modules. Control Manifest prevents AI overreach. Scale-adaptive (bug fix → full methodology). Steep learning curve, heavy upfront overhead, designed for teams.

**cc-sdd** (gotalab/cc-sdd, 2.9k stars, npm). Kiro-style workflow for any AI agent. EARS-format requirements improve AI accuracy. 13 language localisations. v2.0+ uses Claude sub-agents. Manual approval gates between phases.

**SpecFlow** (marcusgoll/Spec-Flow, 71 stars). Claude Code-specific. Three quality gate levels, multi-agent voting review (3 agents at different temperatures), TDD-structured tasks, auto-resumability via state.yaml. Early stage, single maintainer, web-stack focused.

**Agent OS** (buildermethods/agent-os, 4.1k stars). v3 removed orchestration, focuses on context. Standards discovery analyses your codebase and generates granular convention files. Shape-spec interrogation step. Standards injection loads only relevant files. Tool-agnostic.

### Planning & Orchestration

**Taskmaster AI** (eyaltoledano/claude-task-master, 26k stars, MIT+Commons). MCP server with 36 tools. PRD → dependency DAG → `next` command. Complexity analysis scores tasks 1-10. `update-tasks --from=N` rewrites future tasks. Tagged task lists per branch. Research integration via Perplexity. 21k token default payload (configurable to 5k).

**GSD** (gsd-build/get-shit-done, 23k stars). v2 is TypeScript CLI on Pi SDK. Milestone → Slice → Task hierarchy. Each task runs in fresh context window. Wave-based parallel execution. 29 slash commands, 12 sub-agents. Auto-advance through milestones without human intervention. Known issue: doesn't merge cleanly with existing CLAUDE.md.

**Ralph Loop** (~300 lines bash). Autonomous TDD loop: PLANNING prompt → BUILDING prompt → bash loop restarts until done. Fresh context per iteration. TDD gate: cannot commit without green tests. Anthropic ships official plugin. Community ecosystem: ralph-orchestrator (253 stars), ralph-claude-code (463 stars), smart-ralph, choo-choo-ralph.

### Autonomous Agents

**OpenHands** (All-Hands-AI/OpenHands, 69k stars). Formerly OpenDevin. CodeAct paradigm (ICML 2024): agent writes executable Python as its action. Sandboxed Docker runtime. SWE-bench 77.6%. Multi-agent via event stream. CLI/GUI/cloud. GitHub/GitLab/Slack integrations. Heavy infrastructure (Docker required).

**SWE-Agent** (princeton-nlp/SWE-agent, 19k stars, NeurIPS 2024). Agent- Computer Interface (ACI): purpose-built shell for LM agents. Custom file viewer (~100 lines/turn), linter on every edit, explicit "no output = success" feedback. Mini-SWE-agent (~100 lines) matches full system. Now in maintenance mode.

**Devika** (stitionai/devika, 20k stars). Open-source Devin clone. Planner → Researcher → Coder → Executor pipeline. **Effectively abandoned** — 138 open issues, no maintainer response, unpatched security vulns.

**AutoDev** (unit-mesh/auto-dev, 4.4k stars). Seven SDLC-phase agents with DevIns scripting language. KMP architecture (IDE plugin + CLI + server). Chinese developer community. Several agents still in alpha.

**Sweep AI** (sweepai/sweep). Pivoted from GitHub PR bot to JetBrains IDE plugin. JetBrains PSI integration for exact symbol resolution (30ms initial, <1ms cached). Adaptive file reading (structural outline for large files, 90% token reduction). Output normalisation (strips whitespace drift, reduced edit failures 38%). Open-sourced 1.5B next-edit model.

**AutoCodeRover** (AutoCodeRoverSG/auto-code-rover, 3.1k stars, ISSTA 2024). AST-aware code search + spectrum-based fault localisation. Uses test coverage to score suspicious lines before patching. 46.2% SWE-bench Verified. Under $0.70 per issue, ~7 min per issue.

### AI IDEs

**Kiro** (AWS, beta). Spec-driven: requirements.md (EARS) → design.md → tasks.md, committed to `.kiro/specs/`. Steering files with four loading modes (Always/FileMatch/Auto/Manual). Agent Hooks fire on file events. AST-based editing. Autopilot mode. Checkpointing.

**Windsurf/Cascade** (Codeium → OpenAI, 1M+ users). Flow awareness: real-time editor state tracking. Auto-generated Memories + explicit Rules + AGENTS.md. Planning Mode with dual timeline (immediate + long-term). Arena Mode (parallel instances). Cascade Hooks (12 events, blocking pre-hooks). Acquired by OpenAI early 2025.

**Cursor Plan Mode**. Clarify → Research → Plan → Execute. Plan as reviewable Markdown. "Alignment ceremony" framing: value is the forcing function, not the document. Plans save to home directory (not repo) by default — a design weakness. Manual and chat editing paths conflict.

### Multi-Agent Frameworks

**LangGraph** (langchain-ai/langgraph, 90k+ stars). Directed-graph agent workflows with persistent state, cyclic support, human-in-the-loop, time-travel debugging. Steep learning curve. Over-engineered for simple tasks.

**CrewAI** (crewAIInc/crewAI, 46k stars). Role-based AI teams with crew/flow dual architecture. Lowest barrier to entry. 180% star growth in 2025. Role/ backstory is prompt engineering, not hard architectural guarantee.

**AutoGen** (microsoft/autogen, 56k stars). Conversational multi-agent. MagenticOne: Task Ledger + Progress Ledger with inner/outer planning loops. Microsoft deprecated active development; AG2 fork is the active path.

### Experimental / Context

**EvoGit** (BillHuang2001/evogit, 1.2k stars, AGPL-3.0). Evolutionary code via Git graph. 16 parallel agents, stigmergic coordination (communication via commits only). Mutation + crossover operations on code. Berkeley AgentX Competition winner. No benchmarks vs. existing tools.

**EnvX** (arXiv paper, no confirmed OSS repo). Transforms repos into autonomous agents via three-phase agentization. Agent cards for capability discovery. 74% execution completion, 52% task pass. 10x fewer tokens than competitors.

**Constitutional SDD** (arXiv:2602.02584, Jan 2026). Security rules embedded in machine-readable constitution with CWE references. Selective injection of 3-5 relevant principles per task. 73% reduction in CWE violations. Builds on Spec Kit. Meta-insight: enforce quality at generation time, not review time.

**Beads** (steveyegge/beads, 19k stars, v0.61 today). Dolt-backed dependency- aware task store. `bd ready` returns unblocked tasks in ~10ms. `bd prime` injects ~1-2k tokens at session start. `PreCompact` hook auto-syncs before context compaction. Formulas/Molecules for reusable workflow templates. `--claim-next` atomic close-and-claim.

**Tessl** (tessl.io, VC-backed). Skills registry — npm for agent context, not spec-as-source. Task Evals measure whether a skill changes agent behaviour. 3,000+ indexed skills. Cisco, HashiCorp, JustEat adoption.

**Superpowers** (obra/superpowers, 87k stars, MIT). Claude Code plugin. Brainstorm → spec → micro-task pipeline. Subagent dispatch per task. TDD enforcement. Two-stage code review. Git worktree isolation. Most-starred Claude Code plugin.

---

## Sources

Sources are cited per-tool in the detailed findings above. Key references:

- Spec Kit: [github.com/github/spec-kit](https://github.com/github/spec-kit); Scott Logic benchmark; Martin Fowler SDD analysis
- GSD: [github.com/gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)
- Ralph Loop: [ghuntley.com/loop](https://ghuntley.com/loop)
- Taskmaster: [github.com/eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master)
- SWE-Agent: [arxiv.org/abs/2310.06770](https://arxiv.org/abs/2310.06770) (NeurIPS 2024)
- AutoCodeRover: [arxiv.org/abs/2404.05427](https://arxiv.org/abs/2404.05427) (ISSTA 2024)
- OpenHands: [github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) (ICLR 2025)
- Constitutional SDD: [arxiv.org/abs/2602.02584](https://arxiv.org/abs/2602.02584)
- Kiro: [kiro.dev](https://kiro.dev)
- Windsurf: [codeium.com/windsurf](https://codeium.com/windsurf)
- Superpowers: [github.com/obra/superpowers](https://github.com/obra/superpowers)
- Agent OS: [github.com/buildermethods/agent-os](https://github.com/buildermethods/agent-os)
