# Research: TDD by Example — Book Synthesis & Skill Review

**Source**: Kent Beck, *Test-Driven Development by Example* (Addison-Wesley, 2003), 240 pages **Output**: `/SKILL.md` — incompressible TDD skill for AI coding agents **Date**: 2026-03-13

---

## Book Structure

| Part               | Chapters | Content                                                                                                                        |
| ------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------ |
| I — Money Example  | 1–17     | Java. Multi-currency arithmetic. Dollar/Franc → Money, Expression/Sum/Bank.reduce(), Factory Methods, Polymorphism, Composite. |
| II — xUnit Example | 18–24    | Python. Building a test framework in itself. TestCase, TestResult, TestSuite, setUp/tearDown, Template Method.                 |
| III — Patterns     | 25–32    | TDD patterns, green bar patterns, xUnit patterns, design patterns, refactoring patterns.                                       |
| Appendix I         | —        | Influence diagrams (feedback loops in software).                                                                               |

## Core Thesis

Two rules generate all of TDD: (1) write new code only when an automated test has failed, (2) eliminate duplication. Dependency between code is the problem; duplication is the symptom. The red/green/refactor cycle is the mechanical expression of these rules.

## Concepts Catalog

### The Cycle

Red (write failing test, run, confirm failure) → Green (simplest possible change, any shortcut acceptable) → Refactor (remove duplication, including between test and production code).

### Strategies to Get to Green

1. **Fake It**: Return constant, then replace with real computation by removing test↔code duplication.
2. **Triangulation**: Second test demands different output; generalize only when 2+ examples force it.
3. **Obvious Implementation**: Type real code if confident. Back up to Fake It on unexpected red.

### Test Selection

- **Starter Test** (Ch 26): Simplest degenerate case — empty, zero, identity.
- **One Step Test** (Ch 26): Next test you can pass in one step that teaches something new.
- **Regression Test** (Ch 26): Smallest failing test reproducing a defect, before fixing.

### Test Construction

- **Assert First** (Ch 26): Start with the assertion, work backward to setup.
- **Evident Data** (Ch 26): Literal readable values; input→output relationship obvious from test alone.

### Step Size

Smaller when uncertain, bigger when confident. Unexpected red → shift down. Unexpected green → suspect the test.

### Testing Patterns (Ch 27)

Child Test, Mock Object, Self Shunt, Log String, Crash Test Dummy, Broken Test, Clean Check-in.

### Green Bar Patterns (Ch 27)

Fake It, Triangulate, Obvious Implementation, One to Many (single element first, then collection).

### xUnit Patterns (Ch 28–29)

Assertion (assertEquals > assertTrue), Fixture (setUp/tearDown), External Fixture, Test Method (test*), Exception Test.

### Design Patterns in TDD (Ch 30)

Command, Value Object, Null Object, Template Method, Pluggable Object, Pluggable Selector, Factory Method, Imposter, Composite, Collecting Parameter. Key insight: these **emerge** from refactoring, not upfront design.

### Refactoring Patterns (Ch 31)

Reconcile Differences, Isolate Change (Extract Method/Object, Method Object), Migrate Data, Extract/Inline Method, Extract Interface, Move Method, Method Object, Add Parameter, Method Parameter to Constructor Parameter.

### Mastering TDD (Ch 32)

Test conditionals, loops, operations, polymorphism. "Write tests until fear is transformed into boredom." Test quality signals = design signals: long setup (objects too big), duplicate setup (too coupled), slow tests (resource coupling), fragile tests (action at distance). At the limit, TDD is indistinguishable from designing ahead.

---

## Skill Review Process

4 subagent reviews across 2 rounds, reviewing SKILL.md against both the source PDF and AI-agent operationalizability.

### Changes Made After Round 1

| Finding                                                                                | Source             | Action                                     |
| -------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------ |
| Missing test selection strategy (starter/next test)                                    | Fidelity + Quality | Added "Choosing Tests" section             |
| Missing regression test rule                                                           | Fidelity           | Added                                      |
| Missing assert-first technique                                                         | Fidelity           | Added to "Writing Tests"                   |
| Missing evident data guidance                                                          | Fidelity           | Added to "Writing Tests"                   |
| "Run tests" not explicit in cycle                                                      | Quality            | Added to cycle step                        |
| Isolate Change had wrong techniques (Extract Interface → Extract Object/Method Object) | Fidelity           | Fixed                                      |
| Fake It missing duplication-removal rationale                                          | Fidelity           | Strengthened                               |
| "Any sin is permitted" too broad                                                       | Quality            | Scoped to "shortcuts within current scope" |
| Emotion heuristics non-operational for AI                                              | Quality            | Replaced with concrete stopping criterion  |
| To-do list mechanism unspecified                                                       | Quality            | Specified (comments in test file)          |
| Broken Test pattern irrelevant to AI agents                                            | Fidelity + Quality | Removed                                    |
| Duplicate Triangulation entry                                                          | Fidelity           | Removed (table sufficient)                 |
| Inspirational quote non-instructional                                                  | Quality            | Removed                                    |
| Design pattern name list non-actionable                                                | Fidelity           | Removed                                    |
| Self Shunt too Java-specific                                                           | Quality            | Simplified to generic Mock Objects         |
| Child Test buried in Rhythm section                                                    | Fidelity           | Elevated to named pattern                  |

### Declined Suggestions

| Suggestion                                       | Rationale for declining                                 |
| ------------------------------------------------ | ------------------------------------------------------- |
| Add preconditions block (test runner, framework) | Too environment-specific; not a TDD skill concern       |
| Reorder cycle before rules                       | Rules are the foundation; cycle is their expression     |
| Cut Value Objects                                | Core TDD concept from Part I, not just a design pattern |
| Add existing-code TDD section                    | Regression test + normal cycle covers it; would bloat   |
| Replace all confidence-based language            | "Confidence" maps naturally to AI uncertainty           |

### Round 2 Verdict

Two fresh reviewers independently confirmed convergence:

- **Fidelity**: Zero inaccuracies, zero meaningful omissions. "Ship it."
- **Quality**: "Close to optimal form." No further revision recommended.
