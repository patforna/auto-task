# BDD Principles for Agentic Task Specifications

Research conducted 2026-03-13 via three parallel agents: BDD principles mapping, BDD practitioners' wisdom, and Aviator Verify analysis. Findings informed the define-task skill's Step 2 (Shape and flesh out) guidance.

## Background: What BDD Actually Is

BDD is widely misunderstood as "Cucumber + Gherkin." Dan North created it in 2003-2006 as a way to help developers "get straight to the good stuff" in TDD, by replacing the word "test" with "behaviour." It evolved into what he called "a second-generation, outside-in, pull-based, multiple-stakeholder, multiple-scale, high-automation, agile methodology."

The core insight, as Liz Keogh puts it: "BDD is the art of using examples in conversation to illustrate behaviour." Not to specify it exhaustively, but to *explore* it.

Gojko Adzic's retrospective on Specification by Example after 10 years confirmed the hierarchy: "having conversations is more important than capturing conversations is more important than automating conversations."

## Principles Mapped to Agentic Development

### 1. Ubiquitous Language (From DDD)

**Original:** Everyone uses the same vocabulary. Eliminates translation errors.

**Agentic context:** MORE important. The implementing agent can't ask "what did you mean by X?" mid-implementation. Every ambiguous term is a coin flip.

**Implication:** Task definitions must use domain terms from the codebase consistently. Define terms if there's any chance of ambiguity.

### 2. Examples Over Abstractions (Specification by Example)

**Original:** Abstract rules are ambiguous. Concrete examples force precision.

**Agentic context:** The SINGLE MOST IMPORTANT principle for agentic work. An abstract AC like "handle edge cases gracefully" gives the implementing agent no useful signal. A concrete example is verifiable, testable, and unambiguous.

**Implication:** Every AC should either BE a concrete example or be accompanied by one when ambiguous. The Keogh heuristic: if two agents could read a criterion and build different things, add a concrete example.

### 3. The Conversation (CCC: Card, Conversation, Criteria)

**Original:** The card is a placeholder for a conversation. Criteria emerge from the conversation.

**Agentic context:** This is where CCC breaks most dramatically. There is no mid-implementation conversation. The task file must carry the load of both the Card AND the Conversation — it's the artifact of a completed conversation, not a placeholder for one.

**Implication:** The define-task phase IS the conversation. It must be thorough enough that someone with zero context can execute from the artifact alone. Signal without noise.

### 4. Three Amigos

**Original:** Developer, tester, and business person collaborate to discover blind spots.

**Agentic context:** The roles collapse:

- Business person = the human developer (knows the "why")
- Tester = the defining agent (should probe for edge cases)
- Developer = the implementing agent (arrives later, has only the artifact)

The critical loss: the "developer" can't participate in the conversation. In traditional Three Amigos, the developer says "that's actually hard because of X." This feedback loop is severed.

**Implication:** The defining agent must explicitly take the developer's perspective: "What would an implementing agent find ambiguous here?"

### 5. Discovery / Formulation / Automation (Rose & Nagy)

**Original:** Three distinct practices — discovery (build understanding), formulation (write precise examples), automation (make them executable).

**Agentic context:** Maps to the workflow phases:

- Discovery = exploration session + define-task
- Formulation = the task file itself
- Automation = plan-task + impl-task

Key insight: Discovery and Formulation are interleaved (you discover a rule, formulate it, realize it's two rules, reformulate). But both are separate from Automation. The define-task skill respects this by merging the thinking steps (old Steps 2+3) while keeping file creation separate.

### 6. Outside-in Development

**Original:** Start from the outermost boundary and work inward.

**Agentic context:** Directly applies to ACs. Criteria should describe observable external behaviour, not internal implementation steps.

**Implication:** "The CLI prints X when given Y" not "Create a new class that does Z." Two exceptions: structural criteria for refactoring tasks, and formulas that define correctness.

### 7. Living Documentation

**Original:** Executable specifications serve as always-up-to-date documentation.

**Agentic context:** ACs written as concrete examples can become test cases almost verbatim. This eliminates the interpretation gap between "what was specified" and "what was tested."

## What Becomes MORE Important in the Agentic World

1. **Concrete examples over abstract rules.** Humans interpret abstractions using context. Agents interpret them literally or hallucinate the missing context.

2. **Eliminating ambiguity BEFORE handoff.** In human teams, ambiguity is resolved through hallway conversations. In agentic work, ambiguity in the task file becomes ambiguity in the implementation.

3. **Separation of "what" from "how."** ACs (what) must be rock-solid. Implementation plan (how) can be flexible. If the agent meets the criteria via a different path, that's fine.

4. **The "questions" column from Example Mapping.** Unresolved questions in traditional BDD are parked. In agentic work, an unresolved question that reaches the implementing agent will be silently resolved — probably wrong.

## Failure Modes the Agentic Context Introduces

1. **Silent assumption resolution.** The implementing agent encounters ambiguity and picks an interpretation without flagging it.

2. **Criteria-implementation drift.** The agent satisfies the letter of the criteria but not the intent. Concrete examples prevent this.

3. **Context loss across session boundaries.** Exploration context about WHY decisions were made doesn't survive if not captured in the task.

4. **Over-specification trap.** To compensate for the absent conversation, the human over-specifies implementation details, removing the agent's ability to find better solutions. BDD's answer: specify BEHAVIOUR, not mechanism.

5. **Example poverty.** The defining agent writes 3 ACs where 8 concrete examples are needed.

## BDD Practitioner Anti-Patterns (And Agentic Equivalents)

### "Cucumber as Test Automation"

Treating BDD as a testing technique rather than a discovery technique. The agentic equivalent: treating the task file as a to-do list rather than captured understanding. If the exploration session was shallow, the define step should say so (placeholder task) rather than fabricate specificity.

### Incidental Details (The "UI Test Trap")

Ferguson Smart's rule: don't mention UI in scenarios. Imperative scenarios spell out *how* instead of *what*. The agentic equivalent: over-specifying file paths, function signatures, module structure when only behaviour matters. ACs should be implementation-free. Implementation hints belong in Notes or the plan.

### Over-Specification Vs Under-Specification

Liz Keogh's key distinction: acceptance criteria are rules; scenarios are concrete examples that illustrate rules. Both are needed. A rule without examples is ambiguous. Examples without a rule are disconnected data points.

For each AC, ask: "Could two engineers read this and build different things?" If yes, add a concrete example.

### Given/When/Then as Straitjacket

Requirements discovery needs broad strokes before narrow brushes. Teams that force every requirement into G/W/T format too early lose the forest for trees.

Don't force ACs into rigid format. Free-form bullet points are often clearer than forced G/W/T. Reserve structured scenario format for behavioural rules that genuinely have preconditions, triggers, and outcomes.

### The Gap Between Business Language and Implementation

Domain language gets lost when scenarios use generic implementation terms. The agentic equivalent: "modify the class" instead of "make `ReversalStrategy` require explicit thresholds."

Use the codebase's domain vocabulary in ACs. This also helps the implementing agent grep for relevant code.

## Aviator Verify: Ideas Worth Stealing

Aviator reframes BDD for the agent era by shifting the unit of review from code to intent. They don't use BDD terminology (Given/When/Then) at all.

**Ideas worth incorporating:**

1. **Intent as anchoring section.** Every task must lead with purpose (why). Already in our skill as the Description opener.

2. **Three-layer invariant hierarchy.** Some requirements are universal (codebase-level), some domain-specific, some task-specific. Don't repeat in tasks what CLAUDE.md already says.

3. **Checklist-style ACs over structured syntax.** They abandoned G/W/T. Plain language checklist items are easier to write and verify. Already our approach.

**Ideas to push back on:**

1. **Execution Steps.** Their specs include hierarchical implementation steps. For capable models, this is counterproductive — constrains the agent's ability to find better solutions. The task should say *what* and *why*, not *how*.

2. **Scope-as-file-list.** Too granular. The agent should determine which files to touch based on the ACs.

3. **Approval workflows / audit trails.** Enterprise bloat for a solo dev.

## Key Takeaway

The BDD principles that matter most for agentic task specs are:

1. Lead with why
2. Write rules, not scripts — ACs describe observable behaviour
3. Anchor ambiguous rules with concrete examples (Keogh heuristic)
4. Use domain vocabulary from the codebase
5. Separate constraints from suggestions (ACs vs Notes)
6. Surface unknowns explicitly — don't let them reach the implementing agent
7. Specify BEHAVIOUR, not mechanism — unless the mechanism IS the spec

## Sources

- Dan North — [Introducing BDD](https://dannorth.net/blog/introducing-bdd/)
- Dan North — [What's in a Story?](https://dannorth.net/blog/whats-in-a-story/)
- Liz Keogh — [Acceptance Criteria vs Scenarios](https://lizkeogh.com/2011/06/20/acceptance-criteria-vs-scenarios/)
- Liz Keogh — [Behaviour-Driven Development](https://lizkeogh.com/behaviour-driven-development/)
- Liz Keogh — [BDD Shallow and Deep](https://lizkeogh.com/2013/07/01/behavior-driven-development-shallow-and-deep/)
- Liz Keogh — [Conversational Patterns in BDD](https://lizkeogh.com/2011/09/22/conversational-patterns-in-bdd/)
- Gojko Adzic — [Specification by Example, 10 Years Later](https://gojko.net/2020/03/17/sbe-10-years.html)
- Matt Wynne — [Introducing Example Mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/)
- Seb Rose & Gaspar Nagy — [BDD Books (Discovery, Formulation)](https://bddbooks.com/)
- John Ferguson Smart — [BDD Anti-patterns](https://johnfergusonsmart.com/slidedecks/bdd-anti-patterns/)
- Cucumber — [Anti-patterns Part 1](https://cucumber.io/blog/bdd/cucumber-antipatterns-part-one/)
- Cucumber — [Anti-patterns Part 2](https://cucumber.io/blog/bdd/cucumber-anti-patterns-part-two/)
- Cucumber — [History of BDD](https://cucumber.io/docs/bdd/history/)
- Aviator — [Verify Documentation](https://docs.aviator.co/verify/your-first-spec)
