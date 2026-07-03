# Beads — Steve Yegge's Agent Memory System

Research session: 2026-03-06

## Context

Investigating whether Beads (or ideas from it) should be integrated into TAD's agent workflow. Currently thinking about agent memory, session continuity, and task orchestration — see `/write-story`, `/play-story`, `/impl` skills and the `specs/` directory.

---

## What Beads Is

Beads (`bd`) is a git-backed, dependency-aware issue tracker designed as **external memory for AI coding agents**. Created by Steve Yegge (~Oct 2025), written in Go (~130K LOC, half tests), ~12.6K GitHub stars.

Core problem: agents have amnesia. Every new session is "50 First Dates." Markdown plans degrade into competing, contradicting files that confuse agents rather than guiding them.

Beads is not "issue tracking for agents" — it's **structured external memory** with dependency tracking and query capabilities.

Repository: <https://github.com/steveyegge/beads>

## How It Works Technically

| Layer          | Detail                                                                                |
| -------------- | ------------------------------------------------------------------------------------- |
| **Storage**    | `.beads/beads.jsonl` — JSONL in git for diffability                                   |
| **Query**      | Local SQLite cache for fast SQL queries (~10ms)                                       |
| **IDs**        | Hash-based like `bd-a1b2` — collision-resistant for multi-agent                       |
| **Hierarchy**  | `bd-a3f8` (epic) → `bd-a3f8.1` (task) → `bd-a3f8.1.1` (subtask)                       |
| **Links**      | `blocks`, `parent-child`, `relates_to`, `duplicates`, `supersedes`, `discovered-from` |
| **Compaction** | "Memory decay" — old closed tasks get semantically summarized                         |
| **Modes**      | Stealth (local only), Contributor (separate repo), Maintainer                         |

Key CLI commands:

- `bd ready` / `bd ready --json` — primary work-discovery: shows tasks with no blockers
- `bd create "Title" -p 0` — create a priority-0 task
- `bd update <id> --claim` — atomically assign + mark in-progress
- `bd dep add <child> <parent>` — establish dependency
- `bd show <id>` — full detail + audit trail
- `bd prime` — generates ~1-2K token context summary for agent consumption

Agents integrate via `AGENT_INSTRUCTIONS.md` in the `.beads` directory.

## The Ecosystem

### Gas Town (`steveyegge/gastown`)

Multi-agent orchestration layer built on Beads. Coordinates 20-30 parallel Claude Code agents using:

- **Mayor** — central coordinator agent
- **Polecats** — worker agents with persistent identities (stored as Beads)
- **Rigs** — project containers wrapping git repos
- **Convoys** — work packages bundling multiple beads, assigned to agents
- Git worktrees for workspace isolation

~189K LOC of Go. Represents "developer as factory operator managing agent swarms." Burns ~$100/hour in tokens at peak. Work generation (planning) becomes the bottleneck, not implementation.

Repository: <https://github.com/steveyegge/gastown>

### Beads Viewer (`Dicklesworthstone/beads_viewer`)

Jeffrey Emanuel's graph-aware TUI for Beads:

- 9 graph-theoretic metrics (PageRank, betweenness centrality, HITS, critical path)
- DAG visualization of task dependencies
- Kanban board view
- **Robot mode** (`--robot-triage`, `--robot-next`, `--robot-plan`) for agent consumption
- Time-travel diffing across git revisions
- Built in Go with Bubble Tea (60fps rendering)

Repository: <https://github.com/Dicklesworthstone/beads_viewer>

### Beads Rust (`Dicklesworthstone/beads_rust`)

Emanuel's Rust port — deliberate "classic beads" snapshot because the Go version evolved toward Gas Town. With Steve's endorsement.

| Aspect            | br (Rust)    | beads (Go)  |
| ----------------- | ------------ | ----------- |
| Lines of code     | ~20K         | ~276K       |
| Git operations    | Explicit     | Auto-commit |
| Binary size       | 5-8 MB       | 30+ MB      |
| Background daemon | No           | Yes         |
| Storage           | SQLite+JSONL | Dolt        |

Repository: <https://github.com/Dicklesworthstone/beads_rust>

### Agentic Coding Flywheel (`Dicklesworthstone/agentic_coding_flywheel_setup`)

Emanuel's bootstrapper: fresh Ubuntu VPS → complete multi-agent dev environment in ~30 minutes. Beads is one component alongside Claude Code, Codex CLI, Gemini CLI, and coordination tooling.

Repository: <https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup>

## Landing the Plane — Session Handoff Protocol

The most practically useful pattern from Beads. When an agent hears "let's land the plane," it must complete ALL steps before ending:

1. **File remaining work** — discovered-but-unfinished work → new bead issues
2. **Pass quality gates** — lint, test. If gates fail, file P0 issues
3. **Update issue state** — close completed, update in-progress
4. **Mandatory push** — `git pull --rebase && git push`. The plane has NOT landed until push succeeds
5. **Clean git state** — `git stash clear`, prune remotes
6. **Generate handoff prompt** — concise "Next Session Prompt" containing:
   - What was accomplished this session
   - The immediate next step
   - Known problems needing attention

Counterpart: **"Preflight the plane"** at session start:

- `bd prime` — fresh workflow context
- `bd ready --json` — what to work on
- `bd update <id> --claim` — atomic claim

The two form a closed loop: land → handoff → new session → preflight → work → land → ...

Key insight: the magic is making this **mandatory and non-negotiable**. Agents will happily stop mid-task if you let them. The protocol turns session boundaries from context loss into context crystallization.

## Beads Vs GitHub Issues

Yegge addresses this in the [FAQ](https://github.com/steveyegge/beads/blob/main/docs/FAQ.md). Five concrete differences:

### 1. Latency and Offline

GitHub Issues: 100-500ms+ per API call, rate-limited. Beads: ~10ms local SQLite. Agents do a lot of tracker interaction — at GH latency this drags; at local latency it's invisible.

### 2. Deterministic Work Discovery (`bd ready`)

Computes transitive blocking relationships offline. GitHub has basic blocks/blocked-by but no transitive resolution, no built-in "what's ready?" concept, no `discovered-from` dependency type. Agent would need to load issues, parse relationships, build dependency graph in-context — consuming tokens for bookkeeping instead of coding.

### 3. Git-First Vs Cloud-First

| Dimension       | GitHub Issues       | Beads                                |
| --------------- | ------------------- | ------------------------------------ |
| Data location   | GitHub's servers    | `.beads/` in your repo               |
| Branching       | Global per-repo     | Branch-scoped task memory            |
| Merge conflicts | Manual close-as-dup | Auto-resolution, reference rewriting |
| ID scheme       | Sequential integers | Hash-based — no collision on merge   |
| Offline         | No                  | Yes, fully                           |

Branch-scoping: agent on a feature branch has its own task context that merges cleanly back to main. GitHub Issues is global.

### 4. Agent Ergonomics

- Every `bd` command supports `--json`
- `bd update <id> --claim` is atomic (no race conditions)
- `bd prime` gives compressed "here's your world" snapshot
- No interactive editors, no confirmations, no browser

### 5. Memory Compaction

GitHub accumulates forever. Beads: old closed tasks get semantically summarized, keeping active working set small. Directly addresses context window budget.

## Honest Limitations

From multiple independent reviewers:

1. **"Beads provides the memory. You provide the discipline to use it."** — agents won't spontaneously use it without explicit prompting
2. **Context drift** — even with hooks, long sessions cause agents to forget cleanup
3. **Manual handoffs** — session starts require explicit "check bd ready" prompts
4. **Merge friction** — Yegge himself calls it "a crummy architecture"
5. **Cost** — Gas Town at scale burns ~$100/hour in tokens
6. **Work generation bottleneck** — agents churn through tasks so fast that planning becomes the bottleneck

## Relevance to TAD

### What TAD Already Has That Overlaps

| TAD System                       | Beads Equivalent                               |
| -------------------------------- | ---------------------------------------------- |
| `specs/*.md` with frontmatter    | Beads issues with priority/status              |
| `/write-story` → `/play-story`   | `bd create` → `bd ready` → `bd update --claim` |
| Story status (draft/in-dev/done) | Bead status lifecycle                          |
| Epic files with story index      | Bead parent-child hierarchy                    |
| `CLAUDE.md` as memory            | `AGENT_INSTRUCTIONS.md` as memory              |
| Acceptance criteria in specs     | Acceptance criteria in beads                   |
| `/impl` parallel worktrees       | Gas Town's polecat worktrees                   |

### Where Beads Adds Something TAD Lacks

1. **Queryable state** — `bd ready --json` gives agents machine-readable "what next" that spec files don't
2. **Dependency graph** — formal `blocks` relationships with transitive resolution
3. **Memory compaction** — automatic summarization of old completed work
4. **Audit trail** — every change logged (specs rely on git history)
5. **Session handoff protocol** — "landing the plane" with automated next-session prompt

### Where Beads Would Add Complexity Without Clear Value

1. **Solo dev** — Gas Town's multi-agent orchestration is for 20-30 agents; TAD runs 1-2 at most
2. **Spec workflow already works** — `/write-story` → `/play-story` is clean and battle-tested
3. **Focused codebase** — ~16 specs; markdown is fine at this scale
4. **Setup overhead** — Go binary, `.beads/` init, agent training
5. **Discipline problem solved differently** — skill-based approach already embeds workflow discipline

### Assessment

**Don't integrate Beads into TAD now.** The spec-based workflow is effectively a lightweight, bespoke version tuned to a solo-dev quant workflow.

**Worth stealing:**

1. **Landing the plane** — add a step to `/play-story` for incomplete sessions: file discovered work as draft specs, generate a handoff prompt
2. **Machine-readable task discovery** — a simple script parsing frontmatter (`status: draft/in-dev`) would give agents the `bd ready` equivalent
3. **Memory compaction** — periodic summarization of old MEMORY.md entries

**Revisit when:** 3+ parallel agents regularly, spec count >50, or session continuity becomes painful despite the spec system.

## Sources

- [steveyegge/beads — GitHub](https://github.com/steveyegge/beads)
- [beads/docs/FAQ.md — GitHub](https://github.com/steveyegge/beads/blob/main/docs/FAQ.md)
- [beads/AGENT_INSTRUCTIONS.md — GitHub](https://github.com/steveyegge/beads/blob/main/AGENT_INSTRUCTIONS.md)
- [steveyegge/gastown — GitHub](https://github.com/steveyegge/gastown)
- [Dicklesworthstone/beads_viewer — GitHub](https://github.com/Dicklesworthstone/beads_viewer)
- [Dicklesworthstone/beads_rust — GitHub](https://github.com/Dicklesworthstone/beads_rust)
- [Dicklesworthstone/agentic_coding_flywheel_setup — GitHub](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup)
- [Beads: Memory for your Agent — Ian Bull](https://ianbull.com/posts/beads/)
- [Beads: Memory for Coding Agents — paddo.dev](https://paddo.dev/blog/beads-memory-for-coding-agents/)
- [GasTown and the Two Kinds of Multi-Agent — paddo.dev](https://paddo.dev/blog/gastown-two-kinds-of-multi-agent/)
- [Wrapping my head around Gas Town — Justin Abrahms](https://justin.abrah.ms/blog/2026-01-05-wrapping-my-head-around-gas-town.html)
- [Long-running Agentic Work with Beads — DoltHub](https://www.dolthub.com/blog/2026-01-27-long-running-agentic-work-with-beads/)
- [Landing the Plane — AI-Assisted Software Development](https://ai-assisted-software-development.com/landing-the-plane/)
- [AI Agent Integration — DeepWiki](https://deepwiki.com/steveyegge/beads/8-ai-agent-integration)
- [Beads — bruton.ai](https://bruton.ai/blog/ai-trends/beads-bd-missing-upgrade-your-ai-coding-agent-needs-2026)
- [Beads: A Git-Friendly Issue Tracker — Better Stack](https://betterstack.com/community/guides/ai/beads-issue-tracker-ai-agents/)
- [Gas Town, Beads, and the Rise of Agentic Development — SE Daily](https://softwareengineeringdaily.com/2026/02/12/gas-town-beads-and-the-rise-of-agentic-development-with-steve-yegge/)
