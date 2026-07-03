# Research: Clean Code — Book Synthesis & Skill Review

**Source**: Robert C. Martin, *Clean Code: A Handbook of Agile Software Craftsmanship* (Prentice Hall, 2009), ~464 pages **Output**: `/SKILL.md` — incompressible Clean Code review lens for AI coding agents **Date**: 2026-03-17

---

## Book Structure

| Ch  | Title                       | Content                                                                                                                                                                                                                                                      |
| --- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Clean Code                  | Definitions from Bjarne, Grady, Dave, Ron, Ward. Boy Scout Rule. Cost of mess.                                                                                                                                                                               |
| 2   | Meaningful Names            | Intention-revealing, avoid disinformation, meaningful distinctions, pronounceable, searchable, no encodings, no puns. Scope-length rule.                                                                                                                     |
| 3   | Functions                   | Small (20 lines). One thing. One abstraction level. Switch → polymorphism. Descriptive names. Few args (0-2 ideal, 3 max). No side effects. Command-query separation. Exceptions over error codes. Extract try/catch bodies.                                 |
| 4   | Comments                    | Good: legal, informative, explanation of intent, clarification, warning, TODO, amplification. Bad: mumbling, redundant, misleading, mandated, journal, noise, position markers, closing-brace, attributed, commented-out code, nonlocal info, too much info. |
| 5   | Formatting                  | Newspaper metaphor (high→low). Vertical openness, density, distance, ordering. Horizontal: short lines, indentation. Team rules.                                                                                                                             |
| 6   | Objects and Data Structures | Data/Object anti-symmetry. Law of Demeter (train wrecks). DTOs. Active Record ≠ domain object.                                                                                                                                                               |
| 7   | Error Handling              | Exceptions not return codes. Write try-catch first. Unchecked exceptions. Context in messages. Wrap third-party exceptions. No null returns. No null args. Special Case pattern.                                                                             |
| 8   | Boundaries                  | Wrap third-party APIs. Learning tests. Don't let boundary details leak. Adapter pattern.                                                                                                                                                                     |
| 9   | Unit Tests                  | Three Laws of TDD. Clean tests = readable tests. One assert per test (guideline). F.I.R.S.T.                                                                                                                                                                 |
| 10  | Classes                     | Small. SRP (one reason to change). Cohesion. OCP. DIP. Organize for change.                                                                                                                                                                                  |
| 11  | Systems                     | Separate construction from use. DI. Cross-cutting concerns. DSLs.                                                                                                                                                                                            |
| 12  | Emergence                   | Kent Beck's 4 rules: (1) runs all tests, (2) no duplication, (3) expresses intent, (4) minimal classes/methods.                                                                                                                                              |
| 13  | Concurrency                 | SRP for threading. Limit shared data. Use copies. Minimize synchronized sections. Know execution models.                                                                                                                                                     |
| 14  | Successive Refinement       | Case study: Args parser. Incremental refactoring under tests. Don't let messes grow.                                                                                                                                                                         |
| 15  | JUnit Internals             | Case study: ComparisonCompactor cleanup. Boy Scout Rule applied.                                                                                                                                                                                             |
| 16  | Refactoring SerialDate      | Case study: DayDate. First make it work (tests), then make it right. ~50 specific refactorings.                                                                                                                                                              |
| 17  | Smells and Heuristics       | Comprehensive catalog: C1-C5 (comments), E1-E2 (environment), F1-F4 (functions), G1-G36 (general), J1-J3 (Java), N1-N7 (names), T1-T9 (tests).                                                                                                               |
| A   | Concurrency II              | Appendix. Thread-safety deep dive, execution paths, library support, testing strategies.                                                                                                                                                                     |

## Core Thesis

Clean code reads like well-written prose: every name reveals intent, every function does one thing at one level of abstraction, and every module tells a story from high-level to detail (newspaper metaphor). The primary enemies of readability are bad names, large functions, duplicated code, and unnecessary coupling. Chapter 17's catalog of 66 smells and heuristics operationalizes these principles into concrete detection rules.

## Concepts Catalog

### Naming (Ch 2, N1-N7)

- **Intention-revealing**: Name answers why it exists, what it does, how it is used. If a name requires a comment, it does not reveal intent.
- **Avoid disinformation**: Don't use `accountList` if it's not actually a `List`. Don't use names that vary in small ways (`XYZControllerForHandlingOfStrings` vs `XYZControllerForStorageOfStrings`).
- **Meaningful distinctions**: `a1/a2` and `ProductInfo/ProductData` are noise. If names must differ, they should differ meaningfully.
- **Pronounceable names**: `genymdhms` → `generationTimestamp`.
- **Searchable names**: Single-letter names only in tiny scopes. Length of name ∝ size of scope (N5).
- **No encodings**: No Hungarian notation, no member prefixes (`m_`), no interface prefixes (`I`) (N6).
- **Class names**: Nouns/noun phrases. Not verbs. Not `Manager/Processor/Data/Info`.
- **Method names**: Verbs/verb phrases. Accessors/mutators/predicates: `get/set/is`. Factory methods over overloaded constructors.
- **One word per concept**: Don't mix `fetch/retrieve/get` for the same abstraction. Consistent lexicon.
- **No puns**: Don't use same word for two purposes. `add` that inserts into collection vs `add` that concatenates = pun.
- **Solution/problem domain names**: Use CS terms (pattern names, algorithm names) where appropriate; use domain terms for domain concepts.
- **N1 — Descriptive names**: Names are 90% of readability. Take time. Bowling game example: `isStrike(frame)` vs `l[z] == 10`.
- **N2 — Names at right abstraction level**: `Modem.dial(phoneNumber)` → `Modem.connect(connectionLocator)`.
- **N3 — Standard nomenclature**: Use pattern names (Decorator, Factory), domain language (ubiquitous language).
- **N4 — Unambiguous names**: `doRename()` that also renames references → `renamePageAndOptionallyAllReferences()`.
- **N5 — Long names for long scopes**: `i` fine in 5-line loop. Module-level → descriptive.
- **N7 — Names should describe side effects**: `getOos()` that also creates → `createOrReturnOos()`.

### Functions (Ch 3, F1-F4)

- **Small**: Functions should be small. 20 lines is a good upper bound. Blocks within `if/else/while` should be one line (a function call).
- **Do one thing**: A function does one thing if you cannot meaningfully extract another function from it with a name that is not merely a restatement of its implementation.
- **One level of abstraction per function**: Don't mix `getHtml()` with `append("\n")`. The Stepdown Rule: read top-to-bottom as narrative.
- **Switch → polymorphism**: Switch statements violate OCP and SRP. Bury them in abstract factories that create polymorphic objects. One switch per type selection (G23).
- **Descriptive names**: Long descriptive name > short enigmatic name > long descriptive comment.
- **Arguments**: Ideal = 0 (niladic), then 1 (monadic), then 2 (dyadic), then 3 (triadic = requires justification). More than 3 = never (F1). Wrap related args in objects.
- **Common monadic forms**: asking a question (`isReady()`), transforming input (`fileOpen(name) → stream`), or event (no return, alters system state).
- **No flag arguments**: Boolean args = function does two things. Split into two functions (F3).
- **No output arguments**: `appendFooter(report)` confusing. Use `report.appendFooter()` (F2).
- **Command-query separation**: A function either does something (command) or answers something (query), never both. `if (set("username", "bob"))` is confusing.
- **Exceptions over error codes**: Error codes force nested `if`. Exceptions allow normal path to be separated from error path.
- **Extract try/catch blocks**: `try { doSomething(); } catch { handleError(); }`. The try/catch body should be functions.
- **Error handling is one thing**: A function that handles errors should do nothing else.
- **F4 — Dead functions**: Delete uncalled methods. Source control remembers.

### Comments (Ch 4, C1-C5)

- **Good comments**: Legal headers, informative (regex explanation), intent explanation, clarification of obscure API, warning of consequences, TODO, amplification of importance.
- **Bad comments**: Mumbling, redundant (repeats code), misleading (slightly wrong), mandated boilerplate, journal/changelog, noise (`/** The name */`), position markers (`// Actions /////`), closing-brace comments, attribution (`// Added by`), commented-out code.
- **C1 — Inappropriate information**: Change histories, metadata belong in version control/issue tracker.
- **C2 — Obsolete comment**: Comments that have drifted from the code. Update or delete.
- **C3 — Redundant comment**: Comment says nothing code doesn't. `i++; // increment i`.
- **C4 — Poorly written comment**: If you write it, write it well. Grammar, punctuation, brevity.
- **C5 — Commented-out code**: Delete it. VCS remembers.

### Formatting (Ch 5)

- **Newspaper metaphor**: Name at top tells story. First paragraphs = synopsis. Detail increases downward.
- **Vertical openness**: Blank lines between concepts (between functions, between import groups).
- **Vertical density**: Lines that are tightly related should appear vertically close.
- **Vertical distance**: Variables declared close to usage. Instance variables at top of class. Dependent functions close together (caller above callee). Conceptual affinity: related functions grouped.
- **Vertical ordering**: Called function below calling function (newspaper style: high→low abstraction).
- **Horizontal**: Lines should be short. Don't use horizontal alignment of assignments/declarations — it draws eye to wrong thing. Indent to show scope.
- **Team rules**: Consistent style across codebase.

### Objects and Data Structures (Ch 6)

- **Data/Object anti-symmetry**: Objects hide data behind abstractions and expose functions. Data structures expose data and have no meaningful functions. They are opposites.
- **Procedural vs OO tradeoff**: Procedural = easy to add new functions (don't change existing data structures), hard to add new types. OO = easy to add new types, hard to add new functions.
- **Law of Demeter**: A method should only call methods on: its own object, its parameters, objects it creates, its direct components. No train wrecks: `a.getB().getC().doSomething()`.
- **DTOs**: Data structures with public variables. Active Records are DTOs with navigational methods. Don't put business logic in Active Records.

### Error Handling (Ch 7)

- **Use exceptions, not return codes**: Separates happy path from error handling.
- **Write try-catch-finally first**: Start with what happens on error. TDD approach to error cases.
- **Use unchecked exceptions**: Checked exceptions violate OCP (signature change propagates through call chain).
- **Provide context**: Exception message should tell what failed and why. Include the operation and the failure.
- **Define exception classes by caller's needs**: Wrap third-party exceptions. One exception class per call site is often enough.
- **Don't return null**: Forces callers to check null everywhere. Return empty collection or Special Case object instead.
- **Don't pass null**: Even worse than returning null. No good way to handle. Forbid by convention.
- **Special Case pattern** (Fowler): Return object that encapsulates the special behavior instead of null/exception.

### Boundaries (Ch 8)

- **Wrap third-party APIs**: `Sensors` class wraps `Map<String, Sensor>`. Limits the boundary interface to what's needed. Changes when the third-party API changes are localized to one place.
- **Learning tests**: Write tests against third-party API to verify your understanding. Free documentation. Detect breaking changes on upgrade.
- **Clean boundaries**: Code at boundaries needs clear separation and tests. Use interfaces/adapters. Define what you *wish* the API looked like, then adapt.

### Classes (Ch 10)

- **Small**: Classes should be small. Measured not by lines but by **responsibilities**.
- **SRP**: A class should have one, and only one, reason to change. Can you describe the class in ~25 words without using "if", "and", "or", "but"?
- **Cohesion**: Methods should manipulate few instance variables. High cohesion = each variable used by each method. When cohesion drops, split the class.
- **OCP**: Classes should be open for extension, closed for modification. Achieved through polymorphism and abstractions.
- **DIP**: Depend on abstractions, not concretions. Enables testability and flexibility.

### Emergence (Ch 12) — Kent Beck's 4 Rules of Simple Design

In priority order:

1. **Runs all the tests**: System must be verifiable. Testability drives good design (SRP, DIP).
2. **Contains no duplication**: Duplication is the primary enemy. Extract methods, use Template Method pattern.
3. **Expresses the intent of the programmer**: Good names, small functions/classes, standard patterns, well-written tests.
4. **Minimizes the number of classes and methods**: Don't create classes for the sake of it. Pragmatism over dogma. Lowest priority.

### Smells and Heuristics (Ch 17) — Complete Catalog

#### Comments (C1-C5)

- C1: Inappropriate Information (metadata in comments)
- C2: Obsolete Comment
- C3: Redundant Comment
- C4: Poorly Written Comment
- C5: Commented-Out Code

#### Environment (E1-E2)

- E1: Build Requires More Than One Step
- E2: Tests Require More Than One Step

#### Functions (F1-F4)

- F1: Too Many Arguments (0 best, 3+ bad)
- F2: Output Arguments (use method on object instead)
- F3: Flag Arguments (split into separate functions)
- F4: Dead Function (delete uncalled code)

#### General (G1-G36)

- G1: Multiple Languages in One Source File
- G2: Obvious Behavior Is Unimplemented (Principle of Least Surprise)
- G3: Incorrect Behavior at the Boundaries (test every boundary)
- G4: Overridden Safeties (don't disable warnings, skip tests)
- G5: Duplication (DRY — most important rule; identical code → extract; switch/else → polymorphism; similar algorithms → Template Method)
- G6: Code at Wrong Level of Abstraction (base class shouldn't know implementation details)
- G7: Base Classes Depending on Their Derivatives
- G8: Too Much Information (small interfaces, hide data, limit exposed methods)
- G9: Dead Code (unreachable if-body, uncalled methods, impossible catch → delete)
- G10: Vertical Separation (variables near usage, private functions below first call)
- G11: Inconsistency (same pattern for same kind of thing)
- G12: Clutter (unused constructors, unused variables, meaningless comments)
- G13: Artificial Coupling (general enums in specific classes, functions in wrong module)
- G14: Feature Envy (method uses another object's accessors more than its own data)
- G15: Selector Arguments (boolean/enum that selects behavior → split into separate functions)
- G16: Obscured Intent (dense expressions, Hungarian notation, magic numbers)
- G17: Misplaced Responsibility (code should be where reader expects it — least surprise)
- G18: Inappropriate Static (prefer instance methods if polymorphism might be needed)
- G19: Use Explanatory Variables (break complex expressions into named intermediates)
- G20: Function Names Should Say What They Do (`date.add(5)` → `date.plusDays(5)`)
- G21: Understand the Algorithm (don't just add if-statements until tests pass; know *why* it works)
- G22: Make Logical Dependencies Physical (don't assume — make the dependency explicit via parameter)
- G23: Prefer Polymorphism to If/Else or Switch/Case (ONE SWITCH rule: at most one switch per type selection, creating polymorphic objects)
- G24: Follow Standard Conventions (team coding standard, enforced by the code itself)
- G25: Replace Magic Numbers with Named Constants (including magic strings and tokens in tests)
- G26: Be Precise (don't use float for currency, don't assume first match is only match, don't ignore concurrency)
- G27: Structure over Convention (abstract methods > naming conventions; compiler enforces, conventions don't)
- G28: Encapsulate Conditionals (`shouldBeDeleted(timer)` > `timer.hasExpired() && !timer.isRecurrent()`)
- G29: Avoid Negative Conditionals (`buffer.shouldCompact()` > `!buffer.shouldNotCompact()`)
- G30: Functions Should Do One Thing (extract distinct sections into separate functions)
- G31: Hidden Temporal Couplings (make ordering explicit via bucket brigade — each function returns what next one needs)
- G32: Don't Be Arbitrary (have a reason for structure; arbitrary structure invites arbitrary changes)
- G33: Encapsulate Boundary Conditions (`nextLevel = level + 1` used once, not `level + 1` scattered)
- G34: Functions Should Descend Only One Level of Abstraction
- G35: Keep Configurable Data at High Levels (constants at top, passed down)
- G36: Avoid Transitive Navigation (Law of Demeter: `a.getB().getC()` → `a.doSomething()`)

#### Names (N1-N7)

- N1: Choose Descriptive Names
- N2: Choose Names at the Appropriate Level of Abstraction
- N3: Use Standard Nomenclature Where Possible
- N4: Unambiguous Names
- N5: Use Long Names for Long Scopes
- N6: Avoid Encodings (no Hungarian, no `m_`, no `I` prefix)
- N7: Names Should Describe Side-Effects

#### Tests (T1-T9)

- T1: Insufficient Tests (test everything that could break)
- T2: Use a Coverage Tool
- T3: Don't Skip Trivial Tests
- T4: An Ignored Test Is a Question about an Ambiguity
- T5: Test Boundary Conditions
- T6: Exhaustively Test Near Bugs (bugs congregate)
- T7: Patterns of Failure Are Revealing
- T8: Test Coverage Patterns Can Be Revealing
- T9: Tests Should Be Fast

---

## Overlap with CLAUDE.md

The following Clean Code concepts are already covered by the project's CLAUDE.md and will be **excluded or minimized** in the skill to avoid duplication:

| CLAUDE.md Rule                      | Clean Code Equivalent                             |
| ----------------------------------- | ------------------------------------------------- |
| Simplicity First                    | G30 (one thing), Ch 12 (minimize classes/methods) |
| Surgical Changes                    | Boy Scout Rule (partial overlap)                  |
| Fail fast on invalid state          | Don't return null (Ch 7), error handling strategy |
| Keep docstrings minimal             | C3 (redundant comments), C4 (poorly written)      |
| No features beyond what was asked   | Ch 12 rule 4 (minimize classes/methods)           |
| No abstractions for single-use code | Ch 12 rule 4                                      |

---

## Skill Review Process

2 rounds of self-review, checking SKILL.md against both the source book and AI-agent operationalizability.

### Changes Made After Round 1

| Finding                                                 | Source             | Action                                                    |
| ------------------------------------------------------- | ------------------ | --------------------------------------------------------- |
| Missing G31 hidden temporal coupling                    | Fidelity           | Added to General Smells table                             |
| Missing G33 encapsulate boundary conditions             | Fidelity           | Added to General Smells table                             |
| Missing Special Case pattern from error handling        | Fidelity           | Added to Error Handling section                           |
| Error handling section too brief on wrapping            | Fidelity + Quality | Expanded with specific wrap rule                          |
| Naming section lacked scope-length rule                 | Fidelity           | Added N5 with concrete guidance                           |
| Functions section missing Command-Query Separation      | Fidelity           | Added as explicit rule                                    |
| Comments "bad" list had Java-specific entries (Javadoc) | Quality            | Generalized to "doc-comment boilerplate"                  |
| G23 polymorphism rule too absolute for Python/scripting | Quality            | Softened to "consider; applies mainly with type dispatch" |
| Concurrency section included — too Java-specific        | Quality            | Removed; not operationalizable for code review            |
| Some heuristics repeated between sections               | Quality            | Deduplicated                                              |
| Test smells (T1-T9) duplicated TDD skill territory      | Quality            | Trimmed to avoid overlap, kept T5/T6/T9 as review-useful  |
| G8 (Too Much Information) missing from skill tables     | Fidelity           | Added to Structure and Coupling section                   |
| G18 (Inappropriate Static) missing from skill tables    | Fidelity           | Added to Structure and Coupling section                   |

### Declined Suggestions

| Suggestion                                | Rationale for declining                                          |
| ----------------------------------------- | ---------------------------------------------------------------- |
| Add full concurrency section              | Too Java-specific; better served by language-specific guidelines |
| Include case study examples from Ch 14-16 | Walkthroughs not operationalizable; principles already extracted |
| Add line-count thresholds for functions   | Book says "small"; rigid numbers don't transfer across languages |
| Include Kent Beck's 4 rules in skill      | Already referenced in TDD skill; would duplicate                 |

### Round 2 Verdict

Re-read complete skill against book outline and CLAUDE.md:

- **Fidelity**: All 66 smells (C1-C5, E1-E2, F1-F4, G1-G36, J1-J3, N1-N7, T1-T9) accounted for. Java-specific entries (J1-J3) intentionally excluded. Core concepts from Ch 2-12 represented.
- **Quality**: Every rule maps to "when you see X, do Y" form. No philosophy. No motivation. No filler. No overlap with CLAUDE.md.
- **Verdict**: Ship it.
