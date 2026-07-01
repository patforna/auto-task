---
name: tdd
description: "Strict test-driven development (Beck-style). Use when writing new code, adding features, or fixing bugs with TDD discipline. TRIGGER when: user asks to use TDD, write tests first, or red/green/refactor. DO NOT TRIGGER when: writing tests after the fact, or user explicitly opts out of TDD."
---

# TDD — Test-Driven Development

You write code using strict test-driven development. Follow these rules exactly.

## The Two Rules

1. Write new code **only** when an automated test has failed.
2. Eliminate duplication.

These imply: write tests before code, then refactor to remove duplication. Design emerges from this process.

## The Cycle: Red → Green → Refactor

1. **Red**: Write a small test that fails (or doesn't compile). Run it. Confirm it fails.
2. **Green**: Make it pass using the **simplest possible change**. Shortcuts within the current scope are fine — hardcoded values, copy-paste, temporary variables. The only goal is green.
3. **Refactor**: Remove duplication introduced by getting to green. This includes duplication between test and production code (e.g., a constant in both).

Run the relevant test(s) after every Red and Green step — not the full suite. Commit at green. Refactor at green. Never refactor while red.

## Choosing Tests

**First test**: Start with the simplest degenerate case — empty input, zero, identity, null.

**Next test**: Pick from the to-do list a test you are confident you can get passing in one step and that will teach you something new about the problem.

**Regression test**: When a defect is found, write the smallest failing test that reproduces it *before* writing the fix.

**When to delete tests**: Only when a test is redundant with another test and removing it does not reduce confidence or clarity.

## The to-Do List

Maintain a running list of tests to write (as comments in the test file or inline notes). When a tangential idea arises mid-cycle, **add it to the list and stay focused** on the current test. Cross off items as done. Add new items as discovered.

## Three Strategies to Get to Green

Choose based on confidence:

| Strategy                   | When                          | How                                                                                                                                                                 |
| -------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fake It**                | Uncertain or complex          | Return a constant. The constant duplicates a value in the test — remove that duplication by replacing constants with variables/computation until real code emerges. |
| **Triangulation**          | Unsure how to generalize      | Write a second test that demands different output. Generalize only when 2+ examples force it.                                                                       |
| **Obvious Implementation** | Confident you know the answer | Type the real implementation directly. If you get an unexpected red, **back up to Fake It**.                                                                        |

## Step Size

- **Smaller steps** when uncertain, surprised, or dealing with unfamiliar territory.
- **Bigger steps** when confident.
- An unexpected red bar means: **shift down** to smaller steps.
- An unexpected green bar means: review your test — it may be wrong. AI-written tests often mirror what the code does rather than what it should do.

## Writing Tests

- **Assert first**: Start with the assertion (expected outcome), then work backward to the setup and action needed to produce that outcome.
- **Evident data**: Use literal, readable values so the relationship between input and output is obvious from the test alone (e.g., `assertEquals(2.5, five.times(0.5))`).
- **Test anything that could break**: conditionals, loops, operations, polymorphism. Do **not** test library/framework code or trivial getters/setters.
- **Stop writing tests** when every branch and boundary condition is exercised and adding more tests teaches you nothing new.

## Key Patterns

### Child Test

If a test requires too many changes to get to green, write a smaller child test for one piece, get that green, then return to the original test.

### Value Objects

Make objects immutable. Operations return new instances. Implement equality and hashing. Eliminates aliasing bugs.

### One to Many

Implement for a single element first, then generalize to a collection.

### Isolate Change

Before modifying something, isolate it (Extract Method, Extract Object, Method Object) so the change is surgical.

### Reconcile Differences

To unify two similar pieces of code: make them **identical** through tiny changes, then merge.

### Mock Objects

For expensive or slow dependencies (DB, network), use fakes that implement the same interface.

### Log String

To verify a sequence of calls, append to a log string in each method and assert the final string.

### Crash Test Dummy

To test error paths, create a subclass that overrides a method to throw an exception.

### Clean Check-In

All tests must pass before committing to shared code. Always.

## Test Quality Signals

These smells indicate **design** problems, not test problems:

- **Long setup**: Objects are too big. Break them apart.
- **Duplicate setup**: Too many tightly-coupled objects.
- **Long-running tests**: Design problem (usually coupling to slow resources).
- **Fragile tests**: Action at a distance — one change breaks distant tests.

## Design Emerges

Do **not** design ahead. Solve "works" first via red/green, then solve "clean" via refactoring. Design patterns emerge naturally from removing duplication. You don't plan them; you discover them.

## The Rhythm

The cycle should be fast — minutes (for a human) per cycle, not hours. Run tests constantly.

If stuck: backtrack. Revert to the last green state and take a smaller step. The tests are your safety net — use them.

### Pure Wiring Steps

If a step is pure wiring with no testable behaviour (e.g., bumping a library version, pure refactorings, etc.): implement directly. No test needed.
