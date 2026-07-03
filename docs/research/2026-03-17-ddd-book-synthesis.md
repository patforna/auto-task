# Research: Domain-Driven Design -- Book Synthesis & Skill Review

**Source**: Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (Addison-Wesley, 2003), ~560 pages **Output**: `.claude/skills/ddd/SKILL.md` -- incompressible DDD skill for AI coding agents **Date**: 2026-03-17

---

## Book Structure

| Part                                     | Chapters | Content                                                                                                                                                                                                                                                                                |
| ---------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| I -- Putting the Domain Model to Work    | 1--3     | Knowledge crunching, Ubiquitous Language, Model-Driven Design, binding model and implementation, hands-on modelling with domain experts.                                                                                                                                               |
| II -- The Building Blocks                | 4--7     | Layered Architecture, Entities, Value Objects, Services, Modules, Aggregates, Factories, Repositories. Extended shipping example.                                                                                                                                                      |
| III -- Refactoring Toward Deeper Insight | 8--13    | Breakthroughs, making implicit concepts explicit (Specification, Strategy, Constraint), Supple Design patterns, Analysis Patterns, Design Patterns, Refactoring.                                                                                                                       |
| IV -- Strategic Design                   | 14--17   | Bounded Context, Context Map, Continuous Integration, Shared Kernel, Customer/Supplier, Conformist, Anti-Corruption Layer, Separate Ways, Open Host, Published Language, Distillation, Core Domain, Generic Subdomains, Large-Scale Structure, Responsibility Layers, Knowledge Level. |
| Conclusion                               | --       | Epilogues (5 projects revisited), Looking Forward.                                                                                                                                                                                                                                     |

## Core Thesis

Software complexity is most fundamentally a domain-modelling problem, not a technical one. The premise of DDD is that the most significant complexity in many software applications is not technical but in the domain itself. A model is a rigorously organized and selective abstraction of domain knowledge; when model and implementation are tightly bound (Model-Driven Design), the code becomes an expression of the model, and insights about the domain directly improve the software. The Ubiquitous Language -- shared terminology between domain experts and developers, used in code, discussions, and documentation alike -- is the mechanism that binds model to communication to implementation.

## Concepts Catalog

### Part I: Putting the Domain Model to Work

#### Ubiquitous Language (Ch 2)

A language structured around the domain model and used consistently in code, speech, and writing. Every class name, method name, and module name should be drawn from this language. A change in the language is a change to the model. When domain experts do not understand the terms in the model, or when developers cannot express domain rules using model concepts, the model is wrong.

#### Model-Driven Design (Ch 3)

The model is not a diagram separate from code -- the code **is** the model. Every design element maps directly to a model concept. If the design diverges from the model, one or both must change. Analysis models that cannot be implemented directly are dangerous -- they create a gap that grows over time.

#### Knowledge Crunching (Ch 1)

Modelling is an iterative process of dialogue with domain experts, prototyping, and refining. The most important modelling breakthroughs come from making implicit domain concepts explicit. Domain experts bring deep knowledge; developers bring the ability to abstract and implement.

### Part II: Building Blocks of a Model-Driven Design

#### Layered Architecture (Ch 4)

Separate domain logic from UI, application logic, and infrastructure. Four layers: **User Interface** (presentation), **Application** (thin orchestration, no domain logic), **Domain** (the model -- the heart), **Infrastructure** (persistence, messaging, etc.). Domain layer depends on nothing above it. Infrastructure supports the domain layer, typically via dependency inversion.

#### Entities (Ch 5)

Objects defined by identity, not attributes. Two objects with the same attributes are still different if they have different identities. The identity must be meaningful and stable -- it persists across state changes, serialization, and distribution. Design Entity classes to focus on identity continuity and lifecycle, not on attributes.

#### Value Objects (Ch 5)

Objects defined entirely by their attributes -- no identity. Two Value Objects with the same attributes **are** the same thing. Design rules: make them **immutable**; all operations return new instances; implement equality by attribute comparison. Value Objects can be shared freely, copied, replaced. When in doubt, prefer Value Object over Entity -- they are simpler, safer, and more optimizable.

#### Services (Ch 5)

Operations that do not naturally belong to any Entity or Value Object. A Service is **stateless**, defined by what it does for a client of the domain in terms of domain concepts. Name the operation from the Ubiquitous Language. Three characteristics: (1) the operation relates to a domain concept that is not a natural part of an Entity or Value Object, (2) the interface is defined in terms of other domain model elements, (3) the operation is stateless. Distinguish domain Services from application Services and infrastructure Services.

#### Modules (Ch 5)

Modules (packages) are a model element. They should reflect domain concepts, not technical categories. Choose module names from the Ubiquitous Language. Low coupling between modules, high cohesion within. Module boundaries should tell a story about the domain.

#### Aggregates (Ch 6)

A cluster of associated objects treated as a unit for data changes. Rules:

- Each Aggregate has a **root Entity** -- the only object external code may hold references to.
- Objects within the Aggregate boundary may hold references to other Aggregate roots, but not to non-root objects of other Aggregates.
- Only the root can be obtained directly from a Repository. Internal objects are obtained by traversal from the root.
- A delete of the root must remove everything within the boundary.
- **Invariants** (consistency rules) that span objects within the Aggregate boundary are enforced on every state change (transaction boundary = Aggregate boundary).
- Invariants that span Aggregates are not expected to be immediately consistent -- use eventual consistency.

#### Factories (Ch 6)

When creating an Aggregate is complex or reveals too much internal structure, encapsulate creation in a Factory. A Factory's job is to produce a consistent, fully-formed Aggregate. Factory methods can live on the Aggregate root, on a standalone Factory, or on another object involved in the creation. A Factory must produce objects that satisfy all invariants. Reconstitution from storage is different from creation -- Repositories handle that.

#### Repositories (Ch 6)

Provide the illusion of an in-memory collection of all objects of a certain type. Encapsulate the technology of storage, retrieval, and search. The interface speaks pure domain language -- no SQL, no ORM concepts leak through. Provide Repositories only for Aggregate roots. A Repository decouples the domain from data-mapping layers, query languages, and infrastructure. Strategically, Repositories make it possible to substitute different storage implementations.

### Part III: Refactoring Toward Deeper Insight

#### Breakthroughs (Ch 8)

Modelling breakthroughs -- moments when a deeper model suddenly replaces a superficial one -- are the highest-value events in a project. They are unpredictable but can be cultivated by continuous refactoring, dialogue with domain experts, and willingness to discard what you have. Signs you need a breakthrough: awkward code that is hard to extend, a concept that domain experts keep trying to explain and the code does not capture.

#### Making Implicit Concepts Explicit (Ch 9)

Listen for concepts that domain experts use but that are not yet in the model. Common categories:

- **Specification**: A predicate that tests whether an object satisfies some criteria. Make it a first-class object. Specifications can be combined (AND, OR, NOT) and used for validation, selection, and building-to-order.
- **Constraint**: A rule limiting values or combinations. When a constraint is significant enough to name, make it explicit.
- **Process**: A domain procedure described by experts. If it is important, model it as a Service or Strategy.
- **Strategy/Policy**: An interchangeable algorithm for accomplishing a domain goal. Use the Strategy pattern (GoF) but name the class from the domain ("OverbookingPolicy"), not the pattern ("Strategy").

#### Supple Design (Ch 10)

Patterns that make a design easy to use and change:

- **Intention-Revealing Interfaces**: Name classes and methods to express effect and purpose, not mechanism. A client developer should not need to read the implementation to understand what a method does.
- **Side-Effect-Free Functions**: Separate commands (state-changing operations) from queries (functions that return results without side effects). Place as much logic as possible in functions that return Value Objects. When commands are necessary, keep them simple and avoid returning domain information from them.
- **Assertions**: State post-conditions and invariants explicitly (in documentation, tests, or language constructs). Make the consequences of calling an operation obvious without requiring the caller to understand the internals.
- **Conceptual Contours**: Decompose design elements so that boundaries align with the conceptual contours of the domain. If a concept changes independently, it should be a separate element. If concepts change together, they belong together. This is not a mechanical process -- it requires deep domain understanding.
- **Standalone Classes**: Reduce coupling to the point where a class can be understood and tested in isolation. Every dependency is a burden on understanding. The ultimate goal: self-contained classes that express a single concept.
- **Closure of Operations**: Where possible, define operations whose argument type and return type are the same as the type they are defined on (e.g., `Set.union(Set) -> Set`, `Money.add(Money) -> Money`). This creates a closed system that is easy to understand and combine.

#### Analysis Patterns (Ch 11)

Reusable domain model fragments from published literature (e.g., Fowler's *Analysis Patterns*). Use them as a starting point, not a blueprint. They accelerate modelling by providing a vocabulary of proven abstractions.

#### Design Patterns in the Domain (Ch 12)

GoF patterns (Strategy, Composite, etc.) can serve domain modelling when applied with domain semantics. Name the pattern from the domain, not the GoF name. A Composite of `Route` legs is a domain concept; calling it "Composite" loses the domain meaning. Flyweight, Facade, etc. are infrastructure patterns and do not enter the domain model.

#### Refactoring Toward Deeper Insight (Ch 13)

Continuous refactoring is the vehicle for model evolution. Refactoring is not just code cleanup -- it is re-modelling. The domain expert and the developer collaborate in every significant refactoring. Watch for rigidity: when a change is hard to make, the model may be wrong, not just the code.

### Part IV: Strategic Design

#### Bounded Context (Ch 14)

A Bounded Context is the boundary within which a particular model is defined and applicable. A single term can mean different things in different Bounded Contexts (e.g., "Account" in banking vs. accounting). Do not try to unify models across contexts -- explicitly define boundaries. Each Bounded Context should have its own Ubiquitous Language.

#### Continuous Integration (Ch 14)

Within a Bounded Context, all work on the model must be integrated frequently. A fragmented model within a single context is a contradiction. Use automated tests and frequent merges to keep the model consistent.

#### Context Map (Ch 14)

A global view of all Bounded Contexts and the relationships between them. The Context Map is a strategic tool -- it shows where translation is needed, where models diverge, and where integration is required. Relationships between contexts:

| Pattern                   | Relationship                                                                                             |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Shared Kernel**         | Two contexts share a subset of the model. Changes require coordination.                                  |
| **Customer/Supplier**     | Upstream context provides what downstream needs. Downstream has input on upstream priorities.            |
| **Conformist**            | Downstream adopts upstream's model as-is. No negotiation.                                                |
| **Anti-Corruption Layer** | Downstream builds a translation layer that maps the upstream model to its own. Protects model integrity. |
| **Separate Ways**         | No integration. Each context is independent.                                                             |
| **Open Host Service**     | Upstream defines a protocol for access. Multiple downstream consumers use it.                            |
| **Published Language**    | A well-documented shared language for interchange (e.g., XML schema, protocol buffers).                  |

#### Anti-Corruption Layer (Ch 14)

When integrating with external systems (especially legacy), build a translation layer. The ACL has three parts: a **Facade** (simplified interface to the external system), an **Adapter** (maps between protocols), and a **Translator** (maps between models). The domain model never directly references external system concepts.

#### Distillation (Ch 15)

Separate the Core Domain from supporting elements:

- **Core Domain**: The part of the model that is the reason the software exists. The most valuable, differentiating part. Invest design effort here.
- **Generic Subdomains**: Model elements that are necessary but not special to your application (e.g., money, time zones, organizational charts). Separate into their own modules. Consider off-the-shelf solutions or published models.
- **Domain Vision Statement**: A short document (~1 page) describing the Core Domain and its value. Focuses on what is distinctive, not on technology.
- **Highlighted Core**: Mark core elements explicitly in code or documentation so developers can distinguish core from supporting code at a glance.
- **Cohesive Mechanisms**: Separate computational frameworks from the expressive domain model. The model says "what"; the mechanism says "how."
- **Segregated Core**: Refactor to physically separate core concepts into their own modules, reducing coupling to supporting code.

#### Large-Scale Structure (Ch 16)

Optional patterns for organizing very large models:

- **Responsibility Layers**: Assign domain objects to conceptual layers based on domain responsibilities (e.g., Potential, Operations, Policy, Decision Support).
- **Knowledge Level**: Separate the model into an operational level (runtime instances) and a knowledge level (rules/types that constrain the operational level).
- **Evolving Order**: Let structure emerge and evolve -- do not impose it prematurely.

---

## Skill Review Process

2 rounds of self-review, checking SKILL.md against the source PDF and AI-agent operationalizability.

### Changes Made After Round 1

| Finding                                                                              | Source             | Action                                                                                              |
| ------------------------------------------------------------------------------------ | ------------------ | --------------------------------------------------------------------------------------------------- |
| Entity vs Value Object decision procedure too vague                                  | Quality            | Added concrete decision table with when/how                                                         |
| Missing Specification pattern                                                        | Fidelity           | Added to Making Implicit Concepts Explicit section                                                  |
| Aggregate rules not strict enough on reference rules                                 | Fidelity           | Strengthened: explicit "no references to non-root internals from outside"                           |
| Anti-Corruption Layer lacked structural guidance                                     | Quality            | Added Facade/Adapter/Translator triad from Ch 14                                                    |
| Supple Design patterns listed but not operationalized                                | Quality            | Converted each to imperative instruction with decision trigger                                      |
| Modules section mentioned "tell a story" without guidance                            | Quality            | Added concrete rule: name from domain, not technical layers                                         |
| Missing Closure of Operations                                                        | Fidelity           | Added with definition and examples                                                                  |
| Context Map relationship table incomplete                                            | Fidelity           | Added all 7 patterns from Ch 14                                                                     |
| Service definition too loose -- could be confused with application Service           | Fidelity + Quality | Added three-characteristic test from Evans                                                          |
| Core Domain vs Generic Subdomain decision not operationalized                        | Quality            | Added decision procedure: "if removing it makes your software generic, it is Core"                  |
| Large-scale structure patterns (Responsibility Layers, Knowledge Level) too detailed | Quality (scope)    | Reduced to brief mention -- solo dev unlikely to use these at scale                                 |
| Factory pattern mentioned but missing "reconstitution vs creation" distinction       | Fidelity           | Added Evans' distinction                                                                            |
| Entity section used Python-specific `__eq__`/`__hash__`                              | Quality (scope)    | Made language-agnostic: "Implement equality and hashing based on identity only"                     |
| "Get these rules right" motivational language in Aggregates header                   | Quality            | Replaced with factual: "Aggregates enforce consistency boundaries. These rules are non-negotiable:" |
| Making Implicit Concepts Explicit table columns misaligned                           | Quality (style)    | Realigned all table columns                                                                         |

### Declined Suggestions

| Suggestion                                              | Rationale for declining                                                                                     |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Add team organization patterns (Ch 14, 17)              | Solo dev context -- team topology patterns not actionable for user + AI agent                               |
| Include all Context Map relationship patterns in detail | Table sufficient; detailed strategies for each are organizational, not code-structural                      |
| Add Large-Scale Structure as full section               | Primarily useful for very large multi-team systems; solo dev gets most value from Modules + Bounded Context |
| Include Knowledge Level as primary pattern              | Advanced pattern for user-configurable rule systems; add if needed, but not default                         |
| Add Evolving Order as standalone principle              | Already implied by CLAUDE.md's iterative approach and simplicity-first guidelines                           |
| Duplicate Layered Architecture guidance                 | Already covered by Hexagonal Architecture in GOOS skill; reference rather than duplicate                    |

### Round 2 Verdict

Fresh review against the complete book confirmed convergence:

- **Fidelity**: All major patterns covered. Aggregate rules match Evans precisely. Value Object/Entity distinction faithful. Specification pattern included. No hallucinated concepts.
- **Quality**: Every section now contains decision procedures or concrete rules. No motivational text remains. Removed Large-Scale Structure details that are not actionable for solo dev + AI agent. The "when to use each building block" table is the highest-value section for an AI agent.
- **Verdict**: Ship it.
