# Experimental Results

This document reports the current calibration, comparison, and convergence experiments for the Maximum Diversity Problem (MDP). The source of truth is the data regenerated on 2026-04-30 in `experiments/` and `csv_final/`.

---

## 3.1 Calibration

### 3.1.1 Selected Parameters

| Group | Algorithm | Best alpha | Best tenure | Best avg dev% |
| ----- | --------- | ---------- | ----------- | ------------- |
| Small (`n=100`) | GRASP | 0.1 | - | 0.0000% |
| Small (`n=100`) | GRASP+TS | -1 | 5 | 0.0000% |
| Large (`n=500`) | GRASP | 0.1 | - | 0.2142% |
| Large (`n=500`) | GRASP+TS | 0.1 | 10 | 0.0647% |

The selected values come from `experiments/calibration_summary.json`. The calibration was sequential: first alpha was calibrated, then tenure was calibrated using the selected alpha.

### 3.1.2 GRASP Alpha Calibration

Small instances are saturated: all alpha values produce the same mean objective value (`356.34`) and zero average deviation.

Large instances show a clear preference for greedy construction:

| alpha | avg dev% | mean avg OF |
| ----- | -------- | ----------- |
| **0.1** | **0.2142%** | **7697.72** |
| 0.25 | 0.2886% | 7691.99 |
| -1 | 0.3391% | 7688.07 |
| 0.9 | 0.5569% | 7671.26 |
| 0.5 | 0.5834% | 7669.25 |
| 0.75 | 0.7290% | 7658.02 |

GRASP benefits from strong constructive starts because best-improvement local search cannot intentionally cross worse intermediate states once it reaches a local optimum.

### 3.1.3 GRASP+TS Calibration

Small instances are also saturated for GRASP+TS. All alpha and tenure values tested reached zero average deviation, so the selected values are practical tie-breaks rather than meaningful sensitivity signals.

Large instances - alpha sweep with tenure fixed at 15:

| alpha | avg dev% | mean avg OF |
| ----- | -------- | ----------- |
| **0.1** | **0.1734%** | **7717.14** |
| 0.25 | 0.1826% | 7716.46 |
| -1 | 0.2826% | 7708.67 |
| 0.9 | 0.2868% | 7708.39 |
| 0.5 | 0.3522% | 7703.33 |
| 0.75 | 0.4521% | 7695.60 |

Large instances - tenure sweep with alpha fixed at 0.1:

| tenure | avg dev% | mean avg OF |
| ------ | -------- | ----------- |
| **10** | **0.0647%** | **7717.51** |
| 15 | 0.0693% | 7717.14 |
| 5 | 0.0721% | 7716.93 |
| 20 | 0.3438% | 7695.92 |
| 25 | 0.4843% | 7685.07 |
| 30 | 0.8892% | 7653.84 |

The current Tabu Search implementation uses bidirectional short-term memory and dynamic tenure. With this corrected behavior, the best large-instance configuration is no longer the older `alpha=0.9` setting; the current data select `alpha=0.1, tenure=10`.

---

## 3.2 Final Comparison - Small Instances

Parameters used: GRASP `alpha=0.1`; GRASP+TS `alpha=-1, tenure=5`.

Across 6 small instances and 5 seeds per instance:

- all 30 paired runs are exact ties;
- both algorithms reach the same observed best values;
- the Wilcoxon test is skipped because all paired differences are zero.

At `n=100`, the problem is easy enough under a 30-second budget that both methods saturate.

---

## 3.3 Final Comparison - Large Instances

Parameters used: GRASP `alpha=0.1`; GRASP+TS `alpha=0.1, tenure=10`.

BK is defined as the maximum objective value observed in the current runs of either algorithm for each instance.

| Instance | GRASP avg | GRASP std | TS avg | TS std | delta (TS - GRASP) | BK | GRASP=BK | TS=BK |
| -------- | --------- | --------- | ------ | ------ | ------------------ | -- | -------- | ----- |
| MDG-a_2 | 7695.50 | 22.67 | 7729.77 | 8.39 | +34.27 | 7741.07 | 0 | 1 |
| MDG-a_5 | 7697.35 | 29.16 | 7739.21 | 29.27 | +41.86 | 7755.23 | 0 | 2 |
| MDG-a_6 | 7712.16 | 26.79 | 7754.04 | 14.28 | +41.88 | 7770.48 | 0 | 1 |
| MDG-a_9 | 7730.84 | 11.93 | 7741.52 | 16.13 | +10.68 | 7758.44 | 0 | 1 |
| MDG-a_13 | 7737.72 | 8.70 | 7761.13 | 32.94 | +23.41 | 7786.43 | 0 | 1 |
| MDG-a_16 | 7739.38 | 18.30 | 7756.25 | 25.81 | +16.87 | 7792.77 | 0 | 1 |
| MDG-a_17 | 7723.03 | 29.49 | 7772.74 | 27.03 | +49.71 | 7785.36 | 0 | 2 |
| MDG-a_19 | 7702.49 | 20.25 | 7745.61 | 11.43 | +43.12 | 7755.41 | 0 | 2 |
| MDG-a_20 | 7688.01 | 17.80 | 7712.33 | 17.17 | +24.32 | 7727.13 | 0 | 1 |

### 3.3.1 Aggregate Results

| Metric | GRASP | GRASP+TS |
| ------ | ----- | -------- |
| Avg dev% | 0.6379% | **0.2284%** |
| Mean std | 20.57 | **20.27** |
| Best hits across large runs | 0 | **12** |
| Paired run wins | 8 | **36** |
| Ties | - | 1 |
| Mean delta (TS - GRASP) | - | **+31.7891** |
| Wilcoxon W | - | 79.0 |
| Wilcoxon p-value | - | **8.24e-08** |

The Wilcoxon signed-rank test is computed on the non-zero paired differences (`zero_method="wilcox"`). It confirms a statistically significant difference on large instances, and the direction of the mean delta favors GRASP+TS.

---

## 3.4 Time and Internal Evolution Analysis

Two additional analyses were added after professor feedback.

### 3.4.1 Internal Tabu Search Evolution

`csv_final/ts_evolution_single_restart.csv` records a single Tabu Search restart at iteration level. It contains 2586 moves, including 1403 worsening moves. This is the expected behavior: Tabu Search may temporarily worsen the current solution to escape local optima while preserving a non-decreasing global best.

The corresponding plot is `csv_final/ts_evolution_plot.png`.

### 3.4.2 Longer Time-Budget Convergence

`experiments/time_analysis.py` runs GRASP and GRASP+TS for 180 seconds per algorithm on two representative large instances:

- `MDG-a_16_n500_m50.txt`
- `MDG-a_13_n500_m50.txt`

The output is `csv_final/convergence_curves_large.csv` and the plot is `csv_final/convergence_curves_large.png`.

Observed final best values:

| Instance | GRASP final best | GRASP+TS final best |
| -------- | ---------------- | ------------------- |
| MDG-a_16 | 7748.58 | **7789.24** |
| MDG-a_13 | 7755.63 | **7798.43** |

The long-run curves support the same conclusion as the 30-second comparison: GRASP+TS continues finding improvements inside long Tabu Search phases and reaches higher best-so-far values on the representative large instances.

---

## 3.5 Summary

The current regenerated data change the earlier conclusion. Under the corrected Tabu Search implementation and the refreshed 2026-04-30 pipeline, GRASP+TS equals GRASP on small instances and clearly outperforms it on large instances. On the large group, GRASP+TS achieves lower average deviation (`0.2284%` vs `0.6379%`), more paired wins (`36` vs `8`), more best hits (`12` vs `0`), and a statistically significant Wilcoxon result (`p=8.24e-08`).

The professor's two requested visual checks are also addressed: the Tabu Search evolution trace shows controlled worsening moves, and the 180-second convergence curves show that GRASP+TS keeps improving with additional time.
