# Karpathy's Autoresearch: Lessons for TAD

Analysis of [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — an autonomous ML research loop — and what patterns transfer to agentic strategy discovery.

Date: 2026-03-17

---

## What Autoresearch Is

An AI agent gets a GPT training script (`train.py`), modifies it freely, runs a 5-minute experiment on a single H100, checks if `val_bpb` (validation bits per byte) improved, keeps or discards the change, and repeats ~12x/hour overnight.

The key insight: **the constraints are the product, not the code.**

## Architecture (3 Files)

| File         | Role                  | Who modifies it       |
| ------------ | --------------------- | --------------------- |
| `prepare.py` | Data loading, eval    | Human only (frozen)   |
| `train.py`   | Model + training loop | Agent only (mutable)  |
| `program.md` | Agent instructions    | Human only (iterated) |

The separation is strict: `prepare.py` is infrastructure the agent cannot touch. `train.py` is the full experimentation surface. `program.md` is what Karpathy calls "research org code" — it encodes research methodology, not implementation.

## Key Design Decisions in Train.py

- **Fixed time budget:** Exactly 5 min wall-clock per experiment. Makes every result directly comparable regardless of what the agent changed.
- **Single scalar metric:** `val_bpb` — lower is better. No multi-objective, no dashboards. The agent checks one number.
- **Hyperparams as top-level constants, not CLI flags:** `DEPTH = 8`, `MATRIX_LR = 0.04`, etc. Makes the tunable surface visible at a glance and trivially editable by an agent.
- **Fast fail:** `if math.isnan(train_loss_f) or train_loss_f > 100: exit(1)`. Don't waste 5 minutes on a diverged run.
- **Simplicity:** Single GPU, single file, no distributed training, minimal dependencies. ~500 lines total for model + optimizer + training loop.

## Technical Details Worth Noting

- **Optimizer:** MuonAdamW — Muon (orthogonalized momentum) for 2D matrix params, AdamW for embeddings/scalars. Different LRs per parameter group.
- **Architecture tricks:** Value embeddings (ResFormer), sliding window attention pattern (`SSSL`), RMS norm, logit softcapping, per-layer residual scaling (`resid_lambdas`, `x0_lambdas`).
- **GC management:** Disables Python GC after step 0 to avoid ~500ms stalls. Runs manual GC every 5000 steps.
- **Warmup skip:** First 10 steps excluded from time budget (torch.compile compilation overhead).

## Lessons for TAD

### 1. Mutable Vs Immutable Boundary

TAD already has a dependency DAG enforcing module boundaries. The missing piece is making the "experimentation surface" explicit. For autonomous strategy discovery:

- **Frozen:** `load/`, `common/`, `features/`, `backtest/` engine, evaluation metrics
- **Mutable:** Strategy logic — signal construction, filters, thresholds, holding rules
- **Instructions:** A `research-program.md` encoding domain constraints

### 2. Fixed Evaluation Budget

Each strategy experiment should use a fixed date range, fixed universe, and deterministic backtest so results are directly comparable. The "budget" isn't compute time (backtests are fast) but standardized evaluation conditions.

### 3. Single Scalar Metric

Autoresearch optimizes exactly one number. For strategies, candidates:

- Risk-adjusted CAGR
- Modified Sharpe with drawdown penalty
- Some composite of hit rate + payoff ratio

**This is the hardest design decision.** Without a single scalar, autonomous iteration doesn't work. The metric must match the level you trade at (per CLAUDE.md: "don't use unconditional analysis as kill criterion for conditional strategies").

### 4. Keep/Discard Loop

```text
while True:
    modify strategy parameters/logic
    run backtest
    if metric_improved:
        keep changes
    else:
        revert
```

Plus fast-fail: abort backtests where drawdown exceeds threshold partway through.

### 5. Program.md — the Human-Iterable Agent Contract

A `research-program.md` for TAD would encode:

- What kinds of experiments to try (parameter sweeps, new signal combinations, different filters)
- What constitutes "interesting" vs "noise"
- Domain constraints (earnings exclusion, within-gate testing, etc.)
- Kill criteria and statistical significance thresholds

### 6. Hyperparams as Visible Constants

Surface strategy parameters as a single config block rather than scattered function defaults. Makes the tunable surface legible to both humans and agents.

### 7. What TAD Already Does Better

- **Decision log** (`decisions.md`) — autoresearch has no institutional memory
- **Dependency DAG** — proper module boundaries vs single-file
- **Backlog prioritization** — structured exploration roadmap

## Critical Assessment: Do You Need an LLM for This?

Asked provocatively: do you really need an LLM to run a loop over a parameter space and evaluate one fitness function?

### Where Classic Methods Win

For pure parameter optimization over a fixed search space, an LLM is dramatically overkill:

| Method                     | Strength                                           |
| -------------------------- | -------------------------------------------------- |
| Grid/random search         | Exhaustive, reproducible, trivially parallelizable |
| Bayesian optimization      | Sample-efficient, models the objective surface     |
| Evolutionary/genetic algos | Good at combinatorial spaces (filter on/off, etc.) |
| Monte Carlo tree search    | Explores branching strategy configurations         |

These are faster, cheaper, more reproducible, and mathematically principled about exploration vs exploitation. An LLM calling `exit(1)` on NaN loss is a laughably expensive replacement for `scipy.optimize`.

For TAD: sweeping z-score thresholds, volume ratio cutoffs, holding periods, filter combinations — that's a finite, well-structured parameter space. Bayesian optimization or random search would crush an LLM loop on cost-efficiency.

### Where the LLM Adds Something Different

The LLM isn't optimizing parameters — it's **modifying code**. The agent can:

1. **Change the architecture itself** — add a layer type, swap an activation, restructure the forward pass. Not a point in parameter space; changes the space itself.
2. **Combine ideas from the literature** — "value embeddings from ResFormer with sliding window attention." A Bayesian optimizer can't invent a new mechanism.
3. **Make structural leaps** — from "tune learning rate" to "use a different optimizer" to "change the loss function."

The search space isn't fixed and enumerable — it's the space of all valid Python programs. That's where classic methods genuinely can't compete.

### Task-Appropriate Tooling for TAD

| Task                                        | Best tool                      |
| ------------------------------------------- | ------------------------------ |
| Sweep filter thresholds (z < -2.0, etc.)    | Bayesian opt / random search   |
| Test signal combinations from a fixed set   | Combinatorial search / genetic |
| Find optimal holding period                 | Grid search                    |
| **Invent a new signal** from raw features   | LLM (or human)                 |
| **Reframe the strategy** (ranker → scanner) | LLM (or human)                 |
| **Encode domain knowledge** as constraints  | LLM (or human)                 |

### The Hybrid That Actually Makes Sense

Use the LLM to generate the search space, then use classic methods to explore it:

1. **LLM proposes** structural change: "add a momentum-regime filter" — writes the code
2. **Classic optimizer sweeps** the new parameters: lookback window, threshold, interaction with existing filters
3. **LLM evaluates** results: "regime filter helps 2020-2022 but hurts 2023 — probably overfitting to COVID recovery"
4. **LLM proposes** next structural change

This mirrors how a human quant researcher works — you don't grid-search your way to a new idea, but you also don't manually try 500 parameter combinations.

**Bottom line:** Autoresearch's loop is valuable when you've exhausted the obvious parameter space and need creative leaps. For everything structured and enumerable, use optuna/scipy/genetic algos and save the LLM budget for the parts that require reasoning.

## Minimum Viable "Autoresearch for Strategies"

1. Define the experimentation surface (single file/module with strategy params)
2. Define the scalar metric
3. Build eval harness: `run_experiment(config) -> float` — fast, deterministic
4. Write `research-program.md` with domain constraints
5. Build the keep/discard loop

## Source

- Repository: <https://github.com/karpathy/autoresearch>
- Key file: <https://github.com/karpathy/autoresearch/blob/master/train.py>
- Key file: `program.md` (agent instructions, not public at time of writing)
