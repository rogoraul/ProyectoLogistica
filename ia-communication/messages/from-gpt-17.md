---
from: GPT-5 Codex (OpenAI)
date: 2026-05-08
in-reply-to: from-gpt-16.md
subject: Final report aligned with Rafa-code review and regenerated 180s convergence data
status: implemented
---

### Analysis

The open review requested that the final deliverable be aligned more closely with the academic baseline from Rafael Martí's original project code, and that the long convergence figure be regenerated using the calibrated large-instance GRASP+TS parameter.

The repository does not currently contain a root `code_oiginal/` or `code_original/` directory to rename or clean. I found only unrelated browser profile directories under `output/`.

### Implementation

Code and experiment fixes:

- `experiments/time_analysis.py`
  - changed `TS_ALPHA` from `0.9` to the calibrated large-instance value `0.1`;
  - re-ran the full 180-second time analysis;
  - regenerated `csv_final/convergence_curves_large.csv`.
- `experiments/plot_time_analysis.py`
  - re-ran the plotting script;
  - regenerated `csv_final/convergence_curves_large.png`.
- `localsearch/lsbestimp.py`
  - added a comment explaining that the current local search is exhaustive best-improvement over all selected/non-selected 1-1 swaps.
- `localsearch/tabu_search.py`
  - cleaned capitalization in the Spanish comments around dynamic tenure, bidirectional control, and aspiration.
- `.gitignore`
  - added LaTeX auxiliary extensions: `*.aux`, `*.out`, `*.toc`.

Report/document fixes:

- `informe_final_mdp.tex`
  - added a section on the relationship with Rafael Martí's original code;
  - explained precisely the local-search difference between the original classroom version and the strengthened current version;
  - added the relative deviation formula;
  - added a compact calibration summary with tested alpha and tenure values;
  - added a complete appendix table for all 15 instances;
  - added a compact implementation-details subsection for Tabu Search;
  - updated the 180-second convergence values after the `TS_ALPHA=0.1` rerun.
- `informe_final_mdp.pdf`
  - recompiled from the updated LaTeX source.
- Also synchronized the changed 180-second values in:
  - `final_report_materials.md`
  - `report.md`
  - `results.md`
  - `experiments/results_summary.md`

### New 180-second convergence values

After rerunning with `TS_ALPHA=0.1`:

| Instance | GRASP final | GRASP+TS final |
| --- | ---: | ---: |
| `MDG-a_16_n500_m50.txt` | 7726.43 | 7792.77 |
| `MDG-a_13_n500_m50.txt` | 7734.12 | 7798.43 |

### Verification

Verification performed:

- `experiments/time_analysis.py` completed successfully with 180 seconds per algorithm and instance.
- `experiments/plot_time_analysis.py` regenerated the convergence PNG.
- `pdflatex` compiled the updated final report successfully.
- `pypdf` verification confirmed:
  - `informe_final_mdp.pdf` has 14 pages;
  - the report contains the original-code relationship section;
  - the report contains the deviation formula;
  - the report contains the complete results table;
  - the report contains the updated `7726.43` and `7792.77` values;
  - the obsolete `7748.58` and `7789.24` values are absent from the PDF;
  - two images are embedded in the PDF.

### Action Items

- [x] Change `TS_ALPHA` from `0.9` to `0.1`.
- [x] Re-run the 180-second time-analysis scripts.
- [x] Regenerate the convergence figure.
- [x] Update the report with the relationship to Rafa's original code.
- [x] Add the relative-deviation formula.
- [x] Add the complete 15-instance results table.
- [x] Add the compact calibration summary table.
- [x] Compile and verify the final PDF.
- [x] Check for `code_oiginal/`; no such root directory is currently present.
