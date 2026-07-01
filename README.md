# Auto-Task

A Claude Code plugin providing an opinionated, end-to-end agentic task workflow: plan, implement, review, and ship a well-defined task with minimal human input.

## Install

```
/plugin marketplace add patforna/auto-task
```

Then install `auto-task@auto-task` from the marketplace.

## Self-Contained

This plugin vendors its generic dependencies (`panel`, `synthesize`, `tdd`) so it works standalone — no need to also install `core-skills`.

## Skills

Workflow: `auto-task`, `create-task`, `clarify-task`, `plan-task`, `impl-task`, `review-code`, `review-task`, `ship-task`, `review-design`. Vendored: `panel`, `synthesize`, `tdd`.

## Caveat

The workflow currently assumes TAD conventions (`just` recipes, the sibling `tad-tasks` repo). Decoupling it from those is future work.
