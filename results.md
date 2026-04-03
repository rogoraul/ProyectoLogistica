# Results Draft

This document is a working draft of the experimental results section for the Maximum Diversity Problem project. It summarizes the calibration stage, the final comparison between GRASP and GRASP+TS, and the main interpretation supported by the generated CSV and JSON files in `experiments/`.

## 3.1 Calibration

### 3.1.1 Selected parameters

| Group | GRASP alpha | GRASP+TS alpha | GRASP+TS tenure |
| --- | --- | --- | --- |
| Small (`n=100`) | 0.1 | 0.25 | 15 |
| Large (`n=500`) | 0.1 | 0.9 | 10 |

These values were selected automatically by the sequential calibration pipeline implemented in `experiments/calibration.py` and stored in `experiments/calibration_summary.json`.

### 3.1.2 GRASP alpha calibration

For the small instances, all six tested alpha values produced exactly the same mean objective value (`356.34`) and zero standard deviation. In practice, this means alpha had no measurable effect at `n=100` under the chosen calibration budget. The selected value `alpha = 0.1` should therefore be interpreted as a tie-break outcome, not as evidence of a strong preference.

For the large instances, the calibration results were clearly differentiated. The best value was `alpha = 0.1`, with `avg_dev_pct = 0.2536%` and `mean_avg_of = 7694.55`. Larger alpha values degraded performance, with `alpha = 0.75` and `alpha = 0.9` producing the weakest average results. This indicates that GRASP with best-improvement local search benefits from a relatively greedy construction phase when the wall-clock budget is fixed.

### 3.1.3 GRASP+TS calibration

For the small instances, the calibration again showed almost complete saturation. Several parameter settings tied at `avg_dev_pct = 0.0%`, while only `alpha = -1` and `tenure = 5` showed a slight deterioration. As with GRASP, the selected small-instance parameters should be described as practical defaults rather than as strong evidence of sensitivity.

For the large instances, the pattern was much more informative:

| Phase | Best value(s) | Best avg_dev_pct | Mean average objective |
| --- | --- | --- | --- |
| Alpha sweep (tenure fixed at 15) | `alpha = 0.9` | `0.1094%` | `7700.98` |
| Tenure sweep (alpha fixed at 0.9) | `tenure = 10` | `0.0906%` | `7705.39` |

The most interesting calibration result is that GRASP and GRASP+TS favor opposite ends of the alpha spectrum on large instances:

- GRASP alone performs best with a greedy construction (`alpha = 0.1`).
- GRASP+TS performs best with a highly random construction (`alpha = 0.9`).

This is worth highlighting explicitly in the report. A plausible explanation is that best-improvement local search benefits from strong starting solutions, while Tabu Search benefits from more diverse starting points because it can exploit them more aggressively afterward.

## 3.2 Final Comparison on Small Instances

The small instances do not meaningfully separate the algorithms. Across the 6 small instances and 5 runs per instance:

- both algorithms produced identical objective values on every run
- all standard deviations were `0.0`
- all 30 paired comparisons were ties
- the paired statistical test was skipped because all pairs were tied

This suggests that, at `n=100`, the local search landscape is already easy enough that both GRASP+BI and GRASP+TS converge to the same local optimum under a 30-second budget. As a result, the small-instance group is useful as a sanity check, but it should not be the main basis for discussing differences between the methods.

## 3.3 Final Comparison on Large Instances

The large instances provide the real discrimination power of the benchmark. The table below summarizes the per-instance averages:

| Instance | GRASP avg | GRASP std | TS avg | TS std | delta (TS - GRASP) | GRASP best | TS best |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MDG-a_2 | 7695.50 | 22.67 | 7694.42 | 40.22 | -1.08 | 7722.22 | 7756.24 |
| MDG-a_5 | 7697.35 | 29.16 | 7635.25 | 77.71 | -62.10 | 7746.00 | 7755.23 |
| MDG-a_6 | 7712.16 | 26.79 | 7691.21 | 31.49 | -20.95 | 7752.31 | 7726.58 |
| MDG-a_9 | 7730.84 | 11.93 | 7700.91 | 40.82 | -29.93 | 7749.40 | 7755.20 |
| MDG-a_13 | 7737.72 | 8.70 | 7747.95 | 36.99 | 10.23 | 7748.34 | 7780.22 |
| MDG-a_16 | 7739.38 | 18.30 | 7690.25 | 31.04 | -49.13 | 7757.50 | 7728.40 |
| MDG-a_17 | 7723.03 | 29.49 | 7704.35 | 54.84 | -18.68 | 7756.16 | 7785.30 |
| MDG-a_19 | 7702.49 | 20.26 | 7677.74 | 28.99 | -24.75 | 7729.01 | 7722.68 |
| MDG-a_20 | 7688.01 | 17.80 | 7658.29 | 33.11 | -29.72 | 7718.59 | 7686.17 |

### 3.3.1 Aggregate view on large instances

| Metric | GRASP | GRASP+TS |
| --- | --- | --- |
| Average deviation (%) | 0.5196 | 0.8401 |
| Mean standard deviation | 20.57 | 41.69 |
| Best-known hits | 4 | 5 |
| Paired wins | 30 | 15 |
| Mean delta (TS - GRASP) | -- | -25.13 |

The large-instance group supports two complementary conclusions:

1. **GRASP is more robust on average.** It achieves better average quality on 8 of the 9 large instances, wins 30 of the 45 non-tied paired comparisons, and shows roughly half the variability of GRASP+TS.
2. **GRASP+TS occasionally reaches better peaks.** Even though its average quality is lower, it hits the best-known solution on more large instances (5 vs 4), which shows that its deeper search can occasionally reach solutions beyond GRASP's reach.

### 3.3.2 The MDG-a_5 outlier

`MDG-a_5_n500_m50.txt` deserves an explicit mention because it is the clearest example of the variance trade-off. GRASP+TS reached the best-known objective value (`7755.23`) in one run, but three other runs landed much lower (`7578.52`, `7619.24`, `7560.80`), yielding both the worst mean difference and the highest standard deviation in the benchmark.

This should not be used to discard TS results as noise. Instead, it is strong evidence that TS is less stable under the fixed 30-second budget used in the comparison.

## 3.4 Discussion

The results do not support a simple "one algorithm dominates the other" conclusion. A more accurate interpretation is a trade-off between **breadth** and **depth** under equal wall-clock time:

- GRASP spends the budget on many restarts, each followed by a best-improvement local search. This gives more breadth and more stable average performance.
- GRASP+TS spends more time exploiting each constructed solution. This gives deeper search per iteration and occasionally better maxima, but at the cost of much higher variance.

This interpretation is reinforced by the calibration outcome. The best alpha for GRASP (`0.1`) is greedy, while the best alpha for GRASP+TS (`0.9`) is highly random. In other words, the stronger local improvement phase changes what counts as a good starting solution.

One limitation should be stated explicitly in the report: the current environment did not have SciPy installed, so `experiments/comparison_tests.json` does not contain a Wilcoxon p-value. The descriptive evidence is still strong, but the text should avoid making a formal significance claim unless the test is rerun in an environment with SciPy available.

## 3.5 Recommended wording

If the report needs a short conclusion paragraph, the following message is faithful to the data:

> Under a fixed 30-second budget, GRASP with best-improvement local search is the more robust algorithm, delivering better average solution quality and lower variance on large instances. However, GRASP+TS occasionally reaches higher-quality solutions and hits the best-known objective value on more large instances. The comparison therefore reveals a breadth-versus-depth trade-off rather than a strict dominance relation.
