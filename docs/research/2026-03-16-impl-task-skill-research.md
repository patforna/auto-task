# Impl-Task Skill Research

**Date:** 2026-03-16 **Goal:** Design a maximally effective `/impl-task` skill for solo-dev agentic workflow, incorporating latest insights from practitioners and research.

---

## 1. Research Sources

### Codebase (6 Agents)

- Full task workflow: define-task, plan-task, create-task, review-task, code-review, repo-health
- Current impl-task and impl skills
- tddv2 skill (Beck-style TDD)
- docs/research (14 prior research documents)
- Codebase conventions, test infra, CI/CD

### External (6 Agents)

- **Kent Beck**: TDD + AI ("augmented coding"), Canon TDD, breathing rhythm
- **Peter Steinberger**: Agentic engineering, blast radius, post-impl testing
- **Steve Yegge**: Molecular tasks, 30-40% code health, multiple review passes
- **Jeffrey Emanuel**: Rule of Five, sequential review passes, coordination > generation
- **Simon Willison**: Red/Green TDD with agents, zero tolerance for code smells
- **Addy Osmani**: 70/30 ratio (verification/execution), spec-first, self-improving agents
- **Frontier labs**: Anthropic, OpenAI, Google best practices; ETH Zurich context file research
- **Academic**: DORA 2025, METR study, SWE-bench insights, agentic SE pillars
- **Community**: Karpathy, swyx, Jason Liu, Martin Fowler, Tweag handbook

---

## 2. What Exists Today

The current `/impl-task` is a 100-line skill with six steps:

1. **Read and Understand** — task, plan, epic, CLAUDE.md, referenced files
2. **Implement** — follow plan step-by-step, TDD style, verify after each step
3. **Commit** — pull, commit with task reference, don't push
4. **Summarise** — write summary into task below plan
5. **Codify Learnings** — knowledge.md, decisions.md, or CLAUDE.md
6. **Update Status** — set `done`, update epic if applicable

### Strengths

- Clear phased structure with self-contained handoff
- Enforces reading CLAUDE.md and plan before implementing
- Plans are treated as self-contained (no original context needed)
- Epic integration for status tracking
- Anti-patterns section

### Gaps Identified Across All Research

- **No TDD mechanics** — says "use TDD style" but doesn't specify how (the tddv2 skill has the detail but isn't integrated)
- **No self-review** — research shows 29.6% of plausible fixes introduce regressions (SWE-bench); fresh-session review catches 40-60% more issues but a pre-commit self-check still adds value
- **No scope creep detection** — Spotify: ~25% of AI changes vetoed for exceeding scope; no mid-flight checks
- **No error recovery** — what to do when a step fails, when to backtrack vs push forward
- **No breathing rhythm** — Beck: AI only inhales (adds complexity), never exhales (refactors); the skill doesn't force refactoring
- **No commit hygiene** — no "review your diff before committing" step
- **No context management** — no guidance on when to clear, compact, or scope context
- **Vague deviation handling** — "update plan in task to reflect reality" but no guidance on when deviation warrants stopping vs continuing

---

## 3. Key Insights from Research

### 3.1 the TDD Question (Resolved: Yes, with Adaptations)

**The tension:**

- Beck, Yegge, Willison, DORA, Codemanship all advocate TDD with AI
- Steinberger explicitly does NOT do TDD, preferring post-impl testing in same context

**The evidence:**

- **DORA 2025**: AI amplifies existing practices; TDD becomes MORE critical, not less
- **Codemanship**: LLMs have effective context limits far smaller than advertised; single-problem-at-a-time approaches stay within effective processing capacity
- **SWE-bench**: 29.6% of "plausible" fixes introduce regressions — tests catch these
- **Beck**: AI cannot distinguish working from broken code; once broken code enters context, it pollutes subsequent predictions
- **Steinberger's context**: He works on UI/product code where visual testing (screenshots) is primary; his "post-impl testing in same context" is functionally similar to TDD — write code, then write tests that verify it, in the same session

**Resolution for TAD:** TDD is non-negotiable for this codebase. Quant code has silent-corruption risks (NaN propagation, division-by-zero, rolling window edge cases) that produce wrong numbers, not errors. Tests are the only defense. The tddv2 skill's mechanics should be deeply integrated into impl-task, not merely referenced.

**However**, the TDD cycle should be adapted for agentic execution:

- **Step size flexibility**: Beck's "obvious implementation" for trivial wiring steps; "fake it" / "triangulation" for uncertain quant logic
- **Plan steps as test selection guidance**: Each plan step already names a "behaviour to verify" — this IS the test to write
- **No approval gates**: Unlike the /tdd skill, impl-task runs autonomously; the plan IS the pre-approved specification
- **Commit at green**: Each step that passes gets committed, creating fine-grained git history as a safety net

### 3.2 the Breathing Rhythm (Beck)

Beck's most important insight for agentic development: AI only "inhales" (adds features, complexity) and never "exhales" (refactors). His first two B+ tree attempts failed because accumulated complexity stalled the agent.

**Implication for impl-task:** After each step reaches green, the agent MUST consider refactoring before moving to the next step. This is not optional tidying — it's load-bearing for the agent's ability to continue working effectively. The tddv2 skill already encodes this as "Refactor: Remove duplication introduced by getting to green."

### 3.3 Molecular Task Decomposition (Yegge)

Yegge's single most repeated advice: "Give them the tiniest task, the most molecularly tiny segmented task you can give them."

**Implication for impl-task:** Each plan step should be small enough to complete in one red-green-refactor cycle. If a step requires multiple test-implement cycles, it's too big. The impl-task skill should detect this and either:

1. Break the step into sub-steps in the moment, or
2. Flag that the plan needs re-scoping

### 3.4 Sequential Review Passes (Emanuel)

Emanuel's "Rule of Five": sequential passes with narrowing focus beat single comprehensive review:

1. Correctness — fix errors, bugs, logic
2. Clarity — simplify, remove jargon
3. Edge cases — what could go wrong
4. Excellence — final polish

**Implication for impl-task:** A pre-commit self-review with focused lenses catches issues the implementation phase misses. Not a replacement for `/review-task` (fresh session), but valuable preparation. The focus should be narrow: scope compliance and diff hygiene (did I change only what I should have?).

### 3.5 Context Engineering > Prompt Engineering

**ETH Zurich finding**: LLM-generated context files REDUCE task success by 3% and increase costs by 20%. Even human-written context files offer marginal 4% gains.

**Anthropic**: "The smallest set of high-signal tokens that maximize the likelihood of the desired outcome." A clean context on a weaker model beats a cluttered context on a stronger model.

**Implication for impl-task:** The skill should be lean. Don't repeat CLAUDE.md rules. Don't add universal truths. Every line must earn its place by preventing a specific failure mode that the agent would otherwise hit. The plan-task skill already embodies this via the "nervousness heuristic" — the same principle applies to the impl-task skill itself.

### 3.6 Verification Is the Highest-Leverage Practice (Anthropic)

Anthropic's official best practice: "The single highest-leverage thing you can do is give the agent a way to verify its own work."

**What this means concretely:**

- Run tests after every change (already in tddv2)
- Run `just check` before committing (already in impl-task)
- Review the diff before committing (missing from current skill)
- Verify acceptance criteria are met before declaring done (missing)

### 3.7 Incompressible Prompt Design

Research on what makes prompts robust across model versions:

- **Structural elements** (clear section headers, numbered steps) survive model transitions better than stylistic cues
- **Concrete examples** are more portable than abstract rules
- **Verification criteria** are model-agnostic by nature
- **Don't over-constrain**: future models are more capable; leave room for the model to use its judgment
- **Self-consistency** benefits increase with model scale (+23% for larger models)

**Implication for impl-task:** Write the skill as a clear sequence of checkpoints with concrete verification, not as a set of rules the model must remember. Structure > prose. Let the model fill in details from CLAUDE.md and the codebase.

### 3.8 the Osmani Ratio (70/30)

Developers succeeding with AI spend 70% of time on problem definition and verification, 30% on execution. This is inverted from traditional development.

**Implication for impl-task:** The skill should allocate attention proportionally:

- Steps 1 (Read/Understand) and the verification portions of Step 2 are the 70%
- The actual code writing is the 30%
- This means the skill should spend more words on HOW to verify than HOW to implement

### 3.9 Commit Frequency as Safety Net

Both Yegge and Beck emphasise frequent commits:

- Yegge: "Commit every few minutes"
- Beck: "Commit at green" (after every successful test cycle)
- Steinberger: Small, isolated commits always preferable to one massive refactor

**Implication for impl-task:** Commit after each plan step passes (not just at the end). This creates fine-grained git history, enables selective revert, and prevents the catastrophic loss of a long implementation session. Use `just commit` which runs `just check` atomically.

---

## 4. Design Decisions

### D1: Integrate TDD Mechanics Directly (Not by Reference)

The current skill says "use TDD style" without specifying how. The tddv2 skill has the detail. Options:

**Option A: Reference tddv2** — "Follow the tddv2 skill for each step." Problem: adds a 110-line skill to the context that the model may not fully absorb.

**Option B: Inline the essential TDD mechanics** — Extract the core cycle and strategies into impl-task. Problem: duplication with tddv2.

**Option C: Inline the TDD checkpoint pattern, reference tddv2 for depth** — Include the red-green-refactor cycle and the three strategies as a concise summary within impl-task, with a note that tddv2 has full patterns for complex cases.

**Decision: Option C.** The cycle and three strategies (Fake It, Triangulation, Obvious Implementation) fit in ~15 lines and are the highest-leverage content. The full pattern catalog (Child Test, Value Objects, etc.) is useful but only needed for complex implementations — reference, don't inline.

### D2: Pre-Commit Self-Review (Yes, Focused)

Research shows self-review catches fewer issues than fresh-session review (40-60% gap). But it catches DIFFERENT issues — primarily scope creep and diff hygiene. Include a focused pre-commit check:

1. **Scope check**: Does the diff touch only what the plan requires?
2. **AC verification**: Can each acceptance criterion be demonstrated?
3. **Commit hygiene**: Are there unrelated changes, debug prints, or TODO comments?

This is NOT a comprehensive code review (that's `/code-review`'s job).

### D3: Commit per Step Vs Commit at End

**Decision: Commit per step.** Each plan step that passes `just check` gets its own commit. Benefits:

- Fine-grained git history
- Selective revert capability
- Progress is never lost
- Natural checkpoints for context management

The final commit updates the task file (summary, status, learnings).

### D4: When to Stop Vs When to Continue

The current skill has no guidance on error recovery. Add explicit decision points:

- **Test fails after implementation**: Try to fix. If stuck after 2 attempts, backtrack to last green state and take a smaller step (Beck's advice).
- **Plan step seems wrong**: Update the plan in the task, note the deviation, continue.
- **Scope creep detected**: Stop, note what was discovered, flag to user.
- **`just check` fails**: Fix. If the failure is in unrelated code, flag to user rather than fixing silently.

### D5: Context Management Guidance

Add explicit guidance:

- Start implementation with the task file + CLAUDE.md + referenced files loaded
- Don't read the entire codebase upfront — load files as needed per step
- If context becomes cluttered mid-implementation, the frequent commits mean progress is safe

### D6: Skill Length and Density

**Target: ~150 lines.** The current skill is 100 lines. Adding TDD mechanics, self-review, commit-per-step, and error recovery will increase length. But per ETH Zurich, overspecification hurts. Every line must prevent a specific failure the agent would otherwise hit.

Apply the nervousness heuristic to the skill itself: what would you be nervous about if the agent had only CLAUDE.md and the plan? Those things — and only those — belong in the skill.

### D7: Incorporate Tddv2 or Keep Separate

**Decision: Subsume tddv2 into impl-task for the task workflow.** Keep tddv2 as a standalone skill for ad-hoc TDD work outside the task workflow. The impl-task skill will contain the essential TDD mechanics tailored to plan-step execution, which is a more specific and effective framing than generic TDD.

The key adaptation: each plan step names a behaviour to verify → that behaviour IS the first test to write. The plan provides the test selection strategy that tddv2 leaves to the developer.

### D8: Drop the /Impl (Divergent Generation) Approach

The current `/impl` skill launches parallel Opus + Codex agents for divergent generation. This is powerful for high-stakes quant logic but:

- Adds significant complexity and cost
- Assumes specific models are available
- The plan-task skill already supports dialectic planning (multi-model diversity)
- Divergent generation at implementation time is less valuable when the plan was already stress-tested

**Decision: Don't merge /impl into /impl-task.** Keep `/impl` as a separate specialist skill for cases where the user explicitly wants divergent implementation. `/impl-task` is the standard path.

---

## 5. The Ideal Impl-Task Flow

Based on all research, the ideal flow is:

```text
1. ORIENT
   Read task → plan → ACs → epic (if any) → CLAUDE.md → referenced files
   Confirm understanding — no silent assumptions

2. IMPLEMENT (per plan step)
   For each step:
   a. RED    — write a failing test for the behaviour the step names
   b. GREEN  — make it pass (simplest change; choose strategy by confidence)
   c. REFACTOR — remove duplication (Beck's "exhale")
   d. VERIFY — run `just check`
   e. COMMIT — `just commit "step description (refs task)" <files>`

   If step is pure wiring (no behaviour to test): implement, verify, commit.
   If step fails after 2 fix attempts: backtrack to last green, take smaller step.
   If plan step seems wrong: update plan in task, note deviation, continue.

3. FINAL VERIFICATION
   Run `just check` (full suite)
   Review the full diff (git diff main..HEAD or since first commit)
   For each AC: verify it's demonstrably met
   Check: only task-related files changed? No debug artifacts? No scope creep?

4. SUMMARISE
   Write summary into task below plan
   Note deviations, commit hashes, anything surprising

5. CODIFY LEARNINGS
   Domain insight → knowledge.md
   Design decision → decisions.md
   New convention → CLAUDE.md
   Skip if nothing surprising

6. UPDATE STATUS
   Task status → done
   Epic table → updated (if applicable)
   Commit task file update
```

### Key Differences from Current Skill

| Aspect                | Current           | Proposed                                          |
| :-------------------- | :---------------- | :------------------------------------------------ |
| TDD mechanics         | "Use TDD style"   | Inline red-green-refactor cycle with 3 strategies |
| Commit cadence        | Once at end       | Per plan step                                     |
| Refactoring           | Not mentioned     | Mandatory after each green (breathing rhythm)     |
| Self-review           | None              | Pre-commit scope + AC verification                |
| Error recovery        | None              | 2-attempt rule, backtrack to green                |
| Diff review           | None              | Review full diff before final commit              |
| Scope creep detection | None              | Flag if diff touches non-plan files               |
| Context management    | None              | Load files per step, not all upfront              |
| Wiring steps          | Not distinguished | Explicit skip-TDD path for pure wiring            |

---

## 6. What NOT to Include (Anti-Overspecification)

Per ETH Zurich research and the nervousness heuristic, these should NOT be in the skill:

- **CLAUDE.md rules** — the agent reads CLAUDE.md in Step 1; don't duplicate
- **How to write good tests** — tddv2 has this for complex cases; the cycle is enough for impl-task
- **Code style guidance** — ruff + pyright enforce this mechanically
- **Architecture rules** — test_architecture.py enforces these
- **Generic software engineering wisdom** — "handle errors", "follow conventions", "be careful"
- **Full TDD pattern catalog** — Child Test, Value Objects, etc. Reference tddv2 for these
- **Domain-specific quant patterns** — these belong in CLAUDE.md, not the skill
- **How to use git** — the commit recipe is in CLAUDE.md; `just commit` handles mechanics

---

## 7. Open Questions

### Q1: Should Impl-Task Auto-Trigger Tddv2?

Could impl-task set a flag or instruction that causes tddv2 to auto-load alongside it? This would give the agent access to the full TDD pattern catalog without inlining it. **Recommendation: No.** The essential cycle is inlined; the full catalog is a reference for the user to invoke manually if the implementation hits complexity.

### Q2: Should the Skill Support Resumption?

If the agent runs out of context or the session is interrupted, can it resume? The per-step commits make this possible — the agent can check git log and the task file to see which steps are done. **Recommendation: Yes, implicitly.** The skill already says "start fresh session" and the plan + commit history provides state. No explicit resumption protocol needed — the plan IS the resumption protocol.

### Q3: Should There Be a "Complexity Gate" That Routes to /Impl?

For high-stakes quant logic, should impl-task detect complexity and suggest using /impl (divergent generation) instead? **Recommendation: No.** The user makes this call when choosing the skill. The plan-task skill already uses dialectic planning for complex tasks, which is where model diversity adds the most value.

---

## 8. Practitioner Positions Summary

| Practitioner      | TDD? | Key Contribution to impl-task                                                                   |
| :---------------- | :--- | :---------------------------------------------------------------------------------------------- |
| Kent Beck         | Yes  | Breathing rhythm (refactor after green), Canon TDD, never delete tests, context restriction     |
| Steve Yegge       | Yes  | Molecular tasks, 30-40% code health budget, multiple review passes, commit constantly           |
| Jeffrey Emanuel   | —    | Rule of Five (sequential focused review passes), coordination > generation                      |
| Peter Steinberger | No   | Blast radius concept, living CLAUDE.md, "just talk to it" (don't over-constrain)                |
| Simon Willison    | Yes  | Red/Green TDD with agents, zero tolerance for code smells, hoard reusable instructions          |
| Addy Osmani       | —    | 70/30 ratio (verification/execution), spec-first, self-improving agents via git history         |
| Anthropic         | —    | Verification is highest-leverage, lean CLAUDE.md, subagents for exploration, context management |
| ETH Zurich        | —    | Overspecification hurts (-3% success, +20% cost), only include non-inferable information        |
| DORA 2025         | Yes  | AI amplifies practices — TDD becomes MORE critical with AI, not less                            |
| METR 2025         | —    | Agents that verify avoid the 200K token plateau; 29.6% of plausible fixes regress               |

---

## 9. Recommended Next Steps

1. **Write the new impl-task skill** based on the flow in Section 5 and decisions in Section 4
2. **Keep tddv2 as standalone** for ad-hoc TDD outside the task workflow
3. **Keep /impl as specialist** for divergent generation (user-invoked, not default)
4. **Test the skill** on 2-3 real tasks to validate before committing to using it 100s of times
5. **Iterate** — the skill itself should evolve via the same define → plan → implement cycle
