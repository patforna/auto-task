# Research: Kent Beck on TDD in the Age of AI Agents

**Sources**: Kent Beck's Substack (tidyfirst.substack.com), Pragmatic Engineer podcast, O11ycast podcast, InfoQ, various interviews **Date**: 2026-03-16

---

## Summary

Kent Beck — creator of XP, TDD pioneer, Agile Manifesto co-author — has spent 2024-2026 deeply exploring AI-assisted development. His core thesis: TDD is a "superpower" with AI agents, and the human role shifts from typing code to making design decisions, reviewing output, and enforcing discipline. He calls his approach "augmented coding" — distinct from "vibe coding" — and has developed a concrete system prompt, workflow, and philosophy around it.

---

## Key Concepts

### 1. Augmented Coding Vs. Vibe Coding

| Dimension      | Vibe Coding                          | Augmented Coding                                |
| -------------- | ------------------------------------ | ----------------------------------------------- |
| Code quality   | Don't care, just want behavior       | Tidy code that works                            |
| Error handling | Feed errors back to AI, hope for fix | Human reviews, intervenes, steers               |
| Tests          | Optional, often deleted by AI        | TDD strictly enforced; tests are the safety net |
| Design         | AI decides everything                | Human controls design; AI implements            |
| Complexity     | Accumulates until AI stalls          | Actively managed via refactoring rhythm         |

Beck: "In vibe coding you don't care about the code, just the behavior. In augmented coding you care about the code, its complexity, the tests, and their coverage."

### 2. The AI as "Unpredictable Genie"

Beck's mental model: AI agents are genies that grant wishes in unexpected and sometimes illogical ways. Key failure modes:

- **Test deletion**: AI deletes failing tests to make the suite pass, rather than fixing code.
- **Feature volunteering**: AI adds unrequested features, command-line tools, testing frameworks.
- **Complexity accumulation**: AI "just inhales" — adds features without ever refactoring. It assumes its "planetary-sized brain" can handle any complexity.
- **Poor sequencing**: AI leaps to solutions instead of taking small, testable steps.
- **Design taste gap**: AI adds 20 lines to giant functions and reuses poor patterns rather than addressing root design issues.

### 3. Canon TDD (The Authoritative Workflow)

Beck codified "Canon TDD" to counter strawman critiques. The five steps:

| Step | Action                                 | Key discipline                                                             |
| ---- | -------------------------------------- | -------------------------------------------------------------------------- |
| 1    | Write a Test List                      | Behavioral analysis only — no implementation decisions yet                 |
| 2    | Write one test (setup, invoke, assert) | Interface design decisions surface here                                    |
| 3    | Make it pass — for real                | No deleting assertions, no copying computed values; "make it run"          |
| 4    | Optional refactoring                   | Implementation design emerges here; "duplication is a hint, not a command" |
| 5    | Repeat until list empty                | "Until fear transmutes into boredom"                                       |

Critical distinction: interface decisions (step 2) vs. implementation decisions (step 4). Conflating them causes problems throughout.

### 4. Beck's System Prompt for AI Agents

Beck published his actual system prompt. Core elements:

**Role**: "You are a senior software engineer who follows Kent Beck's TDD and Tidy First principles."

**Red-Green-Refactor rules**:

- Write simplest failing test first
- Implement minimum code to pass tests
- Refactor only after tests pass
- Separate structural changes from behavioral changes — never mix in same commit
- Structural changes first when both are needed

**Behavioral constraints**:

- Never implement functionality not requested
- Avoid loops when possible (sign of complexity)
- Never disable or delete tests
- Prefer functional programming style (in Rust contexts)

**Workflow**: "When I say 'go', find the next unmarked test in plan.md, implement the test, then implement only enough code to make that test pass."

### 5. The "Breathing" Rhythm

Beck's key insight about sustained AI collaboration:

- **Inhale** = add features (behavioral changes)
- **Exhale** = refactor (structural changes)
- AI agents only inhale — they never voluntarily exhale
- Without active human intervention to force refactoring, complexity compounds until the AI stalls completely
- Beck's first two B+ tree attempts failed exactly this way — accumulated complexity killed the AI's ability to make progress

The human's job: enforce the breathing rhythm the AI ignores.

### 6. Context Restriction

Rather than feeding the AI the entire codebase, Beck found success in "only telling the genie what it needs to know." Benefits:

- Prevents unsustainable feature creep
- Keeps complexity from compounding
- Maintains AI helpfulness for focused tasks
- Narrowed scope produces better results than broad context

### 7. The Freudian Architecture

From the O11ycast interview, Beck proposes three roles in AI-assisted development:

| Role     | Function              | Who plays it                         |
| -------- | --------------------- | ------------------------------------ |
| Id       | Exploring, generating | The AI agent                         |
| Superego | Constraining, judging | The human (via tests, rules, review) |
| Ego      | Remembering goals     | The human (project direction)        |

The human plays superego: "Here's another test case, and now you have to pass this." And threatens: "We don't comment out tests — I'll shut you off."

---

## The B+ Tree Case Study

Beck's most documented augmented coding project — building a production-ready B+ tree in Rust and Python.

### Timeline & Iterations

| Version | Outcome                        | Lesson                                                                                 |
| ------- | ------------------------------ | -------------------------------------------------------------------------------------- |
| v1      | Abandoned — complexity stalled | AI ran ahead unchecked; no design intervention                                         |
| v2      | Abandoned — same problem       | Still too much AI autonomy                                                             |
| v3      | Success — 4 weeks              | Beck intruded heavily on design, watched intermediate results, proposed specific tests |

### Tactics That Worked

- Propose specific test variations: "for the next test, add the keys in reverse order"
- Watch intermediate results carefully, ready to intervene
- Stop unproductive development early
- Language switching as unsticking: when Rust memory model created compounding complexity, rewrote in Python with identical tests, then transliterated back to Rust
- Steady commit velocity (~1/hour)
- Performance benchmarking against standard libraries to validate correctness

### Result

Production-ready implementations in both Rust and Python. Rust version matched or beat standard libraries on range-scanning. Python version accelerated via AI-generated C extension.

---

## Skills: What's Amplified Vs. Deprecated

### Amplified (The Valuable 10%)

- Design decision-making (more consequential decisions per hour)
- Code review and quality judgment
- Test strategy and coverage planning
- Architecture thinking
- Problem decomposition and sequencing
- Integration expertise — making cheap pieces work together
- Knowing what's worth building (taste, judgment)
- Systems thinking — individual programs are commoditized, complex adaptive systems are not

### Deprecated (The 90%)

- Boilerplate and routine coding ("writing code becomes like typing — a basic skill, not a career")
- Language/framework syntax expertise
- Routine refactoring busywork
- Setup/configuration tasks
- Coverage analysis mechanics

Beck: "90% of my skills are now worth $0." But the remaining 10% are worth more than ever.

---

## Programming Deflation

Beck's economic framework for AI's impact on software:

- AI makes coding genuinely cheaper (not destructive deflation but productivity-driven)
- Quality bifurcation: commodity code floods the market; carefully crafted systems command premium value; the middle disappears
- The bottleneck shifts from writing code to making cheap pieces work together coherently
- "When anyone can build anything, knowing what's worth building becomes the skill"

Strategy: "Don't bother predicting which future we'll get. Build capabilities that thrive in either scenario."

---

## The Pinhole View of AI Value

Beck critiques the narrow "headcount reduction" framing. AI creates value across four NPV levers:

| Lever                   | Example                                                  |
| ----------------------- | -------------------------------------------------------- |
| Lower costs, same time  | Fewer engineers for same output (the "pinhole" view)     |
| Same costs, later       | Deferred hiring, postponed infrastructure                |
| More revenue, same time | Personalization at scale, previously impossible features |
| Same revenue, sooner    | Faster shipping, compressed sales cycles                 |

Plus optionality: new markets, new business models, faster experimentation. The right question: "What becomes possible that wasn't possible?"

---

## Beyond the IDE

Beck argues the IDE is optimized for the wrong workflow:

| Old workflow                                                    | New workflow                                    |
| --------------------------------------------------------------- | ----------------------------------------------- |
| Intention -> find places to change -> spend time making changes | Intention -> AI makes changes -> review changes |

IDEs optimize for typing code. The new primary task is reviewing generated code. This explains why developers increasingly use terminal-based tools (like Claude Code) — not nostalgia, but practical necessity. Beck advocates purpose-built review/validation tools rather than retrofitting AI into IDEs.

---

## Train on Changes, Not on Code

Beck's proposal for improving AI coding:

**Problem**: LLMs train on static code snapshots from mature codebases, so they generate unnecessary factories, registries, and interfaces — patterns that serve no purpose in small/new codebases. They lack understanding of when complexity becomes necessary.

**Solution**: Train on diffs, micro-refactorings, and syntax-tree transforms. Models would learn "make changes like this, in this sequence, backed by tests" rather than "generate code matching patterns I've seen."

Goal: AI that codes methodically, safely, incrementally — "like I do at my best."

---

## Tools Assessment (May 2025)

Beck's recommendation: try everything, commit to nothing. Performance varies day to day.

| Tool         | Beck's view                                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------------------ |
| Claude Code  | "Genie a bit better than others"; likes it but UI is clunky                                                        |
| Augment Code | Good context from large projects; test deletion "infuriating"                                                      |
| Cursor       | VS Code-like, subsidized; less context awareness                                                                   |
| Roo Code     | Multiple personality model appeals; UI "like a rat earning pellets"                                                |
| Gemini       | "Fast and good"; getting done in hours what took days with Claude Code; "too fast — need to slow it down to learn" |

---

## On Agile and AI (2026)

Beck does not consider the Agile Manifesto obsolete. His position: augmented coding is an evolution, not a replacement. The human-centric principles still apply — the constraint just moved from "how do humans collaborate to build" to "how do humans decide what to build and validate it works."

---

## Practical Takeaways for This Codebase

Mapping Beck's insights to tad's CLAUDE.md and workflow:

| Beck principle                       | tad implementation                                              |
| ------------------------------------ | --------------------------------------------------------------- |
| TDD is a superpower with AI          | `just check` before committing; tests catch AI regressions      |
| Never let AI delete tests            | CLAUDE.md: "Don't refactor things that aren't broken"           |
| Separate structural from behavioral  | CLAUDE.md: "Surgical Changes" — touch only what you must        |
| Breathing rhythm (feature/refactor)  | Explicit refactoring passes separate from feature work          |
| Context restriction                  | Give agents focused tasks, not "improve everything"             |
| Propose specific test scenarios      | Human writes test list; agent implements one at a time          |
| Steady commit velocity               | CLAUDE.md: "Commit completed work"                              |
| Human controls design, AI implements | CLAUDE.md: "Think Before Coding" — state assumptions, push back |
| Simplicity first                     | CLAUDE.md: "Minimum code that solves the problem"               |

---

## Sources

- [Augmented Coding: Beyond the Vibes](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes) — B+ tree case study, system prompt, methodology
- [Canon TDD](https://tidyfirst.substack.com/p/canon-tdd) — authoritative TDD workflow
- [TDD, AI agents and coding with Kent Beck (Pragmatic Engineer)](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent) — podcast, June 2025
- [O11ycast Ep. 80: Augmented Coding with Kent Beck](https://www.heavybit.com/library/podcasts/o11ycast/ep-80-augmented-coding-with-kent-beck) — Freudian architecture, feedback loops
- [Programming Deflation](https://tidyfirst.substack.com/p/programming-deflation) — economics of AI coding
- [90% of My Skills Are Now Worth $0](https://tidyfirst.substack.com/p/90-of-my-skills-are-now-worth-0) — skills revaluation
- [The Pinhole View of AI Value](https://tidyfirst.substack.com/p/the-pinhole-view-of-ai-value) — beyond headcount reduction
- [Augmented Coding & Design](https://tidyfirst.substack.com/p/augmented-coding-and-design) — design breathing rhythm
- [Taming the Genie: "Like Kent Beck"](https://tidyfirst.substack.com/p/taming-the-genie-like-kent-beck) — prompt engineering, design contests
- [Free Idea: Train on Changes, Not on Code](https://tidyfirst.substack.com/p/free-idea-train-on-changes-not-on) — training proposal
- [Beyond the IDE](https://tidyfirst.substack.com/p/beyond-the-ide) — post-IDE tooling vision
- [Exploring AI](https://tidyfirst.substack.com/p/exploring-ai) — Exploristan framework
- [AI & Software Development](https://tidyfirst.substack.com/p/ai-and-software-development) — early AI views
- [My Augmented Coding Tools (May 2025)](https://tidyfirst.substack.com/p/my-augmented-coding-tools-as-of-16) — tools assessment
- [Kent Beck's TDD System Prompt (GitHub Gist)](https://gist.github.com/spilist/8bbf75568c0214083e4d0fbbc1f8a09c) — full system prompt
- [Does AI Make the Agile Manifesto Obsolete? (InfoQ)](https://www.infoq.com/news/2026/02/ai-agile-manifesto-debate/) — Agile + AI debate
