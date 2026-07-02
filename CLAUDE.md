# CLAUDE.md — auto-task Plugin

## Vendored Skills — Do Not Edit Here

`skills/panel`, `skills/synthesize`, and `skills/tdd` are **vendored copies** from the
`core-skills` plugin (`~/github/core-skills`), which is their source of truth. Do **not**
edit them in this repo — edits here will be overwritten on the next re-vendor and silently
diverge from core-skills.

To change one of them: edit it in `core-skills`, then re-vendor here by running
`scripts/vendor.sh`. It copies the three dirs and rewrites `/core-skills:` → `/at:` —
the **only** way the vendored copies differ from the originals (keeping this plugin
self-contained). Then bump the version in `.claude-plugin/plugin.json` +
`.claude-plugin/marketplace.json` and refresh the installed plugin:
`claude plugin marketplace update auto-task && claude plugin update at@auto-task`.

## Internal Skill References

This plugin is self-contained: its skills invoke each other via the `/at:<skill>`
namespace (never bare `/<skill>`), so they resolve regardless of what else is installed. The
only external dependency is the `codex` plugin (`/codex:*`).
