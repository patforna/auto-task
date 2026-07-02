# Auto-Task

A Claude Code plugin providing an opinionated, end-to-end agentic task workflow: plan, implement, review, and ship a well-defined task with minimal human input.

```text
create-task → clarify-task → plan-task → impl-task → review-code → review-task → ship-task
                            └───────────────────── auto-task ─────────────────────────────┘
```

`/at:auto-task` drives the middle of that pipeline autonomously: it creates a git worktree, plans (multi-model panel + synthesis), implements test-first, runs independent code reviews plus an adversarial pass, triages findings with cited reasons, reviews the task against its acceptance criteria, and stops at a human ship gate.

## Install

```text
/plugin marketplace add patforna/auto-task
```

Then install `at@auto-task` from the marketplace. Skills are namespaced `/at:` (e.g. `/at:auto-task`).

## The Task Convention

Tasks are markdown files the agent manages with plain file I/O — no extra tooling required.

- Location: `tasks/{NNN}-{slug}.md` in your repo ({NNN} = next number, zero-padded to 3).
- Frontmatter: `title`, `date`, `status`, `type`.
- Status lifecycle: `new` → `ready-for-dev` → `in-dev` → `ready-for-signoff` → `done` (plus `rejected`, `later`).
- Types: `feat`, `design`, `tech`, `bug`, `research`, `other`.
- Attachments (briefs, screenshots, sample data): `tasks/attachments/{NNN}/`.

`/at:create-task` documents the full convention, including epics.

## Project Bindings

Projects can override the defaults in a `.claude/auto-task.md` file at the repo root. Every skill reads it first if it exists. Recognised bindings (all optional — plain markdown sections the agent reads, not a machine-parsed schema):

| Binding             | Default                                                    | Override example                                    |
| ------------------- | ---------------------------------------------------------- | --------------------------------------------------- |
| Task store          | `tasks/` in the repo, agent-managed                        | A separate sibling repo + helper recipes            |
| Verification        | Auto-discover (a `just`/`make` check recipe, CI, tests)    | `just check-all`                                     |
| Worktrees           | `../<repo>.worktrees/NNN-<slug>` + dependency install      | A pinned path + a `worktree-init` recipe             |
| Review context      | None                                                       | Standing focus text appended to adversarial reviews  |
| Design review       | None (skill requires a fixture-backed serve command)       | `just serve test`                                    |
| Transcript capture  | Skipped                                                    | A capture command + out-of-repo destination          |
| Feedback snapshots  | Skipped                                                    | An out-of-repo snapshot directory                    |

## Self-Contained

This plugin vendors its generic dependencies (`panel`, `synthesize`, `tdd`) so it works standalone — no need to also install [core-skills](https://github.com/patforna/core-skills).

Optional integration: if the [Codex plugin](https://github.com/openai/codex-plugin-cc) is installed, the review step uses `/codex:adversarial-review` as the independent adversarial reviewer; otherwise a second fresh-context Claude subagent takes that role.

## Skills

Workflow: `auto-task`, `create-task`, `clarify-task`, `plan-task`, `impl-task`, `review-code`, `review-task`, `ship-task`, `review-design`. Vendored: `panel`, `synthesize`, `tdd`.
