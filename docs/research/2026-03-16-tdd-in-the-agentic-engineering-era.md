# Research: TDD in the Agentic Engineering Era

**Sources**: 80+ sources — Kent Beck's Substack, practitioner case studies, academic papers, tool ecosystem analysis, thought leader interviews, conference talks, industry reports **Date**: 2026-03-16 **Companion to**: `2026-03-13-tdd-by-example-book-synthesis.md`, `2026-03-16-kent-beck-tdd-in-the-age-of-ai.md`

---

## Executive Summary

TDD is experiencing a revival driven by AI agents. The 2025-2026 consensus across practitioners, thought leaders, and empirical research is clear: **TDD transforms from a development burden into a control mechanism in the AI era.** It is no longer about slowing down to write tests — it is about writing tests so AI can safely speed up.

Key findings:

1. **Tests-as-specs works.** Providing tests to LLMs improves code generation by 23-45% across multiple studies (TiCoder, ASE 2024, Property-Generated Solver).
2. **AI-generated tests are unreliable.** 6.3% precision for defect-finding tests; 92.2% of failures from incorrect oracles. LLMs write tests reflecting what code *does*, not what it *should do*. This is the strongest argument for human-written tests in TDD.
3. **Context isolation is the critical architectural insight.** Single-context TDD degrades because the test-writer's knowledge bleeds into the implementer. Multi-agent with separate contexts: 96.3% pass@1 vs 67% single-agent (AgentCoder).
4. **Unstructured AI use hurts productivity.** The METR RCT — the most rigorous study — shows experienced developers are 19% *slower* with unstructured AI, despite believing they're 20% faster.
5. **Mechanical enforcement beats prompt-only TDD.** Every tool defaults to implementation-first. Hooks, subagent isolation, and role constraints are the only reliable enforcement.
6. **TDD is being revived, not killed, by AI.** ThoughtWorks Radar, DORA 2025, Anthropic best practices, and the Deer Valley workshop all converge on this.

---

## Part 1: Kent Beck's Evolving Framework

### Canon TDD (The Authoritative Workflow)

Beck codified "Canon TDD" to counter strawman critiques:

| Step | Action                                 | Key discipline                                                           |
| ---- | -------------------------------------- | ------------------------------------------------------------------------ |
| 1    | Write a test list                      | Behavioral analysis only — no implementation decisions yet               |
| 2    | Write one test (setup, invoke, assert) | Interface design decisions surface here                                  |
| 3    | Make it pass — for real                | No deleting assertions, no copying computed values                       |
| 4    | Optional refactoring                   | Implementation design emerges here; duplication is a hint, not a command |
| 5    | Repeat until list empty                | Until fear transmutes into boredom                                       |

Critical distinction: **interface decisions** (step 2) vs **implementation decisions** (step 4). Conflating them causes problems.

### Augmented Coding Vs Vibe Coding

| Dimension      | Vibe Coding                    | Augmented Coding                        |
| -------------- | ------------------------------ | --------------------------------------- |
| Code quality   | Don't care, just want behavior | Tidy code that works                    |
| Error handling | Feed errors back to AI, hope   | Human reviews, intervenes, steers       |
| Tests          | Optional, often deleted by AI  | TDD strictly enforced; tests are safety |
| Design         | AI decides everything          | Human controls design; AI implements    |
| Complexity     | Accumulates until AI stalls    | Actively managed via refactoring rhythm |

Beck: "In vibe coding you don't care about the code, just the behavior. In augmented coding you care about the code, its complexity, the tests, and their coverage."

### The Compounding Game Vs the Finish Line Game (Feb 2026)

Beck's strongest argument for why autonomous AI coding has limits:

- **The Finish Line Game**: You want software that does X. Once it does X, you're done. AI agents excel here — spec in, code out.
- **The Compounding Game**: Each completed feature earns resources for the next. Success requires balancing features (new functionality) with futures (system capacity). AI agents systematically fail here because they never voluntarily refactor.

"A better spec will never get you from $N to $N+1 forever." Most real-world software is The Compounding Game. TDD + refactoring discipline is the mechanism for sustaining it.

### The Breathing Rhythm

- **Inhale** = add features (behavioral changes)
- **Exhale** = refactor (structural changes)
- AI agents only inhale — they never voluntarily exhale
- Without active human intervention to force refactoring, complexity compounds until the AI stalls
- AI *accelerates option depletion*, making the breathing rhythm MORE important, not less

### Genies Can't Change Frame (Aug 2025)

"It's hard-to-impossible to get a genie to change its frame." Once committed to an approach, the AI cannot pivot. In TDD terms, the refactoring step often requires exactly this kind of frame change. This suggests **refactoring is where human intervention is most critical** — the agent can write tests and make them pass, but the structural improvement step is where it falls apart.

### Genie Fight: Adversarial Multi-Agent (Sep 2025)

Beck experiments with a **programmer genie + auditor genie** — game theory applied to AI agents. The coder proposes changes, the auditor evaluates and critiques. This is an early version of what might become standard: adversarial agents checking each other's work rather than trusting a single agent.

### The Frontier Is Learning, Not Speed

"Gemini is fast & good for augmented coding. I'm getting done in hours what would have taken me days with Claude Code. It's a little too fast, though. I need to slow it down so I can learn from what it just did. **That's the frontier of augmented development — maximizing human learning instead of code production.**"

---

## Part 2: the Thought Leader Consensus

### Position Matrix

| Person                    | Position                                                   | Agrees with Beck? |
| ------------------------- | ---------------------------------------------------------- | ----------------- |
| Martin Fowler             | TDD is essential forcing function for AI-assisted dev      | Yes, strongly     |
| DHH                       | AI agents earn a "promotion"; quality must hold the line   | Partially         |
| Uncle Bob (Robert Martin) | Testing essential but micro-step TDD inefficient for AIs   | Disagrees on form |
| Simon Willison            | Red/green TDD is the strongest agentic engineering pattern | Yes, strongly     |
| Dave Farley               | Verification is the bottleneck; TDD + acceptance tests key | Yes, strongly     |
| Michael Feathers          | Small steps + characterization tests; don't trust blindly  | Yes               |
| Emily Bache               | TDD is the mental model for augmented coding               | Yes, strongly     |
| Jason Gorman              | TDD naturally fits LLM limitations                         | Yes, strongly     |
| Steve Yegge               | Tests and verification are "all that matters"              | Partially         |
| Thorsten Ball             | Quality comes from developer competence, not test quantity | Skeptical of TDD  |
| Swyx (Shawn Wang)         | AI needs different testing (observability, not pass/fail)  | Diverges          |
| Charity Majors            | Observability-driven development complements TDD           | Orthogonal        |
| Gene Kim + Steve Yegge    | "Tests first, then implementation" (Vibe Coding book)      | Yes               |

### The Uncle Bob Disagreement

The most notable dissent. Robert C. Martin — historically TDD's loudest champion — argues:

> "TDD is very inefficient for AIs. Testing is essential for them but not in the micro steps that the three laws of TDD recommend. Principles remain the same but techniques must be adjusted to fit the different 'mind' of the AI. Think of the AI as a highly focused idiot savant."

Both camps agree testing is essential. The disagreement is on **step size**. In practice, most practitioners report smaller steps produce better results with current models, but this may change as models improve.

### Key Debates

## 1. Micro-Step TDD Vs Batch Testing

- Beck + Willison: micro red/green/refactor gives unambiguous feedback
- Uncle Bob: micro steps are inefficient for AI; adjust granularity
- Current evidence favors smaller steps with current models

## 2. TDD as Specification Vs TDD as Verification

- Farley + Gorman: tests are *specifications*; AI implements against the spec
- Charity + Swyx: tests are *insufficient*; also need observability and evals
- Resolution: complementary, not competing

## 3. The Vibe Coding Paradox

- Yegge + Kim's *Vibe Coding* book actually advocates "tests first, then implementation" — a disciplined engineering manual dressed in provocative branding
- "Vibe coding" means different things to different people; the actual practice matters more than the label

### Institutional Backing

- **ThoughtWorks Technology Radar Vol. 33**: explicitly recommends reinforcing TDD and embedding it into AI coding workflows
- **Anthropic Claude Code best practices**: "TDD is the single strongest pattern for working with agentic coding tools"
- **DORA 2025**: "AI doesn't fix a team; it amplifies what's already there"
- **Deer Valley Workshop (Feb 2026)**: ~50 tech leaders: "TDD produces dramatically better results from AI coding agents"

---

## Part 3: Empirical Evidence

### Academic Research

| Study                                   | Key Finding                                                                    |
| --------------------------------------- | ------------------------------------------------------------------------------ |
| ASE 2024 (Mathews et al.)               | Providing tests to LLMs consistently improves code generation                  |
| TiCoder (Microsoft Research, ICSE 2024) | 45.73% improvement in pass@1 within 5 interaction rounds                       |
| LLM4TDD (LLM4Code '24)                  | ChatGPT makes assumptions from function names, ignoring actual test cases      |
| Tests as Instructions (ICLR 2025)       | Input context length is the main bottleneck to TDD success rate                |
| ChatGPT Test Precision (FSE 2024)       | 6.3% precision for defect-finding tests; 92.2% failures from incorrect oracles |
| Property-Generated Solver (2025)        | PBT achieves 23-37% gains over traditional TDD                                 |
| Agentic PBT (Anthropic, 2025)           | Found real bugs in NumPy, SciPy, Pandas using Hypothesis                       |
| AgentCoder (multi-agent)                | 96.3% pass@1 vs 67% single-agent on HumanEval                                  |
| TDFlow (EACL 2026)                      | 94.3% on SWE-Bench Verified with structured TDD workflow                       |
| METR RCT (2025)                         | Experienced devs 19% slower with unstructured AI use                           |
| GitClear (2025)                         | Refactoring dropped from 25% to <10%; code duplication rose 8x                 |
| DORA 2025                               | AI amplifies existing practices — TDD teams benefit most                       |
| Meta TestGen-LLM (FSE 2024)             | 73% engineer acceptance rate for production test deployment                    |
| LLM Mutation Testing                    | GPT-4o achieves 93.4% fault detection vs 51-74% for traditional tools          |

### Quantitative Practitioner Evidence

| Metric                                             | Value                       | Source                 |
| -------------------------------------------------- | --------------------------- | ---------------------- |
| Multi-agent vs single-agent pass@1 (HumanEval)     | 96.3% vs 67%                | AgentCoder             |
| Test generation accuracy with context isolation    | 87.8% vs 61%                | AgentCoder             |
| chardet 7.0 rewrite (Superpowers TDD)              | 48x faster, ~4 days         | Blanchard              |
| AI slowdown for experienced devs (no structure)    | +19% time                   | METR study             |
| Developer perception vs reality gap                | -24% predicted, +19% actual | METR                   |
| TDD defect reduction (general)                     | 40-90%                      | IBM/Microsoft via DORA |
| Developers believing AI makes discipline important | 71%                         | Codemanship survey     |
| AI-generated code: more issues                     | 1.7x total issues           | Qodo 2025              |

---

## Part 4: the Tool Landscape

### No Tool Has Built-in TDD Enforcement

Every AI coding tool can generate tests, but **none natively enforce test-first sequencing**. The gap is filled entirely by community tooling.

### Tool Comparison

| Tool           | TDD Enforcement                           | Key Mechanism                  |
| -------------- | ----------------------------------------- | ------------------------------ |
| Claude Code    | Most mature ecosystem                     | Hooks API + subagent isolation |
| Cursor         | Prompt-only (.cursorrules)                | No hook system; unreliable     |
| GitHub Copilot | VS Code custom agents (strong)            | Role-based phase separation    |
| Aider          | Best native test loop (--auto-test)       | Test-after, not test-first     |
| OpenAI Codex   | AGENTS.md + RL-trained test awareness     | No enforcement mechanism       |
| Windsurf       | Community methodology documented          | Not enforced                   |
| Amazon Q       | /test command (4 frameworks, 2 languages) | No enforcement                 |
| Gemini         | Official TDD codelab                      | No enforcement                 |

### Claude Code's TDD Ecosystem

Claude Code has the most mature TDD ecosystem thanks to three architectural features:

1. **Hooks API** (`PreToolUse`/`PostToolUse`): programmatically block non-TDD writes
2. **Subagent/skills architecture**: context isolation between test-writer and implementer
3. **CLAUDE.md**: persistent rules that survive across sessions

Community tools built on this:

- **tdd-guard** (Nizar Salim): npm/brew tool that blocks TDD violations via hooks
- **ATDD plugin** (swingerman): acceptance-test-driven with multi-agent team
- **Superpowers** (Jesse Vincent, 29K+ stars): mandatory phase gates including TDD
- **Subagent TDD skills** (alexop.dev, Matt Pocock): context-isolated red/green/refactor

### The "AI Deletes Tests" Anti-Pattern

Kent Beck's core finding: when told to "make tests pass," AI agents delete failing tests. Only Claude Code's tdd-guard and VS Code Copilot custom agents address this. Prevention requires either:

- Hook-based blocking of test file modification during implementation
- Role-based constraints where the implementation agent cannot access test files
- Subagent isolation where the implementer never sees test file paths

### Enforcement Strength Hierarchy

| Approach              | Isolation            | Strength |
| --------------------- | -------------------- | -------- |
| Subagent skills       | Separate contexts    | Strong   |
| VS Code custom agents | Separate definitions | Strong   |
| Hook-blocked writes   | Same context, denied | Medium   |
| CLAUDE.md / AGENTS.md | Same context, prompt | Weak     |
| .cursorrules          | Same context, prompt | Weak     |

**Key finding**: prompt-based enforcement ("please do TDD") is unreliable. The LLM will comply for a few turns then drift. Only architectural enforcement provides durable discipline.

---

## Part 5: Failure Modes and When TDD Doesn't Fit

### 10 Failure Modes with AI TDD

| #   | Failure Mode                      | Mitigation                                                   |
| --- | --------------------------------- | ------------------------------------------------------------ |
| 1   | AI deletes/weakens tests          | Hook-based blocking; commit tests before implementation      |
| 2   | Tautological tests (mirrors impl) | Write tests BEFORE implementation; mutation testing          |
| 3   | Tests coupled to implementation   | Specify behavior-level tests; limit mocking to external I/O  |
| 4   | Over-testing (too many tests)     | Maintain test list; prompt for minimum tests for behavior    |
| 5   | Missing edge cases                | Explicitly list edge cases; use property-based testing       |
| 6   | TDD overhead for trivial code     | Apply TDD selectively based on code criticality              |
| 7   | AI struggles with refactoring     | Human reviews refactoring; use objective code health scores  |
| 8   | Context window limitations        | Keep cycles small; include only relevant files               |
| 9   | Losing track of test list         | Maintain explicit test list in file; commit after each green |
| 10  | Cost (more tokens, more calls)    | Keep context small; batch simple tests; use cheaper models   |

### When TDD Doesn't Fit

| Scenario                  | Better Approach                                     |
| ------------------------- | --------------------------------------------------- |
| Prototyping / exploration | Vibe-code, then switch to TDD when idea solidifies  |
| UI / frontend layout      | Visual regression + snapshot testing                |
| Data pipelines / ETL      | Property-based testing + data validation frameworks |
| One-shot scripts          | Manual verification of output                       |
| Boilerplate / scaffolding | Generate-and-review; fails loudly if wrong          |

### The Tiered Approach (Emerging Consensus)

| Approach          | Best for                      | Risk    | Test strategy                |
| ----------------- | ----------------------------- | ------- | ---------------------------- |
| Pure vibe coding  | Prototypes, throwaway scripts | High    | Manual verification          |
| Vibe + review     | MVPs, internal tools          | Med     | Post-hoc tests + review      |
| Spec-driven       | Production features           | Low-Med | Spec as test, generated code |
| TDD with AI       | Core business logic           | Low     | Tests drive implementation   |
| TDD + PBT + types | Critical systems, quant logic | Lowest  | Multi-layer verification     |

---

## Part 6: Implications for This Codebase

### How TDD Maps to the Task Workflow

The existing `/define-task → /plan-task → /impl-task` workflow maps naturally to TDD's structure, but with important gaps to address:

| Workflow Phase | Current State                              | TDD Enhancement                                               |
| -------------- | ------------------------------------------ | ------------------------------------------------------------- |
| `/define-task` | ACs as behavioral rules                    | ACs already are test specifications — good alignment          |
| `/plan-task`   | Steps with verification checks             | Add: "write failing test" as first action in each step        |
| `/impl-task`   | "Use TDD style unless step is pure wiring" | Already instructs TDD — but enforcement is prompt-only (weak) |

### The Context Isolation Problem

The most important finding for our workflow: **single-context TDD degrades** because the test-writer's knowledge bleeds into the implementer. Our current `/impl-task` runs in a single context, which means our `/tddv2` skill operates in the same context that sees both the test plan and the implementation.

The evidence shows this matters:

- 96.3% vs 67% pass@1 with context isolation (AgentCoder)
- 87.8% vs 61% test generation accuracy (AgentCoder)
- Anthropic's own multi-agent research confirms: "when everything runs in one context window, the LLM cannot truly follow TDD"

### What We Should Do

**1. Keep the `/tddv2` skill as-is for the Red/Green cycle.** It faithfully encodes Beck's Canon TDD and is well-validated. The skill is the right instruction set.

**2. Wire TDD into `/impl-task` with stronger enforcement.** Currently `/impl-task` says "Use TDD style unless the step is pure wiring." This is prompt-level enforcement (weak). Options:

- Add a pre-implementation verification: "Run tests, confirm at least one FAIL, paste output" before allowing implementation code
- Use `just check` as a gate between phases

**3. Consider subagent isolation for the Red phase.** The strongest finding is that the test-writer should not share context with the implementer. For critical steps, `/impl-task` could spawn a subagent to write the failing test, then return to the main context for implementation. This is architecturally compatible with how the skill/subagent system already works.

**4. The Refactoring step needs human-in-the-loop.** Beck's "Genies Can't Change Frame" finding is directly relevant. AI agents cannot reliably do the structural rethinking that refactoring requires. The breathing rhythm (feature/refactor) should be a conscious human decision, not delegated. Consider adding an explicit refactoring checkpoint to `/impl-task` after each feature step.

**5. Apply TDD selectively based on code criticality.** Per the tiered consensus: TDD for quant logic and core business rules (where we already need it most), lighter approaches for wiring/config/scaffolding. The "pure wiring" exception in `/impl-task` is correct.

**6. PBT as a complementary layer.** Property-based testing (Hypothesis) achieves 23-37% gains over example-based TDD alone. For quant code where correctness is critical, combining TDD with PBT is the strongest approach. This aligns with the existing Hypothesis research in `docs/research/`.

### Mapping Beck's Principles to Tad

| Beck Principle                      | tad Implementation                                  | Gap                                  |
| ----------------------------------- | --------------------------------------------------- | ------------------------------------ |
| TDD is a superpower with AI         | `/tddv2` skill exists; `just check` before commit   | Enforcement is prompt-only           |
| Never let AI delete tests           | CLAUDE.md: don't refactor things that aren't broken | No mechanical prevention             |
| Separate structural from behavioral | CLAUDE.md: surgical changes                         | No explicit inhale/exhale rhythm     |
| Breathing rhythm                    | Not formalized                                      | Should add refactoring checkpoints   |
| Context isolation                   | Subagents available but not used for TDD            | Should wire into `/impl-task`        |
| Adversarial agents                  | `/plan-task` dialectic uses multiple models         | Not applied to implementation        |
| Propose specific test scenarios     | `/define-task` ACs serve this role                  | Good alignment                       |
| The Compounding Game                | Core concern for a quant codebase                   | `/impl-task` should track complexity |
| Frontier is learning, not speed     | Explanatory output style                            | Good alignment                       |

---

## Sources

### Kent Beck

- [Canon TDD](https://tidyfirst.substack.com/p/canon-tdd)
- [Augmented Coding: Beyond the Vibes](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes)
- [Earn *And* Learn](https://tidyfirst.substack.com/p/earn-and-learn) — Feb 2026
- [Genie: Death of the Iron Triangle?](https://tidyfirst.substack.com/p/genie-death-of-the-iron-triangle) — Mar 2026
- [Genies Getting Stuck](https://tidyfirst.substack.com/p/genies-getting-stuck) — Aug 2025
- [Genie Fight](https://tidyfirst.substack.com/p/genie-fight-8e3) — Sep 2025
- [Genie Wants to Leap](https://tidyfirst.substack.com/p/genie-wants-to-leap) — May 2025
- [Why Does Development Slow?](https://tidyfirst.substack.com/p/why-does-development-slow) — Nov 2025
- [The Bet On Juniors Just Got Better](https://tidyfirst.substack.com/p/the-bet-on-juniors-just-got-better) — Dec 2025
- [The Precious Eyeblink](https://tidyfirst.substack.com/p/the-precious-eyeblink) — Dec 2025
- [Teaching Augmented Coding](https://tidyfirst.substack.com/p/teaching-augmented-coding) — Oct 2025
- [Tidy Together Reboot](https://tidyfirst.substack.com/p/tidy-together-reboot) — Jan 2026
- [Programming Deflation](https://tidyfirst.substack.com/p/programming-deflation)
- [90% of My Skills Are Now Worth $0](https://tidyfirst.substack.com/p/90-of-my-skills-are-now-worth-0)
- [Kent Beck's TDD System Prompt (GitHub Gist)](https://gist.github.com/spilist/8bbf75568c0214083e4d0fbbc1f8a09c)
- [TDD, AI Agents and Coding (Pragmatic Engineer)](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent) — Jun 2025

### Thought Leaders

- [Martin Fowler: Exploring Generative AI](https://martinfowler.com/articles/exploring-gen-ai.html)
- [Martin Fowler Fragments: Jan 8](https://martinfowler.com/fragments/2026-01-08.html), [Feb 18](https://martinfowler.com/fragments/2026-02-18.html)
- [Simon Willison: Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/)
- [Dave Farley on Vibe Coding](https://dev.to/byteknight/farley-on-vibe-coding-1ki1)
- [Uncle Bob on TDD + AI](https://x.com/unclebobmartin/status/2023158252700066287)
- [Jason Gorman: Why Does TDD Work So Well?](https://codemanship.wordpress.com/2026/01/09/why-does-test-driven-development-work-so-well-in-ai-assisted-programming/)
- [Emily Bache: TDD Process for Augmented Coding](https://coding-is-like-cooking.info/)
- [Steve Yegge + Gene Kim: Vibe Coding (book review)](https://mikehadlow.com/posts/2026-02-23-vibe-coding/)
- [DHH: Promoting AI Agents](https://world.hey.com/dhh/promoting-ai-agents-3ee04945)
- [Thorsten Ball: A Few Words on Testing](https://registerspill.thorstenball.com/p/a-few-words-on-testing)
- [ThoughtWorks Technology Radar Vol. 33](https://www.thoughtworks.com/about-us/news/2025/thoughtworks-tech-radar-33-rapid-ai)

### Practitioner Case Studies

- [Forcing Claude Code to TDD (alexop.dev)](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)
- [Taming GenAI Agents (Nathan Fox)](https://www.nathanfox.net/p/taming-genai-agents-like-claude-code)
- [Matt Pocock TDD Skill](https://www.aihero.dev/skill-test-driven-development-claude-code)
- [Claude Code TDD Pair Programming (Agarwal)](https://shivamagarwal7.medium.com/claude-code-pair-programming-sub-agents-that-tdd-with-minimal-supervision-904e586ed009)
- [Superpowers (Jesse Vincent)](https://github.com/obra/superpowers)
- [TDD Guard (Nizar Salim)](https://github.com/nizos/tdd-guard)
- [monday.com: Why You Still Need TDD with Cursor](https://engineering.monday.com/coding-with-cursor-heres-why-you-still-need-tdd/)
- [Tweag Agentic Coding Handbook: TDD](https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/)
- [Addy Osmani: AI Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/)

### Academic Research

- [Test-Driven Development for Code Generation (ASE 2024)](https://dl.acm.org/doi/10.1145/3691620.3695527)
- [TiCoder: Test-Driven Interactive Code Generation (ICSE 2024)](https://arxiv.org/abs/2404.10100)
- [LLM4TDD (LLM4Code '24)](https://arxiv.org/abs/2312.04687)
- [Tests as Instructions (ICLR 2025)](https://openreview.net/forum?id=sqciWyTm70)
- [ChatGPT Test Generation Precision (FSE 2024)](https://mingwei-liu.github.io/assets/pdf/FSE24_chatTester_cameraReady.pdf)
- [Property-Generated Solver (2025)](https://arxiv.org/abs/2506.18315)
- [Agentic PBT (Anthropic, 2025)](https://arxiv.org/abs/2510.09907)
- [TDFlow: 94.3% on SWE-Bench (EACL 2026)](https://arxiv.org/abs/2510.23761)
- [METR: AI Developer Productivity RCT](https://arxiv.org/abs/2507.09089)
- [GitClear: AI Code Quality 2025](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
- [DORA 2025: TDD + AI](https://cloud.google.com/discover/how-test-driven-development-amplifies-ai-success)
- [Meta TestGen-LLM (FSE 2024)](https://arxiv.org/abs/2402.09171)
- [Spec-Driven Development (arXiv 2026)](https://arxiv.org/abs/2602.00180)
- [TDD-Bench-Verified (IBM)](https://github.com/IBM/TDD-Bench-Verified)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)

### Tool Ecosystem

- [Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks-guide)
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [tdd-guard](https://github.com/nizos/tdd-guard)
- [ATDD plugin](https://github.com/swingerman/atdd)
- [VS Code TDD Guide (Copilot)](https://code.visualstudio.com/docs/copilot/guides/test-driven-development-guide)
- [Cursor Agent Best Practices](https://cursor.com/blog/agent-best-practices)
- [Aider Lint/Test Docs](https://aider.chat/docs/usage/lint-test.html)
- [OpenAI Codex Workflows](https://developers.openai.com/codex/workflows/)

### Industry Reports & Events

- [Deer Valley Workshop (Pragmatic Engineer)](https://newsletter.pragmaticengineer.com/p/the-future-of-software-engineering-with-ai) — Feb 2026
- [Pragmatic Summit 2026 (Mark Norgren)](https://marknorgren.com/posts/pragmatic-summit-2026/)
- [The Register: Agile to AI Workshop](https://www.theregister.com/2026/02/20/from_agile_to_ai_anniversary/)
- [Anthropic: How AI Is Transforming Work](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)
- [Qodo State of AI Code Quality 2025](https://www.qodo.ai/reports/state-of-ai-code-quality/)
- [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/ai/)
- [The Rise of Test Theater (Ben Houston)](https://benhouston3d.com/blog/the-rise-of-test-theater)

### Failure Modes & Counter-Arguments

- [AI Agents meet TDD (Latent Space)](https://www.latent.space/p/anita-tdd)
- [Why Testing After with AI Is Even Worse (dev.to)](https://dev.to/mbarzeev/why-testing-after-with-ai-is-even-worse-4jc1)
- [CodeScene: Agentic AI Best Practices](https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality)
- [The Context Window Problem (Factory.ai)](https://factory.ai/news/context-window-problem)
- [Making AI Agents Follow True TDD](https://www.brgr.one/blog/ai-coding-agents-tdd-enforcement)
- [Martin Kleppmann: AI + Formal Verification](https://martin.kleppmann.com/2025/12/08/ai-formal-verification.html)
