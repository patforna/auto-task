# Auto-Task

**An opinionated, end-to-end agentic task workflow for Claude Code: scope → plan → build → review → ship.**

Auto-task drives a well-defined task from intent to squash-merged commit with minimal human input — a git worktree, a two-model planning panel, test-first implementation by fresh-context subagents, independent adversarial code review, evidence-cited triage, and a human ship gate at the end.

Think cruise control, not Full Self-Driving: you own what to build and whether it ships; the workflow owns the distance in between.

![A real /at:auto-task run at 14x speed](docs/wordwise-demo.gif)

*A real, unedited run at 14× speed — plan panel, TDD implementation, adversarial review, triage, ship gate. Full recording: [`docs/wordwise-demo.cast`](docs/wordwise-demo.cast); final report: [`examples/sample-run.md`](examples/sample-run.md).*

## Quick Start

```text
/plugin marketplace add patforna/auto-task
/plugin install at@auto-task
```

Then, in any git repo:

1. Discuss what you want to build, then run `/at:create-task` — it crystallises the conversation into a task file under `tasks/` and clarifies ambiguities with you until a fresh agent could pick it up cold.
2. Run `/at:auto-task tasks/NNN-your-task.md` — it plans, implements, reviews, and fixes autonomously, then stops and shows you a triage report.
3. Review the report, then `/at:ship-task` — squash-merge, verify the integrated tree, push, clean up.

No server, no UI, no lock-in: tasks are plain markdown in your repo.

Expect a full `/at:auto-task` run to take 20–60 minutes and spend real tokens — it spawns a planning panel, an implementer, parallel reviewers, and re-reviews across two model families. `--lite` mode (single-pass plan, single reviewer, single task review) roughly halves that.

## The Workflow

```text
create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task
                            └────────────────── auto-task ───────────────────┘
```

Each skill also runs standalone; `/at:auto-task` orchestrates the middle of the pipeline and ends at a human ship gate (shipping is one of the options it offers you):

| Step            | What happens                                                                                                                                                                     |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Worktree**    | The task gets an isolated git worktree at a predictable path, with dependencies installed.                                                                                       |
| **Plan**        | Two models (Claude + Codex by default) independently write implementation plans; a synthesis merges them without forcing consensus.                                              |
| **Implement**   | A fresh-context subagent executes the plan test-first (strict TDD), committing as it goes.                                                                                       |
| **Review**      | Two independent reviews run in parallel — a structured Claude review and an adversarial pass from a different model family.                                                      |
| **Triage**      | Every finding gets an explicit disposition — accept or reject — with cited evidence. Mechanically-certain trivia auto-fixes; Critical/Major findings can never be auto-rejected. |
| **Fix**         | Accepted findings are fixed test-first; the fix itself gets re-reviewed.                                                                                                         |
| **Task review** | An independent agent verifies every acceptance criterion against the actual behaviour, not the diff.                                                                             |
| **Ship gate**   | The workflow stops and reports what was found, fixed, rejected and why. You decide whether it ships.                                                                             |

Why multiple models? Different model families have different blind spots. In practice the adversarial pass regularly catches real bugs the first reviewer missed — and the fix-review catches bugs in the fixes.

See [`examples/sample-run.md`](examples/sample-run.md) for the verbatim report of a real run on defaults — including the triage decisions and the ship gate.

## Tasks

Tasks are the workflow's persistent state: created by a human to capture intent (the why and what — never the how), then accumulating the plan, implementation notes, and review decisions as agents work. Anything that isn't in the task file or the repo doesn't exist for the next session — that constraint is the design.

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

- Location: `tasks/{NNN}-{slug}.md` — attachments in `tasks/attachments/{NNN}/`.
- Status lifecycle: `new` → `ready-for-dev` → `in-dev` → `ready-for-signoff` → `done` (plus `rejected`, `later`).
- Types: `feat`, `design`, `tech`, `bug`, `research`, `other`.
- Acceptance criteria are behavioural, specific, and testable — `/at:create-task` documents the full discipline, including epics.

## Project Bindings

Every default above can be overridden per project — in markdown, not config syntax, because bindings are instructions the agent reads (several are prose, like standing review context), not values code parses.

- **`.claude/auto-task.config.md`** — project bindings. Committed, shared by everyone in the repo.
- **`.claude/auto-task.config.local.md`** — personal overrides. Gitignored; wins over the project file on conflict.

Precedence: plugin defaults ← project bindings ← local overrides. Copy [`examples/auto-task.config.md`](examples/auto-task.config.md) into your repo and edit — it lists every recognised section with its default:

| Binding            | Default                                                    | Override examples                                        |
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

## Requirements and Integrations

- **Claude Code** — the only hard requirement. Skills are namespaced `/at:` and invoked explicitly; nothing auto-triggers.
- **Codex plugin (optional)** — if [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) is installed (`/plugin marketplace add openai/codex-plugin-cc`, then install `codex`), planning and adversarial review use Codex as the second model family. Without it, a second fresh-context Claude subagent takes that role (weaker: same family, same blind spots).
- **chrome-devtools MCP (optional)** — used by `/at:review-design` to verify UI changes against a spec with real browser input.

This plugin is self-contained: it vendors its generic dependencies (`panel`, `synthesize`, `tdd`) from [core-skills](https://github.com/patforna/core-skills), so nothing else needs to be installed.

## Skills

Workflow: `auto-task`, `create-task`, `clarify-task`, `plan-task`, `impl-task`, `review-code`, `review-task`, `ship-task`, `review-design`. Vendored: `panel`, `synthesize`, `tdd`.

## FAQ

**Why tasks and not specs?** A spec describes a system; a task describes a change — sized like 1–3 old-fashioned human-days, small enough to review honestly, big enough to matter. The task also outlives the chat: it's the only state that survives across sessions, so everything load-bearing must land in it.

**Why markdown bindings and not TOML/JSON?** Nothing parses the bindings — an agent reads them. Several bindings are irreducibly prose (standing review context, domain review rules); the rest read better as one-line instructions than as string values quoted inside config syntax.

**Do I need Codex?** No, but the multi-model review is materially better than single-family review — it's the part of this workflow that has most reliably caught real bugs. Any second model family can fill the role via the Models binding.

**Can I use just parts of it?** Yes. Every skill runs standalone — `/at:review-code` on any diff, `/at:create-task` without ever running the orchestrator.

**Where did this come from?** Six months of full-time agentic development on a real quant-research codebase, shaped by XP (small tasks, TDD, continuous integration) and a review protocol distilled from the code-review research literature.

## Status

Early and opinionated (pre-1.0), extracted from daily personal use. Shared as-is; issues and feedback welcome. See [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
