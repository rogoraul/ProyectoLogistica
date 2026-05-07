---
from: GPT-5 Codex (OpenAI)
date: 2026-05-07
in-reply-to: from-gpt-12.md
subject: Final LaTeX report drafted with current figures and refreshed conclusions
status: implemented
---

### Analysis

The human asked for the final report to be rebuilt in LaTeX, using the latest `ia-communication` instructions and the current material map rather than the obsolete Word/PDF report in `basura/legacy_reports/`.

I used the legacy report only as a structural reference. Its old numerical conclusions were not reused because they contradict the refreshed 2026-04-30/2026-05-07 data.

### Implementation

Created:

- `informe_final_mdp.tex`

The LaTeX report includes:

- problem formulation for the Maximum Diversity Problem;
- descriptions of GRASP, Tabu Search, and GRASP+TS;
- implementation decisions and difficulties;
- calibration protocol and selected parameters;
- final comparison on small and large instances;
- Wilcoxon result favoring GRASP+TS on large instances;
- professor-requested visual analysis;
- the two main current figures:
  - `csv_final/ts_evolution_plot.png`
  - `csv_final/convergence_curves_large.png`
- reproducibility appendix listing the current source-of-truth files.

### Verification

Checked that:

- both referenced PNG figures exist;
- the LaTeX file contains the two expected `includegraphics` statements;
- LaTeX `begin`/`end` counts are balanced;
- obsolete claims such as `p=0.002628`, `alpha=0.9` as final configuration, `scipy_not_installed`, or "GRASP is better" do not appear as current conclusions.

No LaTeX compiler (`pdflatex`, `xelatex`, `lualatex`, `latexmk`, or `tectonic`) is available in the current PATH, so I could not compile the PDF locally in this environment.

### Action Items

- [x] Draft final report in LaTeX.
- [x] Include current generated figures.
- [x] Align conclusions with refreshed data.
- [x] Record the report rebuild in the communication channel.
