# Reusable Claude Code Skills: Architecture for a Solo Developer

**Status:** done — actioned into task/017

## Problem Anchor

## "For a Solo Developer with 16+ Claude Code Skills Split Across Two Repos (Tad Project-Local, System Global), What Is the Most Practical, Low-Ceremony Approach to Making Generic Skills (TDD, GOOS, DDD, Clean-Code, Software-Design, Research, Review-Loop, Cross-Pollinate, Task Workflow) Reusable Across Multiple Projects While Keeping Project-Specific Customization Possible?"

## Key Findings

### 1. Precedence Is Personal > Project — You Cannot Override Global Skills Locally

The single most important technical constraint. Claude Code's documented precedence is:

```text
enterprise > personal (~/.claude/skills/) > project (.claude/skills/)
```

This is the **opposite** of VS Code, neovim, and most layered config systems where project-local wins. If you put `/research` in `~/.claude/skills/` and also have `/research` in `tad/.claude/skills/`, the global version wins — the project version is ignored.

**Consequence**: Only put skills in `~/.claude/skills/` that you **never** want to override per-project. This creates a clean bright line between universal skills and project-customizable ones.

Source: [Claude Code docs](https://code.claude.com/docs/en/skills) (verbatim: "When skills share the same name across levels, higher-priority locations win: enterprise > personal > project"). Issue [#10061](https://github.com/anthropics/claude-code/issues/10061) and [#22208](https://github.com/anthropics/claude-code/issues/22208) confirm this causes real friction — users expect project to win.

### 2. Seven Skills Are Fully Portable with Zero Changes

The portability audit classified all 16 tad skills:

| Tier | Skills                                                                    | Count |
| :--- | :------------------------------------------------------------------------ | ----: |
| A    | tdd, ddd, goos, clean-code, software-design, review-loop, cross-pollinate |     7 |
| B    | code-review, cross-pollinate-code-review, kaizen, research, plan-task,    |     8 |
|      | impl-task, review-task, define-task                                       |       |
| C    | create-task                                                               |     1 |

**Tier A** skills contain zero project-specific references — no paths, no commands, no domain terms. They are pure methodology (Beck, Evans, Martin, Ousterhout, Freeman & Pryce) and generic protocols (review-loop, cross-pollinate).

**Tier B** skills have 1-5 sticky references each, primarily: `just check`, `just commit`, `just task-status`, `tasks/` paths, `docs/research/` path, and `backtester/` as an example scope. The `just` commands are the single biggest portability blocker.

**Tier C** (`create-task`) is deeply tied to tad's `tasks/<NNN>-<slug>.md` naming convention and task tooling.

### 3. Skills Are Stable After Creation — the Sharing Problem Barely Exists Today

Git history shows 39 commits touching skills across 65 days, but the distribution is revealing:

- **Mar 13-17**: 15 commits (build burst — skill creation)
- **Since Mar 18**: 5 commits (all adding *new* skills, not fixing existing ones)
- **Bug-fix rate for existing skills**: approximately zero

The generic skills (tdd: created once + 6 initial iterations, then stable; ddd, goos, clean-code, software-design: created once, never changed) are essentially write-once artifacts. The scenario that justifies a sharing mechanism — "I fixed a bug in /tdd and need to propagate it" — has not occurred.

Currently only one project (tad) actively uses skills. Other repos (`google-calendar-colorizer`, `tldr`, `trackid`) have no `.claude/` directory at all.

### 4. Symlinks Work but with Quirks

Individual skill directory symlinks (e.g., `~/.claude/skills/trackid -> ~/github/system/private/skills/trackid`) work for runtime loading — confirmed by the 5 symlinked global skills already in use. However, symlink support for skills is **not officially documented** ([issue #37590](https://github.com/anthropics/claude-code/issues/37590) requests this). It works in practice but is not guaranteed.

Known issues:

- The `/skills` autocomplete listing shows **nothing** (not just missing symlinked skills) when symlinked skills are present ([issue #14836](https://github.com/anthropics/claude-code/issues/14836))
- Symlinking the entire `.claude/skills/` directory (not individual skill dirs within it) is unreliable ([issue #36659](https://github.com/anthropics/claude-code/issues/36659))
- Direct `/skill-name` invocation works regardless of autocomplete state

### 5. Context Budget Is Not a Concern Yet

Skill descriptions consume ~2% of context window (fallback: 16,000 chars). The practical limit is approximately **28 skills** based on real-world reports ([issue #31505](https://github.com/anthropics/claude-code/issues/31505)), though this depends on description lengths. Current total: 21 skills (16 project + 5 global) — within budget but approaching the limit if all Tier A skills move to global (28 total).

Beyond the budget, skills are silently excluded from auto-invocation. Programmatic `Skill()` calls (cross-skill invocation) also fail for excluded skills. Only direct `/skill-name` slash invocation continues to work by reading from disk. The limit is configurable via the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable.

### 6. Useful Skill Features for Sharing

| Variable               | Description                                              |
| :--------------------- | :------------------------------------------------------- |
| `$ARGUMENTS`           | All arguments passed to the skill                        |
| `$ARGUMENTS[N]` / `$N` | Specific argument by 0-based index                       |
| `${CLAUDE_SESSION_ID}` | Current session ID (useful for session-specific files)   |
| `${CLAUDE_SKILL_DIR}`  | Absolute path to the skill's directory                   |
| `` !`command` ``       | Shell command injection, output replaces token           |
| `context: fork`        | Run skill in isolated subagent (no conversation history) |

`${CLAUDE_SKILL_DIR}` is particularly useful — skills can reference bundled scripts or data relative to their own location, regardless of where they're installed.

Note: `--add-dir <path>` at session start also loads skills from the specified directory with live-reload support. This is an alternative to symlinks but requires passing a CLI flag every session — more ceremony than symlinks for a permanent setup, but useful for temporary access to a skill library.

## Analysis

### The Natural Split

The precedence constraint (personal > project) and the portability audit converge on the same answer: a **two-tier** architecture with a clean bright line.

**Global tier** (`~/.claude/skills/` via system repo): Skills that are universal methodology with no project-specific references. You never want to override these per-project because the methodology doesn't change — TDD is TDD whether you're in a quant project or a web app.

**Project tier** (`.claude/skills/`): Skills that encode project-specific workflow, tooling, or conventions. These reference `just check`, `tasks/`, `docs/research/`, etc. They should be copied and adapted per-project because the customization IS the value.

This split aligns with the precedence model instead of fighting it.

### What Goes Where

**Move to global** (zero changes needed):

| Skill           | Rationale                                               |
| :-------------- | :------------------------------------------------------ |
| tdd             | Pure Beck-style TDD. Zero project references.           |
| ddd             | Pure Evans DDD. Zero project references.                |
| goos            | Pure Freeman & Pryce. References `/tdd` (also global).  |
| clean-code      | Pure Martin. Zero project references.                   |
| software-design | Pure Ousterhout. Zero project references.               |
| review-loop     | Generic convergence protocol. Zero project references.  |
| cross-pollinate | Generic multi-model synthesis. Zero project references. |

**Keep project-local** (copy and adapt per-project):

| Skill                       | Sticky references                                 |
| :-------------------------- | :------------------------------------------------ |
| code-review                 | `just check`, domain examples, CI workflow name   |
| cross-pollinate-code-review | Inherits from code-review                         |
| kaizen                      | `tasks/`, `experimental/` exclusion, `just check` |
| research                    | `docs/research/` output path                      |
| define-task                 | `tasks/_backlog.md`, task directory structure     |
| plan-task                   | `just task-status`, cross-skill workflow          |
| impl-task                   | `just check/commit/task-status`, TDD embed path   |
| review-task                 | `just check`, `just task-status`                  |
| create-task                 | Entire task schema (`tasks/<NNN>-<slug>.md`)      |

### The `impl-task` Cross-Reference Problem

`/impl-task` embeds `/tdd` via:

```text
!`sed '1,/^---$/d' .claude/skills/tdd/SKILL.md`
```

If `/tdd` moves to global (`~/.claude/skills/tdd/`), this relative path breaks. Two options:

1. **Absolute path**: Change to `!`sed '1,/^---$/d' ~/.claude/skills/tdd/SKILL.md`` — works but couples the local skill to a global path
2. **Drop the embed**: `/impl-task` already contains an inline TDD cycle (Red/Green/Refactor instructions in its own body, lines ~50-68). The `sed` embed at line 169 is a *second copy* of the same content — a reference appendix, not the primary instruction source. Removing the embed does not degrade `/impl-task` because the inline cycle remains.

Option 2 is simpler and avoids cross-tier coupling.

### Why Not Build More Infrastructure?

The contrarian analysis is persuasive:

- **One active project** currently uses skills
- **Zero cross-project bug-fix incidents** in 65 days
- **Copying 7 generic skills** to a new project is a 5-minute operation
- **Skills are write-once** — the generic ones haven't changed after initial creation
- **Claude Code is evolving fast** — a lightweight approach adapts more easily

The cost of moving 7 Tier A skills to `~/.claude/skills/` (via the existing system repo symlink pattern) is ~10 minutes of one-time work. The ongoing cost is zero because these skills don't change. This passes the "worth doing even with one project" threshold because:

1. It clarifies the taxonomy (universal vs project-specific)
2. When starting a new project, 7 skills are just there — no copying needed
3. It follows the existing pattern (your 5 financial skills already work this way)

Building anything more — convention frameworks, template variables, override mechanisms — is premature. Revisit if and when you have 3+ active projects simultaneously receiving skill updates.

### Parameterizing the Project-Local Skills

For the 9 project-local skills, when copying to a new project the main changes needed are:

1. **Build commands**: Replace `just check` / `just commit` / `just task-status` with the project's equivalents (or define these recipes in a project Justfile for consistency)
2. **Output paths**: `docs/research/`, `tasks/`, `docs/knowledge.md` — either adopt the same conventions or change the paths
3. **Domain examples**: Remove `backtester/` scope examples, quant-specific correctness concerns
4. **CI references**: Update `claude-code-review.yml` workflow name

The simplest approach: **adopt the same directory conventions across projects** (`tasks/`, `docs/research/`, `docs/knowledge.md`). Then the project-local skills need only build-command changes. If you use Justfiles everywhere with the same recipe names (`just check`, `just commit`), even those become portable.

This is the convention-based approach — not an abstraction layer, just a decision to use the same directory layout. Be realistic: a TypeScript project won't have `just check` or `tasks/`. Porting the task-workflow cluster to a different-stack project means deciding whether to import tad's conventions wholesale (install `just`, create `tasks/`) or rewrite the sticky references. The first is cheaper than it sounds; the second is more work than "change 3 lines."

### Versioning: a Non-Issue Today, Worth Noting for Later

Global skills are live — any update to `~/github/system/shared/skills/tdd/` is immediately visible to all projects. For methodology skills this is a feature: improvements propagate instantly. There is no version-pinning mechanism; if you need to freeze a skill mid-sprint, the only option is a local copy.

This is fine for a solo dev with write-once skills. It becomes a concern if skills start receiving frequent updates that could change agent behavior during active work. At that point, consider tagging the system repo before updating skills, so you can revert if needed.

## Recommendation

### Option 0: Do Nothing (The Default)

The data supports waiting. One active project, zero cross-project bug-fix incidents, stable-after-creation skills. Copying 7 skills to a new project is a 5-minute `cp -r` operation.

**Trigger to act**: When you actually start a second project that needs these skills. Not "might need someday" — actually need, right now.

The options below describe what to do when that trigger fires.

### Option 1: Move Tier a to Global (10 Minutes of Work)

1. Move the 7 Tier A skills to `~/github/system/` (alongside the existing private skills) and symlink them into `~/.claude/skills/`:

   ```text
   # In ~/github/system/ — create a shared skills directory
   # (alongside private/skills/ which has personal/financial ones)
   shared/skills/
   ├── tdd/SKILL.md
   ├── ddd/SKILL.md
   ├── goos/SKILL.md
   ├── clean-code/SKILL.md
   ├── software-design/SKILL.md
   ├── review-loop/SKILL.md
   └── cross-pollinate/SKILL.md
   ```

   ```bash
   # Symlink each into ~/.claude/skills/
   for skill in tdd ddd goos clean-code software-design review-loop cross-pollinate; do
     ln -s ~/github/system/shared/skills/$skill ~/.claude/skills/$skill
   done
   ```

2. Remove these 7 skills from `tad/.claude/skills/` (they'll be available globally).

3. In `/impl-task`, remove the `sed` embed of `/tdd` — the agent already has access to the global `/tdd` skill.

### When Starting a New Project

1. The 7 global skills are already available.
2. Copy the project-local skills you need from tad (typically the task-workflow cluster + research + code-review).
3. Update `just` commands and paths to match the new project.
4. Consider adopting the same directory conventions (`tasks/`, `docs/research/`) to minimize changes.

### When to Revisit

Revisit this architecture when any of these become true:

- 3+ active projects using skills simultaneously
- You find yourself propagating a skill fix across multiple projects
- Claude Code adds project > personal precedence or skill inheritance
- The context budget becomes a concern (approaching 40+ skills)

## Pre-Mortem: What Could Be Wrong

**The precedence claim might be wrong or might change.** The `enterprise > personal > project` precedence comes from the official docs, but Claude Code is evolving rapidly. If precedence flips to `project > personal` (the more intuitive model), the "global defaults + local override" pattern becomes viable and the constraint driving the two-tier split disappears.

**Skills might not be as stable as they appear.** The 65-day history includes only one project. If you start using skills in 3 projects simultaneously, you might discover improvements needed that DO require cross-project propagation.

**Convention adoption has hidden friction.** Saying "use the same directory layout" is easy; actually maintaining identical `just check` recipes across projects may not be practical if the projects have very different tech stacks (Python vs TypeScript vs Go).

**The autocomplete bug for symlinked skills might annoy you enough to revert.** If `/skills` shows nothing when symlinked skills are present, you lose discoverability — you have to remember skill names. This is a UX papercut, not a blocker, but it adds up.

**Skills may not be the right unit of sharing for methodology.** An alternative framing: embed TDD/DDD/GOOS principles in CLAUDE.md as ambient rules rather than on-demand skills. A project whose CLAUDE.md says "use TDD" gets the behavior without needing a `/tdd` skill. Skills are the right unit only if you want explicit on-demand invocation with full methodology loading — if ambient is enough, CLAUDE.md is simpler.

**The context budget is tighter than expected.** With ~28 practical skill slots and 21 skills today, moving 7 more to global puts you at 28 — right at the limit. Adding any new skills could cause silent exclusion. The `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var is an escape hatch, but this deserves monitoring.

## References

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Issue #10061 — Skill precedence: user-level chosen over project-level](https://github.com/anthropics/claude-code/issues/10061)
- [Issue #22208 — Feature request: configurable skill precedence](https://github.com/anthropics/claude-code/issues/22208)
- [Issue #14836 — Symlinked skills not in autocomplete](https://github.com/anthropics/claude-code/issues/14836)
- [Issue #26489 — skills/ should traverse parent directories](https://github.com/anthropics/claude-code/issues/26489)
- [Issue #31505 — Silent skill exclusion beyond context budget](https://github.com/anthropics/claude-code/issues/31505)
- [Issue #36659 — Symlinked .claude directory breaks autocomplete](https://github.com/anthropics/claude-code/issues/36659)
- [Issue #37590 — Document symlink support for skills](https://github.com/anthropics/claude-code/issues/37590)
- [skillshare — CLI for syncing AI skills across tools](https://github.com/runkids/skillshare)
- [Chezmoi comparison table](https://www.chezmoi.io/comparison-table/)
- [VS Code User and Workspace Settings](https://code.visualstudio.com/docs/configure/settings)
- [Confused About Where to Put Your Agent Skills? — DEV Community](https://dev.to/gde/confused-about-where-to-put-your-agent-skills-mdo)
