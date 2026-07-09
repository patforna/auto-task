# auto-task

An opinionated agentic workflow to automate a non-trivial slice of the software development life cycle (SDLC).

_auto-task_ turns well-defined units of work into shippable code with minimal human input. To achieve this, it uses git worktrees, persistent task state, fresh-context subagents, multi-model panels, TDD, and evidence-cited triage.

I imagine _auto-task_ will be most useful to experienced engineers who want to ship software at an accelerated pace but remain in control while doing so. **Think: cruise control, not Full Self-Driving.** 🙃

> [!NOTE]
> Extracted from my own daily workflow and shared early — rough edges included. Issues and feedback welcome.

## Typical Workflow

At a high-level, a typical _auto-task_ session looks something like this:

1. **Explore:** You explore a topic, e.g. a product increment, a bug, an issue, a refactoring, etc.
2. **Scope:** Once your idea on what to build converges, you crystallise it into a *well-defined task* (remember: sh\*t in → sh\*t out).
3. **Build:** You hand the task over to agents to complete with full autonomy.
4. **Ship:** You review the work, potentially give feedback, and ship.


TODO: Add terminal cast

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

*Expect a full run to take 20–40 minutes and spend a decent amount of tokens.

## The Workflow

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

## Configuration

Defaults can be overridden per project in markdown.

- Project config: `.claude/auto-task.config.md` — Committed. Shared by everyone in the repo.
- Personal overrides: `.claude/auto-task.config.local.md` — Gitignored. Takes precedence over project config on conflict.

[`examples/auto-task.config.md`](examples/auto-task.config.md) lists every recognised section with its default — an easy way to get started is to copy it into your repo and amend as needed:

| Setting            | Default                                                    | Override examples                                        |
| ------------------ | ---------------------------------------------------------- | -------------------------------------------------------- |
| Task store         | `tasks/` in the repo, agent-managed                        | A separate sibling repo + helper recipes                 |
| Verification       | Auto-discover (a `just`/`make` check recipe, CI, tests)    | `npm run check`                                          |
| Worktrees          | `../<repo>.worktrees/NNN-<slug>` + dependency install      | A pinned path + a `worktree-init` script                 |
| Review             | No standing context                                        | Focus text appended to adversarial reviews; domain rules |
| Design review      | Auto-discover a fixture-backed server, else fail loudly    | A fixture-backed serve command                           |
| Models             | Claude (strongest) + Codex panel; Codex adversarial review | Different panelists, implementer, or reviewer            |
| Conventions        | Repo's own commit style + `(task/NNN)` subject suffix      | Conventional Commits; merge commits instead of squash    |
| Transcript capture | Skipped                                                    | A capture command + out-of-repo destination              |
| Feedback snapshots | Skipped                                                    | An out-of-repo snapshot directory                        |

## Skills

All skills are namespaced under `/at:` and run standalone.

| Skill           | One-liner                                                   |
| --------------- | ----------------------------------------------------------- |
| `auto-task`     | Run the whole pipeline on a task, hands-off until shipping.  |
| `create-task`   | Turn a conversation into a scoped, well-defined task file.   |
| `clarify-task`  | Surface ambiguities and pin down vague criteria.            |
| `plan-task`     | Produce an implementation plan for a task.                  |
| `impl-task`     | Execute a plan test-first, committing as it goes.           |
| `review-code`   | Review any diff for correctness, design, and security.      |
| `review-design` | Review a UI change against its design spec.                 |
| `review-task`   | Check a task meets its intent and acceptance criteria.      |
| `panel`         | Get independent takes from multiple models on any question. |
| `synthesize`    | Merge those takes into one view without forcing consensus.  |
| `tdd`           | Drive new code with strict red/green/refactor.              |
| `ship-task`     | Finish up: mark done, merge, clean up.                      |

* `clarify-task` runs automatically at the end of `create-task`; invoke it directly to re-validate a task you've hand-edited.
* `panel`, `synthesize`, and `tdd` are vendored from [core-skills](https://github.com/patforna/core-skills).

## FAQ

**Why tasks and not specs?** A spec describes a system; a task describes a change — sized like 1–3 old-fashioned human-days, small enough to review honestly, big enough to matter. The task also outlives the chat: it's the only state that survives across sessions, so everything load-bearing must land in it.

**Why markdown config and not TOML/JSON?** Nothing parses the config — an agent reads it. Several entries are irreducibly prose (standing review context, domain review rules); the rest read better as one-line instructions than as string values quoted inside config syntax.

**Do I need Codex?** No, but the multi-model review is materially better than single-family review — it's the part of this workflow that has most reliably caught real bugs. Any second model family can fill the role via the Models setting.

**Can I use just parts of it?** Yes. Every skill runs standalone — `/at:review-code` on any diff, `/at:create-task` without ever running the orchestrator.

**Where did this come from?** Six months of full-time agentic development on a real quant-research codebase, shaped by XP (small tasks, TDD, continuous integration) and a review protocol distilled from the code-review research literature.