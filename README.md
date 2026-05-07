# Maximum Diversity Problem - GRASP and Tabu Search

Metaheuristic project for the Maximum Diversity Problem (MDP), using GRASP with best-improvement local search and GRASP combined with Tabu Search.

The current repository state reflects the refreshed experimental pipeline from 2026-04-30 and the report reconciliation from 2026-05-07.

---

## Problem

Given `n` elements and pairwise distances `d(i, j)`, the Maximum Diversity Problem selects a subset `S` of size `p` that maximizes the total distance between selected elements:

```text
maximize  sum d(i,j), for i,j in S and i < j
```

The instances used are from the MDG-a family:

- small instances: `n = 100`, `p = 10`
- large instances: `n = 500`, `p = 50`

---

## Implemented Algorithms

| Algorithm | File | Description |
| --------- | ---- | ----------- |
| GRASP | `algorithms/grasp_timed.py` | GRASP with greedy-randomized construction and exhaustive best-improvement local search. |
| GRASP+TS | `algorithms/grasp_ts.py` | GRASP construction followed by Tabu Search under a shared global time budget. |

Core modules:

| Component | File |
| --------- | ---- |
| GRASP construction | `constructives/cgrasp.py` |
| Best-improvement local search | `localsearch/lsbestimp.py` |
| Tabu Search | `localsearch/tabu_search.py` |
| Solution operations | `structure/solution.py` |
| Instance reader | `structure/instance.py` |

The current Tabu Search implementation includes bidirectional short-term memory, dynamic tenure, aspiration, and telemetry for internal convergence improvements.

---

## Current Results

### Calibrated Parameters

| Group | GRASP alpha | GRASP+TS alpha | GRASP+TS tenure |
| ----- | ----------- | -------------- | --------------- |
| small | 0.1 | -1 | 5 |
| large | 0.1 | 0.1 | 10 |

### Final Comparison

Small instances are saturated: all 30 paired runs are exact ties.

On large instances, the current data favor GRASP+TS:

| Metric | GRASP | GRASP+TS |
| ------ | ----- | -------- |
| Avg dev% | 0.6379% | 0.2284% |
| Mean std | 20.57 | 20.27 |
| Best hits | 0 | 12 |
| Paired wins | 8 | 36 |
| Mean delta (TS - GRASP) | - | +31.7891 |
| Wilcoxon p-value | - | 8.24e-08 |

Interpretation: GRASP+TS equals GRASP on small instances and clearly improves it on large instances under the current corrected implementation and refreshed data.

---

## Professor Feedback Artifacts

Two additional artifacts address the requested analysis of Tabu Search behavior:

| Question | Artifact |
| -------- | -------- |
| How does Tabu Search evolve internally? | `csv_final/ts_evolution_plot.png` and `csv_final/ts_evolution_single_restart.csv` |
| What happens if GRASP+TS receives more time? | `csv_final/convergence_curves_large.png` and `csv_final/convergence_curves_large.csv` |

The internal Tabu Search trace contains 2586 iterations, including 1403 worsening moves. The 180-second convergence curves show GRASP+TS continuing to improve and reaching higher final values than GRASP on the representative large instances.

---

## Important Report Files

| File | Purpose |
| ---- | ------- |
| `final_report_materials.md` | Map of useful final-report material and files to avoid. |
| `report.md` | Main narrative base for the final report. |
| `results.md` | Technical experimental-results section. |
| `experiments/results_summary.md` | Concise summary of current results. |
| `ia-communication/messages/from-gpt-11.md` | Trace of the results/report reconciliation. |
| `ia-communication/messages/from-gpt-12.md` | Trace of the final material map and cleanup. |

---

## Generated Tables and Figures

Current formatted Excel files:

- `experiments/calibracion_grasp.xlsx`
- `experiments/calibracion_ts.xlsx`
- `experiments/comparacion_final.xlsx`

Current figures:

- `csv_final/convergence_plot.png`
- `csv_final/ts_evolution_plot.png`
- `csv_final/convergence_curves_large.png`

---

## How to Run

Run commands from the repository root.

Calibration:

```bash
python experiments/calibration.py
```

Final comparison:

```bash
python experiments/comparison.py
```

Excel export:

```bash
python experiments/generate_excel.py
```

Convergence/evolution demo:

```bash
python main.py
```

Long time-budget analysis:

```bash
python experiments/time_analysis.py
python experiments/plot_time_analysis.py
```

The full pipeline is also described in `run_pipeline.sh`.

---

## Submission Cleanup Notes

The `basura/` folder contains legacy material moved out of the main working set. Do not include it in the final academic submission unless explicitly needed as historical backup.

When preparing a final ZIP or submission folder, exclude:

- `.git/`
- `.idea/`
- `venv/`
- `__pycache__/`
- `basura/`
- `*.pyc`
