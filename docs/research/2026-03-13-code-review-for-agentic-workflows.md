# Code Review for Agentic Workflows

Research conducted 2026-03-13 via ten parallel agents covering: traditional code review best practices, agentic AI review patterns, Anthropic's review tools, task verification vs code review, solo dev review workflows, compressed review checklists, AI self-review loops, GitHub Actions review workflows, XP/BDD verification philosophy, and modern AI review tools comparison.

Findings informed the design of two new skills: `review-task` (task lifecycle verification) and `code-review` (general code quality review).

---

## 1. The Two Concerns: Verification Vs Review

The research converged strongly on a fundamental distinction that runs through traditional agile, BDD, Google's engineering practices, and emerging agentic workflows:

**Task verification** ("Does it do what was asked?"):

- Grounded in the task specification (ACs, plan, description, notes)
- Objective — each AC either passes or fails
- Automatable via tests that map to ACs
- In BDD: "a story's behaviour is simply its acceptance criteria" (Dan North)

**Code review** ("Is the code good?"):

- Grounded in codebase conventions, design principles, and domain knowledge
- Judgment-based — design fit, maintainability, security
- Requires understanding the system beyond the immediate change
- In Google's terms: "improves overall code health"

Traditional agile separates these: QA verifies stories; peers review code. In agentic workflows, the separation is even more important because it maps to different prompts, different grounding, and — critically — different contexts.

### Optimal Sequence

Research from multiple sources (Google eng-practices, BDD practitioners, CI/CD pipeline design) converges on:

1. Implement (agent)
2. Self-verify against ACs + run tests (agent, same session)
3. **Verify task** (separate session — AC satisfaction with evidence)
4. **Review code** (separate pass — quality, design, conventions)
5. Human approval

The key insight: code review assumes correctness. Reviewers shouldn't waste attention on "does it work?" — that's proven by verification. This separation lets each pass focus deeply on its concern.

---

## 2. Fresh Context Is Not Optional

This was the strongest empirical finding across the research:

**Self-review is fundamentally unreliable.** LLMs reviewing their own output exhibit confirmation bias and anchoring. Key evidence:

- GPT-4 self-critique showed **zero performance improvement** over baseline (Evjang, 2023)
- Self-generated test suites pass at artificially high rates — they share the model's cognitive biases (CRITIC framework research)
- LLMs rate their own work highest; separate reviewers give average ratings (Gemini self-assessment study)
- Self-review retention rate <60%, verifier accuracy <10% against ground truth

**Separate context catches 40-60% more issues.** The mechanism is anchoring prevention: the reviewer doesn't inherit the generator's initial framing of the problem.

**Practical implication:** The reviewing agent must start in a fresh session with no access to the implementation conversation. If the task is truly self-contained (carrying all necessary context), the reviewer needs only:

1. The task file (ACs, plan, description, notes)
2. The codebase (code + tests + CLAUDE.md)
3. The diff (what changed)

This validates the TAD workflow principle that tasks must be self-contained — "signal without noise."

---

## 3. The Priority Hierarchy (80/20 of Code Review)

Research from Google, Microsoft (1.5M review comments), SmartBear (Cisco study), and practitioner surveys converges on a clear priority hierarchy:

| Priority | Concern          | Value | Best Checker        |
| -------- | ---------------- | ----- | ------------------- |
| 1        | Correctness      | 40%   | Tests + human/AI    |
| 2        | Design fit       | 25%   | Human/AI review     |
| 3        | Testing quality  | 20%   | Human/AI review     |
| 4        | Security         | —     | SAST + human/AI     |
| 5        | Conventions      | 10%   | Linters + human/AI  |
| 6        | Style/formatting | 5%    | Linters (automate!) |

**Key insight:** Correctness + design + testing = 85% of review value. Style and formatting should never appear in human or AI review — automate them completely. This is already TAD's approach (`just check` runs ruff, pyright, architecture tests).

### What NOT to Review (Already Automated)

- Lint/format violations (ruff)
- Type errors (pyright)
- Import/dependency violations (test_architecture.py)
- Missing docstrings on clear code
- Subjective style preferences

### What to Focus Review On

- Logic errors, off-by-one, incorrect conditionals, missing guards
- Silent-corruption risks (division by zero, NaN propagation)
- Domain-specific gotchas (quant: unconditional signal analysis)
- Design coherence with existing system
- Test quality (right things tested, not just coverage %)
- Convention consistency with CLAUDE.md and codebase patterns

---

## 4. Cognitive Limits and Review Size

Hard biological/cognitive constraints validated by research:

- **Optimal review size:** 200-400 LOC (Cisco 2006, LinearB 2025)
- **Quality collapse:** >450 LOC/hour, 87% of reviews drop below average
- **Session fatigue:** Effectiveness drops sharply after 60 minutes
- **Comment quality by size:** Under 300 LOC → substantive architectural feedback. Over 600 LOC → only style and obvious bugs.

**Implication for agentic review:** AI reviewers don't fatigue the same way, but the finding about review size still matters — larger diffs have more interaction effects that any reviewer (human or AI) will miss. This reinforces the task sizing principle: smaller tasks → better review.

---

## 5. AI Self-Review Loops: What Works

### The CRITIC Framework

Self-critique without external tools fails. The CRITIC framework (2023) showed that effective self-correction requires:

1. Generate initial output
2. Use **external tools** to validate (tests, linters, specs)
3. Revise based on tool feedback
4. Repeat until valid

**Without external tools:** Modest improvement or degradation. **With external tools:** 7.7 F1 improvement (QA), 7.0% gains (math).

### Optimal Iterations

Research shows clear diminishing returns:

| Iterations | Improvement | Recommendation      |
| ---------- | ----------- | ------------------- |
| 1-2        | ~15-20%     | Always do           |
| 3-4        | ~5-10% more | Sweet spot          |
| 5+         | <5% more    | Stop — negative ROI |

SelFee model research: minimum 3 revisions optimal; more than 3 shows diminishing or negative returns.

### Multi-Agent Vs Single-Agent Review

Separating concerns architecturally beats iterating within a single agent:

- Specialized agents ("find security bugs") outperform generalists ("review everything")
- Multi-lens analysis (security + performance + logic in parallel) catches more than sequential passes by one agent
- Anthropic's code-review plugin uses 4 parallel agents with this pattern

---

## 6. Anthropic's Code Review Tools

### Claude Code Code-Review Plugin

Anthropic published a code-review plugin that uses **4 parallel review agents**:

1. 2x CLAUDE.md compliance auditors
2. 1x bug detector (focused on changes only)
3. 1x git history analyzer

Key design choices:

- **Confidence scoring** (0-100) with **80+ threshold** to filter noise
- Automatic skipping of closed, draft, trivial, or already-reviewed PRs
- Direct links to flagged code with full SHA and line ranges
- Output: terminal or PR comment (`/code-review --comment`)

### Claude-Code-Action

The GitHub Action (`anthropics/claude-code-action@v1`) provides:

- Schedule, workflow_dispatch, issue_comment, pull_request triggers
- `--allowedTools` for explicit tool sandboxing
- `--max-turns 30` for thorough reviews
- Full repo context (fetch-depth: 0)

TAD already uses this for daily scheduled review with the same 80% confidence threshold as Anthropic's plugin.

### Multi-Agent Code Review (March 2026)

Anthropic launched a multi-agent code review system deploying specialized agents in parallel (security, performance, architecture, domain logic). Agents peer-review each other's findings — sub-1% false positive rate.

---

## 7. The False Positive Problem

This emerged as the central challenge of AI code review:

- Most AI review tools generate 10-20 comments per PR with ~80% noise
- **Good tool threshold:** >60% signal ratio
- **Excellent tool threshold:** >80% signal ratio
- Tools exceeding 5% false positive rate get abandoned by teams
- Cost of noise: 33 hours/dev/month filtering = $33K/month for 10 devs

**What drives false positives:**

- Reviewing style when linters exist
- Flagging pre-existing issues
- Vague concerns without specific code citations
- Generic suggestions without codebase context

**TAD's existing mitigations** (already in claude-code-review.yml):

- >80% confidence threshold
- Explicit skip-list (linting, types, architecture tests)
- "Below threshold" section for calibration
- Focus on issues introduced by the diff, not pre-existing

---

## 8. AI Review Tools Landscape (2026)

| Tool             | Signal Ratio | Context       | Best For                |
| ---------------- | ------------ | ------------- | ----------------------- |
| Graphite Agent   | >80%         | Stacked PRs   | Lowest noise            |
| Greptile         | High         | Full codebase | Systemic/arch issues    |
| Qodo 2.0         | High         | Semantic      | Deep analysis           |
| Anthropic plugin | High         | Multi-agent   | CLAUDE.md compliance    |
| CodeRabbit       | ~60-70%      | PR only       | Multi-platform          |
| Sourcery         | Good         | 30+ languages | Language variety        |
| GitHub Copilot   | Poor         | PR only       | GitHub-native (limited) |

**For solo dev without PRs:** SaaS tools (CodeRabbit, Greptile, etc.) are PR-centric and don't fit the schedule-based workflow. The claude-code-action approach (TAD's current setup) is the best fit.

---

## 9. Solo Dev Review Practices

### The "Refine Then Fresh" Pattern

The most effective solo dev review pattern:

1. **Refine:** Iterate within a single session to working state
2. **Break context:** Start fresh session
3. **Review cold:** New session reads code without implementation bias

Fresh sessions catch meaningful issues ~1/3 of the time that the original session missed.

### Time-Delayed Review

24-48 hours between implementation and review has measurable payoff — your brain (or the model's context) forgets implementation details and notices problems. For AI agents, a fresh session achieves the same effect instantly.

### Adversarial Review

Explicitly prompting for adversarial thinking catches edge cases:

- "What edge cases would break this?"
- "How would an attacker exploit this?"
- "What happens with 0, negative, null, empty, huge inputs?"

**Caution:** Adversarial AI reviewers will find "problems" even when none exist. Validate findings before acting.

---

## 10. XP/BDD/TDD Connection

### BDD: Verification IS Acceptance Criteria

Dan North: "A story's behaviour is simply its acceptance criteria — if the system fulfils all the acceptance criteria, it's behaving correctly."

This maps directly to `review-task`: verify each AC with evidence.

### TDD as Quality Gate

Kent Beck's TDD provides continuous verification during implementation. The test suite IS the verification mechanism. `review-task` then checks: do the tests actually cover the ACs? Is there a gap between what's tested and what's specified?

### Pair Programming Vs Review

Martin Fowler: code review is not an adequate substitute for pair programming due to sunk cost fallacy and deferred responsibility. In agentic work, this translates to: self-review (same session) has the same problems as reviewing your pair's code after the fact. Fresh context is the closest agentic equivalent to a pair's "navigator" role.

### Collective Code Ownership

XP's collective code ownership means anyone can change any code. The corollary: review should check that changes are consistent with the whole system, not just locally correct. This is `code-review`'s domain — codebase patterns, conventions, architectural fit.

---

## 11. Design Decisions for TAD Skills

Based on the research:

### Review-Task

1. **Fresh session required** — self-review is unreliable
2. **Grounded in task spec** — ACs, plan, description, notes
3. **Evidence-based** — each AC verified with specific evidence
4. **Binary outcome** — pass (with evidence) or fail (with specific gaps)
5. **No code quality concerns** — that's code-review's job
6. **Human decides next step** — re-implement, adjust task, or proceed

### Code-Review

1. **Grounded in CLAUDE.md and codebase** — not task specs
2. **Priority hierarchy** — correctness > design > testing > security > conventions
3. **Skip automated concerns** — linting, types, formatting
4. **Confidence threshold** — only report high-confidence findings
5. **Serves both interactive and CI** — same principles, different triggers
6. **Evidence required** — every finding cites specific code

### Relationship

- `review-task` is Phase 4 of the task lifecycle (after impl-task)
- `code-review` is independent — runs daily in CI, or on-demand
- They don't call each other — orchestration is the human's job
- Together they cover both concerns: "does it do what was asked?" + "is the code good?"

---

## Sources

### Traditional Code Review

- Google Engineering Practices — eng-practices/review
- Microsoft Research — Characteristics of Useful Code Reviews (1.5M comments)
- SmartBear/Cisco — Best Kept Secrets of Peer Code Review (200-400 LOC)
- LinearB 2025 — Analysis of 6.1M PRs (average 219 lines)
- Rishi Baldawa — The Cognitive Load Cliff in Code Review

### Agentic AI Review

- Anthropic — Multi-agent code review (March 2026, sub-1% FP rate)
- CRITIC framework — Tool-interactive correction (arxiv 2305.11738)
- Self-Refine — Iterative self-feedback (OpenReview)
- SelFee — Optimal 3 revisions (KAIST)
- Atom Robot — Two-phase refine-then-fresh workflow

### AI Review Tools

- Graphite Agent — >80% signal ratio, <3% unhelpful rate
- Greptile — Full codebase context, 3x bug detection vs diff-only
- CodeRabbit — 2M+ repos, 46% runtime bug accuracy
- Qodo 2.0 — Semantic analysis, highest F1 score
- GitHub Copilot — 60M+ reviews, poor signal ratio

### BDD/XP/TDD

- Dan North — Introducing BDD (dannorth.net)
- Martin Fowler — Pair Programming Misconceptions
- Kent Beck — TDD By Example, 3X
- Liz Keogh — Acceptance Criteria vs Scenarios

### Solo Dev Practices

- Sean Goedecke — "If you are good at code review, you will be good at using AI agents"
- Jonathan Hall — Code review for solo projects
- Addy Osmani — Code Review in the Age of AI

### Empirical Studies

- SWR-Bench — 1,000 GitHub PRs, LLM evaluation ~90% alignment
- CodeRabbit vs Human — AI code creates 1.7x more issues
- Anchoring Bias in LLMs — arxiv 2412.06593
- Systematic Overcorrection — arxiv 2603.00539
