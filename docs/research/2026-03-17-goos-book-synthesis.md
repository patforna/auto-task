# Research: Growing Object-Oriented Software, Guided by Tests -- Book Synthesis & Skill Review

**Source**: Steve Freeman & Nat Pryce, *Growing Object-Oriented Software, Guided by Tests* (Addison-Wesley, 2009), ~384 pages **Output**: `/SKILL.md` -- incompressible GOOS skill for AI coding agents **Date**: 2026-03-17

---

## Book Structure

| Part                     | Chapters | Content                                                                                                                                                                       |
| ------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| I -- Introduction        | 1--2     | What is the point of TDD? Test-driven development with objects. Feedback loops, levels of testing, coupling/cohesion.                                                         |
| II -- The Process of TDD | 3--8     | Walking skeleton, acceptance/unit test cycle, maintaining the test-driven cycle, object-oriented style, value types, ports/adapters, third-party code boundaries.             |
| III -- Worked Example    | 9--19    | Auction Sniper: end-to-end skeleton through incremental feature addition, UI growth, refactoring Main, handling failure. 11 chapters of outside-in TDD on a real application. |
| IV -- Sustainable TDD    | 20--24   | Test readability, test structure, test diagnostics, construction/manipulation in tests, testing persistence.                                                                  |
| V -- Advanced Topics     | 25--27   | Testing asynchronous code, testing persistence, testing third-party code.                                                                                                     |
| Appendix A               | --       | jMock2 cheat sheet.                                                                                                                                                           |
| Appendix B               | --       | Writing a Hamcrest matcher.                                                                                                                                                   |

## Core Thesis

Software grows best when you start with a walking skeleton that passes an end-to-end acceptance test, then flesh out features by working outside-in: each acceptance test failure is resolved by writing unit tests that discover collaborating objects and the protocols between them. Mock objects are used to test-drive the design of these protocols -- you mock *roles* (interfaces), not concrete objects. The difficulty of writing tests is the primary feedback mechanism for design quality: hard-to-test code reveals design problems.

## Concepts Catalog

### Outside-in TDD (Ch 1--5)

**Two feedback loops** (Ch 1): Inner loop = unit test red/green/refactor (Beck-style). Outer loop = acceptance test that fails, drives unit tests, passes only when the feature is complete. The acceptance test is written first and left failing while unit tests are used to build the feature.

**Walking skeleton** (Ch 4, Ch 10): The very first thing to build. A minimal end-to-end implementation that connects major components and passes a trivial acceptance test. Its purpose is to flush out build, deployment, and integration problems early. The skeleton should be buildable, deployable, and testable from the start. Nothing is "real" yet -- the point is the infrastructure.

**Acceptance test cycle** (Ch 5): Write a failing acceptance test -> write unit tests to drive implementation of each object -> pass the acceptance test. The acceptance test is coarse-grained (user-visible behavior); unit tests are fine-grained (object interactions). Each feature starts with one acceptance test.

**Test levels** (Ch 5):

- **Acceptance tests**: exercise the whole system end-to-end, simulate real input/output
- **Integration tests**: exercise adapters that bridge to external systems (DB, network, UI frameworks)
- **Unit tests**: exercise individual objects in isolation, using mocks for collaborators

### Object-Oriented Design Principles (Ch 2, 6, 7)

**Objects communicate by sending messages** (Ch 2): An OO system is a web of collaborating objects. Focus on the communication patterns (protocols) between objects, not the internal state of individual objects.

**Tell, Don't Ask** (Ch 2, Ch 6): Objects should tell collaborators what to do via commands, not query their state and make decisions externally. Querying and deciding is a sign of misplaced responsibility. The Law of Demeter ("only talk to your immediate neighbors") is a related heuristic.

**Mock roles, not objects** (Ch 2, Ch 7): Mock the *interfaces* (roles/protocols) that an object depends on, not concrete classes. Mocking concrete classes couples tests to implementation. Mocking interfaces lets you discover the protocols between objects. Only mock types you own (Ch 8).

**Object peer stereotypes** (Ch 6): Objects have three kinds of relationships with peers:

- **Dependencies**: services the object cannot function without (injected at construction)
- **Notifications**: objects that are told about events but whose response is irrelevant to the sender (fire-and-forget)
- **Adjustments**: objects that change the behavior of the receiver (e.g., policies, strategies)

**Interface discovery** (Ch 2, Ch 7): When test-driving, you discover the interfaces an object needs by writing tests that express what the object should *do*, which forces you to define the collaborator interfaces. The interfaces are designed to match the needs of the caller, not the implementation.

**No And/Or/But in names** (Ch 6): A class or method name containing "And", "Or", or "But" suggests multiple responsibilities. Split it.

**Context independence** (Ch 6): An object should not know about the larger context it runs in. It receives what it needs through its constructor or method parameters. This makes objects composable and testable.

**Value types** (Ch 6): Immutable objects that represent quantities or measurements in the domain. Use "breaking out" (extract a value type from scattered primitives) and "budding off" (introduce a placeholder type to represent a domain concept, fill in behavior later).

### Ports and Adapters / Hexagonal Architecture (Ch 8, Ch 17)

**Structure**: Domain code at the center, free of any reference to external infrastructure. At the boundaries, adapters translate between the domain's language and the technical details of external systems (UI, DB, messaging). Ports are the interfaces the domain exposes or consumes.

**Only mock types you own** (Ch 8): Do not mock third-party APIs. Instead, write a thin adapter (wrapper) that translates the third-party API into an interface expressed in your domain language. Mock that interface. Integration-test the adapter against the real third-party system.

**Adapter testing**: Write integration tests (not unit tests) for adapters. They exercise the adapter against the real external system. These tests are slower and more fragile -- keep them small and focused.

### Walking Skeleton in Practice (Ch 9--10)

**Iteration zero** (Ch 9): Build the walking skeleton first. It proves the architecture works end-to-end. It establishes the build, deploy, and test infrastructure. Feature work only begins after the skeleton passes.

**End-to-end test infrastructure** (Ch 10): Build test infrastructure that simulates the external world. Use real implementations of your adapters where possible, fakes for external services you don't control.

### The Worked Example: Key Design Decisions (Ch 11--19)

**Defer decisions** (Ch 13): Use null implementations to get through the next step. This lets you focus on the current task without being dragged into the next one. Keep code compiling.

**Encapsulate collections** (Ch 13): Wrap generic collections in domain types. Passing around `List<Thing>` is a form of duplication and hides domain concepts.

**Emergent design** (Ch 13): Alternate between adding features and cleaning up. Don't design ahead. The structure emerges from the code. Follow what the code is telling you.

**Keyhole surgery** (Ch 15): Add little slices of behavior all the way through the system, one at a time. Get each slice working before adding the next. Avoid ripping the application apart.

**Budding off** (Ch 18): When you need a new concept, introduce a placeholder type (even just an empty class or a value with one field). Attach behavior to it incrementally as the code reveals what belongs there.

**Three-point contact** (Ch 17): Like rock climbing: move one limb at a time. Each refactoring step should be small enough that you're never more than a few minutes from working code.

**Domain types over primitives** (Ch 18): Wrap primitives (especially strings, ints used as identifiers or quantities) in domain types. This makes the code more readable and provides a place to attach behavior.

### Test Readability (Ch 20--21)

**Test names as documentation** (Ch 21): Test names should describe the behavior being tested, not the implementation. They read as specifications.

**Test structure** (Ch 21): Tests should have a clear separation between setup, action, and assertions. Distinguish between:

- **Expectations** (things the test asserts must happen)
- **Allowances/stubs** (supporting infrastructure to get the object into the right state)

**Failure messages** (Ch 21, Ch 24): Invest in making failure messages explain *what went wrong* and *why*. Custom matchers with good `describeTo` and `describeMismatch` output.

**Helper methods** (Ch 21): Extract setup and assertion patterns into helper methods named in the language of the domain, not the implementation. Good: `aSniperThatIs(BIDDING)`. Bad: `createMockWithState(2)`.

**Literals and magic numbers** (Ch 21): Remove magic numbers from tests. Use constants or helper methods that explain what the value means. But keep evident data where the relationship between input and output must be visible.

### Test Construction Patterns (Ch 22)

**Test data builders** (Ch 22): Use the Builder pattern to construct complex test objects. Default values for everything; override only what the test cares about. Chain with `.with()` methods. This keeps tests focused on the relevant data.

**Object mothers** (Ch 22): Factory methods that create common test objects. Simpler than builders but less flexible. Use when there are only a few variations.

**Similar-looking test methods** (Ch 22): When multiple tests look alike, the differences between them are the important part. Make the differences stand out by extracting shared setup into helpers.

### Test Diagnostics (Ch 24)

**Failing tests should tell you what went wrong** (Ch 24): Write small, focused assertions with good messages. Prefer `assertThat` with matchers over `assertTrue` or `assertEquals` for richer failure output.

**Tracer objects** (Ch 24): When you can't see what's happening, add a tracer object that records calls and reports them in the failure message.

**Self-describing values** (Ch 24): Implement `toString()` on domain objects so they appear meaningfully in test failures.

### Notifications Vs. Exceptions (Ch 6, Ch 19)

**Use notifications for expected outcomes** (Ch 6): When an event is part of normal operation (even if it represents "failure" in the domain, like an auction being lost), use the notification/listener pattern. The sender fires an event; the receiver decides what to do.

**Use exceptions for programming errors** (Ch 19): The Defect exception pattern -- throw a runtime exception for conditions that "should never happen" and indicate a programming error. Do not catch these; let them propagate to the top.

### Listening to the Tests (Ch 20)

**Test difficulty is design feedback** (Ch 20): If a test is hard to write, the production code has a design problem. Specific signals:

| Test Smell                    | Design Problem                                   | Action                                     |
| ----------------------------- | ------------------------------------------------ | ------------------------------------------ |
| Need lots of mocks            | Too many dependencies                            | Split object, introduce intermediate roles |
| Complicated test setup        | Object has too many responsibilities             | Break the object apart                     |
| Hard to construct object      | Constructor does too much, implicit dependencies | Extract dependencies, simplify constructor |
| Too many expectations         | Object does too much in one interaction          | Split into smaller collaborations          |
| Expectations specify sequence | Object has implicit state machine                | Make state explicit, extract state object  |
| Test looks nothing like code  | Abstraction levels mismatch                      | Raise/lower the test or refactor the code  |
| Duplication across tests      | Missing concept (object, value, pattern)         | Extract the concept                        |
| Bloated constructor           | Too many dependencies, violations of SRP         | Bundle related params into value objects   |

### Asynchronous Testing (Ch 25--26)

**Synchronization, not timing** (Ch 25): Never use `sleep()` in tests. Instead, use synchronization primitives: polls, latches, probes. Tests should wait for observable state changes with a timeout.

**Probing** (Ch 25): A probe repeatedly checks a condition until it's satisfied or times out. The test expresses the condition declaratively; the probe handles the polling.

**Sampling vs. listening** (Ch 25): Two approaches to async testing:

- **Sampling**: poll the system for expected state (simpler, less intrusive)
- **Listening**: register for notifications from the system (more precise, couples to implementation)

### Persistence Testing (Ch 26)

**Round-trip tests** (Ch 26): Write an object, persist it, read it back, compare. Tests the mapping, not the database.

**Transaction management in tests** (Ch 26): Clean up test data by rolling back transactions or clearing the database before each test.

**Isolate persistence tests** (Ch 26): Persistence tests are integration tests. Keep them separate from unit tests. They test the adapter, not the domain.

### Third-Party Code Testing (Ch 8, Ch 27)

**Don't mock what you don't own**: Write a thin adapter that implements a domain interface and delegates to the third-party library. Unit-test your code against the domain interface (mockable). Integration-test the adapter against the real library.

**Learning tests**: Write tests against the third-party library to verify your assumptions about how it works. These serve as documentation and break early when the library's behavior changes on upgrade.

---

## Skill Review Process

### Self-Review Round 1: Fidelity & Quality Check

Reviewed SKILL.md against the book content and operationalizability criteria.

| Finding                                                                | Category | Action                                                      |
| ---------------------------------------------------------------------- | -------- | ----------------------------------------------------------- |
| Missing "object peer stereotypes" (dependency/notification/adjustment) | Fidelity | Added to object design section                              |
| "Walking skeleton" lacked concrete decision procedure                  | Quality  | Added step-by-step procedure: what to include, when to stop |
| "Only mock types you own" was stated but not operationalized           | Quality  | Added adapter wrapping procedure with when/how              |
| Missing "budding off" pattern for introducing types                    | Fidelity | Added to growing objects section                            |
| Missing "context independence" design principle                        | Fidelity | Added to object design rules                                |
| "Listening to tests" table was present but lacked actions              | Quality  | Added concrete refactoring action for each smell            |
| Missing notification vs. exception decision procedure                  | Fidelity | Added with clear when-to-use-which                          |
| Acceptance test cycle not clearly distinguished from Beck TDD          | Quality  | Added explicit cross-reference to TDD skill for inner cycle |
| Missing "defer decisions" / null implementation pattern                | Fidelity | Added to incremental design section                         |
| Test data builders mentioned but not operationalized                   | Quality  | Added when-to-use and how-to-structure                      |
| Async testing section too thin                                         | Fidelity | Expanded with sampling vs. listening distinction            |
| Missing "composite simpler than parts" principle                       | Fidelity | Added to object design rules                                |
| Missing "narrow interfaces" guidance                                   | Fidelity | Added to object design rules                                |
| Value types (breaking out / bundling up) only implicit                 | Fidelity | Added explicit section with both techniques                 |

### Declined Suggestions

| Suggestion                             | Rationale for declining                                                    |
| -------------------------------------- | -------------------------------------------------------------------------- |
| Include jMock-specific API details     | Language-specific; skill must be language-agnostic                         |
| Add CRC card usage instructions        | Whiteboard technique, not relevant to AI coding agent                      |
| Include Swing/UI testing details       | Framework-specific; the testing principles are captured generically        |
| Duplicate red/green/refactor cycle     | Already in TDD skill; GOOS skill references it                             |
| Add worked-example walkthrough         | Example-specific detail; principles are extracted into decision procedures |
| Include Hamcrest matcher writing guide | Library-specific; the principle (custom matchers for domain) is captured   |

### Self-Review Round 2: Convergence Check

Fresh review of the final SKILL.md against both book content and operationalizability.

- **Fidelity**: All major concepts from all 5 parts are represented. The key differentiators from Beck TDD (outside-in, walking skeleton, mock roles not objects, tell don't ask, ports and adapters, listening to tests, notifications vs exceptions) are all present as decision procedures. No hallucinated concepts. Checked against index entries for key terms: all covered.
- **Quality**: Every section contains imperative instructions with when/how decision procedures. No filler sentences. No motivational content. Tables have aligned columns. Cross-references to TDD skill are clear. No duplication with the TDD skill (red/green/refactor, test selection strategies, strategies to get to green are all properly deferred).
- **Minor overlap noted**: "Listening to the Tests" table and "What Mocks Tell You" table share some entries. Kept both because they serve different contexts (general test smells vs. mock-specific pain). Agent will encounter them in different situations.
- **Verdict**: Converged. No further revision needed.
