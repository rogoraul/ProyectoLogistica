# Maximum Diversity Problem - Metaheuristics Project

Metaheuristic implementations for the **Maximum Diversity Problem (MDP)** using GRASP with best-improvement local search and GRASP + Tabu Search, together with calibration, comparison, and reporting utilities.

---

## Problem

Given a set of `n` elements and pairwise distances `d(i, j)`, select a subset `S` of size `p` that maximizes the sum of pairwise distances:

```text
maximize  sum{ d(i,j) : i,j in S, i < j }
```

MDP is NP-hard. The benchmark instances used here are from the MDG-a family:

- small instances: `n = 100`, `p = 10`
- large instances: `n = 500`, `p = 50`

---

## Implemented Algorithms

| Algorithm | File | Description |
| --------- | ---- | ----------- |
| GRASP | `algorithms/grasp_timed.py` | GRASP with exhaustive best-improvement local search under a time limit |
| GRASP+TS | `algorithms/grasp_ts.py` | GRASP construction plus Tabu Search under a shared global time budget |

Core components:

| Component | File |
| --------- | ---- |
| GRASP construction (RCL) | `constructives/cgrasp.py` |
| Best-improvement local search | `localsearch/lsbestimp.py` |
| Tabu Search with aspiration | `localsearch/tabu_search.py` |
| Solution operations | `structure/solution.py` |
| Instance reader | `structure/instance.py` |

---

## Project Structure

```text
ProyectoLogistica/
|- algorithms/
|  |- grasp.py
|  |- grasp_timed.py
|  `- grasp_ts.py
|- constructives/
|  `- cgrasp.py
|- localsearch/
|  |- lsbestimp.py
|  `- tabu_search.py
|- structure/
|  |- instance.py
|  `- solution.py
|- instances/
|  `- MDG-a benchmark instances
|- experiments/
|  |- calibration.py
|  |- comparison.py
|  |- generate_excel.py
|  |- calibration_summary.json
|  |- calibration_grasp_summary.csv
|  |- calibration_ts_summary.csv
|  |- comparison_results.csv
|  |- comparison_runs.csv
|  |- comparison_tests.json
|  `- resultados.xlsx
|- ia-communication/
|- main.py
|- README.md
|- results.md
`- report.md
```

---

## Dependencies

Minimum:

```text
Python >= 3.8
```

Optional extras:

```text
openpyxl   # for experiments/generate_excel.py
scipy      # for Wilcoxon test output in experiments/comparison.py
```

`scipy` is optional. If it is not installed, `comparison.py` skips the Wilcoxon test and writes `"status": "unavailable"` in `comparison_tests.json`.

---

## How to Run

Run all commands from the project root.

### 1. Calibration

```bash
python experiments/calibration.py
```

This performs:

- GRASP alpha calibration
- GRASP+TS sequential calibration of alpha and tenure

Main outputs:

- `experiments/calibration_grasp_summary.csv`
- `experiments/calibration_ts_summary.csv`
- `experiments/calibration_summary.json`

### 2. Final comparison

```bash
python experiments/comparison.py
```

This reads calibrated parameters from `experiments/calibration_summary.json` when available, otherwise it falls back to built-in defaults.

Main outputs:

- `experiments/comparison_results.csv`
- `experiments/comparison_runs.csv`
- `experiments/comparison_tests.json`

### 3. Excel export

```bash
python experiments/generate_excel.py
```

Output:

- `experiments/resultados.xlsx`

### 4. Demo entry point

```bash
python main.py
```

This runs a short demonstration on one large instance for:

- GRASP with `alpha = 0.1`
- GRASP+TS with `alpha = 0.9`, `tenure = 10`

---

## Reproducibility Notes

- Seeds are paired as `seed = 42 + run_index`.
- Calibration uses a 10-second budget and 3 runs per configuration.
- Final comparison uses a 30-second budget and 5 runs per instance.
- Instance files must be present in `instances/`.
- `comparison.py` uses `calibration_summary.json` if present; otherwise it prints that fallback parameters are being used.

---

## Key Results

Under a 30-second budget on large instances (`n = 500`):

| Metric | GRASP | GRASP+TS |
| ------ | ----- | -------- |
| Avg dev% from BK | **0.52%** | 0.84% |
| Mean std across instances | **20.57** | 41.69 |
| Instances reaching BK at least once | 4 | **5** |
| Paired run wins (out of 45) | **30** | 15 |
| Wilcoxon p-value (two-sided) | - | **0.0026** |

GRASP is more robust on average, while GRASP+TS reaches higher peak solutions more often. The final interpretation is a breadth-versus-depth trade-off under a fixed time budget, not a strict dominance relation.

See:

- `results.md` for the experimental results section
- `report.md` for the full report draft

---

## Key Calibration Finding

On large instances, the two algorithms calibrate to opposite ends of the alpha spectrum:

- GRASP best alpha = `0.1`
- GRASP+TS best alpha = `0.9`

This reflects a genuine methodological result: best-improvement local search benefits from strong starting solutions, while Tabu Search benefits from more diverse starts because it can exploit them more aggressively afterward.
