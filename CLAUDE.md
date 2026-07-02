# CLAUDE.md — Auto-Task Plugin

## Vendored Skills — Do Not Edit Here

`skills/panel`, `skills/synthesize`, and `skills/tdd` are **vendored copies** from the [core-skills](https://github.com/patforna/core-skills) plugin (a sibling checkout; `scripts/vendor.sh` takes its path as an argument), which is their source of truth. Do **not** edit them in this repo — edits here will be overwritten on the next re-vendor and silently diverge from core-skills.

To change one of them: edit it in `core-skills`, then re-vendor here by running `scripts/vendor.sh`. It copies the three dirs and rewrites `/core-skills:` → `/at:` — the **only** way the vendored copies differ from the originals (keeping this plugin self-contained). Then bump the version in `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` and refresh the installed plugin: `claude plugin marketplace update auto-task && claude plugin update at@auto-task`.

## Internal Skill References

This plugin is self-contained: its skills invoke each other via the `/at:<skill>` namespace (never bare `/<skill>`), so they resolve regardless of what else is installed. The only external reference is the `codex` plugin (`/codex:*`), which is **optional** — skills must degrade gracefully (documented fallback) when it is not installed.

## Portability

Skills must stay project-agnostic: generic instructions with sensible defaults, and any project-specific behaviour sourced from the consuming repo's bindings — `.claude/auto-task.md` (project) and `.claude/auto-task.local.md` (personal overrides, win on conflict). Never hardcode a specific project's paths, recipes, conventions, or context into a skill body.

When adding or renaming a binding, update all three places in the same change: the skill(s) that consume it, `examples/auto-task.md` (the copy-paste template), and the README's bindings table.
