# Maximum Diversity Problem — Metaheuristics Project

Metaheuristic implementations for the **Maximum Diversity Problem (MDP)** using GRASP with best-improvement local search and GRASP + Tabu Search, with calibration and comparison experiments.

---

## Problem

Given a set of *n* elements and pairwise distances *d(i, j)*, select a subset *S* of size *p* that maximises the sum of pairwise distances:

```
maximise  sum{ d(i,j) : i,j in S, i < j }
```

MDP is NP-hard. Instances used are from the MDG-a benchmark (n=100, p=10 and n=500, p=50).

---

## Algorithms

| Algorithm | File | Description |
| --------- | ---- | ----------- |
| GRASP | `algorithms/grasp_timed.py` | Greedy Randomised Adaptive Search with best-improvement LS, timed |
| GRASP+TS | `algorithms/grasp_ts.py` | GRASP construction + Tabu Search improvement, shared time budget |

Core components:

| Component | File |
| --------- | ---- |
| GRASP construction (RCL) | `constructives/cgrasp.py` |
| Best-improvement local search | `localsearch/lsbestimp.py` |
| Tabu Search (FIFO list + aspiration) | `localsearch/tabu_search.py` |
| Solution data structure | `structure/solution.py` |
| Instance reader | `structure/instance.py` |

---

## Project Structure

```
ProyectoLogistica/
├── algorithms/
│   ├── grasp_timed.py       GRASP with time limit
│   └── grasp_ts.py          GRASP + Tabu Search
├── constructives/
│   └── cgrasp.py            GRASP RCL construction
├── localsearch/
│   ├── lsbestimp.py         Exhaustive best-improvement LS
│   └── tabu_search.py       Tabu Search with aspiration criterion
├── structure/
│   ├── instance.py          Instance file reader
│   └── solution.py          Solution representation and operations
├── instances/               MDG-a benchmark instances (not in repo)
├── experiments/
│   ├── calibration.py       Hyperparameter calibration sweep
│   ├── comparison.py        Final GRASP vs GRASP+TS comparison
│   ├── generate_excel.py    Produces resultados.xlsx from CSV outputs
│   ├── calibration_summary.json        Best parameters per group
│   ├── calibration_grasp_summary.csv   GRASP alpha sweep results
│   ├── calibration_ts_summary.csv      TS (alpha, tenure) sweep results
│   ├── comparison_results.csv          Per-instance aggregate stats
│   ├── comparison_runs.csv             Per-run individual data
│   ├── comparison_tests.json           Wilcoxon test results
│   └── resultados.xlsx                 Formatted Excel (5 sheets)
├── results.md               Empirical results (calibration + comparison)
├── report.md                Full academic report (source for PDF)
└── ia-communication/        AI collaboration protocol and messages
```

---

## Dependencies

```
Python >= 3.8
openpyxl        # Excel generation  (pip install openpyxl)
scipy           # Wilcoxon test     (pip install scipy)
```

`scipy` is optional: `comparison.py` degrades gracefully if not installed, skipping the Wilcoxon test and writing `"status": "unavailable"` to `comparison_tests.json`.

---

## How to Run

All commands are run from the **project root**.

### 1. Calibration

```bash
python3 experiments/calibration.py
```

Sweeps `alpha` values for GRASP and `(alpha, tenure)` values for GRASP+TS on a representative subset of instances. Uses a 10-second time budget per configuration and 3 runs.

**Outputs:**
- `experiments/calibration_grasp_summary.csv`
- `experiments/calibration_ts_summary.csv`
- `experiments/calibration_summary.json` — best parameters per group (read by comparison.py)

### 2. Comparison

```bash
python3 experiments/comparison.py
```

Reads best parameters from `calibration_summary.json` (or uses fallback defaults if the file is missing). Runs 5 independent seeds per instance per algorithm with a 30-second budget.

**Outputs:**
- `experiments/comparison_results.csv` — per-instance aggregate statistics
- `experiments/comparison_runs.csv` — individual run data
- `experiments/comparison_tests.json` — Wilcoxon signed-rank test results

### 3. Excel report

```bash
python3 experiments/generate_excel.py
```

Reads the CSV/JSON outputs from steps 1 and 2 and produces a formatted Excel file.

**Output:** `experiments/resultados.xlsx` (5 sheets)

---

## Reproducibility Notes

- **Random seeds**: `seed = 42 + run_index` (runs 0–4 → seeds 42–46). Seeds are identical across GRASP and GRASP+TS for the same instance, enabling paired statistical comparison.
- **Calibration budget**: 10 s per configuration, 3 runs per configuration (fast sweep).
- **Comparison budget**: 30 s per algorithm run, 5 runs per instance.
- **Instance files** must be present in `instances/` before running any experiment. The expected filenames are listed in `experiments/comparison.py` (`ALL_INSTANCES`).
- **`calibration_summary.json` must exist** before `comparison.py` to use calibrated parameters. If absent, fallback defaults are used (printed to stdout).

---

## Key Results

Under a 30-second budget on large instances (n=500):

| Metric | GRASP | GRASP+TS |
| ------ | ----- | -------- |
| Avg dev% from BK | **0.52%** | 0.84% |
| Mean std across instances | **20.6** | 41.7 |
| Instances reaching BK (out of 9) | 4 | **5** |
| Paired run wins (out of 45) | **30** | 15 |
| Wilcoxon p-value (two-sided) | — | **0.0026** |

GRASP is the more robust algorithm on average (p = 0.0026). GRASP+TS reaches higher peak solutions more often (5/9 vs 4/9 instances). This is a breadth-versus-depth trade-off under a fixed time budget, not a strict dominance relation.

See `results.md` for full analysis and `report.md` for the complete academic report.

---

## Calibration Finding

GRASP and GRASP+TS calibrate to **opposite ends** of the alpha spectrum on large instances:

- GRASP best alpha = **0.1** (greedy construction)
- GRASP+TS best alpha = **0.9** (random construction)

Best-improvement LS benefits from strong starting points; Tabu Search is powerful enough to escape poor constructions and benefits from the diversity that random starts provide.
