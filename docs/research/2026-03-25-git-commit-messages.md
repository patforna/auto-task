# Git Commit Messages: SOTA Guidance for Solo Dev + Agentic AI (2026)

**Status:** rejected — YAGNI; current CLAUDE.md rules are sufficient **Problem Anchor**: What is the current (2026) SOTA guidance for git commit messages for a solo developer working with agentic AI on GitHub, and what is the most pragmatic mechanism (CLAUDE.md, skill, hook) to enforce it?

**Date**: 2026-03-25

---

## Current Patterns (This Repo, Last 60 Commits)

Existing style: imperative verb + description, single-line, no type prefix.

```text
Research skill: require all agents to complete, add monitoring and recovery
Remove run-research.sh script (no longer needed)
Add convergence synthesis: 6-month strategic action plan
Fix code review workflow: add Agent to allowedTools (#41)
Rename repo-health to kaizen — skill, workflow, issue labels
```

**What's working**: imperative mood, descriptive, consistent voice. **Gaps**: 28 of 60 subjects (47%) exceed 72 chars, no body for complex changes, task references inconsistent.

---

## Key Research Findings

### 1. The 50/72 Rule Is Alive but Relaxed

The 50-char subject limit (Chris Beams, 2014) remains the target, but the hard consensus is **72 chars** — where Git and GitHub truncate. The 72-char body wrap is uncontroversial. Independent justification from typographic research: 50-60 chars/line is optimal readability (Emil Ruder). Source: [cbea.ms/git-commit](https://cbea.ms/git-commit/), [blog.thirstybear.co.uk/2025/05](https://blog.thirstybear.co.uk/2025/05/git-commit-messages-why-keep-50.html)

### 2. Conventional Commits: Strong in JS, Contested Elsewhere

Conventional Commits (`feat:`, `fix:`, etc.) has near-universal adoption in the NPM ecosystem (~94.5% of 381 popular projects), driven by semantic-release and commitlint. Outside JS, adoption is patchier and more contested.

**The main criticism**: type confusion is the #1 reported problem (~58% of issues). `feat` vs `chore`, `refactor` vs `perf` are genuinely ambiguous. The prefix also eats 10-15 chars from the subject budget.

**For this repo specifically** (Python, no published package, no semantic-release, no changelogs): CC's primary value — driving automated versioning — doesn't apply. The secondary value — giving agents a structured vocabulary for parsing history — is real but achievable with simpler rules (imperative verbs are already a structured vocabulary; `Add` vs `Fix` vs `Refactor` communicates intent without the type-prefix overhead or the `feat` vs `chore` ambiguity).

Sources: [conventionalcommits.org](https://www.conventionalcommits.org/en/v1.0.0/), [lobste.rs discussions](https://lobste.rs/s/szoe3m/conventional_commits_considered)

### 3. The Go/Linux Kernel Pattern Is the Pragmatic Alternative

Both use **scope prefix without type taxonomy**: `math: improve Sin precision` (Go), `mm/slub: fix krealloc` (Linux). The component IS the organizational unit; adding a behavioral type on top is where ambiguity enters. This pattern fits projects where the codebase has clear modules but no automated release pipeline.

Sources: [go.dev/doc/contribute](https://go.dev/doc/contribute#commit_messages), [kernel.org/doc/html/latest/process/submitting-patches.html](https://www.kernel.org/doc/html/latest/process/submitting-patches.html)

### 4. In the Agentic Era, Commit Quality Is a Direct Productivity Input

**The key non-obvious insight**: AI agents are now the primary *consumers* of git history, not just producers. When Claude Code reads recent commits to build context, vague messages degrade subsequent session quality. This creates a feedback loop: agent commits today are agent context tomorrow.

Evidence: agents are adequate at describing *what* changed, but structurally weak on *why* (arXiv:2507.10906). A documented Claude Code failure mode: message reflects the conversation turn, not the actual diff (SFEIR Institute reports this as a common pattern, though the frequency claim lacks rigorous methodology). Agents also batch changes into fewer, larger commits than humans would (Cliff's delta = 0.54, arXiv:2601.17581).

**Practical implications**: (1) investing in the "why" line has higher ROI in an agentic workflow than a purely human one, and (2) agent instructions should explicitly say "describe the diff, not the conversation" to counter the conversation-mirroring failure mode.

Sources: [arXiv:2601.17581](https://arxiv.org/html/2601.17581), [SFEIR Institute](https://institute.sfeir.com/en/claude-code/claude-code-git-integration/errors/), [Lore protocol](https://arxiv.org/html/2603.15566)

### 5. Attribution: No Standard, but the Default Is Fine

`Co-Authored-By: Claude <noreply@anthropic.com>` is the de facto emerging norm by volume (Claude Code is one of the most prolific sources of public GitHub commits with attribution trailers). No cross-vendor standard exists. For a solo dev, it's a personal preference — leave it on (default) or suppress it. No compliance requirement as of March 2026.

### 6. Enforcement Mechanism Comparison

| Mechanism                | Reliability | Friction | Setup cost | Covers direct `git commit`?  |
| :----------------------- | :---------- | :------- | :--------- | :--------------------------- |
| CLAUDE.md rules          | Medium      | Zero     | Near-zero  | Soft guidance only           |
| `just commit` validation | High        | Zero     | Minimal    | No (just-only)               |
| Git `commit-msg` hook    | Highest     | Zero     | Low        | Yes                          |
| Claude Code PreToolUse   | High        | Zero     | Moderate   | Yes (fragile parsing)        |
| `/commit` skill          | Medium      | Low      | Minimal    | Only on `/commit` invocation |

**Winner for this repo**: CLAUDE.md rules (soft guide so the agent gets it right first try) + `just commit` validation (hard gate, already the canonical path). Git hook as optional safety net. PreToolUse hook is overkill — fragile command parsing for marginal gain when `just commit` already catches it.

---

## Proposal

### Format: Formalize the Existing Style, Don't Switch to CC

The current pattern is already close to the Go/Linux kernel convention. Formalize it rather than adopting Conventional Commits (which adds type-confusion overhead without driving automation in this repo).

**Subject line** (required):

```text
<imperative verb> <what changed>
```

- 72 chars max (hard cap, enforced)
- Imperative mood: "Add", "Fix", "Remove", "Refactor" — not "Added", "Fixes"
- No trailing period
- If task-related: append `(task/NNN)` at the end

**Body** (optional, blank line after subject):

```text
Why: <motivation — what problem this solves or decision it implements>
```

- Use when the "why" isn't obvious from the subject + diff
- 72-char line wrap
- One line is enough — this isn't a design doc

**Examples** (course-correcting from actual history):

| Before (actual)                                                                                         | After                                                          |
| :------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------- |
| `Research skill: require all agents to complete, add monitoring and recovery`                           | `Add agent monitoring and recovery to research skill`          |
| `Add comprehensive retail day trading research document`                                                | `Add retail day trading research`                              |
| `Evolve backlog to hybrid index — _backlog.md as master registry, column format Title/Type/File/Status` | `Restructure backlog: _backlog.md as index with column format` |

### Enforcement: CLAUDE.md + `just commit` Validation

**Layer 1 — CLAUDE.md** (add to the existing Git section):

```markdown
## Commit Messages

- Subject: `<imperative verb> <what changed>` — 72 chars max, no trailing period
- Describe the diff, not the conversation that produced it
- Body (optional, after blank line): one-line `Why: <motivation>` when the reason isn't obvious from subject + diff
- Task reference: append `(task/NNN)` to subject when applicable
- Do NOT use Conventional Commits prefixes (feat:, fix:, etc.)
- One commit per logical change — don't batch unrelated changes
```

**Layer 2 — `just commit` validation** (add to the existing recipe):

```bash
# Validate: imperative mood, ≤72 chars, no trailing period
msg_len=${#msg}
if [ "$msg_len" -gt 72 ]; then
    echo "ERROR: Subject exceeds 72 chars ($msg_len). Shorten it." >&2; exit 1
fi
if echo "$msg" | grep -qE '\.$'; then
    echo "ERROR: No trailing period on commit subject." >&2; exit 1
fi
```

That's it. Two layers, zero new dependencies, zero new files. The CLAUDE.md rule means the agent generates a good message on the first try (including the "describe the diff, not the conversation" behavioral nudge). The `just commit` validation catches the mechanical misses (length, period). Both work with the existing workflow.

**Note**: the `just commit` recipe takes the message as a single positional string. Multi-line messages (subject + body) require shell quoting: `just commit $'Subject\n\nWhy: motivation' file1 file2`. The body remains optional and unvalidated — a deliberate tradeoff: agents are weak on "why" (Section 4), but enforcing body presence mechanically would produce low-quality boilerplate. The CLAUDE.md rule nudges rather than mandates.

### What NOT to Do

- **Don't add commitlint/husky** — Node.js dependency for a Python repo, overkill for solo dev
- **Don't add a PreToolUse hook** — fragile shell parsing of `git commit -m "..."` from Bash commands, marginal gain over `just commit` validation
- **Don't add a `/commit` skill** — the `just commit` recipe is already the canonical path; adding a skill duplicates the entry point
- **Don't adopt Conventional Commits** — no semantic-release, no changelogs, no published package = no payoff for the type-prefix overhead
- **Don't enforce via git `commit-msg` hook** — `just commit` is already the enforced path via CLAUDE.md; a git hook adds configuration that must survive clones

---

## References

| Source                                                  | URL                                                                                                  |
| :------------------------------------------------------ | :--------------------------------------------------------------------------------------------------- |
| Chris Beams: How to Write a Git Commit Message          | <https://cbea.ms/git-commit/>                                                                        |
| Conventional Commits v1.0.0                             | <https://www.conventionalcommits.org/en/v1.0.0/>                                                     |
| Go contribution guide (commit messages)                 | <https://go.dev/doc/contribute#commit_messages>                                                      |
| Linux kernel: submitting patches                        | <https://www.kernel.org/doc/html/latest/process/submitting-patches.html>                             |
| Thirsty Bear: Why Keep 50 Chars (2025)                  | <https://blog.thirstybear.co.uk/2025/05/git-commit-messages-why-keep-50.html>                        |
| Lobsters: Conventional Commits Considered               | <https://lobste.rs/s/szoe3m/conventional_commits_considered>                                         |
| arXiv:2601.17581 — How AI Coding Agents Modify Code     | <https://arxiv.org/html/2601.17581>                                                                  |
| arXiv:2507.10906 — Evaluating AI Commit Messages        | <https://arxiv.org/html/2507.10906v1>                                                                |
| arXiv:2603.15566 — Lore: Git Commit as Knowledge Record | <https://arxiv.org/html/2603.15566>                                                                  |
| SFEIR Institute: Claude Code Git Best Practices         | <https://institute.sfeir.com/en/claude-code/claude-code-git-integration/best-practices/>             |
| SFEIR Institute: Claude Code Git Errors                 | <https://institute.sfeir.com/en/claude-code/claude-code-git-integration/errors/>                     |
| Simon Willison: Git with Coding Agents                  | <https://simonwillison.net/guides/agentic-engineering-patterns/using-git-with-coding-agents/>        |
| microservices.io: Allow Git Commit Considered Harmful   | <https://microservices.io/post/genaidevelopment/2025/09/10/allow-git-commit-considered-harmful.html> |
| Mike Perham: Conventional Commits (2025)                | <https://www.mikeperham.com/2025/01/30/conventional-commits/>                                        |
| Claude Code Hooks Guide                                 | <https://code.claude.com/docs/en/hooks-guide>                                                        |
| arXiv:2512.00867 — AI Attribution Paradox               | <https://arxiv.org/html/2512.00867v1>                                                                |
| Agentic Commits specification                           | <https://deligoz.me/projects/agentic-commits/>                                                       |
