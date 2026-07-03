# Repo Health Skill — Research Synthesis

Research conducted 2026-03-16 across 10 parallel streams to inform the design of a periodic holistic codebase health review skill. Each section synthesises findings from web research, book summaries, and practitioner frameworks, filtered for relevance to: solo dev, AI-agent-heavy workflow, Python/Polars quant codebase, CLAUDE.md as source of truth, tasks/ for work tracking.

---

## 1. Staff Engineer Holistic Review

Sources: Will Larson (*Staff Engineer*, lethain.com), Tanya Reilly (*The Staff Engineer's Path*), John Ousterhout (*A Philosophy of Software Design*), Adam Tornhill (*Your Code as a Crime Scene*), Google SRE/Engineering Practices, Atomic Object audit checklist.

### Mental Models

**Larson's Quality Ladder** — apply cheapest intervention first, escalate only when it fails:

| Level | Intervention             | Escalation trigger                          |
| ----- | ------------------------ | ------------------------------------------- |
| 1     | Fix hot spots            | Too many hot spots to cool individually     |
| 2     | Adopt best practices     | Want new practice before current one works  |
| 3     | Prioritize leverage pts  | Accessible leverage point impact exhausted  |
| 4     | Align technical vectors  | Teams pulling in incompatible directions    |
| 5     | Measure technical quality| Need data to justify deeper investment      |

Three most impactful leverage points: interfaces between systems, stateful systems, and data models.

Key insight: "At a well-run and successful company, most of your previous technical decisions won't meet your current quality threshold."

**Reilly's Three Maps:**

1. Locator map — where does this system sit in the broader picture?
2. Topological map — how do decisions actually get made?
3. Treasure map — where is this headed in 1-2 years?

Staff engineers use these to avoid reviewing code in isolation — every assessment is relative to where the system needs to go.

**Ousterhout's Complexity Lens:**

- Two root causes: dependencies, obscurity
- Three symptoms: change amplification, cognitive load, unknown unknowns
- 14 named red flags (shallow module, information leakage, temporal decomposition, pass-through method, etc.)

**Tornhill's Behavioural Code Analysis:**

- Hotspots = high complexity + high change frequency
- Priority = f(complexity, change_frequency, business_criticality)
- Change coupling reveals hidden architectural dependencies
- Don't audit uniformly — start where it hurts

### What Holistic Review Catches That per-PR Review Misses

| Dimension               | Per-PR sees                    | Holistic review sees                                  |
| ----------------------- | ------------------------------ | ----------------------------------------------------- |
| Architecture drift      | "This PR is internally clean"  | Components no longer match intended architecture      |
| Accidental coupling     | "These files changed together" | Files that always change together (change coupling)   |
| Complexity accumulation | "This function is complex"     | Which modules accumulated complexity over months      |
| Convention drift        | "This doesn't match style"     | Three patterns for the same thing across the codebase |
| Strategic vs incidental | "This is a TODO"               | Which debt blocks the next 6 months of planned work   |
| Dead/orphaned code      | Unused imports in this PR      | Entire modules nobody calls anymore                   |

### Frequency and Triggers

Most common: quarterly cadence. Also triggered by: pre-major-release, after team changes, when velocity drops, before rebuild decisions. Reilly: context gathering is continuous; formal review crystallises what you already sense.

### Artifacts

Technical vision docs, ADRs, quality scorecards, hotspot reports, findings documents. For a solo dev, a periodic findings report with trend tracking is the right weight.

---

## 2. Technical Debt Taxonomies

Sources: Cunningham (1992 OOPSLA), Fowler's Quadrant, SonarQube/SQALE, Alves et al. (2014, 13-type ontology), Kruchten's Landscape, CodeScene.

### Cunningham's Original Metaphor

The term was specifically about **knowledge debt** — code that no longer reflects what you've since learned about the domain. NOT about sloppy code. The "interest" is friction from working with code that doesn't match your current mental model.

### Fowler's Quadrant

Reckless/Prudent × Deliberate/Inadvertent. Tools detect reckless debt (code smells, complexity). Prudent debt (strategic design decisions, domain-model drift) is invisible to static analysis.

### Solo Dev Relevance

| Priority | Debt type          | Why it matters                             |
| -------- | ------------------ | ------------------------------------------ |
| 1        | Cognitive/design   | Future-you is a stranger to this code      |
| 2        | Test               | Only safety net — no reviewer, no QA       |
| 3        | Dependency         | Silent accumulation, security risk         |
| 4        | Architecture       | Hardest to fix later, constrains everything|
| 5        | Code               | Least harmful if isolated                  |
| 6        | Documentation      | Decision docs only — skip API docs         |

**Key insight for solo devs:** All debt types compound through cognitive load. Code-as-documentation (clear naming, obvious structure, explanatory tests) is the single highest-leverage investment.

### Interest Rate Model

Architecture debt compounds fastest (infects every module built on it). Dependency debt compounds through security exposure. Test debt compounds through undetected regressions. Code debt compounds linearly if isolated.

**Hotspot prioritisation (Tornhill):** priority = complexity × change frequency. Complex code nobody touches is inert. Complex code in the critical path is actively generating bugs.

---

## 3. Architecture Fitness Functions

Sources: Ford/Parsons/Kua (*Building Evolutionary Architectures*), ArchUnit, import-linter, PyTestArch, pytest-archon, Thoughtworks Technology Radar.

### Core Concept

Automated checks that verify architectural characteristics, not business logic. Broader than tests — include metrics, monitoring, static analysis, manual review. But the most practical ones are implemented as tests.

### Categories

- Atomic vs holistic (single characteristic vs combination)
- Triggered vs continuous vs temporal (event, always-on, trend-based)
- Static vs dynamic (code structure vs runtime behaviour)
- Automated vs manual
- Intentional vs emergent (upfront vs after a problem)

**Temporal fitness functions** are particularly powerful for preventing gradual drift: "complexity must not increase month-over-month."

### What Tad Already Has

`test_architecture.py` implements 6 fitness functions via custom AST analysis: dependency direction, no re-exports, cross-package import style, frozen/slotted dataclasses, finite filtering (.is_finite() not .is_not_null()), rolling min_samples enforcement.

### Governance

- Start with 3 fitness functions, not 30
- Add when real problems demand protection, not speculatively
- Exceptions must be explicit (inline `# noqa` comments)
- Review periodically: functions that never fail may be redundant
- "Three strikes" rule: if you flag the same issue in review 3 times, encode it as a rule

### Mechanical Vs Judgment

If you can express "X must/must-not Y" where both are structurally identifiable, automate it. If the rule requires understanding intent or context beyond the code, it needs judgment.

---

## 4. Documentation Health

Sources: Diátaxis/Procida, Nygard (ADRs), Swimm, Codified Context (arXiv:2602.20478), Anthropic CLAUDE.md guidance.

### Diátaxis Taxonomy Priority for Solo Dev + AI Agents

| Type        | Solo dev priority | AI agent priority | Decay rate              |
| ----------- | ----------------- | ----------------- | ----------------------- |
| Reference   | High              | Medium            | Slow (auto-generatable) |
| Explanation | High              | Highest           | Slowest                 |
| How-to      | Medium            | Medium            | Medium                  |
| Tutorial    | Low               | None              | Fastest                 |

### CLAUDE.md as Highest-Leverage Documentation

- Shapes every AI interaction — wrong instruction produces wrong code silently
- Should contain knowledge invisible to code reading (intent, constraints, conventions in developer's head)
- Should NOT duplicate what code reveals (API signatures, file descriptions)
- Keep under 300 lines; use @file references for depth
- Drifts when developer practices change, not when adjacent code changes

### Auditing CLAUDE.md Accuracy

Automated:

- Extract and run all commands mentioned
- Cross-reference file paths and identifiers against codebase
- Spot-check convention compliance in recent code

Periodic (AI-assisted):

- For each rule, find recent code that exercises it
- Check if recent commits routinely violate any stated convention
- Compare CLAUDE.md conventions against actual code patterns

### ADRs for AI-Heavy Codebases

Critical because AI-generated code loses decision context. Record: technology choices, architectural patterns, "why not" decisions, constraint-driven decisions. Not: implementation details, style choices.

---

## 5. Convention Drift Detection

Sources: Google (*Software Engineering at Google*), Meta (Fixit 2), NATURALIZE (Allamanis et al.), Jiang (*Beyond the Prompt*, 2025).

### How Drift Happens

1. Gradual erosion — each change "close enough", accumulates
2. Sudden breaks — new contributor (or AI session) introduces different pattern
3. Convention evolution without backfill — new way going forward, old not updated
4. Import-by-example — copy nearby file, inherit its patterns (good or bad)
5. AI "almost right" — 95% consistent, subtle differences accumulate

### AI-Specific Drift Patterns

| Pattern                      | Example                                     |
| ---------------------------- | ------------------------------------------- |
| Generic over domain-specific | `data` instead of `signal` or `factor`      |
| Over-documentation           | Docstrings on every function, even trivial  |
| Defensive over-engineering   | Try/except around code that can't fail      |
| Wrong abstraction level      | Class where a function suffices (Java-isms) |
| Synonym substitution         | Using wrong domain term in variable names   |

### Detection Heuristics (Actionable)

1. **Synonym grep** — pick core concept, grep for common synonyms
2. **Error handling census** — classify how errors are communicated per module
3. **Type representation audit** — find where same concept uses different types
4. **Test structure diff** — compare fixture patterns, assertion styles
5. **Convention coverage score** — for each CLAUDE.md rule, count comply vs violate
6. **Duplicate implementation scan** — similar functions across modules

### Enforcement Pipeline

```text
Formatter (hard gate) → ruff format, pre-commit
  ↓
Linter (hard gate) → ruff check, pyright, pre-commit + CI
  ↓
Architecture tests (CI) → test_architecture.py
  ↓
Convention file (AI gate) → CLAUDE.md
  ↓
Code review (human/AI) → design fit, domain correctness
```

---

## 6. Task/Backlog Hygiene

Sources: DEEP framework, PM/tech lead literature, Backlog.md, Microsoft issue-bankruptcy pattern.

### Healthy Backlog for Solo Dev

- 15-30 item cap — forces prioritisation
- Every item has a clear "why"
- Can start top item right now without asking questions
- No item untouched >2-3 months without conscious re-prioritisation
- Strict separation: backlog (committed work) vs parking lot (ideas)

### Automatable Checks for Tasks/ Directory

**Structural integrity:**

- Frontmatter parses, required fields present (title, date, status)
- Status is valid (draft/in-progress/done/rejected)
- Epic file exists if referenced; depends_on files exist
- Epic table matches actual subtask files and statuses

**Staleness:**

- Age >90 days AND status != done/rejected → warning
- status=in-progress AND no related commits in 14 days → warning
- Draft backlog bloat (>20 draft items) → info

**Reference integrity:**

- Backtick-quoted paths in task body resolve to existing files
- Dependency status coherence (in-progress but depends_on not done)
- Tasks referencing deleted/refactored code

**Alignment:**

- Orphan tasks (no milestone, no epic)
- Multiple in-progress (solo dev: >2 is a smell)
- All subtasks done but epic still in-progress

**Abandoned work cross-checks:**

- TODO/FIXME comments referencing task IDs
- Stale branches not merged to main (30+ days)

---

## 7. Dependency and Supply Chain Health

Sources: pip-audit, OSV, pip-abandoned, pip-licenses, PEP 740/Sigstore, Veracode, NEP 29.

### Automated Checks (For Uv-Based Project)

| Check                 | Tool/Method                                                      |
| --------------------- | ---------------------------------------------------------------- |
| Known CVEs            | `uv export --format requirements-txt \| pip-audit -r /dev/stdin` |
| Version staleness     | `uv pip list --outdated`; PyPI API for time lag                  |
| Abandoned packages    | `pip-abandoned`                                                  |
| License compliance    | `pip-licenses` with allow-list                                   |
| Environment integrity | `uv pip check`                                                   |
| Python version EOL    | Version comparison                                               |

### Human Judgment Needed

- Reachability assessment for CVEs
- "Should we switch from X to Y?" decisions
- Breaking change absorption timing
- "Done" vs "abandoned" distinction for upstream packages

---

## 8. Test Suite Health

Sources: Codecov, TestDino 2026 Benchmark, Codepipes anti-patterns, mutmut, Hypothesis, Polars testing docs.

### Beyond Coverage %

| Dimension         | Healthy threshold         | Agent-checkable? |
| ----------------- | ------------------------- | ---------------- |
| Speed             | Full suite < 60s          | Yes              |
| Slowest test      | < 2s                      | Yes              |
| Pyramid shape     | Unit:integration >= 3:1   | Yes              |
| Assertion-free    | 0 tests with 0 assertions | Yes              |
| Excessive mocking | < 3 mocks per test        | Yes              |
| Mutation score    | > 80% on core logic       | Yes (expensive)  |
| Flaky rate        | < 1%                      | Yes (run Nx)     |

### Anti-Patterns to Detect

1. Tests testing the framework, not the code
2. Tests coupled to implementation details (assert_called_with heavy)
3. Assertion-free tests ("no exception = pass")
4. Excessive mocking (>3 mocks per test)
5. Duplicate tests (>80% structural similarity)
6. Tautological assertions (assert True, assert x == x)
7. Ice cream cone (>40% E2E tests)

### Quant-Specific Testing

- Never use `==` for float comparison; use `pytest.approx`
- Test division with zero and near-zero divisors
- Test NaN propagation → should produce None, not NaN
- Test empty input, single element, all-nulls column
- Property-based testing (Hypothesis) for: monotonicity, null propagation, scale invariance, bounds, idempotency

---

## 9. AI-Generated Code Accumulation

Sources: CMU study (807 repos), GitClear (211M lines), DORA 2025, CodeRabbit, Veracode (100+ LLMs), vibe coding research.

### Established Findings (Multiple Independent Studies)

| Finding                          | Source   | Magnitude             |
| -------------------------------- | -------- | --------------------- |
| Code complexity increase         | CMU      | +25.1%                |
| Code duplication increase        | GitClear | 8x (5+ line blocks)   |
| Refactoring/reuse decline        | GitClear | -44%                  |
| Short-term churn (revised <2 wk) | GitClear | 3.1% → 5.7%           |
| Bug rate increase                | DORA     | +9%                   |
| Code review time increase        | DORA     | +91%                  |
| PR size increase                 | DORA     | +154%                 |
| Security vulnerabilities         | Veracode | 45% of tasks affected |

### Key Emerging Concepts

**Comprehension debt** — codebase exceeds developer's understanding. Most dangerous AI-induced debt because invisible until something breaks.

**The churn cycle** — AI slop creates problems fixed by more AI code, each round adding complexity.

**~3 month spaghetti point** — unconstrained AI-heavy development hits a complexity wall where new features break existing ones.

**Convention files as immune system** — CLAUDE.md rules are "antibodies" developed in response to bad patterns. The feedback loop (review findings → rule updates → better generation) is the key mechanism.

**DORA amplification principle** — AI amplifies existing engineering culture. Strong practices + AI = compounding gains. Weak practices + AI = compounding problems.

### What to Watch For

- Pattern consistency across sessions (not currently measured)
- Complexity trending over time
- Duplication trending over time
- Security review of AI-generated code
- Convention file staleness

---

## 10. Health Check Design

Sources: Google SRE Book, Rob Ewaschuk (alerting philosophy), PagerDuty/Datadog (alert fatigue), Google static analysis research, CodeScene vs SonarQube benchmarks, broken windows research (2024).

### Core Principles

**Codebase health is a report, never an alert.** The codebase doesn't catch fire — it degrades gradually. Weekly reports are the right channel.

**Finding cap: 3-5 per report.** A solo developer's actionable capacity per review cycle. More creates prioritisation paralysis. Put overflow in a separate "detailed" section.

**The "So what?" test.** Every finding must have a clear next action. If the answer is "nothing" or "I don't know", don't surface it.

**Severity scarcity.** Critical should be rare (0-2 per review). If everything is critical, nothing is. "Everything is medium" = no severity at all.

**Broken windows (empirical, 2024).** Existing debt increases propensity to introduce new debt. Early small findings >> late large catalogues.

### Report Structure (Inverted Pyramid)

1. One-line verdict — "3 findings, 1 high-severity" or "No new issues"
2. Top 3-5 things to fix — minimum viable action list
3. Trend summary — better/worse/stable since last report
4. Detailed findings — full context for each issue
5. Below threshold — things noticed but filtered out

### Cadence

| Check type               | Cadence        | Rationale                              |
| ------------------------ | -------------- | -------------------------------------- |
| Mechanical (lint, types) | Every commit   | Fast, deterministic, no noise risk     |
| Code review              | Per change     | Context-sensitive, tied to what changed|
| Codebase health report   | Weekly         | Enough time for findings to be acted on|
| Architecture review      | Monthly        | Structural changes are slow            |
| Trend analysis           | Monthly        | Need enough data points                |

### AI-Driven Health Check Advantages

- Context awareness — can evaluate whether complexity *matters*
- Natural language findings — can explain *why*, not just flag violations
- Cross-cutting concerns — can spot issues spanning multiple files
- Adaptive severity — calibrate based on domain and risk

### AI-Driven Health Check Risks

- Hallucinated findings (29-45% fabrication risk)
- Inconsistent severity across runs
- Verbose output (laundry list problem)
- Confident wrongness

### Mitigations

1. Confidence filtering (>80% threshold)
2. Mechanical validation — cross-check findings against actual code
3. Structured output schema (forced severity, required fields)
4. Scope constraints — limit review area
5. Finding cap — hard limit forces prioritisation
6. Deterministic anchors — mechanical checks as stable baseline

### What Existing Tools Get Wrong

SonarQube maintainability metrics: only 13.3% accuracy for actual maintainability issues. All snapshot-based tools share the same failure: can't tell whether complexity *matters* (is this code changed often? Is it on a critical path?). AI can evaluate this context — that's its structural advantage.

Why teams abandon quality tools: false positives erode trust, overwhelming first report, misaligned metrics (tools measure found, developers measure worth-fixing), no ownership of fixes.

---

## Context: Tad Codebase

### What Exists (Strengths to Build On)

- **test_architecture.py** — 6 AST-based fitness functions (dependency DAG, no re-exports, import style, frozen dataclasses, finite filtering, rolling min_samples)
- **CLAUDE.md** — well-crafted convention file with domain-specific quant gotchas
- **Daily code-review workflow** — per-commit AI review creating GitHub issues
- **tasks/ directory** — YAML frontmatter (title, date, status, milestone, epic, depends_on), epic/subtask structure
- **docs/decisions.md** — some decision recording
- **just check** — automated verification gate (test, lint, typecheck, format)
- **7-package layered architecture** — domain → common → {features, load} → recommend → backtest → cli

### What's Missing (The Gap Repo-Health Fills)

1. **Holistic periodic review** — stepping back from per-commit to whole-system
2. **Trend tracking** — is the codebase getting better or worse over time?
3. **Cross-cutting drift detection** — convention consistency across packages
4. **Task hygiene** — stale tasks, status lies, priority drift
5. **Dependency health** — CVEs, staleness, abandoned packages
6. **CLAUDE.md/test_architecture.py audit** — are constraints themselves valid?
7. **Comprehension debt awareness** — gap between code and understanding

---

## Sources

### Staff Engineer Walkthroughs

- [Larson: Managing Technical Quality](https://lethain.com/managing-technical-quality/)
- [Reilly: The Staff Engineer's Path](https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/)
- [Ousterhout: A Philosophy of Software Design](https://www.mattduck.com/2021-04-a-philosophy-of-software-design.html)
- [Atomic Object: Application Audit Checklist](https://spin.atomicobject.com/application-audit-checklist/)
- [Google: Code Health](https://testing.googleblog.com/2017/04/code-health-googles-internal-code.html)
- [Google: Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- [CodeScene: Code Biomarkers](https://codescene.com/blog/code-biomarkers/)
- [Spotify: Golden Paths](https://engineering.atspotify.com/2020/08/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem)

### Technical Debt

- [Cunningham: WyCash OOPSLA 1992](https://c2.com/doc/oopsla92.html)
- [Fowler: Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)
- [Kruchten: What Color is Your Backlog](https://www.infoq.com/news/2010/05/what-color-backlog/)
- [Alves et al.: Ontology of TD Terms (2014)](https://ieeexplore.ieee.org/document/6974882)
- [Identifying TD Types (2024)](https://arxiv.org/html/2408.09128v1)
- [SonarQube metrics docs](https://docs.sonarsource.com/sonarqube-server/2025.1/user-guide/code-metrics/metrics-definition)
- [Wouts: TD Interest Rate](https://fwouts.com/articles/tech-debt-interest-rate)
- [CodeScene: Prioritize TD by Impact](https://codescene.com/blog/prioritize-technical-debt-by-impact/)

### Architecture Fitness Functions

- [Ford et al.: Building Evolutionary Architectures](https://evolutionaryarchitecture.com/)
- [Thoughtworks: Fitness Function-Driven Development](https://www.thoughtworks.com/en-us/insights/articles/fitness-function-driven-development)
- [ArchUnit](https://www.archunit.org/)
- [import-linter](https://import-linter.readthedocs.io/en/stable/)
- [PyTestArch](https://pypi.org/project/PyTestArch/)
- [Hands-on Architects: Protecting Architecture with Tests in Python](https://handsonarchitects.com/blog/2026/protecting-architecture-with-automated-tests-in-python/)

### Documentation Health

- [Diátaxis framework](https://diataxis.fr/)
- [Nygard: Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Spotify: When to Write an ADR](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record)
- [Codified Context (arXiv:2602.20478)](https://arxiv.org/abs/2602.20478)
- [Anthropic: Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [Swimm documentation platform](https://swimm.io/)

### Convention Drift

- [Software Engineering at Google, Ch. 8](https://abseil.io/resources/swe-book/html/ch08.html)
- [Meta: Fixit 2](https://engineering.fb.com/2023/08/07/developer-tools/fixit-2-linter-meta/)
- [NATURALIZE (Allamanis et al.)](https://arxiv.org/abs/1402.4182)
- [Beyond the Prompt (Jiang, 2025)](https://arxiv.org/pdf/2512.18925)

### Task/Backlog Hygiene

- [Age of Product: 27 Backlog Anti-Patterns](https://age-of-product.com/28-product-backlog-anti-patterns/)
- [Atlassian: Backlog Grooming](https://www.atlassian.com/agile/project-management/backlog-grooming)
- [Microsoft: Issue Bankruptcy](https://github.com/microsoft/contributor-community-experiments/issues/2)

### Dependency Health

- [pip-audit](https://pypi.org/project/pip-audit/)
- [pip-abandoned](https://pypi.org/project/pip-abandoned/)
- [pip-licenses](https://pypi.org/project/pip-licenses/)
- [PEP 740: Digital Attestations](https://peps.python.org/pep-0740/)
- [uv-secure](https://pypi.org/project/uv-secure/)
- [Veracode GenAI Security Report](https://www.veracode.com/blog/genai-code-security-report/)

### Test Suite Health

- [Codecov: Beyond Coverage](https://about.codecov.io/blog/measuring-the-effectiveness-of-test-suites-beyond-code-coverage-metrics/)
- [TestDino Flaky Test Benchmark 2026](https://testdino.com/blog/flaky-test-benchmark/)
- [Inozemtseva & Holmes: Coverage vs Effectiveness](https://www.researchgate.net/publication/266656203)
- [Codepipes: Testing Anti-patterns](https://blog.codepipes.com/testing/software-testing-antipatterns.html)
- [mutmut](https://mutmut.readthedocs.io/en/latest/)
- [Polars Testing](https://docs.pola.rs/py-polars/html/reference/testing.html)

### AI Code Accumulation

- [CMU: Speed at the Cost of Quality](https://www.cs.cmu.edu/~ckaestne/pdf/msr26.pdf)
- [GitClear 2025 AI Code Quality Report](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
- [DORA 2025 Report](https://dora.dev/research/2025/dora-report/)
- [CodeRabbit: AI vs Human Code Generation](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)
- [Vibe Coding in Practice](https://arxiv.org/abs/2512.11922)
- [Agent READMEs Empirical Study](https://arxiv.org/html/2511.12884v1)

### Health Check Design

- [Google SRE: Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Ewaschuk: Alerting Philosophy](https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q/edit)
- [Datadog: Prevent Alert Fatigue](https://www.datadoghq.com/blog/best-practices-to-prevent-alert-fatigue/)
- [Google: Static Analysis Lessons](https://cacm.acm.org/research/lessons-from-building-static-analysis-tools-at-google/)
- [Broken Windows and TD (2024)](https://link.springer.com/article/10.1007/s10664-024-10456-6)
- [CodeScene: 6x Over SonarQube](https://codescene.com/blog/6x-improvement-over-sonarqube)
