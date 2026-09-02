# auto-task config refactor — consolidated plan v3 (post-Codex, post-scope/security decisions)

## 0. What auto-task is (context)

`auto-task` is a **Claude Code plugin** — skills namespaced `/at:*` (`create-task`, `clarify-task`, `plan-task`, `impl-task`, `review-code`, `review-design`, `review-task`, `ship-task`, `auto-task` [orchestrator], + vendored `panel`/`synthesize`/`tdd`). Drives a unit of work end-to-end: create → clarify → worktree → plan → implement → review → triage → fix → verify → ship. Public plugin, installed into arbitrary consuming repos. Skills stay project-agnostic; repo-specific facts come from config.

**Load-bearing fact: nothing machine-parses the config — an LLM agent reads it at runtime.** No parser, no schema.

## 1. Problems with the current mechanism

1. Bad onboarding: copy `examples/auto-task.config.md` from the plugin cache, delete 7 of 9 sections, edit 2.
2. Defaults sprinkled across 3–7 places (template + create-task § + orchestrator steps + a boilerplate line in 5 skills). Live `<!-- TODO: de-dupe -->` in `auto-task/SKILL.md` admits it.
3. Stale-copy shadowing: a copied-but-unedited section freezes today's default and shadows a future plugin default.
4. Prose too long where a labelled line would do.
5. Meta-rot: CLAUDE.md's "three places" rule names a README "config table" that no longer exists.

## 2. Design

### 2.1 Single source of truth: `/at:config` skill

`skills/config/SKILL.md` owns the canonical settings+defaults AND the resolve procedure:
```
├── § Settings & Defaults   ← canonical table: static defaults + human at-a-glance doc + heading→setting map
├── § Detection             ← how "auto"/"if-installed" defaults resolve locally (narrow — see 2.4)
├── § Resolve               ← merge algorithm → emits the strict resolved block (see 2.7)
├── § Resolved-block grammar← the v1 contract (see 2.7)
├── § Inspect (no args)     ← print resolved block + lint (unknown / copied-default headings)
└── § Init (--init)         ← interactive scaffolder: detect + ask-the-rest + write overrides-only
```
Lazy capture (ask-and-persist on an un-inferable gap) is included too (see §4).

### 2.2 Settings vs workflow core

**Settings** (configurable; canonical value lives only in § Settings & Defaults; read via the resolved block; never restated in skills). The canonical table:

| Setting                          | Default                                                    | Resolved by        | Override (heading → label)             |
| :------------------------------- | :--------------------------------------------------------- | :----------------- | :------------------------------------- |
| `settings.task_store.location`   | `tasks/` at repo root                                      | static             | `## Task Store` → `location:`          |
| `settings.task_store.create`     | create `{location}/{NNN}-{slug}.md` (NNN = max+1, 3-digit; frontmatter + body); attachments in `{location}/attachments/{NNN}/` | static | `## Task Store` → `create:` |
| `settings.task_store.status`     | edit the task file's `status:` frontmatter field in place  | static             | `## Task Store` → `status:`            |
| `settings.verify`                | auto-discover: `just/make check` → `check`/`test` script → full suite | **detected** | `## Verification` (prose/cmd)          |
| `settings.worktree.path`         | `../<repo>.worktrees/NNN-<slug>`                           | static             | `## Worktrees` → `path:`               |
| `settings.worktree.init`         | install deps + copy gitignored runtime files (`.env`)      | static             | `## Worktrees` → `init:`               |
| `settings.models.implementer`    | strongest available model                                  | static (agent)     | `## Models` → `implementer:`           |
| `settings.models.adversarial`    | `codex` if present, else fresh Claude subagent             | **detected**       | `## Models` → `adversarial:`           |
| `settings.models.panel`          | strongest Claude + `codex` if present                      | **detected**       | `## Models` → `panel:`                 |
| `settings.design_review_server`  | none (fail loudly on UI changes)                           | readiness detected | `## Design Review` (cmd)               |
| `settings.conventions.suffix`    | `(task/NNN)` on commit subjects                            | static             | `## Conventions` → `suffix:`           |
| `settings.conventions.merge`     | `squash`                                                   | static             | `## Conventions` → `merge:`            |
| `settings.review_context`        | `""` (none)                                                | static             | `## Review` (free prose)               |
| `settings.transcript_capture`    | skipped                                                    | static             | `## Transcript Capture` (cmd+dir)      |
| `settings.feedback_snapshots`    | skipped                                                    | static             | `## Feedback Snapshots` (dir+exemplar) |

Only three settings touch the environment (codex presence, a check recipe/script, Chrome MCP presence); the rest are static.

**Workflow core** (NOT configurable; inline in skills): TDD loop, review severity taxonomy, triage accept/reject, verify-behaviour-not-diff, AC-by-AC verification, fresh-context-per-step.

A setting factors out the *value/choice*, not the *procedure it selects* (e.g. `settings.conventions.merge` picks squash vs merge-commit; both procedures stay in ship-task).

### 2.3 Canonical names, `settings.`-prefixed

Internal names carry `settings.` — used at skill reference sites, in the resolved block, and in the § Settings table. Unambiguous (value, not verb) and greppable (`rg 'settings\.'`). The prefix does NOT leak into the user override file, which uses prose headings + labelled sub-lines (see 2.6).

### 2.4 Three-layer resolution + per-leaf precedence

Layers: **defaults** (static) → **detection** (local facts only) → **overrides** (`.claude/auto-task.config.md`, then `.local.md`).

**Precedence is per-leaf, not per-section.** Overrides win last; local beats project; each `settings.leaf` resolves independently. An override section supplies only the leaves it names; unspecified leaves fall through to detection/default. (No wholesale section replacement — that would erase sub-defaults in compound settings.) **Detection never clobbers an explicit override** — it only resolves leaves left at `auto` (the codex-staleness fix).

**Detection is narrow** — concrete local facts only:
- `codex` present (`codex` on PATH / `codex doctor`) → `settings.models.adversarial`/`panel` second seat.
- a `just check` / `make check` recipe, or a `check`/`test` package script → `settings.verify`.
- Chrome DevTools MCP present → design-review readiness.
Explicitly NOT detected: CI-workflow steps (need services/secrets — a human sets them as an override, never auto-run); "strongest available model" (not shell-detectable → **static prose default**, resolved by the agent's own knowledge, not a command).

### 2.5 How a skill consumes config

**Step 0 is a short, imperative, mandatory block at the very top of every setting-consuming skill** (not buried preamble):

> **Step 0 — Resolve config (mandatory).** If a `Resolved auto-task settings v1` block was passed in, use it verbatim and do NOT re-run detection. Otherwise resolve now by following `/at:config` § Resolve. Do not proceed without a resolved block.

Reference sites read `settings.*`; never restate a default:
```markdown
Run `settings.verify` after each green step.
Append `settings.review_context` (may be "") verbatim to the reviewer's focus text.
If `settings.design_review_server` is set, boot it; else fail loudly on UI changes.
Integrate per `settings.conventions.merge`: squash → §Squash; merge-commit → §Merge.
```
→ zero restated defaults in skills → nothing to drift. Replaces the 5-skill boilerplate.

### 2.6 The user-facing override file

Overrides-only + one link line to the defaults. Prose headings; **labelled sub-lines for compound settings' leaves**; free prose only where load-bearing:
```markdown
# Auto-Task Config — overrides only. Defaults: see /at:config § Settings & Defaults.

## Verification
`npm run check` — mirrors CI; safe from parallel worktrees.

## Conventions
merge: merge-commit
suffix: [task/NNN]

## Review
Internal-only behind SSO — no public-exposure findings.
Flag unguarded division as Major; silent NaN corruption is our top defect class.
```
Resolver maps heading → setting group, labelled line → leaf. Unknown headings warn; similar headings are never guessed.

### 2.7 Delivery, freshness, and the resolved-block contract

| Context | How config arrives | Freshness | Source path |
| :--- | :--- | :--- | :--- |
| Orchestrated subagent | **injected** resolved block | frozen for the run | (from orchestrator) |
| Orchestrator (Step 0.1) | resolves once via `/at:config` | fresh per run | **primary checkout, before worktree creation** |
| Orchestrator resume | prefer in-conversation block; else re-resolve + report "settings may have changed" | fresh at resume | primary |
| Standalone skill | resolves itself via `/at:config` | fresh per invocation | current repo root; report the path |

*Consumer skills do not independently search the filesystem once a block is passed* (the resolver reads the config files and probes the env; consumers don't). Resolving from the **primary checkout before the worktree exists** means a task branch's own edits to `.claude/auto-task.config.md` never change the in-flight run.

**Strict resolved-block grammar (`v1`):**
```markdown
Resolved auto-task settings v1 (run: task 042; source: /path/to/primary)
- settings.verify: `npm run check` [project]
- settings.task_store.location: tasks/ [default]
- settings.models.adversarial: codex [detected: codex on PATH]
- settings.conventions.merge: squash [default]
- settings.review_context: [project]
  ```text
  Internal-only behind SSO — no public-exposure findings.
  ```
```
Rules: one leaf per line for scalars, `` `backticked` `` commands, `[provenance]` tag (`default`/`detected`/`project`/`local`); prose leaves as a fenced `text` sub-block; empty prose as `settings.review_context: "" [default]`. Version tag `v1` gates future format changes.

### 2.8 Persistence

No disk snapshot for v0.1 (a leftover file can't distinguish a live hand-off from a stale prior run → reintroduces cross-invocation staleness). Audit via the resolved block printed into the **Step 9 run report**. On resume, prefer the in-conversation block, else re-resolve and note settings may have changed.

## 3. Explicitly NOT changing

Markdown (no TOML/JSON — no parser; `review_context` is irreducibly prose) · two-file project/local split + precedence · zero-config-by-default · the set of settings · `review_context` stays prose.

## 4. Delivery slices (incremental)

**Slice 1 — infrastructure + migrate create-task (standalone path only).**
Build the reusable `/at:config` boilerplate — § Resolve (standalone: defaults → overrides), § Resolved-block grammar (full `v1`), § Inspect, Step 0 template, heading→setting map — but populate § Settings & Defaults with **only** `settings.task_store.*` and `settings.feedback_snapshots` (create-task's settings; both static → § Detection is an empty stub this slice). Migrate `create-task`: mandatory Step 0; reference `settings.task_store.*` / `settings.feedback_snapshots`; replace its `## Task Store and Project Config` section with a pointer to `/at:config`. Convert only the Task Store + Feedback Snapshots sections of `examples/auto-task.config.md` to overrides-only. **Untouched:** orchestrator, the other 7 skills (keep inline defaults + boilerplate), README, CLAUDE.md rule. create-task is the ideal first cut — human-invoked, standalone, upstream of the orchestrator → exercises only the standalone resolve path. Coexistence is safe: migrated and legacy defaults are the identical value.
Verify: `/at:create-task` with no config and with a `## Task Store` override; `/at:config` inspect; grep create-task for restated defaults (none).

**Slice 2 — orchestrator + pipeline skills.** Injection, resolve-from-primary-before-worktree, Step-9 report; migrate plan/impl/review-code/review-design/review-task/ship + their settings (verify, models, conventions, review_context, design_review_server, worktree); add real § Detection (codex, check recipe, Chrome MCP).

**Slice 3 — scaffolding.** `/at:config --init` interactive scaffolder + lazy capture (once the contract is proven against real consumers).

**Slice 4 — cleanup.** Full `examples/auto-task.config.md` rewrite, README link, delete every legacy boilerplate line, rewrite CLAUDE.md's maintenance rule, ship valid + compound + unknown-heading **test fixtures**, grep gate green.

**Update cost (post-migration):** change a default = 1 place (§ Settings & Defaults); add a setting = 2 (table + the one enacting skill; README is a link).

## 5. Acknowledged residual risks

- Standalone Step 0 relies on the skill actually following `/at:config` (we don't inline the full resolver 8×). Mitigation: prominent mandatory Step 0. Residual, accepted.
- Per-leaf resolution of compound settings needs the resolver to read labelled sub-lines correctly. Mitigation: labelled-line convention + explicit heading→setting map + lint. Residual, accepted.
