# Architecture Testing Tools for Python

Research conducted 2026-03-16 via twelve parallel agents covering: ArchUnit (Java, foundational), import-linter, PyTestArch, pytest-archon, related tools (tach, grimp, pydeps, ruff TID rules), solo-dev ROI analysis, codebase architecture exploration, import graph mapping, and three hands-on spike experiments (import-linter, pytest-archon, PyTestArch) run in isolated git worktrees against the tad codebase.

Findings validated that the existing custom `test_architecture.py` (320 LOC, stdlib-only) is the right approach for this codebase. One tool (import-linter) could complement the existing tests for declarative dependency contracts, but the marginal benefit is small.

---

## 1. What Architecture Testing Tools Do

Architecture testing tools enforce structural rules — dependency directions, layer boundaries, import constraints — via automated checks. They are essentially "unit tests for your architecture," catching violations before they become entrenched.

The tools operate at the **import/dependency graph** level. They parse source (AST) or bytecode to build a graph of module dependencies, then evaluate rules against that graph. Violations fail the test/check with a message identifying the offending import.

**ArchUnit** (Java, TNG Technology Consulting) is the progenitor. It analyses compiled bytecode, provides a fluent DSL for rules, and supports layers, slices, cycle detection, freezing (baseline existing violations), and architecture metrics. All Python tools in this space are inspired by it.

## 2. Tool Comparison

### The Four Requested Tools

| Dimension              | import-linter                                                | pytest-archon                                     | PyTestArch                                 | ArchUnit (Java)                                      |
| :--------------------- | :----------------------------------------------------------- | :------------------------------------------------ | :----------------------------------------- | :--------------------------------------------------- |
| **Approach**           | Declarative config (TOML/INI)                                | Python test code (fluent API)                     | Python test code (fluent API)              | Java test code (fluent DSL)                          |
| **Rule types**         | Layers, independence, forbidden, protected, acyclic siblings | Forbidden, required, may-import, custom predicate | Module deps, layer deps, PlantUML diagrams | Layers, slices, cycles, annotations, naming, metrics |
| **Transitive checks**  | Yes (via grimp graph)                                        | Yes (default on)                                  | Yes (via NetworkX)                         | Yes (bytecode-level)                                 |
| **TYPE_CHECKING skip** | Yes (`exclude_type_checking_imports`)                        | Yes (`skip_type_checking`)                        | Not documented                             | N/A (Java)                                           |
| **Custom rules**       | Custom contract types                                        | `.should()` predicate                             | No                                         | Custom predicates/conditions                         |
| **Error quality**      | Module + import chain                                        | Module + glob pattern (no file:line)              | Cryptic NetworkX exceptions                | Detailed violation messages                          |
| **Speed (tad)**        | 0.13s                                                        | 0.13s                                             | Could not complete (layout incompatible)   | N/A                                                  |
| **GitHub stars**       | 972                                                          | 78                                                | 152                                        | 6,200+                                               |
| **Maturity**           | Production (v2.11, Mar 2026)                                 | Pre-1.0 (v0.0.7, Sep 2025)                        | v4.0.1 (Aug 2025)                          | v1.4.1, highly mature                                |
| **Maintenance**        | Active (David Seddon, Kraken Tech)                           | Low-activity but stable                           | Active (single maintainer)                 | Very active (TNG)                                    |

### Additional Tools Discovered

| Tool            | What it does                                                                 | Relevance                                     |
| :-------------- | :--------------------------------------------------------------------------- | :-------------------------------------------- |
| **tach**        | Rust-powered modular boundary enforcement, interface checking, visualization | Strong contender — fast, active, opinionated  |
| **grimp**       | Queryable import graph (powers import-linter)                                | Infrastructure, not standalone                |
| **pydeps**      | Dependency graph visualization (SVG/PNG)                                     | Visualization only, no enforcement            |
| **Ruff TID251** | `banned-api` rules banning specific imports                                  | Already in use in tad for test-import fencing |

## 3. Spike Results

### Import-Linter: Works Well, Found a Real Issue

- **Setup**: `uv pip install import-linter` + TOML config — 5 minutes
- **Runtime**: 0.13s for 79 files / 184 dependencies
- **Finding**: Production architecture is clean. `common.testing.fakes` imports `backtest` and `common.testing.factories` imports `features` — lower-layer test helpers reaching up into higher layers. This is a genuine coupling issue (test utilities can't be used without installing higher-layer packages).
- **Signal quality**: High. Zero false positives in production-only mode.
- **Verdict**: The best tool of the four for this codebase.

### Pytest-Archon: Works, but More Verbose Than Existing Tests

- **Setup**: `uv pip install pytest-archon` + test file — 10 minutes
- **Runtime**: 0.13s for 8 rules
- **API**: Fluent builder reads well: `.match().should_not_import().check()`. `skip_type_checking` and `only_direct_imports` flags are practical.
- **Limitation**: No layer abstraction — the DAG must be manually decomposed into per-package `should_not_import` rules. The existing AST test encodes the full DAG in one dict and validates all packages in a single test. Result: 6 tests (70 lines) vs 1 test (25 lines) for the same coverage.
- **Limitation**: No file:line in error messages.
- **Limitation**: Cannot express non-import rules (frozen dataclasses, `is_finite()`, rolling `min_samples`).
- **Verdict**: Well-designed but adds limited value over existing tests.

### PyTestArch: Incompatible with Flat Workspace Layout

- **Setup**: `uv pip install pytestarch` — 2 minutes install, 45 minutes fighting the API
- **Core problem**: `get_evaluable_architecture(root, module)` assumes a single-root package hierarchy (`src/myapp/`). The tad flat uv workspace (sibling top-level packages) creates an irreconcilable naming mismatch — cross-package imports are invisible to the tool.
- **API ergonomics**: Fluent builder looks nice, but error messages are raw `NetworkXError` exceptions with no helpful context.
- **Verdict**: **Hard disqualifier.** Does not work with flat workspace layouts.

## 4. What Tad Already Has

The existing `test_architecture.py` (320 LOC, stdlib `ast` only) enforces six rule categories:

| Rule                       | What it checks                                                | Expressible by tools?                        |
| :------------------------- | :------------------------------------------------------------ | :------------------------------------------- |
| No re-exports              | `__init__.py` must not import from other first-party packages | Partially (import-linter forbidden contract) |
| Dependency direction       | Full DAG in one dict — lower layers cannot import higher      | Yes (all tools)                              |
| Cross-package import style | `from common import X` not `from common.repos import X`       | No                                           |
| Frozen/slotted dataclasses | All `@dataclass` must have `frozen=True, slots=True`          | No (import-only tools)                       |
| Finite filtering           | `.is_not_null()` forbidden in quant code (use `.is_finite()`) | No (import-only tools)                       |
| Rolling min_samples        | Rolling-window calls must specify `min_samples=`              | No (import-only tools)                       |

Three of six rules (50%) are **domain-specific AST checks** that no import-based tool can express. The dependency direction rule — the one these tools are best at — is already handled in 25 lines via a single dict + AST walk.

## 5. Cost/Benefit Analysis for a Solo Dev

### The Cost Side

| Cost               | Assessment                                                                                |
| :----------------- | :---------------------------------------------------------------------------------------- |
| Setup time         | Low (5-15 min for import-linter/pytest-archon)                                            |
| Runtime overhead   | Negligible (0.13s)                                                                        |
| New dependency     | One more package to maintain/update                                                       |
| Maintenance burden | Rules update when packages are added/restructured                                         |
| Learning curve     | Minimal for Python tools                                                                  |
| Dual maintenance   | Would need both the tool AND custom AST tests (tools can't express 50% of existing rules) |

### The Value Side

| Benefit                      | Assessment                                                      |
| :--------------------------- | :-------------------------------------------------------------- |
| Prevent drift                | Already handled by existing `test_architecture.py`              |
| Document intent              | Already documented via the `ALLOWED_DEPS` dict and docstrings   |
| Catch accidental coupling    | Already caught — the existing tests run in `just check`         |
| Transitive dependency checks | Not currently tested — the one genuine gap                      |
| AI agent guardrails          | Already enforced — AI agents run `just check` before committing |
| Declarative readability      | import-linter config is arguably more readable than AST code    |

### The Key Question: Does the Tool Replace or Supplement?

None of the tools can **replace** the existing `test_architecture.py` because they cannot express domain-specific rules (frozen dataclasses, `is_finite()`, `min_samples`). They can only **supplement** it for the import-direction subset.

For the import-direction rules specifically:

- Existing approach: 25 lines, one dict, zero dependencies, file:line errors
- import-linter: ~20 lines of TOML, one dependency, module-level errors
- pytest-archon: ~70 lines of test code, one dependency, module-level errors

The existing approach is already concise and produces better diagnostics.

### Transitive Dependency Checking — the Gap

The existing tests check **direct** imports only. A transitive violation (A imports B imports C, where A should not depend on C) would not be caught. Both import-linter and pytest-archon check transitively by default.

However: the tad dependency graph has zero circular dependencies and clean layered architecture (confirmed by the import graph analysis). Transitive violations through the existing packages are structurally impossible given the DAG — if A may import B and B may import C, then A transitively depends on C only through packages it's already allowed to depend on.

The one exception: the `common.testing` upward dependency (test helpers importing `backtest`/`features`) creates transitive chains through test code. This was found by the import-linter spike, but the existing tests already exclude `testing/` directories.

## 6. Recommendation

**Do not adopt any of these tools.** The existing `test_architecture.py` is the right approach for tad:

1. **It already works.** Zero dependencies, 320 LOC, 0.50s runtime, runs in `just check` before every commit.
2. **It's more expressive.** 50% of its rules (domain-specific AST checks) cannot be expressed by import-based tools.
3. **It's more concise** for the dependency DAG (25 lines vs 70+ with pytest-archon).
4. **It produces better errors** (file:line vs module-name).
5. **Dual maintenance is worse** than single-source-of-truth.

### One Actionable Finding

The import-linter spike revealed that `common.testing.fakes` imports `backtest` and `common.testing.factories` imports `features`. This is a genuine layering violation in test utilities — lower-layer test helpers depend on higher-layer packages. This should be investigated separately (move the fakes/factories to the packages that need them, or accept the coupling as intentional for test convenience).

### When to Reconsider

- **Codebase grows to 20+ packages** — the DAG dict approach may become unwieldy
- **Team grows beyond solo dev** — declarative config is easier for new contributors to understand than custom AST code
- **tach matures** — its Rust speed, interface enforcement (not just imports), and visualization make it the most promising tool in this space; worth re-evaluating in 6-12 months

## Sources

### Tool Documentation

- [ArchUnit Official Docs](https://www.archunit.org/userguide/html/000_Index.html)
- [import-linter Docs](https://import-linter.readthedocs.io/)
- [import-linter GitHub](https://github.com/seddonym/import-linter) — 972 stars, v2.11
- [PyTestArch GitHub](https://github.com/zyskarch/pytestarch) — 152 stars, v4.0.1
- [pytest-archon GitHub](https://github.com/jwbargsten/pytest-archon) — 78 stars, v0.0.7
- [tach GitHub](https://github.com/gauge-sh/tach) — Rust-powered, v0.34.0

### Architecture Testing Rationale

- [Sonar: The Architecture Gap](https://www.sonarsource.com/blog/the-architecture-gap-why-your-code-becomes-hard-to-change/)
- [Hands-on Architects: Protecting Architecture with Tests in Python](https://handsonarchitects.com/blog/2026/protecting-architecture-with-automated-tests-in-python/)
- [How to Tame Your Python Codebase (pytest-archon author)](https://bargsten.org/wissen/how-to-tame-your-python-codebase/)
- [6 Ways to Improve Architecture with import-linter](https://www.piglei.com/articles/en-6-ways-to-improve-the-arch-of-you-py-project/)
- [Scott Logic: Unit Test Your Architecture with ArchUnit](https://blog.scottlogic.com/2019/12/05/unit-test-your-architecture-with-archunit.html)
