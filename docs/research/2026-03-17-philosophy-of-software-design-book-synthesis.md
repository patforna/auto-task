# Research: a Philosophy of Software Design -- Book Synthesis & Skill Review

**Source**: John Ousterhout, *A Philosophy of Software Design* (Yaknyam Press, 2nd ed., 2021), ~190 pages **Output**: `/SKILL.md` -- incompressible software design skill for AI coding agents **Date**: 2026-03-17

---

## Book Structure

| Ch  | Title                                               | Key Concepts                                                                |
| --- | --------------------------------------------------- | --------------------------------------------------------------------------- |
| 1   | Introduction (It's All About Complexity)            | Software design as complexity management; iterative/incremental development |
| 2   | The Nature of Complexity                            | C = sum(cp * tp); change amplification, cognitive load, unknown unknowns    |
| 3   | Working Code Isn't Enough (Strategic vs Tactical)   | Tactical tornado; invest 10-20% in design; strategic programming            |
| 4   | Modules Should Be Deep                              | Interface vs implementation; deep modules; shallow module red flag          |
| 5   | Information Hiding (and Leakage)                    | Information hiding; temporal decomposition; information leakage red flag    |
| 6   | General-Purpose Modules are Deeper                  | Somewhat general-purpose; generality test questions                         |
| 7   | Different Layer, Different Abstraction              | Pass-through methods/args/variables; decorators; interface vs abstraction   |
| 8   | Pull Complexity Downward                            | Configuration as complexity pushed up; simplify caller's life               |
| 9   | Better Together Or Better Apart?                    | Bring together if shared info/simpler interface/eliminate duplication       |
| 10  | Define Errors Out of Existence                      | Four techniques: define away, mask, aggregate, just crash                   |
| 11  | Design it Twice                                     | Consider 2+ approaches; compare on interface simplicity & generality        |
| 12  | Why Write Comments? The Four Excuses                | Comments are not failures; capture what code cannot express                 |
| 13  | Comments Should Describe Things that Aren't Obvious | Interface vs implementation comments; precision vs intuition; cross-module  |
| 14  | Choosing Names                                      | Precision, consistency, avoid extra words; names as abstractions            |
| 15  | Write The Comments First                            | Comments as design tool; hard-to-describe = design problem                  |
| 16  | Modifying Existing Code                             | Stay strategic; maintain comments near code; avoid duplication              |
| 17  | Consistency                                         | Names, style, interfaces, invariants; don't change conventions lightly      |
| 18  | Code Should be Obvious                              | Whitespace, comments, avoid generic containers; nonobvious code red flag    |
| 19  | Software Trends                                     | OOP, agile, TDD, design patterns, getters/setters evaluated                 |
| 20  | Designing for Performance                           | Naturally efficient; measure first; design around the critical path         |
| 21  | Decide What Matters                                 | (2nd ed.) Distinguish important from unimportant; focus design effort       |

## Core Thesis

The greatest limitation on software is our ability to understand the systems we build. Complexity is the root cause of most software difficulties. The primary goal of software design is to reduce complexity: make systems easier to understand and modify. Complexity is defined as `C = sum(cp * tp)` where `cp` is the complexity contributed by each part and `tp` is the fraction of time developers spend working with that part.

## Concepts Catalog

### Complexity Defined (Ch 2)

Three symptoms of complexity:

1. **Change amplification**: A simple change requires modifications in many places.
2. **Cognitive load**: A developer must accumulate a large amount of information to make a change.
3. **Unknown unknowns**: It is unclear what code needs to be modified, or what information must be considered.

Unknown unknowns are the worst form -- they lead to bugs that are discovered only after deployment. Two causes of complexity: **dependencies** (a piece of code cannot be understood in isolation) and **obscurity** (important information is not obvious).

Complexity is incremental -- no single decision makes a system complex. It accumulates through hundreds of small decisions. "Death by a thousand cuts."

### Strategic Vs Tactical Programming (Ch 3)

- **Tactical programming**: Primary goal is to get something working. Shortcuts accumulate complexity. The "tactical tornado" is a developer who produces code fast but leaves a trail of complexity.
- **Strategic programming**: Primary goal is to produce a great system design. "Working code isn't a high enough standard." Invest 10-20% of development time in design improvement.
- Every code change should aim to leave the system with the structure it would have had if you had designed it with this change in mind from the start.

### Deep Modules (Ch 4)

A module's interface describes *what* it does; its implementation describes *how*. The best modules have simple interfaces but powerful functionality -- they are **deep**. The interface is the cost (complexity the user must learn); the implementation is the benefit (functionality provided).

- **Deep module**: Simple interface, lots of hidden functionality. Unix file I/O is the canonical example: 5 system calls hide enormous implementation complexity.
- **Shallow module**: Interface is relatively complex compared to the functionality it provides. The interface does not hide much complexity.
- A module's interface includes both formal elements (function signatures, types) and informal elements (behavior, constraints, side effects -- documented in comments).

### Information Hiding and Leakage (Ch 5)

- **Information hiding**: Each module encapsulates knowledge (data structures, algorithms, low-level details) that is not visible through its interface. Reduces complexity because callers don't need to know.
- **Information leakage**: When a design decision is reflected in multiple modules. Creates dependencies -- if the decision changes, all modules must change.
- **Temporal decomposition**: Structuring code around the order of operations rather than around information. Results in information leakage because knowledge about a particular concern gets split across time-ordered modules. Instead, bring together code that shares the same knowledge.

### General-Purpose Modules (Ch 6)

Make classes somewhat general-purpose, even if currently used in only one place. The sweet spot is: general-purpose interface, special-purpose usage. Questions to test generality:

1. "What is the simplest interface that will cover all my current needs?"
2. "In how many situations will this method be used?" If only one, it may be too special.
3. "Is this API easy to use for my current needs?" If you must write extra code to bridge between general-purpose and current need, the interface is too general.

### Different Layer, Different Abstraction (Ch 7)

Each layer in a system should provide a fundamentally different abstraction than the layers above and below it. Red flags for layer violations:

- **Pass-through method**: A method that does little other than invoke another method with a similar signature. Indicates the layers are not providing different abstractions. Fix by: eliminating the method, redistributing functionality, or merging classes.
- **Pass-through variable**: A variable passed down through a long chain of methods to reach the code that needs it. Adds complexity to every intermediate method. Fix by: shared object/context, global variable, or (less good) passing in a context object.
- **Decorators/wrappers**: Often create shallow layers that duplicate the underlying interface. Use only when the decorator adds significant new functionality that is distinct from the underlying class.

### Pull Complexity Downward (Ch 8)

When there is a choice about where to place complexity, push it into the implementation (where it is hidden) rather than into the interface (where it is exposed to all callers). It is more important for a module to have a simple interface than a simple implementation.

Configuration parameters are a symptom of complexity pushed upward -- the module is saying "I can't figure out the right value, so you deal with it." Ask: can the system determine a good default automatically? If yes, do it.

### Together or Apart (Ch 9)

Bring pieces together when:

- They share information (same knowledge would otherwise leak).
- Combining simplifies the interface (callers make one call instead of two coordinated calls).
- Combining eliminates duplication.

Split pieces apart when:

- Each piece is independently useful.
- Combining would create a complex multi-purpose module with no clear abstraction.

Splitting a method should only be done if it results in abstractions that are each simpler. Splitting into two methods at the same level of abstraction rarely helps -- it just forces the reader to look at two things.

General-purpose and special-purpose code should be separated. The general-purpose mechanism goes in a lower layer; the special-purpose usage goes in a higher layer.

### Define Errors Out of Existence (Ch 10)

Exception handling is a major source of complexity. Four techniques to reduce exception surface:

1. **Define errors out of existence**: Redefine the operation so it cannot fail. Example: `unset` should succeed even if the variable doesn't exist (its job is "ensure variable doesn't exist," not "delete variable"). Python's out-of-range list slicing returns empty rather than throwing.
2. **Exception masking**: Handle the exception at a low level so higher levels need not know. Example: TCP masks packet loss by retransmitting internally. This is pulling complexity downward.
3. **Exception aggregation**: Handle many exceptions with a single handler rather than individual catch blocks. Example: Web server catches all parameter exceptions in one top-level handler. Propagate exceptions upward to a single aggregation point.
4. **Just crash**: For errors that are rare, difficult to handle, and where no recovery is possible (e.g., out of memory), abort with a clear error message. Don't add complexity for errors you can't meaningfully recover from.

Key caveat: only define away or mask exceptions when the exception information isn't needed outside the module. If callers genuinely need to know about the exception, it must be exposed.

### Design It Twice (Ch 11)

For every significant design decision, consider at least two radically different approaches before committing. Compare alternatives on:

- Interface simplicity and ease of use for callers
- Generality
- Performance implications

This applies at multiple levels: interface design, implementation strategy, system architecture. Even if the first idea seems adequate, exploring alternatives reveals trade-offs and often produces a better hybrid design.

### Comments (Ch 12-13, 15-16)

Four categories of comments:

1. **Interface comments**: Describe the abstraction a module/method provides. Must include: what the method does, each argument, return value, side effects, exceptions, preconditions. Should NOT include implementation details.
2. **Data structure member comments**: For instance variables and fields. Document what the variable represents (nouns, not verbs), its units, boundary conditions (inclusive/exclusive), null semantics, invariants.
3. **Implementation comments**: What and why, not how. Place before major blocks. Describe the overall strategy, then annotate tricky parts.
4. **Cross-module comments**: For design decisions that span modules. Use a central `designNotes` file with short references from individual modules.

The guiding rule: **comments should describe things that aren't obvious from the code.** Use different words from the name of the thing being documented. If the comment just repeats the code, it is worthless.

Comments as a design tool: if writing a simple and complete interface comment is hard, the design is probably wrong. A long interface comment indicates a shallow module.

### Naming (Ch 14)

- **Create an image**: A good name conveys information about the underlying entity. Ask: "If someone sees this name in isolation, how closely will they guess what it refers to?"
- **Precision**: Names should be precise enough to be unambiguous. Avoid generic names like `result`, `data`, `tmp`, `status` outside narrow scopes. Boolean variable names should be predicates.
- **Consistency**: Pick a canonical name for each common concept and use it everywhere. Three rules: (1) always use the common name for the purpose, (2) never use it for a different purpose, (3) ensure all variables with that name have the same behavior.
- **Avoid extra words**: Every word in a name should provide useful information. Don't add generic nouns (`Object`, `Field`). Don't include type information in the name.
- **Scope-proportional length**: Short names for short scopes (`i` for 3-line loops), longer names for wider scopes.
- **Hard to name = design problem**: If you can't find a simple, intuitive name, the underlying concept may not have a clean design.

### Consistency (Ch 17)

Consistency reduces cognitive load -- once you learn a pattern, you can immediately understand all similar code. Applies to: names, coding style, interfaces, design patterns, invariants.

- Follow existing conventions even if you'd do it differently.
- Having a "better idea" is not a sufficient excuse to introduce inconsistency.
- Don't force dissimilar things into the same pattern -- consistency is only valuable when "if it looks like an X, it really is an X."

### Code Should Be Obvious (Ch 18)

Code is obvious when a reader can understand it quickly and their first guesses about behavior are correct. Techniques for obviousness:

- Judicious use of whitespace to separate logical blocks.
- Comments to compensate for nonobvious behavior.
- Avoid generic containers (use named structures instead).
- Match declaration types to allocation types.
- Document behavior that violates reader expectations.

Software should be designed for **ease of reading, not ease of writing**.

### Performance (Ch 20)

- Choose "naturally efficient" designs -- prefer hash tables over ordered maps when ordering isn't needed, etc.
- Measure before optimizing. Programmer intuitions about performance are unreliable.
- When optimization is needed, design around the critical path: identify the minimum code that must execute in the common case, then structure everything else around it.
- Simplicity and performance are usually aligned: deep classes are faster than shallow ones (fewer layer crossings), and fewer special cases means less branching.

### Red Flags Catalog (Complete, from the Book)

| Red Flag                                            | Ch  | Diagnostic                                                                       |
| --------------------------------------------------- | --- | -------------------------------------------------------------------------------- |
| Shallow Module                                      | 4   | Interface is complex relative to the functionality it provides.                  |
| Information Leakage                                 | 5   | Same design decision appears in multiple modules.                                |
| Temporal Decomposition                              | 5   | Code structure mirrors order of operations rather than information structure.    |
| Overexposure (too many methods/features)            | 5   | Module's API exposes internal details that callers don't need.                   |
| Pass-Through Method                                 | 7   | Method does little except invoke another method with a similar signature.        |
| Repetition                                          | 7   | Same code or pattern appears in multiple places; sign of missing abstraction.    |
| Special-General Mixture                             | 7   | General-purpose mechanism contains special-purpose code or vice versa.           |
| Conjoined Methods                                   | 9   | You can't understand one method without reading another.                         |
| Comment Repeats Code                                | 13  | Comment uses the same words as the code it describes; adds no information.       |
| Implementation Documentation Contaminates Interface | 13  | Interface comment describes implementation details not needed by callers.        |
| Vague Name                                          | 14  | Name is broad enough to refer to many different things.                          |
| Hard to Pick Name                                   | 14  | Difficulty finding a simple name hints that the underlying concept is not clean. |
| Hard to Describe                                    | 15  | If a simple and complete comment is difficult to write, the design may be wrong. |
| Nonobvious Code                                     | 18  | Meaning and behavior cannot be understood with a quick reading.                  |

---

## Skill Review Process

2 self-review rounds, reviewing SKILL.md against the source book and AI-agent operationalizability.

### Changes Made After Round 1

| Finding                                                     | Source            | Action                                             |
| ----------------------------------------------------------- | ----------------- | -------------------------------------------------- |
| Missing generality test questions from Ch 6                 | Fidelity          | Added 3 decision questions to generality section   |
| Together-or-apart criteria from Ch 9 missing                | Fidelity          | Added decision procedure for merge/split           |
| Exception handling lacked the 4 named techniques            | Fidelity          | Added define-away, mask, aggregate, crash          |
| Comment categories collapsed into vague guidance            | Fidelity          | Separated into interface/data/implementation/cross |
| Design-it-twice not represented                             | Fidelity          | Added as explicit procedure step                   |
| Red flag table missing several flags from later chapters    | Fidelity          | Added Conjoined Methods, Hard to Describe, etc.    |
| "Pull complexity downward" phrased as philosophy not rule   | Quality           | Rewritten as decision procedure                    |
| Naming section overlapped with CLAUDE.md docstring guidance | Overlap avoidance | Removed docstring overlap, focused on naming rules |
| Consistency section generic                                 | Quality           | Made specific: follow existing conventions always  |
| Performance section included; not in CLAUDE.md scope        | Quality           | Removed -- not a design-decision skill concern     |

### Declined Suggestions

| Suggestion                                   | Rationale for declining                                           |
| -------------------------------------------- | ----------------------------------------------------------------- |
| Add OOP/inheritance guidance from Ch 19      | Too language-specific; composition preference is widely known     |
| Include TDD critique from Ch 19              | Conflicts with existing TDD skill; not a software design decision |
| Add "write comments first" as a process step | AI agent writes code and comments together anyway                 |
| Include full code examples from the book     | Non-instructional; skill should be rules not examples             |

### Round 2 Verdict

Self-review confirmed convergence:

- **Fidelity**: All 14 red flags from the book present. All major concepts (deep modules, information hiding, define errors out of existence, design it twice, pull complexity downward, different-layer-different-abstraction) have faithful decision procedures.
- **Quality**: Every sentence maps to a concrete action or diagnostic. No filler. No overlap with CLAUDE.md.
