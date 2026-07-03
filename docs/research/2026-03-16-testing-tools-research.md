# Testing & Code Quality Tools Research

**Date**: 2026-03-16 **Context**: Solo-dev quantitative Python codebase (Polars, 7-package monorepo, ~145 tests, Python 3.14)

---

## Executive Summary

Twelve parallel research agents investigated six named tools plus related alternatives, explored the codebase's test structure and quant patterns, and ran hands-on spikes with Hypothesis and mutation testing (mutmut/cosmic-ray) in isolated worktrees.

### Verdict at a Glance

| Tool                   | Type                      | Verdict        | Rationale                                                                                     |
| :--------------------- | :------------------------ | :------------- | :-------------------------------------------------------------------------------------------- |
| **Hypothesis**         | Property-based testing    | **Adopt**      | High-value for quant math, null/NaN edge cases, and order executor logic. 2.66s for 21 tests. |
| **pytest-cov**         | Branch coverage           | **Adopt**      | Near-zero overhead, catches untested conditional paths. Add `branch = true`.                  |
| **pytest-randomly**    | Test order randomisation  | **Adopt**      | Zero config, catches hidden test coupling. Solo devs have no reviewer to spot these.          |
| **mutmut**             | Mutation testing          | **Skip**       | Broken on Python 3.14 (segfaults). cosmic-ray works but signal-to-noise is poor.              |
| **Codecov**            | Coverage reporting SaaS   | **Skip**       | No PRs workflow, free tier too limited. `pytest-cov` locally covers the need.                 |
| **TestDino 2026**      | Playwright SaaS reporting | **Irrelevant** | Playwright-only product with marketing blog posts. Not a benchmark methodology.               |
| **Codepipes**          | Educational blog          | **Reference**  | Kostis Kapelonis's testing anti-patterns checklist. Not a tool — a useful read.               |
| **Polars parametric**  | DataFrame PBT strategies  | **Adopt**      | Ships with Polars, generates edge-case DataFrames (nulls, NaN, inf) for free.                 |
| **pytest-benchmark**   | Performance regression    | **Consider**   | Worth it for 3-5 hot-path functions. Run separately from coverage.                            |
| **pandera / Patito**   | Schema validation         | **Skip**       | Polars support is immature. Architecture tests already enforce schema invariants.             |
| **Great Expectations** | Data quality platform     | **Skip**       | No Polars support, massive enterprise overhead.                                               |
| **pytest-xdist**       | Parallel test execution   | **Skip**       | Test suite runs in seconds. Not justified until it exceeds 2-3 minutes.                       |

---

## Tool Deep Dives

### 1. Hypothesis — Property-Based Testing

**What it does**: Instead of writing examples by hand, you declare *properties* that should hold for all valid inputs. Hypothesis generates hundreds of random inputs and tries to falsify those properties. When it finds a failure, it *shrinks* the input to the simplest possible reproduction.

**How it works**:

- `@given(st.integers())` — decorator that generates inputs from *strategies*
- Four phases: explicit examples → replay saved failures → generate new → shrink failures
- Persistent database (`.hypothesis/`) caches failing examples across runs
- Profiles: `max_examples=10` locally, `max_examples=500` on CI

**Spike results** (21 tests, 2.66 seconds):

| Target                      | Value | Finding                                                                             |
| :-------------------------- | :---- | :---------------------------------------------------------------------------------- |
| `compute_compounded_return` | High  | Tested associativity, bounds, empty identity, cross-check vs equity curve           |
| `compute_max_drawdown`      | High  | Tested monotonic-gains-→-zero, bounds [0,1], peak tracking                          |
| `Trade` dataclass           | Med   | Validation boundaries well-covered already; adds density                            |
| `compute_return` (Polars)   | Med   | Structural properties (null padding, row count); slower due to DataFrame overhead   |
| `DailyBar` validation       | Bonus | Immediately caught `make_bar(close=X)` with default `high=100.0` breaking for X>100 |

**Highest-value targets not yet spiked**: `order_executor.try_execute()` (complex branching with stop/target/gap fills), `bucketed_opportunity` (ranking edge cases).

**Setup cost**: ~30 minutes. Add `hypothesis` to dev deps, `.hypothesis/` to `.gitignore`, profile config in `conftest.py`.

**Runtime cost**: Negligible with profile pattern (10 examples locally → ~100-200ms per property test).

**Key insight**: The spike found no production bugs — the code is well-implemented. But it *immediately* caught an implicit assumption in the test helper (`make_bar` high vs close). This is exactly the class of bug that surfaces later as a false-positive test failure and wastes debugging time.

### 2. Polars Testing (`polars.testing` + `polars.testing.parametric`)

**What it does**: Assertion utilities (`assert_frame_equal`, `assert_series_equal`) and Hypothesis strategies for generating random DataFrames.

**Key utilities**:

- `assert_frame_equal(left, right, check_exact=False, rel_tol=1e-5)` — float tolerance comparison
- `check_row_order=False` — for non-deterministic operations (joins, group_by)
- `polars.testing.parametric.dataframes([column("x", dtype=pl.Float64)])` — generates edge-case DataFrames

**Critical distinction for this codebase**: `null ≠ NaN` in Polars.

- `null` = missing data (any dtype). `fill_null()` fills these.
- `NaN` = IEEE 754 float value. `fill_nan()` fills these.
- The codebase correctly uses `is_finite()` (catches both NaN and inf) — enforced by architecture tests.

**Relevance**: The codebase already uses factory functions (`make_bar`, `make_ohlcv`) extensively. Polars parametric strategies complement these for edge-case generation — particularly null/NaN/inf injection that hand-written factories don't cover.

### 3. Mutmut / Mutation Testing

**What it does**: Systematically introduces small code changes (swap `+` to `-`, `>` to `>=`, etc.) and checks if tests catch them. Survived mutants = blind spots in your test suite.

**Spike results** (cosmic-ray, since mutmut is broken on Python 3.14):

| Module                  | Mutants | Killed | Survived | Kill Rate | Time | Verdict                                         |
| :---------------------- | ------: | -----: | -------: | --------: | ---: | :---------------------------------------------- |
| `trading_calendar.py`   |     281 |    173 |      108 |     61.6% |  77s | 106/108 survivors are holiday date data — noise |
| `trade.py`              |      51 |     45 |        6 |     88.2% |  34s | 2 minor gaps (no immutability test, no 0<p<1)   |

**Why mutmut specifically fails**: Python 3.14 changed internal frame handling. mutmut v3's trampoline mechanism (which uses `sys._getframe()`) segfaults on all mutants. mutmut v2's `pony` ORM dependency can't `deepcopy` on 3.14.

**Signal-to-noise problem**: For data-heavy modules (static holiday lists, config constants), mutation testing generates hundreds of mutants on literal values that survive because — correctly — nobody writes a test for every individual date in a frozenset. The 2 genuine findings in `trade.py` were low-severity.

**Bottom line**: The tool's value proposition (finding missing boundary tests) is real but the overhead — per-module config, slow runtime, high noise ratio, Python 3.14 incompatibility — makes it a poor fit for this codebase *right now*. Revisit if mutmut fixes Python 3.14 support and the test suite grows.

### 4. Codecov

**What it does**: SaaS that ingests coverage reports from CI, posts PR comments with coverage diffs, and tracks trends over time.

**Why skip**: This codebase doesn't use PRs (solo dev, pushes directly). The core value prop — "coverage diff on PR review" — doesn't apply. The free tier (250 uploads/month) lacks the interesting features (flags, components, carryforward). Adding a third-party service means another token to manage and another CI failure point.

**Alternative**: `pytest --cov --cov-report=term-missing` in `just check` gives the same information with zero external dependencies.

### 5. Codepipes Testing Anti-Patterns

**What it is**: A widely-cited blog post by Kostis Kapelonis (developer advocate at Codefresh/Octopus Deploy) enumerating 13 testing anti-patterns.

**Most relevant anti-patterns for this codebase**:

| #    | Anti-Pattern                            | Applicability                                                                        |
| :--- | :-------------------------------------- | :----------------------------------------------------------------------------------- |
| 4    | Testing the wrong functionality         | Focus tests on quant logic (silent corruption), not trivial getters                  |
| 5    | Testing internal implementation         | Test behavior, not structure — already followed via factory+fake pattern             |
| 6    | Excessive attention to coverage metrics | Coverage is a lagging indicator. Mutation score and PBT coverage are better signals. |
| 10   | Not converting production bugs to tests | Every silent-corruption bug should become a regression test with `@example`          |

**Alternative metrics proposed** (vs coverage %):

- **PBCNT** — % of bugs that create new tests
- **PTVB** — % of tests that verify behavior (vs implementation details)
- **PTD** — % of tests that are deterministic (non-flaky)

### 6. TestDino 2026 Benchmark

**What it actually is**: TestDino is a Playwright-focused SaaS test reporting and analytics platform. The "2026 Benchmark" refers to marketing blog posts comparing Playwright/Cypress/Selenium performance and flaky test rates. It is not a benchmark methodology or tool you can adopt.

**Relevance**: None. This codebase has no browser tests.

### 7. Pytest-Cov (Branch Coverage)

**What it does**: pytest plugin wrapping `coverage.py`. Adds `--cov` flag to pytest to measure which lines and branches are executed during tests.

**Why adopt**: Branch coverage (`branch = true`) catches untested conditional paths — exactly where quant bugs hide (zero divisors, empty frames, all-null columns). The codebase has no coverage tracking currently.

**Setup** (add to `pyproject.toml`):

```toml
[tool.coverage.run]
branch = true
source = ["backtest", "cli", "common", "domain", "features", "load", "recommend"]

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = ["pragma: no cover", "if TYPE_CHECKING:"]
```

**Cost**: Near-zero. One dev dependency, one config block. Adds ~1-2 seconds to test runs.

### 8. Pytest-Randomly

**What it does**: Randomises test execution order on every run. Prints the random seed so failures are reproducible.

**Why adopt**: Catches hidden test coupling (shared state, import-time side effects, fixture ordering assumptions). Solo devs are especially vulnerable because there's no reviewer to notice "this test only passes after that other test."

**Cost**: Zero config. `pip install pytest-randomly` and it activates automatically. Seed is printed in pytest header.

---

## Codebase Analysis: Where Tools Add Most Value

### Silent-Corruption Risk Map

The Polars/quant patterns agent identified these risk areas:

| Risk                         | Severity | Current Guard         | Tool That Helps    |
| :--------------------------- | :------- | :-------------------- | :----------------- |
| Lagged close = 0 → INF       | High     | None (relies on data) | Hypothesis         |
| Zero volatility in division  | Medium   | `when(vol > 0)` ✓     | Already guarded    |
| NaN/Inf propagation          | High     | `is_finite()` ✓       | Architecture tests |
| Empty window edge cases      | Medium   | `.clip()` ✓           | Hypothesis         |
| Cross-sectional ranking ties | Medium   | `rank(ordinal)` ✓     | Hypothesis         |
| Forward date overflow        | Medium   | `is_finite()` filter  | Hypothesis         |
| Division by peak in drawdown | Medium   | Logic (peak ≥ 1.0)    | Hypothesis         |

### Best Hypothesis Targets (By ROI)

1. **`backtest.analysis.metrics`** — Pure math with clear invariants (compounding associativity, drawdown bounds). Highest ROI.
2. **`backtest.order_executor`** — Complex branching (gap stop → gap target → intraday stop → profit → close). State-machine-like logic.
3. **`backtest.analysis.bucketed_opportunity`** — Ranking edge cases, sparse data handling, tied values.
4. **`recommend.strategies.reversal`** — Filter chain with volume ratios, dispersion gate, earnings window.
5. **`features.returns`** — Structural properties (null padding count = period, row count preservation).

### Current Test Suite Gaps

- **No coverage tracking** — unknown which branches are untested
- **No property-based testing** — edge cases depend entirely on developer imagination
- **No test order randomisation** — hidden coupling could exist undetected
- **Architecture tests are strong** — `is_finite()` enforcement, `min_samples` checks, dependency DAG validation

---

## Recommended Adoption Path

### Phase 1: Zero-Effort Wins (30 Minutes)

1. Add `pytest-cov` and `pytest-randomly` to dev dependencies
2. Add `[tool.coverage.run]` config to `pyproject.toml`
3. Update `just test` to include `--cov --cov-report=term-missing`
4. Add `.hypothesis/` to `.gitignore`

### Phase 2: Hypothesis on Critical Paths (2-3 Hours)

1. Add `hypothesis` to dev dependencies
2. Add profile config to `conftest.py` (10 examples dev, 500 CI)
3. Write property tests for `metrics.py` (compounded return, max drawdown)
4. Write property tests for `order_executor.py` (exit always occurs, price matches condition)
5. Write property tests for `bucketed_opportunity.py` (bucket count invariants, sparse handling)

### Phase 3: Polars Parametric Testing (1-2 Hours)

1. Write strategies for core domain objects (OHLCV bars, feature frames)
2. Test null/NaN/inf injection through `compute_return`, `ReversalSignal.compute`
3. Verify `is_finite()` filters actually catch all edge cases end-to-end

### Not Now

- **Mutation testing**: Revisit when mutmut supports Python 3.14 and test suite is larger
- **Codecov**: Revisit if the project ever adopts a PR-based workflow
- **pytest-benchmark**: Add when performance regression becomes a concern
- **Schema validation (pandera/Patito)**: Architecture tests already fill this role

---

## Cost-Benefit Summary for a Solo Dev

| Investment              | Time     | Bugs Caught                                             | Maintenance |
| :---------------------- | :------- | :------------------------------------------------------ | :---------- |
| pytest-cov + randomly   | 30 min   | Hidden coupling, untested branches                      | Zero        |
| Hypothesis (core)       | 2-3 hrs  | Numerical edge cases, boundary conditions, NaN/null     | Low         |
| Polars parametric       | 1-2 hrs  | DataFrame edge cases (empty, all-null, inf)             | Low         |
| mutmut                  | N/A      | Blocked by Python 3.14 incompatibility                  | —           |
| Codecov                 | 30 min   | Nothing pytest-cov doesn't already catch                | Token mgmt  |
| Full mutation CI        | 2-4 hrs  | ~2 minor gaps per module (high noise)                   | Config/run  |

**The 80/20**: `pytest-cov` + `pytest-randomly` + Hypothesis on the 5 critical modules gives ~80% of the value for ~20% of the effort. Everything else is either blocked (mutmut), irrelevant (TestDino), or overhead that doesn't justify itself for a solo developer (Codecov, schema validation frameworks, parallel test execution).

---

## Sources

- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Polars Testing API](https://docs.pola.rs/py-polars/html/reference/testing.html)
- [mutmut GitHub](https://github.com/boxed/mutmut)
- [cosmic-ray GitHub](https://github.com/sixty-north/cosmic-ray)
- [Codecov Documentation](https://docs.codecov.com/)
- [Codepipes Testing Anti-Patterns](https://blog.codepipes.com/testing/software-testing-antipatterns.html)
- [TestDino](https://testdino.com/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-randomly](https://github.com/pytest-dev/pytest-randomly)
