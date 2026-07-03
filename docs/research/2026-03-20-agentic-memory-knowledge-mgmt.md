# Agentic Memory & Knowledge Management: State of the Art

**Status:** rejected — too overengineered; auto-memory is sufficient for now **Date**: 2026-03-20 **Problem Anchor**: What is the state of the art in agentic memory and knowledge management — specifically: (1) how do AI agents best persist, codify, and compound learning across sessions and models, and (2) how should a power user with existing knowledge scattered across Google services, Notion, GitHub, and other platforms architect a unified, model-agnostic knowledge layer that agents can navigate as a "map"?

---

## Executive Summary

This research synthesizes findings from 8 parallel research tracks covering academic foundations, open-source frameworks, commercial products, thought leader perspectives, cross-model architectures, knowledge integration patterns, specific tools (Fireship's 7), and contrarian/adversarial analysis. Two independent review rounds refined the findings. Key conclusions:

1. **The field has converged on a four-type memory taxonomy** (working, episodic, semantic, procedural) from the CoALA framework (Sumers, Yao et al., arXiv:2309.02427, 2023). The consolidation pipeline — episodic → semantic → procedural — is the mechanism for compounding learning.

2. **MCP (Model Context Protocol) is the enabling infrastructure** for model-agnostic, cross-device memory. Now governed by the Linux Foundation's Agentic AI Foundation (co-founded by Anthropic, Block, and OpenAI; with Google, Microsoft, AWS, Cloudflare as supporting members), remote MCP servers solve cross-device access while being inherently model-agnostic.

3. **"Memory as code" should be the primary strategy for a solo power user.** File-based memory (CLAUDE.md, AGENTS.md, structured markdown) is deterministic, auditable, version-controlled, and portable. It outperforms or matches complex vector systems in benchmarks. Add semantic search only when corpus exceeds what fits in structured files (~1000+ heterogeneous documents).

4. **Tiered context loading is the architectural response to context rot.** OpenViking's L0/L1/L2 pattern (<100 tokens → <2000 tokens → full content) directly addresses the empirically measured degradation that occurs with larger contexts. This pattern should inform the design of any knowledge map.

5. **Security risks must be architectural constraints, not afterthoughts.** Memory poisoning (95% storage injection rate, 70% end-to-end attack success), context rot, and GDPR deletion impossibility for embeddings are design constraints that shape what the architecture should look like — not just warnings in a risk section.

6. **Compounding knowledge means updating system prompts, not model weights.** Karpathy's "system prompt learning" and Chase's "sleep-time compute" are the practitioner consensus for cross-session improvement without fine-tuning.

7. **The knowledge "map" should be a tiered navigational index in Notion + structured markdown, not a data warehouse.** Point to where knowledge lives; don't copy it. Use MCP servers as the bridge layer for federated access.

---

## Table of Contents

1. [Theoretical Foundations](#1-theoretical-foundations)
2. [The Memory Taxonomy](#2-the-memory-taxonomy)
3. [Thought Leader Perspectives](#3-thought-leader-perspectives)
4. [Frameworks & Tools Landscape](#4-frameworks--tools-landscape)
5. [Cross-Model & Cross-Device Architectures](#5-cross-model--cross-device-architectures)
6. [Risks as Design Constraints](#6-risks-as-design-constraints)
7. [The Architecture: A Risk-Informed Design](#7-the-architecture-a-risk-informed-design)
8. [The Fireship 7 Tools](#8-the-fireship-7-tools)
9. [Cross-Cutting Synthesis](#9-cross-cutting-synthesis)
10. [References](#10-references)

---

## 1. Theoretical Foundations

### Cognitive Science Roots

The four-way memory taxonomy descends from two 1980s cognitive architectures:

- **ACT-R** (Anderson): Formalizes memory activation, decay, and spreading activation as mathematical principles
- **SOAR** (Laird, Newell, Rosenbloom): Adds episodic memory as distinct from semantic

The **hippocampal indexing theory** from neuroscience provides a second lineage: LLMs are "neocortex" (distributed parametric knowledge) but lack a "hippocampus" (rapid episodic index). HippoRAG and Zep/Graphiti exploit this gap.

### Foundational Papers (2023)

| Paper                                  | Key Contribution                                                             | Result                                   |
| -------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------- |
| Park et al. "Generative Agents" (UIST) | Memory stream + importance-weighted retrieval + reflection loop              | Removing any component degrades behavior |
| Packer et al. "MemGPT"                 | OS-memory-hierarchy analogy: context window = RAM, external = disk           | Agent manages own memory via tool calls  |
| Shinn et al. "Reflexion" (NeurIPS)     | Verbal RL — procedural lessons in episodic buffer; iterative self-reflection | 91% HumanEval pass@1 (multi-attempt)     |

Note on Reflexion: the 91% figure uses iterative self-reflection across multiple attempts, vs. GPT-4's 80% on single-attempt pass@1. This is better-exploited inference-time compute, not a direct apples-to-apples comparison — but it demonstrates that procedural memory (storing what went wrong) enables meaningful performance gains.

### Active Research Frontier (2024–2026)

**Neurobiological inspiration**: HippoRAG (NeurIPS 2024) — knowledge graph as hippocampal index with Personalized PageRank. 20% improvement, 10–20x cost reduction over standard RAG.

**Dynamic linking**: A-MEM (NeurIPS 2025) — Zettelkasten-inspired methodology where new memories retroactively update existing memories' context. 85–93% token reduction. Evaluated on DialSim with relative improvements over LoCoMo baselines; cross-benchmark comparisons should be interpreted cautiously as DialSim and LoCoMo measure different capabilities.

**Learned memory management**: MEM1 (arXiv:2506.15841, June 2025) — trains memory operations via RL. 3.5x performance with 3.7x memory reduction. First system showing consolidation/forgetting policies can be end-to-end trained.

**Multi-graph architectures**: MAGMA (January 2026) — four orthogonal graph views (temporal, causal, semantic, entity) with policy-guided query routing. +45.5% over prior SOTA, 95% token reduction.

**Just-in-time memory assembly**: GAM — "General Agentic Memory via Deep Research" (arXiv:2511.18423) — introduces a dual-agent (memorizer + researcher) architecture where memory is not precomputed but assembled on-demand from a full, preserved session archive. Beats conventional RAG on RULER (90%+ vs. failure) specifically because it avoids the compression failures that plague upfront summarization approaches. This is the most direct architectural response to the five compression failure modes (see §6).

**Formal belief revision**: "Graph-Native Cognitive Memory for AI Agents" (arXiv:2603.17244) demonstrates that AGM belief revision postulates (the formal theory of minimal belief change) map directly onto graph memory operations. This provides formal guarantees for temporal fact management — the "hard unsolved problem" — and gives theoretical grounding to Zep/Graphiti's bi-temporal approach.

**Architecture-level memory**: Titans (NeurIPS 2025) updates its memory module's weights (not full network weights) via gradient steps during the forward pass, scaling to 2M+ context windows. Importantly, these weights reset between independent sessions — this is inference-time adaptation, not permanent learning.

### The Long-Context Vs. Memory Debate

Research consensus (March 2026): **complementary, not competing**. Long context handles within-session reasoning; memory handles cross-session persistence, temporal invalidation, and selective retrieval. Empirical cost-performance analysis (arXiv:2603.04814) shows memory becomes cheaper after ~10 interaction turns at 100k tokens, saving ~26% at 20 turns. However, long-context significantly outperforms memory on complex temporal reasoning (92.85% vs 57.68% on LoCoMo) — memory wins on economics and personalization; long context wins on precision.

---

## 2. The Memory Taxonomy

The canonical four-type taxonomy was established by the CoALA framework (Sumers, Yao et al., arXiv:2309.02427, 2023) and confirmed by the December 2025 survey "Memory in the Age of AI Agents" (arXiv:2512.13564):

| Type          | What It Stores                                 | Examples                                        | Implementation                        |
| ------------- | ---------------------------------------------- | ----------------------------------------------- | ------------------------------------- |
| **Working**   | Active context for current session             | Current task state, recent messages             | Context window (native)               |
| **Episodic**  | Time-stamped interaction logs, trajectories    | "Last time X failed because Y"                  | Trace archives, few-shot examples     |
| **Semantic**  | Accumulated facts, preferences, knowledge      | User prefers TypeScript, codes async/await      | Vector stores, knowledge graphs       |
| **Procedural**| Behavioral patterns, skills, tool sequences    | Build commands, debugging workflows             | System prompts, instruction files     |

**The consolidation pipeline** — episodic → semantic → procedural — is the mechanism for compounding. Each session's interactions distill into facts (semantic), and repeated patterns automate into skills (procedural). This is not "learning" in the parameter-update sense — model weights don't change — but it is genuine compounding of the retrieval index and the quality of procedural instructions.

### Forgetting as Architectural Requirement

Human memory's Ebbinghaus forgetting curve isn't a defect — it's a selection mechanism. Utility-based and retrieval-history-based deletion yields up to 10% performance gains over indiscriminate storage (Johns Hopkins research). Engram's application of FSRS-6 (Anki's spaced repetition algorithm) to agent memory — where access frequency and recency determine retrieval probability — provides a principled decay function.

**This is not a caveat — it is a design requirement.** Any knowledge map or memory system should track access frequency metadata and implement principled decay. Items that are never accessed should eventually lose prominence, not accumulate indefinitely.

---

## 3. Thought Leader Perspectives

Positioning thought leaders before architecture because these perspectives inform the architectural choices that follow.

### Andrej Karpathy — System Prompt Learning

A "third learning paradigm" distinct from pretraining (knowledge) and fine-tuning (behavior). Agents should write "books for themselves" — updating explicit instructions rather than retraining parameters. Called ChatGPT's memory a "primordial crappy implementation" of what this could become.

### Simon Willison — Context Engineering

"Prompt engineering" is deprecated. The craft is now **context engineering** — managing what tokens enter the context window, when, and from where. Surfaced Drew Breunig's four failure modes of context: **poisoning, distraction, confusion, clash**. Emphasized that large context windows are not an excuse to be sloppy.

### Harrison Chase (LangChain) — Sleep-Time Compute + Files as Memory

Most operationally detailed voice. Key positions: (1) "The best memory today is application specific." (2) **Sleep-time compute**: agents analyze their own daily traces overnight and update instructions without human intervention. (3) File systems are "a natural and powerful way to represent an agent's state" — both Anthropic's Deep Research and Manus use them. (4) "Everything's context engineering."

**LangMem SDK** implements this concretely: three tiers (in-context, across-conversation, across-sessions) with a "background memory" concept that makes sleep-time compute practical. Released as standalone SDK because file-based memory alone doesn't cover all patterns.

### Swyx — the IMPACT Framework

Memory as a first-class agent component: Intent, **Memory**, Planning, Authority, Control Flow, Tools. Critique of OpenAI's TRIM: "TRIM has no emphasis on memory, planning, or auth."

### Jerry Liu (LlamaIndex) — RAG Is a Hack

Top-k similarity retrieval is suboptimal because components aren't learned end-to-end. "If you just flat index everything with chunks and embeddings, you can really only do top-K lookup. If you can index in a hierarchy with defined relationships, you can do more interesting things."

### Linus Lee (Ex-Notion) — Knowledge as a Graph

Documents are fundamentally graph-structured. Notion as "a single workspace where all pages exist in a shared context" — agents navigate the graph of interconnected information.

### Anthropic — File-Based Memory Bet

The memory tool uses a `/memory` directory where Claude reads entire files rather than targeted retrieval — betting on full-context loading. Four context strategies: **Write** (scratchpads), **Select** (retrieval), **Compress** (summarize), **Isolate** (sub-agents). Key recommendation: "Find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."

### Sébastien Dubois — Agentic Knowledge Management

Introduces the **proactive heartbeat pattern** — AI proactively scans and proposes actions rather than waiting to be invoked. This inverts the standard model of agents as reactive. In the PKM-to-AI-companion transition (ACM CSCW 2025), agents evolve from "tools I query" to "partners that monitor my knowledge base and propose updates." This is the operational model for the consolidation pipeline.

### Andrew Ng — Memory as Coming Differentiator

"Memory is the key thing coming soon." Launched Context Hub for persistent agent documentation and DeepLearning.AI courses on agent memory with Letta and LangGraph.

### Key Debate Map

| Debate                        | Camp A                                          | Camp B                                            |
| ----------------------------- | ----------------------------------------------- | ------------------------------------------------- |
| Best storage substrate        | Files (Chase, Letta, Anthropic): simple, native | Knowledge graphs (Zep, Cognee): accuracy, temporal|
| Retrieval vs. full read       | Full file read (Anthropic): no targeted search  | Targeted search (Mem0, Zep): latency reduction    |
| Memory ownership              | Platform-controlled (ChatGPT, Claude): easiest  | User-owned (MemOS, Mem0): privacy, portability    |
| Compounding mechanism         | System prompt learning (Karpathy, Chase)        | Fine-tuning (Liu, academic): parametric           |
| Complexity budget             | Simpler is better (Letta benchmark)             | Specialized graph wins at scale (Zep benchmarks)  |

---

## 4. Frameworks & Tools Landscape

### For This Specific User: What Matters

Given the constraints (solo developer, Claude Code primary, already have Notion MCP and GitHub MCP, preference for control and portability), the full landscape of 20+ frameworks collapses to a much smaller set of relevant choices. This section catalogs the landscape and then culls it.

### Production-Ready Memory Frameworks

| Framework      | Stars  | Architecture                                   | Temporal Invalidation | Infrastructure     | Lock-in Risk |
| -------------- | ------ | ---------------------------------------------- | --------------------- | ------------------ | ------------ |
| Mem0           | ~48k   | Hybrid vector + KV + graph (Pro)               | No (OSS)              | Vector DB          | Low (OSS)    |
| Zep/Graphiti   | ~24k   | Bi-temporal knowledge graph                    | **Yes**               | Neo4j required     | Low-Med      |
| Letta (MemGPT) | ~22k   | OS-inspired: core/recall/archival              | No                    | SQLite/PostgreSQL  | Medium       |
| Cognee         | ~8-10k | ECL pipeline → graph + vector + SQL            | Evolves (Memify)      | Zero-infra default | Low          |
| LangGraph      | —      | Checkpointer + Store (namespaced KV)           | No                    | DB required        | Low-Med      |
| Hindsight      | —      | Multi-strategy (semantic+BM25+entity+temporal) | No                    | PostgreSQL         | Low (MIT)    |

**Benchmark landscape** (LoCoMo, as of March 2026):

- SuperLocalMemory Mode C: **87.7%** (arXiv:2603.14588) — current SOTA
- Letta filesystem + grep: 74.0% (2024 benchmark)
- Mem0: 68.5% (Letta's benchmark)
- Hindsight: 91.4% on LongMemEval (different benchmark)
- Graphiti: 94.8% DMR accuracy; +18.5% on LongMemEval

**Caveat**: The "simple filesystem beats specialized tools" conclusion from Letta's 2024 blog post was true at time of writing but the gap has narrowed or reversed for several systems. The insight remains directionally valid — filesystem approaches are surprisingly competitive — but specialized systems have caught up.

### Recently Released Systems (Feb-March 2026)

**Hermes Agent** (Nous Research, February 2026): Multi-level persistent memory following the agentskills.io open standard. Stores skills as searchable markdown files, runs on-device (SQLite), cross-channel (Telegram, Discord, Slack, WhatsApp). MIT-licensed. Directly relevant to the "memory as code" pattern.

**MemOS** (MemTensor/OpenMem, arXiv:2505.22101/2507.03724): "Memory Operating System" with a MemCube abstraction unifying parametric, activation, and plaintext memory. V2.0 Stardust (December 2025) added multi-modal memory, tool memory, and MCP support. Provides a formal model for memory migration across model types — directly addresses the cross-model portability question.

**OpenViking** (ByteDance, January 2026): Hierarchical context filesystem with `viking://` URI scheme. See §8 for detailed analysis.

### Research-Stage Systems

| Framework | Key Innovation                                   | Benchmark Claims                      |
| --------- | ------------------------------------------------ | ------------------------------------- |
| MAGMA     | Four orthogonal graph views + policy routing     | +45.5% reasoning, 95% token reduction |
| GAM       | JIT dual-agent memory assembly from raw archives | 90%+ RULER (vs. RAG failure)          |
| MemoryOS  | Three-tier OS paging (STM→MTM→LPM)               | +49% F1 on LoCoMo                     |
| A-MEM     | Zettelkasten-style dynamic relinking             | 85-93% token reduction                |
| MEM1      | RL-trained memory operations                     | 3.5x perf, 3.7x memory reduction      |

### Multi-Agent Memory Coordination

An important gap in the single-agent framing: when multiple agents (coding, research, email triage) share memory, how should they partition, merge, and resolve conflicts? MemOS v2.0 includes multi-agent memory sharing. MemoryAgentBench (ICLR 2026) explicitly evaluates coordination. The March 2026 paper "Multi-Agent Memory from a Computer Architecture Perspective" (arXiv:2603.10062) proposes cache-coherence-inspired protocols for multi-agent memory consistency. For the target user running parallel agents in Claude Code, this is a practical concern — today's workaround is file-based partitioning (each agent writes to its own namespace).

### Commercial Memory Platforms

| Product     | Pricing            | Lock-in Risk | Best For                                  |
| ----------- | ------------------ | ------------ | ----------------------------------------- |
| Mem0 Cloud  | $19-249/mo         | Low          | Model-agnostic API, browser extension     |
| Zep Cloud   | $25/mo (no gating) | Low-Med      | Temporal reasoning, no Neo4j hassle       |
| SuperMemory | $0-19/mo           | **High**     | Turnkey connectors (Drive, Gmail, Notion) |
| Cognee      | $35/mo dev         | Low          | Document-heavy knowledge bases            |

**Cautionary tale — Limitless**: Acquired by Meta December 2025 → service sunset. Hardware + cloud subscription product shut down post-acquisition, breaking the capture pipeline for all users. This is why self-hosted or portable architectures matter.

### The Culling for a Solo Power User

For this specific user profile, the frameworks that matter are:

1. **CLAUDE.md + AGENTS.md + structured markdown** (primary — memory as code)
2. **Notion as knowledge hub** (via existing MCP — the navigational map)
3. **Zep Cloud ($25/mo) OR Mem0 Cloud ($19/mo)** (when/if vector search is needed — Zep if temporal invalidation matters, Mem0 for simplicity)
4. **A remote MCP memory server** (for cross-device access — see §5)

Everything else is either research-stage, enterprise-scale, or solving problems this user doesn't have.

---

## 5. Cross-Model & Cross-Device Architectures

### MCP: the Universal Adapter

MCP (Anthropic, November 2024; donated to Linux Foundation's Agentic AI Foundation, December 2025) is model-agnostic by construction. A single MCP server works with any compatible host — Claude Desktop, Claude Code CLI, Claude mobile, ChatGPT desktop, VS Code Copilot, Cursor, Windsurf, Gemini CLI.

**Two transports**:

- **STDIO** (local): Zero-latency, single-machine, subprocess
- **Streamable HTTP** (remote): HTTP POST + SSE, OAuth, enables cross-device

### Cross-Device Solution: Remote MCP

1. Deploy a memory server to Cloudflare Workers (free tier sufficient) with Streamable HTTP
2. Configure once via `claude.ai` web interface
3. Configuration syncs automatically to Claude Desktop, Web, iOS, Android
4. Same URL works for any other MCP-compatible client

**Best candidate**: `doobidoo/mcp-memory-service` — explicitly designed for remote deployment, SQLite-vec + Cloudflare Workers backend, 5ms local retrieval, hybrid local+cloud sync mode.

### Instruction File Standards

| Format    | Originator       | Model Support                                                  |
| --------- | ---------------- | -------------------------------------------------------------- |
| CLAUDE.md | Anthropic        | Claude Code only                                               |
| AGENTS.md | OpenAI/community | Claude Code, Cursor, Copilot, Gemini CLI, Windsurf, Aider, Zed |

Both should be checked into every project repo. The content should include: project context, build/test commands, coding conventions, domain terminology, and pointers to where knowledge lives (the "map" for coding agents).

### Claude Code Memory Architecture

Two mechanisms loaded at session start:

| Mechanism   | Written by | Cross-device?                                |
| ----------- | ---------- | -------------------------------------------- |
| CLAUDE.md   | Human      | Yes (via git for project; dotfiles for user) |
| Auto memory | Claude     | No (machine-local at ~/.claude/projects/)    |

**Memory hierarchy** (most general → most specific):

1. `~/.claude/CLAUDE.md` (user global — sync via dotfiles repo)
2. `~/.claude/rules/*.md` (user rules)
3. `./CLAUDE.md` (project — in git)
4. `./.claude/rules/*.md` (project rules)
5. Auto memory `MEMORY.md` (per-machine, per-repo)

**Cross-device gap**: CLAUDE.md files sync naturally via git/dotfiles. Auto memory does not. Options: symlink `~/.claude/projects/` to iCloud/Dropbox, rsync, or use a remote MCP memory server instead.

---

## 6. Risks as Design Constraints

These are not afterthoughts — they are constraints that shape the architecture in §7.

### Constraint 1: Memory Poisoning

- MINJA attacks achieve **95% storage injection rate** (the poisoned memory is stored) and **70% end-to-end attack success** (the desired malicious output is produced). A single poisoned entry persists across all future sessions.
- Microsoft documented real-world exploitation (February 2026): 50+ unique prompts from 31 companies using memory poisoning via embedded "Summarize with AI" buttons.
- Palo Alto Unit 42: indirect prompt injection persists across agent restarts ("ZombieAgent" PoC).
- **Emerging defense**: Cryptographic Provenance Attestation — each memory unit tagged with a cryptographic signature tied to its origin. More tractable than the general defense problem but not yet standard in any production system.

**Architectural implication**: Read/write boundaries must be explicit. The MCP bridge to Gmail and Drive should be **read-only by default** — agents can query but not write memories based on external content without human approval. Memory derived from untrusted sources (emails, web pages) must be tagged with provenance and treated as lower-trust than user-authored memories.

### Constraint 2: Context Rot

Chroma Research tested 18 SOTA models and found performance degrades as context grows, even on trivially simple tasks. The mechanism: structural coherence in context creates strong distributional priors that compete with targeted retrieval. Models perform better on shuffled haystacks than logically coherent ones because coherent structure causes the model to rely on distributional patterns rather than actually finding the needle.

**Architectural implication**: The knowledge map must use **tiered loading** — not dump everything into context. OpenViking's L0/L1/L2 pattern is the direct response:

- **L0 (Abstract)**: <100 tokens — one-sentence summary for identification and scoring
- **L1 (Overview)**: <2,000 tokens — structure, usage patterns, core info for planning
- **L2 (Detail)**: Full content — loaded only when genuinely needed

This tiered pattern should be applied to the Notion knowledge map: each entry has a one-line summary (L0), a structured overview (L1), and a link to the full source (L2). Agents navigate L0 first, load L1 for planning, and fetch L2 only when needed.

### Constraint 3: Compression Failures

Five failure modes when compressing context into stored memory:

1. **Catastrophic forgetting**: Older relevant information disappears silently
2. **Hallucination amplification**: Lossy compression forces gap-filling with invented facts
3. **Context drift**: Meaning shifts gradually as embedding space evolves
4. **Over-compression**: Multi-step reasoning chains no longer fit
5. **Bias creep**: Compression amplifies dominant patterns

**Architectural implication**: GAM's just-in-time assembly pattern (arXiv:2511.18423) directly addresses failures #1 and #2 by storing raw session archives and assembling context on-demand rather than pre-compressing. For a solo user, this translates to: **keep raw interaction logs alongside compressed summaries**. When compressed memory produces unexpected results, the raw archive serves as ground truth.

### Constraint 4: Navigational Map Staleness

The Map of Content (MOC) pattern — the navigational index — has the same temporal invalidation problem as vector stores: if the map doesn't reflect reality (content moved, deleted, added without map update), agents following the map retrieve wrong or null results. This is the enterprise KM failure pattern (systems too complex to maintain) applied to personal knowledge.

**Architectural implication**: The map needs a **freshness mechanism**. Options: (1) map entries carry a `last_verified` date and agents flag entries older than a threshold, (2) a periodic heartbeat job (Dubois's proactive heartbeat pattern) that crawls sources and proposes map updates, (3) agents that encounter stale map entries automatically propose corrections.

### Constraint 5: GDPR and Deletion

Vector embeddings cannot be surgically deleted. GDPR Article 17 was designed for structured databases. Cross-border complexity is severe for unified knowledge layers spanning multiple jurisdictions.

**Architectural implication**: Prefer structured storage (markdown files, Notion databases, SQLite) over vector embeddings for memory that may need deletion. If using vector stores, ensure they support metadata-based filtering so entries can be logically excluded without requiring embedding deletion.

### Constraint 6: the Compound Learning Illusion

There is no learning in current agent memory systems — only retrieval. Model weights don't change. What compounds is the retrieval index and procedural instruction quality, not model capability. This distinction matters: don't over-invest in infrastructure expecting exponential capability growth. The ROI curve for memory infrastructure is logarithmic, not exponential.

---

## 7. The Architecture: a Risk-Informed Design

This architecture is designed with the constraints from §6 baked in, not added as afterthoughts.

### Primary Strategy: Memory as Code

For a solo power user, file-based memory is the **primary strategy**, not a fallback:

- Deterministic, version-controlled, auditable
- No trust calibration problem, no semantic drift, no embedding-space poisoning
- Portable across models (any model reads system prompts)
- Benchmarks competitive with specialized tools
- The limitation is maintenance discipline, which is a feature for a high-trust user who wants control

### The Three-Layer Stack

```text
LAYER 1: NAVIGATIONAL MAP (Notion + structured markdown)
├── Notion Knowledge Map database (tiered: L0 summary, L1 overview, L2 source link)
│   ├── Type: axiom | principle | decision | rule | reference | skill
│   ├── Domain: investing | coding | personal | research | ...
│   ├── Source: gmail | drive | notion | github | direct
│   ├── SourceURL: link to original content
│   ├── Trust: user-authored | agent-proposed | external-derived
│   ├── LastVerified: date
│   └── AccessCount: integer (for FSRS-6 decay)
├── knowledge_map.md in ~/.claude/projects/*/memory/
│   └── Curated index: what exists where, read by agents first
├── CLAUDE.md hierarchy (user global + project-specific)
└── AGENTS.md in each project repo (cross-model instructions)

LAYER 2: MCP BRIDGE (federated access — read-focused)
├── Notion MCP (already connected) — read/write
├── Google Workspace MCP (gws CLI) — READ-ONLY by default
├── GitHub MCP (already connected) — read/write
├── Filesystem MCP — local files
└── Remote Memory MCP (Cloudflare Workers) — cross-device semantic search

LAYER 3: CONTENT (stays in original services — never copied)
├── Gmail, Drive, Docs, Sheets, Keep
├── GitHub repos, issues, PRs
├── Goodreads (CSV export → Notion Reading Library)
└── Blinkist (Readwise → automatic Notion sync)
```

### Read/Write Boundaries (Poisoning Defense)

| Source                 | Read | Write to Memory       | Trust Level               |
| ---------------------- | ---- | --------------------- | ------------------------- |
| User (CLAUDE.md)       | Yes  | Direct                | Highest                   |
| Agent (auto memory)    | Yes  | With review           | High (user can audit)     |
| Notion (user-authored) | Yes  | Via map update        | High                      |
| GitHub (own repos)     | Yes  | Via map update        | High                      |
| Gmail                  | Yes  | **Requires approval** | Medium (external senders) |
| Google Drive (shared)  | Yes  | **Requires approval** | Medium                    |
| Web content            | Yes  | **Never automatic**   | Low                       |

### Tiered Context Loading (Context Rot Defense)

Every entry in the knowledge map follows the L0/L1/L2 pattern:

- **L0**: Single-line summary in `knowledge_map.md` — loaded every session (<100 tokens per entry)
  - Example: `investing/position-sizing: Kelly criterion for portfolio allocation [Notion: /investing/kelly]`
- **L1**: Structured overview in Notion database — loaded when agent identifies relevance (<2000 tokens)
  - Example: The full Notion page with key formulas, constraints, current parameters
- **L2**: Full source content — loaded only when deep work requires it (fetch via MCP)
  - Example: The original research document in Google Drive, the academic paper

### Freshness Mechanism (Staleness Defense)

- Map entries carry `LastVerified` date
- Agents encountering entries older than 90 days flag them for review
- Monthly heartbeat: a scheduled agent crawls top-50 most-accessed map entries, verifies sources still exist, proposes updates
- Access frequency tracked for FSRS-6 decay — low-access entries gradually lose prominence in L0 index

### The Compounding Loop

Following Chase's sleep-time compute and Dubois's proactive heartbeat:

1. **During sessions**: Agent works, interactions accumulate
2. **End-of-session**: Agent proposes additions to MEMORY.md + Notion Knowledge Map
3. **Human approves** in ~5 minutes (critical — keeps human in loop for trust)
4. **Weekly heartbeat**: Scheduled agent reviews recent sessions, proposes consolidated updates to CLAUDE.md (procedural), knowledge_map.md (semantic), and flags stale entries
5. **Next session**: Starts with richer, more accurate context

### Cross-Device Access

| Interface          | How It Accesses Memory                                       |
| ------------------ | ------------------------------------------------------------ |
| Claude Code CLI    | Direct filesystem (CLAUDE.md, MEMORY.md) + local MCP servers |
| Claude Desktop     | Remote Memory MCP + Notion MCP + Google MCP                  |
| Claude iOS/Android | Remote Memory MCP (configured once via claude.ai)            |
| Claude Web         | Same as Desktop                                              |
| Other models       | AGENTS.md (in repo) + same remote MCP servers                |

### Service-Specific Integration

| Service    | Integration Path                                              | Status         |
| ---------- | ------------------------------------------------------------- | -------------- |
| Gmail      | gws CLI (in use) + msgvault offline search                    | Ready          |
| Drive/Docs | gws CLI or Google Workspace MCP                               | Ready          |
| Sheets     | gws CLI                                                       | Ready          |
| Notion     | Official Notion MCP                                           | Connected      |
| GitHub     | gh CLI + GitHub MCP                                           | Connected      |
| Goodreads  | API deprecated → CSV export → Notion Reading Library          | One-time setup |
| Blinkist   | Readwise browser extension → automatic Notion sync            | Setup needed   |
| Keep       | No API → Google Takeout export → manual migration to Notion   | Manual         |

### When to Add Vector/Graph Search

The file-based primary strategy is sufficient until one of these triggers:

- Knowledge map exceeds ~500 entries (L0 index no longer fits in comfortable context)
- Frequent queries require semantic similarity ("what did I read about X?") rather than navigational lookup
- Temporal reasoning becomes important ("what did I believe about X in 2025?")

At that point, add **Zep Cloud** ($25/mo) for temporal knowledge graph + semantic search, exposed via MCP. Or **Mem0 Cloud** ($19/mo) for simpler vector-based recall without temporal invalidation.

---

## 8. The Fireship 7 Tools

From Fireship's "7 new open source AI tools you need right now" (March 2026):

| Tool              | What It Is                                      | Memory Relevance          | Stars  | License    |
| ----------------- | ----------------------------------------------- | ------------------------- | ------ | ---------- |
| **OpenViking**    | Hierarchical context filesystem for agents      | **Most directly relevant**| ~15k   | Apache 2.0 |
| Agency Agents     | 100+ AI agent persona files (markdown)          | Static codified knowledge | ~57k   | MIT        |
| NanoChat          | Karpathy's GPT-2 training pipeline              | Autoresearch loop         | ~50k   | MIT        |
| PromptFoo         | LLM evaluation/testing (acquired by OpenAI)     | Tests memory correctness  | ~18k   | MIT        |
| Heretic           | Removes safety alignment from transformers      | Tangential                | ~16k   | AGPL-3.0   |
| MiroFish          | Multi-agent swarm simulation                    | Episodic + graph memory   | ~37k   | AGPL-3.0   |
| Impeccable        | Design skill files for coding agents            | Static domain knowledge   | ~11k   | Apache 2.0 |

### OpenViking: the Architectural Inspiration

OpenViking (ByteDance/Volcano Engine) introduces the `viking://` URI scheme:

- `viking://resources/` — working materials
- `viking://user/` — persistent preferences and history
- `viking://agent/` — learned skills and task memories

Its L0/L1/L2 tiered loading pattern is adopted in the recommended architecture (§7) as the response to context rot. Results: task completion +46%, input tokens -82%.

**Limitation**: Primary integration targets are Chinese-ecosystem frameworks. The pattern is more valuable than the specific tool for a Western stack.

### Agency Agents & Impeccable: the "Memory as Code" Pattern

Both represent the same pattern: pre-load agents with structured domain knowledge via markdown files. Zero infrastructure, immediately usable, IDE-agnostic. This is the pattern extended by CLAUDE.md/AGENTS.md into project-specific knowledge.

### PromptFoo: Testing Memory Correctness

Essential for validating that memory architecture works. Trajectory assertions (`trajectory:tool-used`, `trajectory:tool-sequence`) verify agent reasoning steps. 67+ red-team attack plugins for security testing. Should be used to test the memory architecture once built.

---

## 9. Cross-Cutting Synthesis

### Points of Agreement Across All Tracks

1. **The four-type taxonomy is canonical.** Every source converges on working/episodic/semantic/procedural.
2. **MCP is the right protocol.** Every track touching cross-model/cross-source access converges on MCP.
3. **File-based memory is surprisingly competitive.** Academic, practitioner, and contrarian tracks agree.
4. **Temporal invalidation is the hard problem.** Only Zep/Graphiti has production-ready temporal management; formal belief revision (arXiv:2603.17244) provides theoretical grounding.
5. **Memory ownership should be user-controlled.** The "Memory as Asset" paper, Limitless shutdown, and GDPR analysis all converge.

### The Central Synthesis: Memory as Code + Tiered Loading + Principled Decay

The strongest conclusion emerges from holding three findings in tension:

1. **Letta benchmark + Chase + Anthropic**: Simple files are surprisingly effective for memory
2. **Chroma context rot + OpenViking**: But dumping files into context degrades performance — tiered loading is essential
3. **Johns Hopkins forgetting research + FSRS-6**: And the index must decay, not just grow

Combined: **The optimal architecture for a solo power user is structured markdown files with tiered loading and principled access-frequency-based decay, exposed via MCP for cross-device access, with Notion as the navigational hub.**

This is not the most technically sophisticated approach. It is the approach that maximizes the ratio of value to complexity, accounts for the empirically demonstrated risks, and can be maintained by one person without dedicated infrastructure.

### Pre-Mortem: Why This Might Be Wrong

1. **MCP might not win.** If OpenAI or Google fragment the standard. Counter: Linux Foundation governance makes this unlikely.
2. **Context windows might grow fast enough.** If 10M+ tokens with solved attention become standard. Counter: cost and context rot are structural, not capacity problems.
3. **The file-based strategy might not scale.** At 10,000+ heterogeneous facts. Counter: that's when the vector/graph trigger fires (see §7).
4. **Notion might add friction.** If Notion's MCP server degrades or pricing changes. Counter: the architecture is Notion-convenient, not Notion-dependent; any structured database works.
5. **Privacy regulation might prohibit unified layers.** Counter: self-hosted, user-controlled systems avoid this.

---

## 10. References

### Academic Papers

- Sumers, Yao et al. "Cognitive Architectures for Language Agents (CoALA)" (arXiv:2309.02427, 2023; ACL 2024)
- "Memory in the Age of AI Agents: A Survey" (arXiv:2512.13564, December 2025)
- Park et al. "Generative Agents: Interactive Simulacra of Human Behavior" (UIST 2023)
- Packer et al. "MemGPT: Towards LLMs as Operating Systems" (2023)
- Shinn et al. "Reflexion: Language Agents with Verbal Reinforcement Learning" (NeurIPS 2023)
- HippoRAG (NeurIPS 2024) — knowledge graph as hippocampal index
- A-MEM (NeurIPS 2025) — Zettelkasten-inspired dynamic memory
- MEM1 (arXiv:2506.15841, June 2025) — RL-trained memory operations
- MAGMA (January 2026) — multi-graph agent memory architecture
- GAM "General Agentic Memory via Deep Research" (arXiv:2511.18423) — JIT memory assembly
- "Graph-Native Cognitive Memory for AI Agents" (arXiv:2603.17244) — AGM belief revision for memory
- Titans (NeurIPS 2025) — architecture-level memory
- MemoryOS (EMNLP 2025) — three-tier OS paging
- MemoryAgentBench (ICLR 2026) — standardized benchmark
- "Memory as Asset" (arXiv:2603.14212, March 2026) — user-owned memory framework
- SuperLocalMemory (arXiv:2603.14588, March 2026) — 87.7% LoCoMo SOTA
- MemOS (arXiv:2505.22101, arXiv:2507.03724) — Memory Operating System
- "Multi-Agent Memory from a Computer Architecture Perspective" (arXiv:2603.10062)
- "Beyond the Context Window" (arXiv:2603.04814) — cost-performance analysis
- "Memory Poisoning Attack and Defense" (arXiv:2601.05504) — MINJA attacks
- "From PKM to Second Brain to Personal AI Companion" (ACM CSCW 2025)
- AGENTPOISON (NeurIPS 2024) — red-teaming LLM agents via memory

### Tools & Frameworks

- Mem0: <https://github.com/mem0ai/mem0> | <https://mem0.ai>
- Zep/Graphiti: <https://github.com/getzep/graphiti> | <https://www.getzep.com>
- Letta (MemGPT): <https://github.com/letta-ai/letta>
- Cognee: <https://github.com/topoteretes/cognee>
- OpenViking: <https://github.com/volcengine/OpenViking>
- Hermes Agent: <https://github.com/NousResearch/hermes-agent> (Nous Research, Feb 2026)
- MemOS: <https://github.com/MemTensor/OpenMem>
- Agency Agents: <https://github.com/msitarzewski/agency-agents>
- NanoChat: <https://github.com/karpathy/nanochat>
- PromptFoo: <https://github.com/promptfoo/promptfoo>
- Impeccable: <https://github.com/pbakaus/impeccable>
- MiroFish: <https://github.com/666ghj/MiroFish>
- Heretic: <https://github.com/p-e-w/heretic>
- mcp-memory-service: <https://github.com/doobidoo/mcp-memory-service>
- Hindsight (Vectorize): <https://vectorize.io>
- LangMem: <https://blog.langchain.com/langmem-sdk-launch/>

### Standards & Protocols

- MCP: <https://modelcontextprotocol.io>
- AGENTS.md: <https://agents.md>
- Agentic AI Foundation: <https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation>

### Thought Leader Sources

- Karpathy on system prompt learning: <https://x.com/karpathy/status/1921368644069765486>
- Willison context engineering: <https://simonwillison.net/tags/context-engineering/>
- Swyx IMPACT framework: <https://www.latent.space/p/agent>
- Chase on memory: <https://blog.langchain.com/memory-for-agents/>
- Liu on RAG: <https://www.latent.space/p/llamaindex>
- Lee on knowledge graphs: <https://www.latent.space/p/ai-interfaces-and-notion>
- Anthropic context engineering: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Dubois agentic KM: <https://www.dsebastien.net/agentic-knowledge-management-the-next-evolution-of-pkm/>

### Security & Risk

- Context Rot — Chroma Research: <https://research.trychroma.com/context-rot>
- AI Recommendation Poisoning — Microsoft: <https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/>
- Indirect Prompt Injection — Palo Alto Unit42: <https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/>
- Agentic AI Threats — Lakera: <https://www.lakera.ai/blog/agentic-ai-threats-p1>
- Right to Be Forgotten — CSA: <https://cloudsecurityalliance.org/blog/2025/04/11/the-right-to-be-forgotten-but-can-ai-forget>
- Why KM Efforts Fail: <https://enterprise-knowledge.com/why-km-efforts-fail/>
- Johns Hopkins selective forgetting: <https://www.cs.jhu.edu/news/forget-me-not-selective-memory-can-help-ai-remember-more-not-less/>
- Engram (FSRS-6 for agent memory): <https://engram.lol/>
