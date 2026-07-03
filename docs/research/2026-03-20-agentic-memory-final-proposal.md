# Agentic Memory & Knowledge Management: Final Implementation Proposal

**Status:** rejected — too overengineered; auto-memory is sufficient for now **Date**: 2026-03-20

---

## Thesis

Memory as code is the primary strategy. Extend what already exists (CLAUDE.md, MEMORY.md, Notion MCP, gws CLI) into a coherent three-tier knowledge system with tiered context loading, principled decay, and an agent-initiated compounding loop. Add infrastructure only when measurable triggers fire. Each phase delivers standalone value.

---

## Design Principles (Non-Negotiable)

1. **Human approves every memory write** from agent-proposed or external sources. This is a security constraint (MINJA: 95% injection storage rate, 70% end-to-end attack success), not a workflow preference.
2. **The markdown foundation must always work alone.** If Notion, Cloudflare, and Zep all change pricing simultaneously, the system must still function via files.
3. **Every knowledge item carries provenance and trust level** as first-class fields, not comments.
4. **Triggers, not vibes.** Phase advancement requires observable events, not feelings.
5. **Forgetting is a feature.** The system decays low-access items rather than accumulating indefinitely.

---

## Architecture Overview

```text
TIER 0 — PROCEDURAL MEMORY (files, always loaded, highest trust)
├── ~/.claude/CLAUDE.md           — global: identity, tools, preferences, knowledge nav
├── <repo>/CLAUDE.md              — project: domain rules, commands, gotchas
├── <repo>/AGENTS.md              — cross-model mirror (from Day 1)
└── ~/.claude/projects/*/memory/  — auto memory + knowledge_map.md (L0 index)

TIER 1 — NAVIGATIONAL MAP (Notion, fetched on demand via MCP)
├── Knowledge Map database        — L1 overviews, typed, with provenance + decay metadata
├── Decisions Log database        — settled choices, prevents re-litigation
└── Reading Library database      — books + highlights (auto-synced via Readwise)

TIER 2 — SEMANTIC STORE (remote MCP, added at Phase 2 trigger)
└── Cloudflare Worker + D1        — cross-device queryable memory, scoped API keys

TIER 3 — CONTENT (stays in place, accessed via MCP bridges)
├── Gmail / Drive / Docs / Sheets — via gws CLI (read-only by default)
├── GitHub                        — via gh CLI + GitHub MCP
└── Notion pages                  — via Notion MCP
```

---

## Tiered Context Loading (L0/l1/l2)

Informed by OpenViking's architecture (+46% task completion, -82% input tokens) and Chroma's context rot research (performance degrades with more context, even on simple tasks):

| Tier | Tokens    | Where It Lives                  | When Loaded                       |
| ---- | --------- | ------------------------------- | --------------------------------- |
| L0   | <100/item | `knowledge_map.md` in memory/   | Every session (always in context) |
| L1   | <2000     | Notion Knowledge Map database   | When agent identifies relevance   |
| L2   | Full      | Original source (Drive, GitHub) | Only for deep work via MCP fetch  |

**Example L0 entry** in `knowledge_map.md`:

```text
investing/kelly-sizing: Half-Kelly position sizing for portfolio allocation [Notion: Knowledge Map > Kelly Criterion] [Trust: user] [Last: 2026-03]
coding/polars-over-pandas: Use Polars for all dataframe ops, never pandas [Decision: 2025-11] [Trust: user]
books/thinking-fast-slow: System 1/2 framework for decision biases [Notion: Reading Library] [Trust: user]
```

---

## Phase 1: Foundation (Week 1, ~6 Hours, $8/Month)

### What You Build

**1. Knowledge Map file** — `~/.claude/projects/-Users-patric-github-tad/memory/knowledge_map.md` (2 hours)

Seed with 30-50 L0 entries across domains: investing axioms, coding conventions, system layout, key decisions, book insights. One line per entry, following the format above. This is the agent's first-read navigational index.

**2. Notion Knowledge Map database** (1.5 hours)

| Property     | Type   | Purpose                                                        |
| ------------ | ------ | -------------------------------------------------------------- |
| Name         | Title  | Human-readable name                                            |
| L0Summary    | Text   | One-sentence summary (<100 tokens)                             |
| L1Overview   | Text   | Structured overview (<2000 tokens)                             |
| Type         | Select | axiom / principle / decision / rule / reference / skill        |
| Domain       | Select | investing / coding / personal / research / system              |
| Source       | Select | user / gmail / drive / notion / github / book / agent-proposed |
| SourceURL    | URL    | Link to original content                                       |
| Trust        | Select | user-authored / agent-proposed / external-derived              |
| LastVerified | Date   | When this entry was last confirmed valid                       |
| AccessCount  | Number | How often agents have loaded this (L1)                         |
| ValidFrom    | Date   | When this fact became true (forward-compat for temporal)       |
| Status       | Select | active / stale / superseded / archived                         |

Views:

- **By Domain** — grouped by Domain, sorted by AccessCount desc
- **Stale Entries** — filter: LastVerified older than 90 days, Status = active
- **Agent-Proposed** — filter: Trust = agent-proposed, for review queue

Seed 20 entries from existing MEMORY.md files and known knowledge.

**3. Decisions Log database** (1 hour)

| Property       | Type          | Purpose                                  |
| -------------- | ------------- | ---------------------------------------- |
| Decision       | Title         | What was decided                         |
| Context        | Text          | Why this came up                         |
| Alternatives   | Text          | What was considered and rejected         |
| Rationale      | Text          | Why this option won                      |
| Date           | Date          | When decided                             |
| Domain         | Select        | investing / coding / system / personal   |
| Outcome        | Select        | open / validated / reversed / superseded |
| ReversedBy     | Relation(self)| Points to the decision that replaced this|

Seed 10-15 decisions: no PRs, Polars over pandas, Kelly half-sizing, stay with Notion (not Obsidian), etc.

**4. Reading Library database + Readwise sync** (1 hour setup, then automatic)

| Property       | Type          | Purpose                                  |
| -------------- | ------------- | ---------------------------------------- |
| Title          | Title         | Book/article title                       |
| Author         | Text          | Author name                              |
| Category       | Select        | investing / psychology / tech / other    |
| KeyInsight     | Text          | 1-3 sentence synthesis                   |
| HighlightCount | Number        | Auto from Readwise                       |
| Status         | Select        | reading / finished / abandoned           |
| RelatedKM      | Relation      | Links to Knowledge Map entries           |

Setup:

- Readwise account ($7.99/month) — captures Kindle, Blinkist, web highlights
- Configure Readwise → Notion sync (automatic, runs throughout the day)
- One-time Goodreads CSV export → import to Reading Library
- Blinkist: Readwise browser extension captures future highlights; past content is manual

**5. AGENTS.md in active repos** (30 minutes)

Add `AGENTS.md` to tad and system repos. Content mirrors the essential project context from CLAUDE.md — build commands, conventions, domain terminology. This costs 30 minutes now and prevents a disruptive migration if another model enters the picture.

**6. CLAUDE.md updates** (30 minutes)

Add to `~/.claude/CLAUDE.md`:

```markdown
## Knowledge Navigation

When starting a session that involves domain knowledge:

1. Read ~/.claude/projects/*/memory/knowledge_map.md for L0 context
2. If a topic appears in the map, fetch the L1 overview from Notion via MCP
3. Only fetch L2 (full source) when deep work requires it

When writing to Gmail or Drive via gws CLI: read-only by default. Do not store facts derived from emails or web content in memory without explicit user approval.

## Session Compounding

At the end of any session lasting more than 30 minutes or involving a non-trivial decision or learning:

- Proactively ask: "Should any of today's learnings be added to MEMORY.md or the knowledge map?"
- Propose specific additions with Trust level and Domain
- Wait for user approval before writing
- If a decision was made, propose a Decisions Log entry
```

This makes the agent initiate the compounding loop — shifting the burden from "user remembers to run an alias" to "agent proactively asks."

### Phase 1 Compounding Loop

```text
Session runs → agent works → session ends (>30 min)
    ↓
Agent proactively proposes:
    - New knowledge_map.md L0 entries
    - New Notion Knowledge Map L1 entries (via MCP)
    - Decisions Log entries for any settled choices
    - MEMORY.md updates for session-specific learnings
    ↓
Human reviews in ~5 minutes → approves/edits/rejects
    ↓
Quarterly: Review knowledge_map.md → promote repeated MEMORY.md
patterns into CLAUDE.md rules (procedural hardening)
```

### Phase 1 Freshness Mechanism

- Map entries carry `LastVerified` date
- Notion "Stale Entries" view flags anything >90 days unverified
- Monthly: 20-minute review via Stale Entries view (add to Dagu as a reminder)
- `AccessCount` tracked — entries with AccessCount=0 at 180 days are candidates for archival

### Phase 1 Value

- **Week 1**: Agents orient faster, navigate knowledge map, don't re-litigate settled decisions
- **Month 1**: 50-80 knowledge map entries, 15+ decisions logged, reading highlights flowing in
- **Month 3**: 100-150 entries, CLAUDE.md has earned procedural rules, agents are measurably better informed

### Phase 1 Cost

| Item        | One-time | Monthly                                                     |
| ----------- | -------- | ----------------------------------------------------------- |
| Setup       | ~6 hours | —                                                           |
| Readwise    | —        | $7.99                                                       |
| Maintenance | —        | ~2 hours (30 min/week session-end + 20 min/month freshness) |

---

## Phase 2: Cross-Device Memory (Trigger-Gated)

### Trigger Conditions (Require at Least ONE)

- You've wanted to continue a Claude session on a different device and couldn't
- You use Claude iOS/Android more than 3 times per week and need context from CLI sessions
- A second AI model (Cursor, Gemini CLI) enters regular use

### What You Build (~4-6 Hours, $0/Month Additional)

Deploy a remote MCP memory server on Cloudflare Workers (free tier):

**Option A**: Evaluate `doobidoo/mcp-memory-service` for Cloudflare Workers deployment — it claims hybrid local+cloud mode. If it works: deploy, configure, done (2 hours).

**Option B** (fallback): Build a minimal custom Worker (~300 lines TypeScript) with these tools:

- `memory_store` — direct write (user-scoped, highest trust)
- `memory_propose` — write to pending queue (agent/external, requires approval)
- `memory_recall` — semantic search over stored facts
- `memory_list_pending` — show unapproved proposals

**Schema** (D1/SQLite):

```sql
CREATE TABLE memories (
  id          TEXT PRIMARY KEY,
  content     TEXT NOT NULL,
  type        TEXT CHECK(type IN ('semantic','episodic','procedural')),
  domain      TEXT,
  source      TEXT,
  source_url  TEXT,
  trust       TEXT CHECK(trust IN ('user','agent','external')),
  valid_from  TEXT,  -- ISO date, forward-compat for temporal
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  tags        TEXT,  -- comma-separated
  status      TEXT DEFAULT 'active'
);
```

Note: `valid_from` is included from Day 1 so temporal migration later is not a schema redesign.

**Authentication**: Per-client API keys with scopes:

- Desktop/CLI: read + write
- Mobile: **read-only by default**
- Admin: read + write + approve-pending

**Configuration**: Configure the Worker URL once at `claude.ai` → syncs to Claude Desktop, Web, iOS, Android automatically. Same URL works for any other MCP-compatible client.

**Seed**: Migrate existing MEMORY.md entries to the remote store. Keep MEMORY.md as the audit trail — write to both.

### Phase 2 Value

- Cross-device: Claude on phone knows what Claude Code learned yesterday
- Cross-model: same URL works for Cursor, Gemini CLI, any MCP client
- Audit trail: every memory has provenance, trust level, and creation date

---

## Phase 3: Temporal Knowledge (Trigger-Gated)

### Trigger Conditions (Require at Least ONE)

- You manually write supersession notes in MEMORY.md more than 5 times in a quarter ("I used to think X, now I think Y")
- An investing thesis changes more than 3 times in a quarter
- You need to answer "what did I believe about X in Q3 2025?" and can't

**Note**: This trigger is domain-specific, not corpus-size-specific. An investor with 50 actively evolving theses needs temporal infrastructure before a developer with 500 stable coding rules.

### What You Build (~8-10 Hours, $25/Month)

**Recommended: Zep Cloud** ($25/month, no feature gating) — bi-temporal knowledge graph with MCP server, no Neo4j to maintain.

If data sovereignty is paramount: self-host Graphiti on Hetzner CX22 ($6.50/month) + Neo4j Community Edition. Use Ollama for entity extraction (no OpenAI dependency for sensitive data). Budget 20+ hours for first-time setup.

**What Zep/Graphiti adds**:

- Every fact carries `valid_from` and `valid_until` timestamps
- Superseded facts are invalidated, not deleted — "what was true at time X" is a first-class query
- Hybrid retrieval: semantic embeddings + BM25 keyword + graph traversal
- The Cloudflare Worker (Phase 2) becomes a thin proxy to Zep, or is replaced by Zep's MCP server

**With Zep Cloud**: quarterly data export to portable format as insurance against the Limitless scenario.

### Phase 3 Value

- Temporal queries: "How has my GOOG thesis evolved since 2024?"
- Belief revision: when you change your mind, the old belief is preserved with context
- The investing use case — where beliefs have explicit time validity — gets first-class support

---

## Phase 4: Semantic Search at Scale (Trigger-Gated)

### Trigger Conditions (Require at Least ONE)

- Knowledge map exceeds 500 entries
- Semantic miss rate exceeds 20% (agents can't find what you know exists)
- You need fuzzy similarity search ("what have I read that's related to X?")

### What You Build

Add vector search to the existing Zep/remote MCP layer. If using Zep Cloud, this is already included. If self-hosted, add embedding-based retrieval to Graphiti.

At this scale, evaluate whether a Notion Business plan ($20/user/month) for AI Connectors (Gmail, Drive, GitHub indexing, hourly updates) provides enough value to justify the cost — it makes Notion's built-in search span all connected services without custom pipelines.

---

## What This Proposal Explicitly Does NOT Do

| Excluded                                     | Why                                                                     |
| -------------------------------------------- | ----------------------------------------------------------------------- |
| Automated memory writes from Gmail/web       | Poisoning vector — human gate is non-negotiable                         |
| Sleep-time compute / overnight consolidation | Premature — prove the manual loop works for 90 days first               |
| Raw session transcript archiving             | Too noisy, large poisoning surface, compounding loop produces summaries |
| Vector search before Phase 4                 | File + Notion navigation is sufficient under 500 entries                |
| Replace CLAUDE.md with a database            | Files are the foundation that survives all infrastructure               |
| Obsidian migration                           | User prefers Notion; architecture works with Notion                     |
| Full GAM (JIT assembly) implementation       | Research-stage; the principle (keep raw + compressed) is adopted        |

---

## Go/No-Go Checkpoints

### 30-Day Check

- Count knowledge_map.md entries. If under 20: the compounding loop is not firing — diagnose why
- Count Decisions Log entries. If under 5: decisions are being made without being recorded
- Is the agent proactively asking about memory at session end? If not: review the CLAUDE.md instruction
- Is Readwise syncing highlights to Notion? Verify the pipeline works

### 90-Day Check

- Has cross-device friction occurred? If yes: evaluate Phase 2 trigger
- Have you written manual supersession notes? If yes >5 times: evaluate Phase 3 trigger
- Review the Stale Entries view — how many entries are >90 days unverified?
- Is the quarterly CLAUDE.md hardening ritual happening? If not: simplify it

### 180-Day Check

- Review AccessCount distribution. Entries with AccessCount=0: candidates for archival
- Has the system saved measurable time or prevented re-work? If you can't point to specific instances, re-evaluate the maintenance investment

---

## Total Investment Summary

| Phase   | Trigger              | Hours    | Monthly Cost | Cumulative |
| ------- | -------------------- | -------- | ------------ | ---------- |
| Phase 1 | Immediate            | ~6       | $8 (Readwise)| $8/mo      |
| Phase 2 | Cross-device need    | ~4-6     | $0 (CF free) | $8/mo      |
| Phase 3 | Temporal pain        | ~8-10    | $25 (Zep)    | $33/mo     |
| Phase 4 | Scale (500+ entries) | ~4       | $0-20        | $33-53/mo  |

**Phase 1 alone delivers 80%+ of the value.** Each subsequent phase is independently justified by its trigger condition.

---

## Quick-Start Checklist

- [ ] Create `knowledge_map.md` — seed 30-50 L0 entries (2h)
- [ ] Create Notion Knowledge Map database with schema above (30m)
- [ ] Seed 20 Notion entries with L1 overviews (1h)
- [ ] Create Notion Decisions Log database — seed 10-15 decisions (1h)
- [ ] Set up Readwise account + Notion sync + Goodreads CSV import (1h)
- [ ] Add `AGENTS.md` to tad and system repos (30m)
- [ ] Update `~/.claude/CLAUDE.md` with Knowledge Navigation + Session Compounding sections (15m)
- [ ] Add monthly "knowledge freshness review" to Dagu (15m)
- [ ] Verify: start a Claude Code session and confirm the agent reads knowledge_map.md
- [ ] Verify: at session end, confirm the agent proactively asks about memory additions

---

## Provenance

This proposal synthesizes the strongest elements from 5 independent proposals:

| Source                  | Contribution to Final Proposal                                            |
| ----------------------- | ------------------------------------------------------------------------- |
| P1 (Minimalist)         | Foundation discipline, honest effort estimates, existing-workflow respect |
| P2 (Notion-Centric)     | Decisions Log, Reading Library + Readwise, Trust classification           |
| P3 (MCP-Native)         | Per-client scoped API keys, propose/approve write boundary                |
| P4 (Temporal KG)        | Domain-specific temporal triggers, self-hosted sovereignty argument       |
| P5 (Hybrid Progressive) | Trigger-gated phases, `just eom` ritual, AGENTS.md from Day 1             |

Refined by three cross-examinations focused on implementability, architectural soundness, and value delivery. Informed by the research document's synthesis: "Memory as Code + Tiered Loading + Principled Decay."
