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

Evaluates all possible swap moves `(i_in, j_out)` and applies the best one. Repeats until no improving move exists. O(p × (n−p)) per iteration.

### Tabu Search (`localsearch/tabu_search.py`)

Enhanced local search:
- Maintains a **tabu list**: recently removed nodes are forbidden from re-entering for `tenure` iterations
- Accepts non-improving moves (aspiration criterion: accept if better than best known)
- Configurable `tenure` (typically 5–30; calibration experiments suggest ~10 for small, ~15 for large instances)
- Tracks selection **frequency** of each node (for potential diversification use)
- Supports **dynamic tenure** (random value in a range each iteration)

### GRASP + Tabu Search (`algorithms/grasp_ts.py`)

The main production algorithm:
- Shares a **global time limit** across all GRASP iterations
- Each iteration: construct solution → improve with Tabu Search
- Returns best solution found within the time budget

---

## Current State

### What works
- All three algorithm variants (GRASP+BI, GRASP+TS) run correctly
- Calibration experiments produce results for tenure optimization
- Comparison experiments benchmark variants across instances

### Known limitations / open areas
- No visualization of results (convergence curves, solution quality over time)
- No statistical analysis of results (confidence intervals, Wilcoxon tests)
- Experiments output to CSV but no automatic plotting
- No implementation of other metaheuristics (ILS, VNS, Simulated Annealing, Genetic Algorithms) for comparison
- Frequency array in Tabu Search is tracked but never used for diversification
- No parallelization (experiments are sequential)
- No formal scientific report structure in the code

---

## Key Design Decisions (for context)

- **Python** is used throughout (no C extensions)
- Solutions are represented as sets of node indices (0-indexed internally)
- Distance matrix is stored as a full n×n numpy/list matrix after parsing
- Time management uses `time.time()` with a shared `start_time` passed to functions
- Alpha = -1 is a special value meaning "randomize alpha each iteration"
