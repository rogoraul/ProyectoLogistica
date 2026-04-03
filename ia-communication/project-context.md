# Project Context — Logística Basada en Datos

> This document is written for an AI reader. It provides full technical context about the project so any AI assistant can contribute meaningfully without needing to re-explore the codebase from scratch.

---

## Problem: Maximum Diversity Problem (MDP)

Given:
- A set of `n` elements
- A symmetric distance matrix `d[i][j]` for all pairs `(i, j)`
- An integer `p < n`

Find: A subset `S` of size exactly `p` that **maximizes** the total pairwise distance:

```
maximize  sum( d[i][j]  for all i,j in S, i < j )
```

This is NP-hard. The project implements **metaheuristic approximations**.

**Application context**: Logistics — selecting `p` locations from `n` candidates to maximize geographic spread (coverage), or selecting a maximally diverse portfolio of items.

---

## Project Structure

```
Proyecto_Logistica/
├── main.py                      # Demo entry point
├── structure/
│   ├── instance.py              # Reads .txt instance files into distance matrix
│   └── solution.py              # Solution class: set of selected nodes + objective value
├── algorithms/
│   ├── grasp.py                 # GRASP + Best-Improvement LS (iteration-limited)
│   ├── grasp_timed.py           # GRASP + Best-Improvement LS (time-limited)
│   └── grasp_ts.py              # GRASP + Tabu Search (time-limited, global clock)
├── constructives/
│   └── cgrasp.py                # Greedy-randomized construction phase
├── localsearch/
│   ├── lsbestimp.py             # Best-improvement local search (swap moves)
│   └── tabu_search.py           # Tabu Search with configurable tenure
├── instances/
│   └── MDG-a_*.txt              # Problem instances (MDG format)
├── experiments/
│   ├── calibration.py           # Calibrates tabu tenure parameter
│   └── comparison.py            # Benchmarks algorithm variants
└── transcripts/                 # Course lecture notes (French/Spanish)
```

---

## Instance Format (MDG)

```
n p
u1 v1 d1
u2 v2 d2
...
```

- `n`: total number of nodes
- `p`: number of nodes to select
- Each subsequent line: edge `(u, v)` with distance `d` (1-indexed, upper triangle only)

Example filenames:
- `MDG-a_1_100_m10.txt` → instance 1, n=100, p=10 (small)
- `MDG-a_1_500_m50.txt` → instance 1, n=500, p=50 (large)

There are 10 instances of each size category.

---

## Key Algorithms

### GRASP (Greedy Randomized Adaptive Search Procedure)

Iterative two-phase metaheuristic:
1. **Construction** (`constructives/cgrasp.py`): Builds a feasible solution using a restricted candidate list (RCL). The `alpha` parameter controls greediness (0 = fully greedy, 1 = random, -1 = random alpha each iteration).
2. **Local Search**: Improves the solution via swaps (replace one selected node with one unselected node).

Repeats until time or iteration limit. Keeps track of best solution found.

### Best-Improvement Local Search (`localsearch/lsbestimp.py`)

Evaluates **all** possible swap pairs `(v_out, v_in)` — every selected node against every
unselected node — and applies the pair with the highest gain delta. Repeats until no
improving swap exists. True O(p × (n−p)) per iteration.

### Tabu Search (`localsearch/tabu_search.py`)

Enhanced local search:
- Maintains a **tabu list**: recently removed nodes are forbidden from re-entering for `tenure` iterations
- **Aspiration criterion** (implemented): a tabu move is accepted if `sol['of'] + delta > best_of` — i.e., if it would produce a new global best, the tabu restriction is overridden
- Configurable `tenure` — calibrated empirically per instance group (see calibration pipeline below)
- Tracks selection **frequency** of each node (tracked but not yet used for diversification)
- Supports **dynamic tenure** (random value in [tenure_min, tenure_max] each iteration)

### GRASP + Tabu Search (`algorithms/grasp_ts.py`)

The main production algorithm:
- Shares a **global time limit** across all GRASP iterations
- Each iteration: construct solution → improve with Tabu Search
- Returns best solution found within the time budget

---

## Experiment Pipeline

The project uses a two-phase experiment pipeline:

### Phase 1 — Calibration (`experiments/calibration.py`)

Calibrates two hyperparameters independently per instance group (small / large):

1. **GRASP alpha**: sweeps `ALPHA_VALUES = [0.1, 0.25, 0.5, 0.75, 0.9, -1]` using
   `grasp_timed.execute`. Selects `best_alpha_grasp` per group.

2. **GRASP+TS (alpha, tenure)**: by default uses **sequential mode**:
   - Step A: fix `tenure = ALPHA_SWEEP_TENURE` (anchor), sweep alpha → select `best_alpha_ts`
   - Step B: fix `best_alpha_ts`, sweep `TENURE_VALUES = [5, 10, 15, 20, 25, 30]` → select `best_tenure`
   - A **joint mode** (full alpha × tenure grid) is available via `CALIBRATION_MODE = "joint"`

Calibration uses a shorter time budget (`TIME_LIMIT = 10s`, `RUNS_PER_CONF = 3`) and
writes all results to CSV. At the end it writes:

```text
experiments/calibration_grasp.csv         # per-instance detail
experiments/calibration_grasp_summary.csv # per-alpha summary
experiments/calibration_grasp_runs.csv    # individual runs
experiments/calibration_ts.csv            # per-instance detail (all phases)
experiments/calibration_ts_summary.csv    # per-(alpha,tenure) summary
experiments/calibration_ts_runs.csv       # individual runs
experiments/calibration_summary.json      # machine-readable best params → consumed by comparison.py
```

### Phase 2 — Comparison (`experiments/comparison.py`)

Reads `experiments/calibration_summary.json` to load calibrated hyperparameters per group
(falls back to hardcoded defaults if the file is missing). Runs:

- **GRASP** with `best_alpha_grasp` (from calibration)
- **GRASP+TS** with `best_alpha_ts` + `best_tenure` (from calibration)

Both algorithms use `TIME_LIMIT = 30s` and `RUNS_PER_INSTANCE = 5`. Outputs:

```text
experiments/comparison_results.csv   # aggregate per-instance stats (avg, best, worst, std, dev%)
experiments/comparison_runs.csv      # individual runs (paired by seed — Wilcoxon-ready)
experiments/comparison_tests.json    # paired Wilcoxon test result (requires scipy; graceful fallback)
```

Convergence history is tracked inside `algorithms/grasp_ts.py` and stored in
`best['history']` as `[(iteration, elapsed_s, best_of)]`.

---

## Current State

### What works

- All algorithm variants (GRASP+BI, GRASP+TS) run correctly with correct local search logic
- Aspiration criterion implemented and active in Tabu Search
- Full calibration pipeline: sweeps alpha (GRASP) and (alpha, tenure) (GRASP+TS), writes JSON handoff
- Comparison pipeline: reads calibrated params, runs both algorithms, exports per-run CSV
- Statistical significance test (Wilcoxon signed-rank) on paired runs, optional scipy dependency

### Known limitations / open areas

- No visualization of results (convergence curves, solution quality over time) — `history` data available but no plot script yet
- Frequency array in Tabu Search is tracked but not used for diversification
- No parallelization (experiments are sequential)
- No other metaheuristics implemented (ILS, SA, etc.) for broader comparison
- Calibration uses a subset of instances; final comparison uses the full benchmark set (limitation noted)

---

## Key Design Decisions (for context)

- **Python** is used throughout (no C extensions)
- Solutions are represented as sets of node indices (0-indexed internally)
- Distance matrix is stored as a full n×n numpy/list matrix after parsing
- Time management uses `time.time()` with a shared `start_time` passed to functions
- Alpha = -1 is a special value meaning "randomize alpha each iteration"
