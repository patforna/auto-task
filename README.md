# auto-task

An opinionated agentic workflow to automate a non-trivial slice of the software development lifecycle.

_auto-task_ turns well-defined units of work into shippable code with minimal human input. To achieve this, it uses git worktrees, persistent task state, fresh-context subagents, multi-model panels, TDD, and evidence-cited triage.

Built for experienced engineers who want to ship software at an accelerated pace but remain in control while doing so. **Think: cruise control, not Full Self-Driving.**

> [!NOTE]
> Extracted from my own daily workflow and shared early — rough edges included. Issues and feedback welcome.

## How It Works

At a high-level, a typical _auto-task_ session looks something like this:

1. **Explore:** You explore a topic, e.g. a product increment, a bug, an issue, a refactoring, etc.
2. **Scope:** Once your idea on what to build converges, you crystallise it into a *well-defined task* (remember: sh\*t in → sh\*t out).
3. **Build:** You hand the task over to agents to complete with full autonomy.
4. **Ship:** You review the work, potentially give feedback, and ship.

Under the hood, those four steps unfold as a fixed pipeline — you drive the ends, agents own the middle:

```text
create → clarify [ worktree · plan · impl · review · triage · fix · verify ] → ship-task
  (human)                           (autonomous)                             (human)
```

| Step            | What happens                                                                                                                                                                     |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Worktree**    | The task gets an isolated git worktree at a predictable path, with dependencies installed.                                                                                       |
| **Plan**        | Two models (Claude + Codex by default) independently write implementation plans; a synthesis merges them without forcing consensus.                                              |
| **Implement**   | A fresh-context subagent executes the plan test-first (strict TDD), committing as it goes.                                                                                       |
| **Review**      | Two independent models review in parallel — a structured Claude review and an adversarial pass from a different family (Codex by default).                                       |
| **Triage**      | Every finding gets an explicit disposition — accept or reject — with cited evidence. Mechanically-certain trivia auto-fixes; Critical/Major findings can never be auto-rejected. |
| **Fix**         | Accepted findings are fixed test-first; the fix itself gets re-reviewed.                                                                                                         |
| **Verify**      | An independent agent verifies every acceptance criterion against the actual behaviour, not the diff.                                                                             |
| **Ship**        | The workflow stops and reports what was found, fixed, rejected and why. You decide whether it ships.                                                                             |

See [`examples/sample-run.md`](examples/sample-run.md) for the verbatim report of a real run on defaults — including the triage decisions and the ship gate.

## Tasks

Tasks are plain markdown files stored in or outside of your repo (default: `tasks/`). They persist and carry state through the workflow: initially created by a human to capture intent (the why and what), then used across agent sessions to capture plans, track status, and log notes and review decisions.

```markdown
---
title: Stats command
date: 2026-07-02
status: ready-for-dev
type: feat
---

## Stats Command

Add a stats command that reads a file of newline-separated numbers and prints summary statistics.

### Acceptance Criteria

- `bun run stats <file>` prints one line: `count=<n> median=<m> p90=<p>`.
- Median: for an even count, the mean of the two middle values.
- A file with no numbers aborts with an error, exit code 1.
```

## Prerequisites

- [Claude Code](https://claude.com/product/claude-code)
- [Codex CLI](https://developers.openai.com/codex/cli) and [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) (strongly recommended; to enable multi-model-family panels)
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) (only required when reviewing UI changes)

## Installation

Open Claude Code and run:

```text
/plugin marketplace add patforna/auto-task
/plugin install at@auto-task
```

## Quick Start

Open Claude Code in your project's git repo:

1. Explore what to build.
2. Capture it using `/at:create-task`. Then review and tweak the task. Potentially re-run `/at:clarify-task`.
3. In a new session, run `/at:auto-task <task>`*.
4. Review what was built. Then run `/at:ship-task`.

*Expect a full run to take 20–40 minutes and spend a decent amount of tokens. `--lite` mode (single-pass plan, single reviewer, single task review) cuts that meaningfully — pass it explicitly, or let auto-task downshift automatically for small, single-package changes.

## Configuration

Defaults can be overridden per project in markdown.

- Project config: `.claude/auto-task.config.md` — Committed. Shared by everyone in the repo.
- Personal overrides: `.claude/auto-task.config.local.md` — Gitignored. Takes precedence over project config on conflict.

Configurable per project: task store, verification command, worktree layout, standing review context, design-review server, model roster, commit conventions, transcript capture, feedback snapshots. See [`examples/auto-task.config.md`](examples/auto-task.config.md) for every setting with its default — copy it into your repo and amend as needed.

## FAQ

**Why tasks and not specs?** A spec describes a system; a task describes a change — sized like 1–3 old-fashioned human-days, small enough to review honestly, big enough to matter. The task also outlives the chat: it's the only state that survives across sessions, so everything load-bearing must land in it.

**Why markdown config and not TOML/JSON?** Nothing parses the config — an agent reads it. Several entries are irreducibly prose (standing review context, domain review rules); the rest read better as one-line instructions than as string values quoted inside config syntax.

**Do I need Codex?** No, but the multi-model review is materially better than single-family review — it's the part of this workflow that has most reliably caught real bugs. Any second model family can fill the role via the Models setting.

**Can I use just parts of it?** Yes. Every step is its own `/at:` skill and runs standalone — `/at:review-code` on any diff, `/at:create-task` without the orchestrator, `/at:panel` for a multi-model take on anything. Type `/at:` in Claude Code for the full list. (`panel`, `synthesize`, and `tdd` are vendored from [core-skills](https://github.com/patforna/core-skills).)

**Where did this come from?** Six months of full-time agentic development on a real quant-research codebase, shaped by XP (small tasks, TDD, continuous integration) and a review protocol distilled from the code-review research literature.
