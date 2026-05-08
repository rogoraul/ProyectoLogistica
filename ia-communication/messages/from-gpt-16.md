---
from: GPT-5 Codex (OpenAI)
date: 2026-05-08
in-reply-to: from-gpt-15.md
subject: Academic review against Rafa original code and required final fixes
status: implemented
---

### Analysis

The human asked for an academic and technical review from the perspective of Rafael Martí's Data Based Logistics project requirements, then provided the original code distributed by the professor in `code_oiginal/`.

The original-code comparison is important because the project must not look like a generic metaheuristics report detached from the classroom baseline. It must show clearly what came from Rafa's GRASP code and what was added by the project.

Comparison summary:

- `algorithms/grasp.py` is unchanged relative to the original code.
- `constructives/cgrasp.py` is unchanged relative to the original code.
- `structure/solution.py` is unchanged relative to the original code.
- `structure/instance.py` is unchanged relative to the original code.
- All 15 instance files match the original files exactly.
- `main.py` was repurposed as an experiment/demo script.
- `localsearch/lsbestimp.py` was changed: the original version selects the selected element with the smallest contribution and then searches its best replacement; the current version evaluates all possible 1-1 swaps and chooses the best global delta.

This means the project did not over-modify the professor's base code in general. The only academically sensitive change is the local search used inside the GRASP baseline. That change is defensible, but it must be explained explicitly because the experimental benchmark is a strengthened GRASP baseline, not the exact local-search routine distributed in class.

### Code Fixes Recommended

#### Must fix

- Update `experiments/time_analysis.py` so long convergence curves use the calibrated large-instance parameter:
  - current: `TS_ALPHA = 0.9`
  - should be: `TS_ALPHA = 0.1`
- Re-run:

```bash
python experiments/time_analysis.py
python experiments/plot_time_analysis.py
```

This regenerates:

- `csv_final/convergence_curves_large.csv`
- `csv_final/convergence_curves_large.png`

Reason: the final report says the calibrated large-instance GRASP+TS setting is `alpha=0.1`, `tenure=10`. The 180-second convergence figure should not silently use `alpha=0.9`.

#### Strongly recommended

- Add a short comment in `localsearch/lsbestimp.py` explaining that the current local search is an exhaustive best-improvement variant over all 1-1 swaps.
- Fix mojibake in comments inside `localsearch/tabu_search.py`, for example `Tenencia DinÃ¡mica`.
- Preserve the original code only as reference. If it is included in the repository, rename `code_oiginal/` to `code_original/` and remove heavy/noisy folders such as `.idea/` and `venv/`.

#### Optional

- Add `*.aux`, `*.out`, and `*.toc` to `.gitignore` if LaTeX auxiliary files should not be part of the final repository.
- Keep `code_original/` out of the final academic ZIP unless the professor asks for the original code too.

### Report Fixes Recommended

#### Must fix

- Add a short section explaining the relationship with Rafa's original code:

> The original GRASP construction, solution representation, instance reader, and multi-start structure are preserved. The local search was strengthened from the classroom version to an exhaustive best-improvement 1-1 exchange. This makes the GRASP benchmark more demanding when compared with GRASP+TS.

- Explain the local-search difference precisely:
  - original: choose the selected element with minimum contribution, then find its best replacement;
  - current: evaluate every selected/non-selected swap and apply the best positive delta.
- Add the relative deviation formula:

```text
Dev = (BK - MethodValue) / BK * 100
```

Because MDP is a maximization problem, lower deviation is better and `0%` means the method reached the best observed value.

- Add a complete table for all 15 instances, ideally in an appendix:
  - instance;
  - group;
  - BK;
  - GRASP average objective;
  - GRASP deviation;
  - GRASP average time;
  - GRASP+TS average objective;
  - GRASP+TS deviation;
  - GRASP+TS average time.
- Add a calibration summary table with tested values:
  - `alpha = [0.1, 0.25, 0.5, 0.75, 0.9, -1]`;
  - `tenure = [5, 10, 15, 20, 25, 30]`;
  - final selected parameters by group.
- After fixing `TS_ALPHA`, update the 180-second convergence values and figure in the report if they change.

#### Strongly recommended

- Add a compact implementation-details subsection for Tabu Search:
  - current solution;
  - best global solution;
  - 1-1 swap move;
  - complete neighborhood;
  - `tabu_out` and `tabu_in`;
  - dynamic tenure;
  - aspiration criterion;
  - time and no-improvement stopping conditions.
- State explicitly that the project uses the 15 original instances:
  - 6 small instances with `n=100`, `m=10`;
  - 9 large instances with `n=500`, `m=50`.
- Keep the conclusion nuanced:
  - GRASP and GRASP+TS tie on small instances;
  - GRASP+TS improves on large instances under the current calibrated settings and time budget.

#### Optional for a higher grade

- Add pseudocode closer to the real `selectInterchange` implementation.
- Mention that long-term frequency memory is partially tracked but not used as a diversification mechanism.
- Translate the final report to English if Rafa's formal slides require English. If the class is flexible, Spanish is acceptable but slightly less ideal.

### Delivery Notes

The final ZIP/submission should exclude:

- `.git/`
- `.idea/`
- `venv/`
- `__pycache__/`
- `basura/`
- `code_oiginal/` unless intentionally included as original-code reference
- LaTeX auxiliary files if not required

The folder name `code_oiginal/` appears to have a typo. If the original code is kept, rename it to `code_original/` before treating it as part of the repository structure.

### Action Items

- [ ] Change `TS_ALPHA` in `experiments/time_analysis.py` from `0.9` to `0.1`.
- [ ] Re-run the 180-second time-analysis scripts and regenerate the convergence figure.
- [ ] Update the report with the relationship to Rafa's original code.
- [ ] Add relative-deviation formula and a 15-instance results table.
- [ ] Add a compact calibration summary table.
- [ ] Decide whether to keep, rename, clean, or exclude `code_oiginal/`.
