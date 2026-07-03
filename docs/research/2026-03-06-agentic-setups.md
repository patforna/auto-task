# Agentic Coding Setups: Yegge, Emanuel, Steinberger

Research into the GitHub repositories and agentic workflows of three prominent AI-assisted developers, compared against our own TAD setup.

Date: 2026-03-06

---

## Steve Yegge (@Steveyegge)

### Profile

Former Google/Amazon engineer. GitHub profile has 18k+ stars across repos, all built predominantly with AI agents. Key repos:

| Repo             | Stars  | Description                                       |
| ---------------- | ------ | ------------------------------------------------- |
| `beads`          | 18,177 | Memory/issue tracker for coding agents (`bd` CLI) |
| `gastown`        | 11,099 | Multi-agent workspace manager (`gt` CLI)          |
| `efrit`          | 404    | Native Elisp coding agent running in Emacs        |
| `vc`             | 313    | AI-orchestrated coding agent colony               |
| `mcp_agent_mail` | 35     | Inter-agent mail/coordination via MCP             |

### Tools

- **Primary agent:** Claude Code
- **Secondary:** OpenAI Codex CLI, Gemini CLI, Amp (as worker agents)
- **Models:** Claude Sonnet 4.5 (AI Supervisor), GPT-5 Pro (planning), Grok4/Opus (iteration)
- **Infrastructure:** Beads (Dolt-backed issue tracker), Gas Town (multi-agent orchestrator), MCP Agent Mail

### Agent Configuration

Uses dual-file convention: `AGENTS.md` (tool-agnostic) + `CLAUDE.md` (Claude-specific), one redirecting to the other.

**`.claude/settings.json` hooks (from `beads` repo):**

- `block-gh-watch.sh` — blocks `gh run watch` (burns 1200 API req/hr)
- `block-interactive-cmds.sh` — blocks `cp`, `mv`, `rm` without `-f` flag (macOS interactive aliases)

**`.claude/settings.json` hooks (from `mcp_agent_mail` repo):**

- **SessionStart:** check active file reservations and pending acknowledgments
- **PreToolUse (Edit):** check for soon-expiring file reservations
- **PostToolUse (send_message):** list acknowledgments
- **PostToolUse (reserve_file_paths):** list reservations

**Slash commands:** `/plan-to-beads` converts Claude Code plans into epic + task hierarchies. `/handoff` sends mail to next session.

### Workflow — "Land the Plane" Protocol

His signature session-end discipline:

1. File remaining work as Beads issues
2. Run quality gates (tests, linters)
3. Update/close Beads issues
4. `git pull --rebase && git push` — mandatory, non-negotiable
5. Clean up stashes, prune branches
6. Verify clean state
7. Provide a follow-up prompt for the next session

Key enforcement: "NEVER say 'ready to push when you are' — YOU must push." Exists because multiple agents + unpushed work = severe rebase conflicts.

### Multi-Agent Architecture (Gas Town)

- **Mayor** (primary Claude Code instance) coordinates everything
- **Rigs** are project containers wrapping git repos
- **Polecats** are worker agents with persistent identity but ephemeral sessions
- **Hooks** provide git-worktree-based persistent storage surviving crashes
- **Convoys** bundle multiple beads for assignment
- Scales to 20-30 agents (vs. 4-10 becoming chaotic without it)

### Key Principles

- **Zero Framework Cognition (ZFC):** all decisions delegated to AI, no heuristics or regex in orchestration
- **Nondeterministic Idempotence:** workflows can crash and resume, AI figures out where it left off
- **Commit and push after every fix** — no batching
- **Pre-landing review:** if >100 lines changed or core files modified, re-read implementation before declaring done
- **"NEVER delete a file without express permission"** (ALL CAPS in AGENTS.md)

---

## Jeffrey Emanuel (@Dicklesworthstone)

### Profile

Former long/short equity analyst at NYC hedge funds. Building with deep learning since 2010, multi-agent systems since 2023. Consults PE/hedge funds on AI automation. 172 public repos, 16.7k+ GitHub stars.

### Tools

- **Primary:** Claude Code via `cc` alias: `ENABLE_BACKGROUND_TASKS=1 claude --dangerously-skip-permissions`
- **Secondary:** OpenAI Codex CLI, Google Gemini CLI (pre-configured but secondary)
- **Workflow:** Terminal-first, not IDE-first
- **Infrastructure:** 14-tool "Agentic Coding Flywheel", dedicated VPS (64GB RAM)

### The 14-Tool Flywheel

| Tool                        | Language   | Purpose                                                     |
| --------------------------- | ---------- | ----------------------------------------------------------- |
| MCP Agent Mail (1.7k stars) | Python     | Messaging, file leases, audit trails for multi-agent coord  |
| Claude Code Agent Farm      | Python     | Orchestrates 20-50+ Claude Code sessions via tmux           |
| Beads Viewer                | Go         | PageRank-powered task prioritization TUI                    |
| CASS                        | Rust       | Unified search across 11+ agent session formats             |
| CASS Memory System          | TypeScript | Three-layer cognitive memory: episodic, working, procedural |
| NTM (Named Tmux Manager)    | Go         | Multi-agent tmux orchestration with dashboards              |
| DCG                         | Rust       | SIMD-accelerated guard that blocks dangerous commands       |
| UBS (Ultimate Bug Scanner)  | Bash       | 1,000+ pattern bug detection, runs as pre-commit hook       |
| SLB                         | Go         | Two-person rule enforcement for risky operations            |
| Meta Skill                  | Rust       | Skill management with Thompson sampling optimization        |
| XF                          | Rust       | Sub-millisecond search over X/Twitter archives              |
| RU (Repo Updater)           | Bash       | Sync hundreds of Git repos with one command                 |
| GIIL                        | Bash       | Image downloading from cloud share links                    |
| ACFS (Flywheel Setup)       | Bash       | One-command VPS bootstrap in 30 minutes                     |

### Agent Configuration — AGENTS.md Patterns

Uses `AGENTS.md` (Codex convention, Claude Code also respects it). Key rules:

- **Rule 0 — Human Override:** "If I tell you to do something, even if it goes against what follows below, YOU MUST LISTEN TO ME."
- **Rule 1 — Never Delete Files:** ALL CAPS, blanket prohibition, requires explicit written permission
- **Irreversible Command Prohibition:** `git reset --hard`, `git clean -fd`, `rm -rf` forbidden without explicit user authorization + 5-step escalation protocol
- **No Script-Based Code Changes:** regex batch transforms banned, all changes must be manual
- **No File Proliferation:** creating `file_v2.py` variants banned, existing files revised in place
- **No Backwards Compatibility:** in early-dev repos, bans compatibility shims
- **Search Online When Uncertain:** if not 100% sure about a library's API, must search docs

Uses **Claude hooks** — `on-file-write.sh` hook runs UBS (Ultimate Bug Scanner) on every file save.

### Multi-Agent Coordination

Runs 10-20+ agents simultaneously. Two coordination approaches:

**1. Agent Farm:** tmux panes, each running a Claude Code session.

**2. Cooperating Agents Protocol:** `/coordination/` directory with:

- `active_work_registry.json`
- Lock files
- Work queue
- Agents claim work, check conflicts, update status every 30 min
- Implemented entirely through prompting — no custom code, just an Opus-class model following the protocol

### Philosophy

> "The bottleneck in software isn't writing code — it's coordination. Build the right tooling and you can run a dozen frontier-model agents on the same repo at the same time, delivering in days what used to take months."

- **Intellectual humility toward frontier models** — accept they are superhuman with right tooling
- **Unix philosophy adapted for agents** — focused, composable tools
- **Separation of cognition** — use agents for plans first, code second
- **Daily forward progress** — specific prompts ensure progress on every active project

---

## Peter Steinberger (@Steipete)

### Profile

Founder of PSPDFKit (exited 2021). Based in Vienna/London. "Polyagentmorous builder." Joined OpenAI in February 2026. 50+ active repos, most built predominantly with AI agents.

### Tool Evolution

| Period         | Primary Agent      | IDE / Editor        | Notes                              |
| -------------- | ------------------ | ------------------- | ---------------------------------- |
| Early-mid 2025 | Claude Code        | Cursor (Gemini 2.5) | Claude Code as "main driver"       |
| Mid 2025       | Claude Code        | Cursor + VS Code    | Multiple model strategy            |
| Late 2025      | Codex CLI (OpenAI) | Ghostty terminal    | Switched citing rate limits        |
| Current (2026) | Codex CLI          | Ghostty + VS Code   | Joined OpenAI; 3-8 parallel agents |

### Agent Configuration — AGENTS.MD

Uses `AGENTS.MD` (not CLAUDE.md) as primary instruction file. Lives at `~/Projects/agent-scripts/AGENTS.MD` (~800 lines, telegraphic style).

**Repo:** `steipete/agent-scripts` contains:

- `AGENTS.MD` — master rules file
- `tools.md` — catalog of CLI tools available on his machines
- `scripts/` — shared utilities (`committer`, `browser-tools.ts`, `docs-list.ts`, `trash.ts`)
- `skills/` — 16 reusable skill files (oracle, create-cli, swift-concurrency-expert, etc.)

**Shared + local pattern:** per-repo AGENTS.md uses `<shared>...</shared>` block (identical across repos, synced from agent-scripts) plus repo-local sections.

**Telegraphic style:** instructions deliberately terse. "Telegraph; noun-phrases ok; drop grammar; min tokens." Minimises context consumption.

### Key Workflow Patterns

1. **"Just Talk To It"** — rejects elaborate frameworks, RAG, complex tooling. Direct conversation, develop intuition through experience.
2. **CLIs over MCPs** — strongly prefers CLI tools. Quote: "if you add MCPs, you just clutter up the context." Ships custom CLIs (`bird`, `peekaboo`, `sonoscli`, etc.) with single-line `--help` documentation.
3. **Main branch, no PRs** — works directly on main with multiple agents. No feature branches.
4. **Spec-first for complex work** — Gemini's large context generates specs, separate AI critically reviews ("give me 20 points that are underspecified"), then hands `docs/spec.md` to agent.
5. **Screenshots are prompts** — ~50% of prompts include screenshots. Visual context faster than text.
6. **Tests after implementation, same context** — write tests in the same session as code, catches bugs immediately.
7. **20% refactoring budget** — allocates time for cleanup, dead code, dependency updates.
8. **`--dangerously-skip-permissions`** — full system access, relies on hourly backups (Arq + SuperDuper) as safety net.

### Custom Tooling

| Tool              | Purpose                                                |
| ----------------- | ------------------------------------------------------ |
| `oracle`          | Cross-validate with a second model (GPT-5.2 Pro)       |
| `peekaboo`        | Screenshot capture + GUI automation                    |
| `committer`       | Safe git staging and commit wrapper                    |
| `bird`            | Twitter/X CLI                                          |
| `claude-code-mcp` | Run Claude Code as MCP tool inside other agents        |
| `poltergeist`     | Universal hot-reload file watcher                      |
| `docs-list.ts`    | Walks `docs/`, enforces front-matter, prints summaries |

---

## Memory Management Systems — Deep Dive

### Beads (Yegge) — the Task Graph

**What it is:** distributed, git-backed graph issue tracker built specifically for AI agents. Written in Go, backed by Dolt (version-controlled SQL database).

**Core data model:** a "bead" is a task/issue with: hash-based ID (`bd-a1b2`), title, description, status, priority (0-4), type (bug/feature/task/epic/chore), dependencies, labels, comments, agent state tracking.

**Hierarchical IDs:** dotted notation for epic decomposition:

- `bd-a3f8` (Epic)
- `bd-a3f8.1` (Task under epic)
- `bd-a3f8.1.1` (Subtask)

**Dependency system:** 10+ relationship types (blocks, parent-child, related, discovered-from, conditional-blocks, waits-for, replies-to, duplicates, supersedes). `bd dep tree` visualises the graph. `bd dep cycles` detects circular dependencies.

**Killer feature:** `bd ready` — computes transitive closure of blocking dependencies locally (~10ms, offline) and returns only truly unblocked tasks.

**Why Dolt over alternatives:**

1. Cell-level 3-way merge — two agents modifying different fields of same issue merge automatically
2. Hash-based IDs prevent collisions across branches
3. Multi-writer support via server mode
4. Native branching independent of git
5. Full SQL query capability
6. Built-in sync via remotes
7. Every mutation is a commit with full history

**Claude Code integration:**

- Claude Plugin (`plugin.json`) with 29 command definitions
- **SessionStart hook:** `bd prime` injects workflow context
- **PreCompact hook:** `bd prime` re-injects before context compaction (ensures agent doesn't forget beads)
- MCP server option (Python, but CLI preferred — 1-2k tokens vs 10-50k)
- `bd setup claude` configures hooks automatically
- `/plan-to-beads` slash command converts plans into epic + task hierarchies

**Strengths:** persistent agent memory across sessions, dependency-aware work selection, offline-first, hierarchical decomposition, compaction survival.

**Weaknesses:** heavyweight Dolt dependency, overkill for solo/simple projects, alpha software (v0.9.x), opaque storage (need CLI to read), no web UI, large surface area (29 commands, 10+ dep types).

### CASS Memory System (Emanuel) — the Learning Engine

**What it is:** three-layer cognitive memory architecture for AI coding agents. Transforms raw session logs into a persistent, cross-agent knowledge base of distilled rules.

**Three memory layers:**

| Layer      | Name     | Purpose                                                        | Format                     |
| ---------- | -------- | -------------------------------------------------------------- | -------------------------- |
| Episodic   | cass     | Raw ground truth — full session transcripts from all agents    | JSONL/JSON indexed by cass |
| Working    | Diary    | Structured session summaries: decisions, challenges, learnings | `~/.cass-memory/diary/`    |
| Procedural | Playbook | Distilled, confidence-tracked rules with maturity lifecycle    | `playbook.yaml`            |

Flow: **Episodic -> Working -> Procedural** (raw logs summarised into diary entries, distilled into playbook rules).

**The ACE Pipeline (four stages):**

1. **Generator** (`cm context "<task>" --json`): hydrates agent with relevant rules, anti-patterns, history snippets before a task
2. **Reflector** (`cm reflect --days N`): LLM-powered pattern extraction from unprocessed sessions
3. **Validator** (evidence gate): proposed rules verified against session history
4. **Curator** (deterministic, NO LLM): applies rule changes, resolves conflicts. Deliberately avoids LLM to prevent feedback loops.

**Scoring algorithm:**

```text
effectiveScore = decayedHelpful - (4 * decayedHarmful)
decayFactor = 0.5 ^ (daysAgo / 90)
```

4x harmful multiplier = bad rules die fast. 90-day half-life = stale rules fade. Rules with 3+ harmful marks auto-convert into anti-pattern warnings.

**Maturity transitions:**

- candidate -> established: 3+ helpful, <25% harmful ratio
- established -> proven: 10+ helpful, <10% harmful ratio
- Any -> deprecated: >25% harmful or explicit deprecation

**Integration:** `cm context` CLI before tasks, `cm guard --install` for Claude Code pre-tool hook (Trauma Guard), MCP server option, cross-agent learning (sessions from any agent feed same knowledge base).

**Strengths:** cross-agent learning, confidence decay with harmful bias, deterministic curator (no LLM feedback loops), evidence-backed rules, anti-pattern auto-conversion, local-first, YAML playbooks (git-friendly), budget controls.

**Weaknesses:** complexity (31+ source files, external binary dependency), requires active maintenance (`cm reflect`, `cm mark`, `cm outcome`), LLM cost for reflection ($1-15/month), cold start problem, Bun runtime requirement.

### Steinberger — Curated Files

No dedicated memory system. Knowledge lives in version-controlled files that agents read at startup.

**Layers:**

| Layer               | Mechanism                                         | Scope           |
| ------------------- | ------------------------------------------------- | --------------- |
| Shared guardrails   | `AGENTS.MD` (pointer pattern across repos)        | All projects    |
| Docs / runbooks     | `docs/` with `read_when` front-matter + list      | Per-repo        |
| Skills              | `skills/` directory with packaged expertise       | Domain-specific |
| External notes      | Obsidian vault, ad-hoc markdown files             | Personal        |
| Per-project context | Minimal `CLAUDE.md` with repo-specific essentials | Single repo     |
| Inline capture      | "Make a concise note in AGENTS.MD"                | Ongoing         |

**Key patterns:**

- `read_when:` front-matter in docs tells agents WHEN to read each doc
- `scripts/docs-list.ts` enumerates available docs at agent startup (lazy knowledge loading)
- AGENTS.MD grows organically — "make a concise note in there" during work
- No databases, no binaries, no APIs, no costs

**Philosophy:** knowledge is best curated by humans, not extracted by LLMs. The tradeoff is manual effort, but for a solo dev the effort is small.

### Comparison Table

| Dimension            | Simple Markdown | Beads                | CASS Memory                  |
| -------------------- | --------------- | -------------------- | ---------------------------- |
| Setup cost           | Zero            | Install bd + Dolt    | Install cm + cass + API keys |
| Running cost         | Free            | Free                 | $1-15/month LLM              |
| Cross-agent          | Manual          | Full                 | Full                         |
| Confidence tracking  | None            | None                 | Decay-weighted               |
| Stale rule handling  | Manual review   | `bd compact`         | 90-day auto-decay            |
| Task dependencies    | Manual          | Full DAG (10+ types) | None                         |
| Ready-work detection | None            | `bd ready` (~10ms)   | None                         |
| Offline              | Yes             | Yes                  | Yes                          |
| Search               | grep            | Full SQL             | Full-text + semantic         |
| Dependencies         | None            | Go + Dolt            | Bun + cass + LLM             |

---

## TAD's Current Setup

### Agentic Configuration

- **Primary tool:** Claude Code (Opus)
- **Instructions:** `CLAUDE.md` (project, ~95 lines)
- **Agents:** `python-expert`, `quant-advisor` (domain-specific advisory agent with checklist)
- **Skills:** `impl` (divergent Opus+Codex generation), `tdd`, `write-story`, `play-story`
- **Commands:** `domain-review`, `full-review`
- **Hooks:** Stop hook (code review gate reviewing diffs against CLAUDE.md rules), PreToolUse hook (block destructive commands)
- **MCP servers:** Notion
- **Plugins:** context7, github
- **Permissions:** selective allow-list (`just check`, `git pull`)

### Knowledge / Memory System

| Layer            | File                          | Purpose                                           |
| ---------------- | ----------------------------- | ------------------------------------------------- |
| Rules            | `CLAUDE.md`                   | Agent behavior, coding conventions, quant gotchas |
| Domain knowledge | `docs/knowledge.md`           | Glossary, research journal, technical insights    |
| Decisions        | `docs/decisions.md`           | ADR-style register with rationale + superseded    |
| Agent memory     | `.claude/memory/MEMORY.md`    | Cross-session preferences, workflow config        |
| Strategy         | `docs/vision-and-strategy.md` | Strategic direction and rationale                 |

### GitHub Workflows

- `claude.yml` — @claude trigger on issues/PRs/comments
- `claude-code-review.yml` — daily automated review with commit-range tracking, confidence thresholds, `last-reviewed` tag

### Strengths Vs the Three

1. **Stop hook as code review gate** — none of the three have automated diff-against-rules review
2. **Domain-specific agent (quant-advisor)** — specialised advisory with checklist, unique
3. **write-story/play-story workflow** — most structured exploration->spec->implementation pipeline
4. **Daily automated review workflow** — most sophisticated CI-level review of the four
5. **impl skill (divergent generation)** — Opus+Codex parallel worktrees with comparative review

---

## Convergent Patterns (All Three Agree)

1. **Never delete files without permission** — all three, ALL CAPS in Yegge and Emanuel
2. **Mandatory verification after changes** — quality gates before declaring done
3. **Explicit destructive command restrictions** — hooks or binary guards
4. **Session continuity / handoff** — follow-up prompts, memory systems, or structured specs
5. **Spec-first for complex work** — plan before coding

## Recommendations for TAD

### Adopted (This Session)

1. PreToolUse hook blocking destructive commands (inspired by Yegge)
2. `just commit` wrapper for atomic safe commits (inspired by Steinberger's `committer`)
3. Removed push restriction from CLAUDE.md

### Worth Considering

1. **`read_when:` front-matter on docs/** (Steinberger) — tells agents when to read each doc without loading everything. Zero cost, immediately useful.
2. **Session-end knowledge capture convention** — extend play-story's "Codify Learnings" step to ad-hoc sessions. "Did anything surprising happen?"
3. **"Current Focus" section in MEMORY.md** — orient agent at session start with active work, open questions, recently completed. Manual but survives across sessions.
4. **Oracle pattern for quant logic** (Steinberger) — cross-validate signal computations with a second model. Lighter weight than `/impl` for spot-checking.
5. **CLI-first tool design** (Steinberger) — expose recurring operations as `just` recipes that agents call naturally.

### Skip for Now

| System             | Why Skip                                                                     | Revisit When                                  |
| ------------------ | ---------------------------------------------------------------------------- | --------------------------------------------- |
| Beads              | Heavyweight Dolt dep; specs/stories handle task structure; solo dev          | Running 3+ parallel agents regularly          |
| CASS Memory        | Requires active feedback loops; LLM cost; knowledge.md works                 | Re-learning same lessons across many sessions |
| Confidence scoring | Daily review catches drift; manual curation more accurate for small rule set | CLAUDE.md grows past ~200 lines               |

---

## Sources

### Steve Yegge

- [steveyegge GitHub](https://github.com/steveyegge)
- [steveyegge/beads](https://github.com/steveyegge/beads)
- [steveyegge/gastown](https://github.com/steveyegge/gastown)
- [steveyegge/mcp_agent_mail](https://github.com/steveyegge/mcp_agent_mail)

### Jeffrey Emanuel

- [Dicklesworthstone GitHub](https://github.com/Dicklesworthstone)
- [jeffreyemanuel.com](https://jeffreyemanuel.com)
- [Agent Flywheel](https://agent-flywheel.com)
- [claude_code_agent_farm](https://github.com/Dicklesworthstone/claude_code_agent_farm)
- [cass_memory_system](https://github.com/Dicklesworthstone/cass_memory_system)
- [mcp_agent_mail](https://github.com/Dicklesworthstone/mcp_agent_mail)

### Peter Steinberger

- [steipete GitHub](https://github.com/steipete)
- [steipete/agent-scripts](https://github.com/steipete/agent-scripts)
- [steipete/claude-code-mcp](https://github.com/steipete/claude-code-mcp)
- [My Current AI Dev Workflow](https://steipete.me/posts/2025/optimal-ai-development-workflow) (Aug 2025)
- [Just Talk To It](https://steipete.me/posts/just-talk-to-it) (Oct 2025)
- [Claude Code is My Computer](https://steipete.me/posts/2025/claude-code-is-my-computer) (Jun 2025)
- [Essential Reading for Agentic Engineers](https://steipete.me/posts/2025/essential-reading)
